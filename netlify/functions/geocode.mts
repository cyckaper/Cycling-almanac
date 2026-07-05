// 地名定位：Google Places（涵蓋小店與地標）→ 查無或未設金鑰時退 OpenStreetMap
// 兩段式：先以台灣為優先範圍（保住雙溪、新城等同名地的在地判讀），
// 查無結果時放寬為全球重試（支援海外路線，如 Urbana / Homer Lake）。
// near（前一定位點）作 30km 圓形偏置，讓同一趟的地名彼此靠攏。
export default async (req) => {
  const url = new URL(req.url);
  const q = (url.searchParams.get("q") || "").trim();
  const region = (url.searchParams.get("region") || "").trim();
  const near = (url.searchParams.get("near") || "").trim();
  if (!q) return json({ results: [], error: "missing q" }, 400);

  let bias = null;
  if (near) {
    const [la, ln] = near.split(",").map(Number);
    if (isFinite(la) && isFinite(ln)) bias = { la, ln };
  }
  const nearTW = bias ? (bias.la > 20 && bias.la < 27 && bias.ln > 118 && bias.ln < 123.5) : true;

  const gkey = Netlify.env.get("GOOGLE_MAPS_API_KEY");
  let results = [], source = "none";

  if (gkey) {
    if (nearTW) {
      results = await gPlaces(gkey, region ? `${q} ${region}` : `${q} 台灣`, "zh-TW", "TW", bias);
      if (results.length) source = "google";
    }
    if (!results.length) {
      results = await gPlaces(gkey, region ? `${q} ${region}` : q, null, null, bias);
      if (results.length) source = "google";
    }
  }

  if (!results.length) {
    if (nearTW) {
      results = await nominatim([q, region, "台灣"].filter(Boolean).join(" "), "tw");
      if (results.length) source = "osm";
    }
    if (!results.length) {
      results = await nominatim([q, region].filter(Boolean).join(" "), null);
      if (results.length) source = "osm";
    }
  }

  return json({ results, source });
};

async function gPlaces(key, textQuery, lang, regionCode, bias) {
  try {
    const body = { textQuery, maxResultCount: 3 };
    if (lang) body.languageCode = lang;
    if (regionCode) body.regionCode = regionCode;
    if (bias) body.locationBias = { circle: { center: { latitude: bias.la, longitude: bias.ln }, radius: 30000 } };
    const r = await fetch("https://places.googleapis.com/v1/places:searchText", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location",
      },
      body: JSON.stringify(body),
    });
    if (!r.ok) return [];
    const j = await r.json();
    return (j.places || []).map(p => ({
      name: p.displayName?.text || textQuery,
      address: p.formattedAddress || "",
      lat: p.location?.latitude, lng: p.location?.longitude,
    })).filter(p => isFinite(p.lat) && isFinite(p.lng));
  } catch (e) { return []; }
}

async function nominatim(query, countrycodes) {
  try {
    const cc = countrycodes ? "&countrycodes=" + countrycodes : "";
    const r = await fetch(
      "https://nominatim.openstreetmap.org/search?format=json&accept-language=zh-TW,en&limit=3" + cc + "&q=" + encodeURIComponent(query),
      { headers: { "User-Agent": "cycling-almanac-netlify-function", "Accept": "application/json" } }
    );
    if (!r.ok) return [];
    const j = await r.json();
    return (j || []).map(p => ({
      name: (p.display_name || query).split(",")[0],
      address: p.display_name || "",
      lat: +p.lat, lng: +p.lon,
    })).filter(p => isFinite(p.lat) && isFinite(p.lng));
  } catch (e) { return []; }
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status, headers: { "content-type": "application/json; charset=utf-8" },
  });
}

export const config = { path: "/api/geocode" };

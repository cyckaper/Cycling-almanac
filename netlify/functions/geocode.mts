// 地名定位：Google Places（涵蓋小店與地標，最完整）→ 查無或未設金鑰時退 OpenStreetMap
// 建議設定 GOOGLE_MAPS_API_KEY（啟用 Places API (New)）；未設定時仍可用，但小店涵蓋率降低
export default async (req) => {
  const url = new URL(req.url);
  const q = (url.searchParams.get("q") || "").trim();
  const region = (url.searchParams.get("region") || "").trim();
  const near = (url.searchParams.get("near") || "").trim();
  if (!q) return json({ results: [], error: "missing q" }, 400);

  const gkey = Netlify.env.get("GOOGLE_MAPS_API_KEY");
  let results = [], source = "none";

  if (gkey) {
    try {
      const body = {
        textQuery: region ? `${q} ${region}` : `${q} 台灣`,
        languageCode: "zh-TW",
        regionCode: "TW",
        maxResultCount: 3,
      };
      if (near) {
        const [la, ln] = near.split(",").map(Number);
        if (isFinite(la) && isFinite(ln)) {
          body.locationBias = { circle: { center: { latitude: la, longitude: ln }, radius: 30000 } };
        }
      }
      const r = await fetch("https://places.googleapis.com/v1/places:searchText", {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "X-Goog-Api-Key": gkey,
          "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location",
        },
        body: JSON.stringify(body),
      });
      if (r.ok) {
        const j = await r.json();
        results = (j.places || []).map(p => ({
          name: p.displayName?.text || q,
          address: p.formattedAddress || "",
          lat: p.location?.latitude, lng: p.location?.longitude,
        })).filter(p => isFinite(p.lat) && isFinite(p.lng));
        if (results.length) source = "google";
      }
    } catch (e) { /* fall through */ }
  }

  if (!results.length) {
    try {
      const nq = encodeURIComponent([q, region, "台灣"].filter(Boolean).join(" "));
      const r = await fetch(
        "https://nominatim.openstreetmap.org/search?format=json&countrycodes=tw&accept-language=zh-TW&limit=3&q=" + nq,
        { headers: { "User-Agent": "cycling-almanac-netlify-function", "Accept": "application/json" } }
      );
      if (r.ok) {
        const j = await r.json();
        results = (j || []).map(p => ({
          name: (p.display_name || q).split(",")[0],
          address: p.display_name || "",
          lat: +p.lat, lng: +p.lon,
        })).filter(p => isFinite(p.lat) && isFinite(p.lng));
        if (results.length) source = "osm";
      }
    } catch (e) { /* return empty */ }
  }

  return json({ results, source });
};

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status, headers: { "content-type": "application/json; charset=utf-8" },
  });
}

export const config = { path: "/api/geocode" };

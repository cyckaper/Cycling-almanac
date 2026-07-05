// 真實路網導航：OpenRouteService 自行車路徑（含沿線海拔與逐步轉向指示）
// 需要環境變數 ORS_API_KEY（免費申請：https://openrouteservice.org/dev/#/signup）
export default async (req) => {
  if (req.method !== "POST") return json({ error: "POST only" }, 405);
  const key = Netlify.env.get("ORS_API_KEY");
  if (!key) return json({ error: "尚未設定 ORS_API_KEY（Netlify 環境變數）" }, 500);

  let body;
  try { body = await req.json(); } catch { return json({ error: "invalid JSON body" }, 400); }
  const coords = body.coordinates; // [[lng,lat],[lng,lat]] — 一段一段呼叫
  if (!Array.isArray(coords) || coords.length < 2 || coords.length > 5) {
    return json({ error: "coordinates 需為 2–5 個 [lng,lat]" }, 400);
  }

  const profile = body.profile === "cycling-road" ? "cycling-road" : "cycling-regular";
  let r;
  try {
    r = await fetch(`https://api.openrouteservice.org/v2/directions/${profile}/geojson`, {
      method: "POST",
      headers: { "content-type": "application/json", "Authorization": key },
      body: JSON.stringify({
        coordinates: coords,
        elevation: true,
        instructions: true,
        language: "zh-cn", // ORS 尚無 zh-TW；簡中指示可讀，README 有註記
        units: "m",
      }),
    });
  } catch (e) {
    return json({ error: "無法連線 OpenRouteService：" + e.message }, 502);
  }
  if (!r.ok) {
    const t = await r.text();
    return json({ error: "ORS " + r.status, detail: t.slice(0, 300) }, 502);
  }
  const j = await r.json();
  const f = j.features && j.features[0];
  if (!f) return json({ error: "ORS 無路徑結果" }, 502);

  const seg = (f.properties.segments && f.properties.segments[0]) || {};
  const steps = (seg.steps || []).map(s => ({
    instruction: s.instruction, distance: Math.round(s.distance), name: s.name || "",
  }));
  return json({
    distance: seg.distance ?? f.properties.summary?.distance ?? 0,   // 公尺
    duration: seg.duration ?? f.properties.summary?.duration ?? 0,   // 秒（ORS 自估，僅參考）
    ascent: f.properties.ascent ?? 0,
    descent: f.properties.descent ?? 0,
    geometry: f.geometry.coordinates, // [[lng,lat,ele], ...]
    steps,
  });
};

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status, headers: { "content-type": "application/json; charset=utf-8" },
  });
}

export const config = { path: "/api/route" };

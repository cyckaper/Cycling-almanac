// 撤退點驗證：以「路網距離」計算每個騎點到候選車站的實際騎乘距離（非直線）
// 與 route.mts 共用 ORS_API_KEY
export default async (req) => {
  if (req.method !== "POST") return json({ error: "POST only" }, 405);
  const key = Netlify.env.get("ORS_API_KEY");
  if (!key) return json({ error: "尚未設定 ORS_API_KEY（Netlify 環境變數）" }, 500);

  let body;
  try { body = await req.json(); } catch { return json({ error: "invalid JSON body" }, 400); }
  const { sources, destinations } = body; // 各為 [[lng,lat],...]
  if (!Array.isArray(sources) || !Array.isArray(destinations) || !sources.length || !destinations.length) {
    return json({ error: "需要 sources 與 destinations（[lng,lat] 陣列）" }, 400);
  }
  if (sources.length + destinations.length > 45) {
    return json({ error: "地點總數上限 45（請減少候選）" }, 400);
  }

  const locations = [...sources, ...destinations];
  let r;
  try {
    r = await fetch("https://api.openrouteservice.org/v2/matrix/cycling-regular", {
      method: "POST",
      headers: { "content-type": "application/json", "Authorization": key },
      body: JSON.stringify({
        locations,
        sources: sources.map((_, i) => i),
        destinations: destinations.map((_, i) => sources.length + i),
        metrics: ["distance"],
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
  return json({ distances: j.distances || [] }); // 公尺；不可達為 null
};

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status, headers: { "content-type": "application/json; charset=utf-8" },
  });
}

export const config = { path: "/api/matrix" };

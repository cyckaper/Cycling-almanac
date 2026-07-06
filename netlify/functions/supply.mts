// 沿線補給點：超商 / 公廁 / 飲水（OpenStreetMap Overpass）
// 前端傳入抽稀後的路線取樣點（≤240），以 around 多點鏈搜尋走廊 250m 內的節點。
export default async (req) => {
  if (req.method !== "POST") return json({ error: "POST only" }, 405);
  let body; try { body = await req.json(); } catch (e) { return json({ error: "bad json" }, 400); }
  const pts = (body.pts || []).filter(p => Array.isArray(p) && isFinite(p[0]) && isFinite(p[1])).slice(0, 240);
  if (pts.length < 2) return json({ nodes: [] });
  const radius = Math.min(400, Math.max(100, +body.radius || 250));
  const chain = pts.map(p => `${(+p[0]).toFixed(4)},${(+p[1]).toFixed(4)}`).join(",");
  const ql = `[out:json][timeout:14];(` +
    `node(around:${radius},${chain})[shop=convenience];` +
    `node(around:${radius},${chain})[amenity=toilets];` +
    `node(around:${radius},${chain})[amenity=drinking_water];` +
    `);out body 350;`;
  const eps = ["https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter"];
  for (const ep of eps) {
    try {
      const ctl = new AbortController(); const to = setTimeout(() => ctl.abort(), 15000);
      const r = await fetch(ep, {
        method: "POST",
        headers: { "content-type": "application/x-www-form-urlencoded" },
        body: "data=" + encodeURIComponent(ql),
        signal: ctl.signal,
      });
      clearTimeout(to);
      if (!r.ok) continue;
      const j = await r.json();
      const nodes = (j.elements || []).map(e => {
        const t = e.tags || {};
        const k = t.shop === "convenience" ? "store" : t.amenity === "toilets" ? "toilet" : "water";
        return { k, nm: t.name || t.brand || "", lat: e.lat, lng: e.lon };
      }).filter(n => isFinite(n.lat) && isFinite(n.lng)).slice(0, 350);
      return json({ nodes });
    } catch (e) {}
  }
  return json({ nodes: [], error: "overpass unavailable" });
};
function json(o, s = 200) {
  return new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json; charset=utf-8" } });
}
export const config = { path: "/api/supply" };

// 沿線補給點：超商 / 公廁 / 飲水（OpenStreetMap Overpass）v2.2.1
// - nwr + out center：node 與建物面(way)一起撈（台灣超商/公廁大量以面標註）
// - 兩鏡像並行競速，總時限貼合 Netlify Functions 10 秒上限
// - 全數失敗回 503（前端據此「不畫」而非誤示「無補給」）
export default async (req) => {
  if (req.method !== "POST") return json({ error: "POST only" }, 405);
  let body; try { body = await req.json(); } catch (e) { return json({ error: "bad json" }, 400); }
  const pts = (body.pts || []).filter(p => Array.isArray(p) && isFinite(p[0]) && isFinite(p[1])).slice(0, 240);
  if (pts.length < 2) return json({ nodes: [] });
  const radius = Math.min(400, Math.max(100, +body.radius || 250));
  const chain = pts.map(p => `${(+p[0]).toFixed(4)},${(+p[1]).toFixed(4)}`).join(",");
  const ql = `[out:json][timeout:8];nwr[~"^(shop|amenity)$"~"^(convenience|toilets|drinking_water)$"](around:${radius},${chain});out center 350;`;

  const eps = ["https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter", "https://overpass.osm.jp/api/interpreter"];
  const attempt = async (ep) => {
    const ctl = new AbortController(); const to = setTimeout(() => ctl.abort(), 8500);
    try {
      const r = await fetch(ep, {
        method: "POST",
        headers: { "content-type": "application/x-www-form-urlencoded", "user-agent": "xiaobu-roadbook (netlify fn)" },
        body: "data=" + encodeURIComponent(ql),
        signal: ctl.signal,
      });
      if (!r.ok) { const t = await r.text().catch(() => ""); throw new Error(`${ep} ${r.status} ${t.slice(0, 160)}`); }
      return await r.json();
    } finally { clearTimeout(to); }
  };

  let j = null; const errs = [];
  await new Promise(resolve => {
    let pending = eps.length;
    eps.forEach(ep => attempt(ep).then(res => { if (!j) { j = res; resolve(); } if (--pending === 0) resolve(); })
                               .catch(e => { errs.push(String(e && e.message || e)); if (--pending === 0) resolve(); }));
  });
  if (!j) return json({ error: "overpass unavailable", detail: errs.slice(0, 2) }, 503);

  const nodes = (j.elements || []).map(e => {
    const t = e.tags || {};
    const k = t.shop === "convenience" ? "store" : t.amenity === "toilets" ? "toilet" : "water";
    const lat = e.lat ?? (e.center && e.center.lat);
    const lng = e.lon ?? (e.center && e.center.lon);
    return { k, nm: t.name || t.brand || "", lat, lng };
  }).filter(n => isFinite(n.lat) && isFinite(n.lng)).slice(0, 350);
  return json({ nodes });
};
function json(o, s = 200) {
  return new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json; charset=utf-8" } });
}
export const config = { path: "/api/supply" };

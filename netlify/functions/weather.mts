// 逐時天氣：CWA 鄉鎮逐3小時預報（主）→ Open-Meteo（備援）；UV 由 Open-Meteo 補充
// 需要 CWA_API_KEY（免費：opendata.cwa.gov.tw 註冊 → 取得 API 授權碼）
// 未設定或查詢失敗時自動退 Open-Meteo，回應中的 source 會如實標示

// 縣市 → CWA「未來2天逐3小時」資料集編號
const COUNTY_DS = {
  "宜蘭縣":"F-D0047-001","桃園市":"F-D0047-005","新竹縣":"F-D0047-009","苗栗縣":"F-D0047-013",
  "彰化縣":"F-D0047-017","南投縣":"F-D0047-021","雲林縣":"F-D0047-025","嘉義縣":"F-D0047-029",
  "屏東縣":"F-D0047-033","臺東縣":"F-D0047-037","花蓮縣":"F-D0047-041","澎湖縣":"F-D0047-045",
  "基隆市":"F-D0047-049","新竹市":"F-D0047-053","嘉義市":"F-D0047-057","臺北市":"F-D0047-061",
  "高雄市":"F-D0047-065","新北市":"F-D0047-069","臺中市":"F-D0047-073","臺南市":"F-D0047-077",
  "連江縣":"F-D0047-081","金門縣":"F-D0047-085",
};
const WD_DEG = { "偏北":0,"東北":45,"偏東":90,"東南":135,"偏南":180,"西南":225,"偏西":270,"西北":315 };

const revCache = new Map();   // "lat,lng"(2dp) → {county,town}
const cwaCache = new Map();   // dsid|town → {t, data}
const TTL = 30 * 60 * 1000;

export default async (req) => {
  if (req.method !== "POST") return json({ error: "POST only" }, 405);
  let body; try { body = await req.json(); } catch { return json({ error: "invalid JSON body" }, 400); }
  const pts = Array.isArray(body.points) ? body.points.slice(0, 12) : [];
  if (!pts.length) return json({ error: "points 為空" }, 400);
  const cwaKey = Netlify.env.get("CWA_API_KEY");
  // 出發日期（可為未來日）：CWA 鄉鎮逐3小時僅涵蓋約2天，超過改用 Open-Meteo 7天預報
  let hoursAhead = 0;
  if (body.date && /^\d{4}-\d{2}-\d{2}$/.test(body.date)) {
    const target = Date.parse(body.date + "T12:00:00+08:00");
    if (isFinite(target)) hoursAhead = (target - Date.now()) / 3600e3;
  }
  const cwaUsable = cwaKey && hoursAhead <= 40;

  const out = [];
  for (const p of pts) {
    if (!isFinite(p.lat) || !isFinite(p.lng)) { out.push({ source: "none" }); continue; }
    let rec = null;
    if (cwaUsable) rec = await tryCwa(p, cwaKey).catch(() => null);
    if (!rec) rec = await tryOpenMeteo(p).catch(() => null);
    out.push(rec || { source: "none" });
  }
  return json({ points: out });
};

async function reverseTown(p) {
  const k = p.lat.toFixed(2) + "," + p.lng.toFixed(2);
  if (revCache.has(k)) return revCache.get(k);
  const r = await fetch(
    `https://nominatim.openstreetmap.org/reverse?format=json&zoom=10&accept-language=zh-TW&lat=${p.lat}&lon=${p.lng}`,
    { headers: { "User-Agent": "cycling-almanac-netlify-function", Accept: "application/json" } }
  );
  if (!r.ok) return null;
  const a = (await r.json()).address || {};
  const county = norm(a.county || a.city || "");
  const town = a.town || a.city_district || a.district || a.suburb || a.village || "";
  const v = county && town ? { county, town } : null;
  revCache.set(k, v);
  return v;
}
function norm(s) { return String(s).replace(/台/g, "臺").trim(); }

async function tryCwa(p, key) {
  const loc = await reverseTown(p);
  if (!loc) return null;
  const ds = COUNTY_DS[loc.county];
  if (!ds) return null;
  const ck = ds + "|" + loc.town;
  const now = Date.now();
  let data = null;
  const hit = cwaCache.get(ck);
  if (hit && now - hit.t < TTL) data = hit.data;
  if (!data) {
    const url = `https://opendata.cwa.gov.tw/api/v1/rest/datastore/${ds}?Authorization=${encodeURIComponent(key)}&locationName=${encodeURIComponent(loc.town)}&format=JSON`;
    const r = await fetch(url, { headers: { Accept: "application/json" } });
    if (!r.ok) return null;
    data = await r.json();
    cwaCache.set(ck, { t: now, data });
  }
  const recs = data.records || {};
  const Ls = recs.Locations || recs.locations || [];
  const L0 = Ls[0] || {};
  const locs = L0.Location || L0.location || [];
  const l0 = locs[0];
  if (!l0) return null;
  const els = l0.WeatherElement || l0.weatherElement || [];
  const findEl = (kw) => els.find(e => String(e.ElementName || e.elementName || "").includes(kw));
  const series = (el) => (el ? (el.Time || el.time || []).map(t => ({
    ms: toMs(t.DataTime || t.StartTime || t.dataTime || t.startTime),
    v: firstVal(t.ElementValue || t.elementValue),
  })).filter(x => x.ms) : []);

  const T = series(findEl("溫度")).filter(x => isFinite(parseFloat(x.v)));
  if (!T.length) return null;
  const POP = series(findEl("降雨機率"));
  const WS = series(findEl("風速"));
  const WD = series(findEl("風向"));
  const time = T.map(x => x.ms);
  const pick = (S, numeric = true) => time.map(ms => {
    if (!S.length) return null;
    let best = S[0];
    for (const s of S) if (Math.abs(s.ms - ms) < Math.abs(best.ms - ms)) best = s;
    if (!numeric) return best.v;
    const f = parseFloat(best.v);
    return isFinite(f) ? f : null;
  });
  const wdDeg = pick(WD, false).map(txt => {
    if (txt == null) return null;
    const f = parseFloat(txt);
    if (isFinite(f)) return f;
    for (const k in WD_DEG) if (String(txt).includes(k)) return WD_DEG[k];
    return null;
  });

  let uvi = null;
  try { uvi = await omUv(p, time); } catch {}
  return {
    source: "cwa",
    label: `${loc.county}${loc.town}`,
    hourly: {
      time,
      temp: T.map(x => parseFloat(x.v)),
      pop: pick(POP),
      windSpd: pick(WS).map(v => v == null ? null : Math.round(v * 3.6)), // m/s → km/h
      windDirDeg: wdDeg,
      uvi,
    },
  };
}

async function tryOpenMeteo(p) {
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${p.lat}&longitude=${p.lng}` +
    `&hourly=temperature_2m,precipitation_probability,wind_speed_10m,wind_direction_10m,uv_index` +
    `&forecast_days=7&timezone=Asia%2FTaipei`;
  const r = await fetch(url);
  if (!r.ok) return null;
  const j = await r.json();
  const H = j.hourly || {};
  if (!H.time) return null;
  return {
    source: "open-meteo",
    label: "Open-Meteo",
    hourly: {
      time: H.time.map(t => toMs(t)),
      temp: H.temperature_2m || [],
      pop: H.precipitation_probability || [],
      windSpd: H.wind_speed_10m || [],
      windDirDeg: H.wind_direction_10m || [],
      uvi: H.uv_index || [],
    },
  };
}
async function omUv(p, timeMs) {
  const r = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${p.lat}&longitude=${p.lng}&hourly=uv_index&forecast_days=7&timezone=Asia%2FTaipei`);
  if (!r.ok) return null;
  const j = await r.json(), H = j.hourly || {};
  if (!H.time) return null;
  const om = H.time.map((t, i) => ({ ms: toMs(t), v: H.uv_index[i] }));
  return timeMs.map(ms => {
    let best = om[0];
    for (const s of om) if (Math.abs(s.ms - ms) < Math.abs(best.ms - ms)) best = s;
    return best ? best.v : null;
  });
}
function toMs(t) {
  if (!t) return null;
  let s = String(t).replace(" ", "T");
  if (!/[Zz+\-]\d{0,2}:?\d{0,2}$/.test(s)) s += "+08:00";
  const ms = Date.parse(s);
  return isFinite(ms) ? ms : null;
}
function firstVal(arr) {
  if (!arr || !arr[0]) return null;
  const o = arr[0];
  const vals = Object.values(o);
  return vals.length ? vals[0] : null;
}
function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status, headers: { "content-type": "application/json; charset=utf-8" },
  });
}

export const config = { path: "/api/weather" };

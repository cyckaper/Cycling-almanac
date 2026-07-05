// TDX 台鐵全站清單（選用）：補齊內建車站底圖，作為撤退點候選
// 需要 TDX_CLIENT_ID / TDX_CLIENT_SECRET（免費申請：https://tdx.transportdata.tw/）
// 未設定時回傳空清單，前端自動改用內建車站，不影響運作
let cache = { token: null, tokenExp: 0, stations: null, staExp: 0 };

export default async (req) => {
  const id = Netlify.env.get("TDX_CLIENT_ID");
  const secret = Netlify.env.get("TDX_CLIENT_SECRET");
  if (!id || !secret) return json({ stations: [], note: "TDX 未設定，使用內建車站清單" });

  const now = Date.now();
  if (cache.stations && now < cache.staExp) {
    return json({ stations: cache.stations, cached: true });
  }

  try {
    if (!cache.token || now >= cache.tokenExp) {
      const tr = await fetch(
        "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token",
        {
          method: "POST",
          headers: { "content-type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams({
            grant_type: "client_credentials",
            client_id: id,
            client_secret: secret,
          }),
        }
      );
      if (!tr.ok) return json({ stations: [], error: "TDX token " + tr.status }, 502);
      const tj = await tr.json();
      cache.token = tj.access_token;
      cache.tokenExp = now + Math.max(60, (tj.expires_in || 1800) - 120) * 1000;
    }

    const sr = await fetch(
      "https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/Station?%24format=JSON",
      { headers: { Authorization: "Bearer " + cache.token } }
    );
    if (!sr.ok) return json({ stations: [], error: "TDX station " + sr.status }, 502);
    const sj = await sr.json();
    const list = (sj.Stations || sj || []).map(s => ([
      s.StationName?.Zh_tw || s.StationName || "",
      s.StationPosition?.PositionLat,
      s.StationPosition?.PositionLon,
      "台鐵",
    ])).filter(x => x[0] && isFinite(x[1]) && isFinite(x[2]));

    cache.stations = list;
    cache.staExp = now + 24 * 3600 * 1000; // 一天更新一次即可
    return json({ stations: list });
  } catch (e) {
    return json({ stations: [], error: "TDX 連線失敗：" + e.message }, 502);
  }
};

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status, headers: { "content-type": "application/json; charset=utf-8" },
  });
}

export const config = { path: "/api/stations" };

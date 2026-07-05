import json, math

# ================= gazetteer (known Taiwan cycling spots) =================
# wzone: basin | valley | coast | exposed | lake
GAZ = [
 {"n":"動物園站","a":["動物園","木柵動物園"],"lat":24.998,"lng":121.579,"elev":30,"wz":"basin",
  "esc":{"st":"捷運 動物園站","km":0,"hard":False}},
 {"n":"平溪車站","a":["平溪"],"lat":25.025,"lng":121.740,"elev":210,"wz":"valley",
  "esc":{"st":"平溪線 平溪站","km":0.1,"hard":False}},
 {"n":"嶺腳瀑布","a":["嶺腳"],"lat":25.028,"lng":121.723,"elev":150,"wz":"valley",
  "esc":{"st":"平溪線 嶺腳站","km":0.3,"hard":False}},
 {"n":"雙溪荷花園","a":["雙溪荷花","荷花園"],"lat":25.033,"lng":121.831,"elev":60,"wz":"valley",
  "esc":{"st":"宜蘭線 雙溪站","km":1.5,"hard":False}},
 {"n":"雙溪老街","a":["雙溪"],"lat":25.037,"lng":121.866,"elev":40,"wz":"valley",
  "esc":{"st":"宜蘭線 雙溪站","km":0.4,"hard":False}},
 {"n":"貢寮","a":["貢寮車站"],"lat":25.021,"lng":121.908,"elev":25,"wz":"coast",
  "esc":{"st":"宜蘭線 貢寮站","km":0.5,"hard":False}},
 {"n":"桃源谷","a":["草嶺線","桃源谷大草原"],"lat":24.997,"lng":121.936,"elev":500,"wz":"exposed",
  "esc":{"st":"稀少 · 退福隆 ~9km／下切大里古道","km":9,"hard":True}},
 {"n":"福隆車站","a":["福隆"],"lat":25.015,"lng":121.944,"elev":10,"wz":"coast",
  "esc":{"st":"宜蘭線 福隆站","km":0,"hard":False}},
 {"n":"大稻埕碼頭","a":["大稻埕"],"lat":25.055,"lng":121.510,"elev":6,"wz":"basin",
  "esc":{"st":"捷運 大橋頭站","km":0.8,"hard":False}},
 {"n":"大佳河濱公園","a":["大佳","大佳河濱"],"lat":25.078,"lng":121.542,"elev":6,"wz":"basin",
  "esc":{"st":"捷運 劍南路站","km":1.6,"hard":False}},
 {"n":"關渡金色水岸","a":["關渡","關渡水岸"],"lat":25.118,"lng":121.462,"elev":5,"wz":"basin",
  "esc":{"st":"捷運 關渡站","km":0.7,"hard":False}},
 {"n":"八里左岸","a":["八里"],"lat":25.152,"lng":121.439,"elev":5,"wz":"coast",
  "esc":{"st":"渡輪轉捷運 淡水站","km":0.5,"hard":False}},
 {"n":"淡水金色水岸","a":["淡水","淡水水岸"],"lat":25.167,"lng":121.438,"elev":4,"wz":"coast",
  "esc":{"st":"捷運 淡水站","km":0.3,"hard":False}},
 {"n":"新店碧潭","a":["碧潭"],"lat":24.957,"lng":121.537,"elev":15,"wz":"basin",
  "esc":{"st":"捷運 新店站","km":0.2,"hard":False}},
 {"n":"貓空","a":["貓空纜車"],"lat":24.968,"lng":121.590,"elev":300,"wz":"exposed",
  "esc":{"st":"貓空纜車 貓空站","km":0.5,"hard":False}},
 {"n":"陽明山","a":["陽明山國家公園","竹子湖"],"lat":25.155,"lng":121.560,"elev":500,"wz":"exposed",
  "esc":{"st":"僅公車（無鄰近車站）","km":0,"hard":True}},
 {"n":"日月潭環潭","a":["日月潭"],"lat":23.858,"lng":120.915,"elev":748,"wz":"lake",
  "esc":{"st":"客運 日月潭站（無鐵路）","km":0.5,"hard":True}},
 {"n":"武嶺","a":["合歡山","合歡山主峰"],"lat":24.137,"lng":121.275,"elev":3275,"wz":"exposed",
  "esc":{"st":"無鄰近轉進點，最近聚落數十公里","km":0,"hard":True}},
 {"n":"西門紅樓","a":["西門","紅樓","西門町"],"lat":25.042,"lng":121.507,"elev":10,"wz":"basin",
  "esc":{"st":"捷運 西門站","km":0.2,"hard":False}},
 {"n":"圓山飯店","a":["圓山","圓山大飯店"],"lat":25.079,"lng":121.526,"elev":40,"wz":"basin",
  "esc":{"st":"捷運 圓山站","km":1.0,"hard":False}},
 {"n":"士林官邸","a":["士林官邸公園"],"lat":25.093,"lng":121.531,"elev":15,"wz":"basin",
  "esc":{"st":"捷運 士林站","km":1.0,"hard":False}},
 {"n":"外雙溪","a":["故宮","故宮博物院","至善路"],"lat":25.102,"lng":121.549,"elev":40,"wz":"valley",
  "esc":{"st":"捷運 士林站","km":3.0,"hard":False}},
 {"n":"帕米爾公園","a":["帕米爾"],"lat":25.118,"lng":121.531,"elev":250,"wz":"valley",
  "esc":{"st":"僅公車（無鄰近車站）","km":0,"hard":True}},
 {"n":"風櫃嘴","a":["風櫃嘴亭","五指山"],"lat":25.140,"lng":121.606,"elev":611,"wz":"exposed",
  "esc":{"st":"僅公車（無鄰近車站）","km":0,"hard":True}},
 {"n":"萬里","a":["萬里區"],"lat":25.181,"lng":121.689,"elev":10,"wz":"coast",
  "esc":{"st":"無鄰近車站（客運）","km":0,"hard":True}},
 {"n":"基隆","a":["基隆車站","基隆火車站","基隆港"],"lat":25.132,"lng":121.740,"elev":8,"wz":"coast",
  "esc":{"st":"台鐵 基隆站","km":0.3,"hard":False}},
 {"n":"七星潭","a":["七星潭風景區"],"lat":24.030,"lng":121.625,"elev":6,"wz":"coast",
  "esc":{"st":"台鐵 北埔站","km":3.5,"hard":False}},
 {"n":"新城老街","a":["新城","新城天主堂"],"lat":24.128,"lng":121.641,"elev":10,"wz":"coast",
  "esc":{"st":"台鐵 新城站","km":0.4,"hard":False}},
 {"n":"太魯閣","a":["太魯閣牌樓","太魯閣遊客中心","太魯閣國家公園","太魯閣口"],"lat":24.158,"lng":121.622,"elev":60,"wz":"valley",
  "esc":{"st":"台鐵 新城站","km":3,"hard":False}},
 {"n":"長春祠","a":["長春祠步道"],"lat":24.168,"lng":121.596,"elev":120,"wz":"valley",
  "esc":{"st":"台鐵 新城站","km":8,"hard":False}},
 {"n":"燕子口","a":["燕子口步道"],"lat":24.174,"lng":121.552,"elev":350,"wz":"exposed",
  "esc":{"st":"稀少 · 退新城 ~14km","km":14,"hard":True}},
 {"n":"慈母橋","a":["綠水"],"lat":24.176,"lng":121.520,"elev":470,"wz":"exposed",
  "esc":{"st":"稀少 · 退新城 ~18km","km":18,"hard":True}},
 {"n":"天祥","a":["天祥青年活動中心","天祥晶英","天祥天主堂","祥德寺"],"lat":24.183,"lng":121.492,"elev":480,"wz":"exposed",
  "esc":{"st":"稀少 · 退新城 ~21km","km":21,"hard":True}},
]

# ================= station list: major TRA + Taipei/New Taipei Metro =================
# [name, lat, lng, system]   (coords approximate — for nearest-station selection)
STATIONS = [
 # 台鐵 縱貫線北段 + 主要西/南站
 ["基隆",25.131,121.740,"台鐵"],["七堵",25.096,121.713,"台鐵"],["汐止",25.069,121.662,"台鐵"],
 ["南港",25.053,121.607,"台鐵"],["松山",25.049,121.577,"台鐵"],["臺北",25.048,121.517,"台鐵"],
 ["萬華",25.033,121.500,"台鐵"],["板橋",25.014,121.464,"台鐵"],["樹林",24.991,121.426,"台鐵"],
 ["鶯歌",24.954,121.354,"台鐵"],["桃園",24.989,121.314,"台鐵"],["中壢",24.954,121.225,"台鐵"],
 ["新竹",24.802,120.972,"台鐵"],["竹南",24.686,120.873,"台鐵"],["苗栗",24.569,120.826,"台鐵"],
 ["臺中",24.137,120.686,"台鐵"],["彰化",24.082,120.538,"台鐵"],["員林",23.959,120.571,"台鐵"],
 ["斗六",23.712,120.535,"台鐵"],["嘉義",23.479,120.442,"台鐵"],["臺南",22.997,120.212,"台鐵"],
 ["高雄",22.639,120.302,"台鐵"],["屏東",22.671,120.488,"台鐵"],["潮州",22.550,120.543,"台鐵"],
 # 台鐵 宜蘭線 / 北迴線 / 花東線
 ["八堵",25.109,121.723,"台鐵"],["瑞芳",25.108,121.806,"台鐵"],["猴硐",25.087,121.828,"台鐵"],
 ["三貂嶺",25.061,121.824,"台鐵"],["牡丹",25.038,121.849,"台鐵"],["雙溪",25.037,121.866,"台鐵"],
 ["貢寮",25.021,121.908,"台鐵"],["福隆",25.015,121.944,"台鐵"],["石城",24.983,121.941,"台鐵"],
 ["大里",24.968,121.918,"台鐵"],["頭城",24.859,121.823,"台鐵"],["礁溪",24.827,121.774,"台鐵"],
 ["宜蘭",24.752,121.751,"台鐵"],["羅東",24.677,121.766,"台鐵"],["冬山",24.635,121.792,"台鐵"],
 ["蘇澳新",24.599,121.833,"台鐵"],["蘇澳",24.594,121.848,"台鐵"],["東澳",24.499,121.831,"台鐵"],
 ["南澳",24.464,121.800,"台鐵"],["和平",24.309,121.755,"台鐵"],["崇德",24.212,121.643,"台鐵"],
 ["新城",24.128,121.641,"台鐵"],["花蓮",23.993,121.601,"台鐵"],["吉安",23.966,121.578,"台鐵"],
 ["志學",23.923,121.545,"台鐵"],["壽豐",23.868,121.508,"台鐵"],["鳳林",23.745,121.451,"台鐵"],
 ["光復",23.669,121.421,"台鐵"],["瑞穗",23.497,121.377,"台鐵"],["玉里",23.337,121.315,"台鐵"],
 ["富里",23.180,121.245,"台鐵"],["池上",23.122,121.215,"台鐵"],["關山",23.049,121.161,"台鐵"],
 ["鹿野",22.921,121.135,"台鐵"],["臺東",22.793,121.130,"台鐵"],
 # 台鐵 平溪 / 深澳 / 集集 支線
 ["海科館",25.135,121.803,"台鐵"],["八斗子",25.139,121.803,"台鐵"],["大華",25.045,121.808,"台鐵"],
 ["十分",25.043,121.775,"台鐵"],["望古",25.036,121.760,"台鐵"],["嶺腳",25.028,121.742,"台鐵"],
 ["平溪",25.025,121.740,"台鐵"],["菁桐",25.023,121.726,"台鐵"],
 ["二水",23.809,120.617,"台鐵"],["集集",23.828,120.785,"台鐵"],["車埕",23.836,120.855,"台鐵"],
 # 捷運 淡水信義線
 ["淡水",25.168,121.446,"捷運"],["紅樹林",25.155,121.459,"捷運"],["竹圍",25.137,121.460,"捷運"],
 ["關渡",25.126,121.467,"捷運"],["北投",25.131,121.499,"捷運"],["新北投",25.137,121.503,"捷運"],
 ["石牌",25.114,121.515,"捷運"],["士林",25.094,121.526,"捷運"],["劍潭",25.084,121.525,"捷運"],
 ["圓山",25.071,121.520,"捷運"],["民權西路",25.063,121.519,"捷運"],["中山",25.053,121.520,"捷運"],
 ["台北車站",25.048,121.517,"捷運"],["中正紀念堂",25.033,121.518,"捷運"],["東門",25.034,121.529,"捷運"],
 ["大安",25.033,121.543,"捷運"],["信義安和",25.033,121.552,"捷運"],["台北101",25.033,121.563,"捷運"],
 ["象山",25.032,121.570,"捷運"],
 # 捷運 松山新店線
 ["古亭",25.026,121.523,"捷運"],["台電大樓",25.021,121.528,"捷運"],["公館",25.015,121.534,"捷運"],
 ["景美",24.993,121.541,"捷運"],["大坪林",24.983,121.541,"捷運"],["七張",24.977,121.542,"捷運"],
 ["新店區公所",24.968,121.537,"捷運"],["新店",24.958,121.537,"捷運"],["西門",25.042,121.508,"捷運"],
 ["松江南京",25.052,121.533,"捷運"],["南京復興",25.052,121.544,"捷運"],["台北小巨蛋",25.052,121.551,"捷運"],
 ["南京三民",25.052,121.560,"捷運"],["松山",25.050,121.578,"捷運"],
 # 捷運 板南線
 ["龍山寺",25.035,121.500,"捷運"],["江子翠",25.030,121.474,"捷運"],["新埔",25.023,121.468,"捷運"],
 ["板橋",25.014,121.462,"捷運"],["府中",25.008,121.459,"捷運"],["亞東醫院",24.998,121.452,"捷運"],
 ["土城",24.973,121.444,"捷運"],["永寧",24.967,121.436,"捷運"],["頂埔",24.960,121.420,"捷運"],
 ["忠孝新生",25.042,121.533,"捷運"],["忠孝復興",25.042,121.544,"捷運"],["忠孝敦化",25.042,121.551,"捷運"],
 ["國父紀念館",25.041,121.557,"捷運"],["市政府",25.041,121.565,"捷運"],["永春",25.041,121.576,"捷運"],
 ["後山埤",25.045,121.582,"捷運"],["昆陽",25.051,121.593,"捷運"],["南港展覽館",25.055,121.618,"捷運"],
 # 捷運 文湖線
 ["動物園",24.998,121.579,"捷運"],["木柵",24.998,121.573,"捷運"],["萬芳社區",24.999,121.568,"捷運"],
 ["六張犁",25.024,121.553,"捷運"],["科技大樓",25.026,121.543,"捷運"],["中山國中",25.061,121.544,"捷運"],
 ["松山機場",25.062,121.552,"捷運"],["大直",25.079,121.547,"捷運"],["劍南路",25.084,121.556,"捷運"],
 ["西湖",25.082,121.567,"捷運"],["內湖",25.084,121.594,"捷運"],
 # 捷運 中和新蘆線
 ["行天宮",25.062,121.533,"捷運"],["中山國小",25.063,121.526,"捷運"],["大橋頭",25.063,121.512,"捷運"],
 ["三重國小",25.070,121.496,"捷運"],["菜寮",25.061,121.489,"捷運"],["頭前庄",25.049,121.460,"捷運"],
 ["新莊",25.037,121.451,"捷運"],["輔大",25.032,121.433,"捷運"],["迴龍",25.028,121.418,"捷運"],
 ["三民高中",25.079,121.484,"捷運"],["蘆洲",25.085,121.472,"捷運"],["頂溪",25.012,121.515,"捷運"],
 ["永安市場",24.994,121.512,"捷運"],["景安",24.994,121.505,"捷運"],["南勢角",24.986,121.507,"捷運"],
 # 捷運 環狀線
 ["新北產業園區",25.062,121.459,"捷運"],["板新",25.021,121.469,"捷運"],["中和",25.001,121.480,"捷運"],
 ["景平",24.992,121.510,"捷運"],["十四張",24.987,121.532,"捷運"],
]


T = [
("立春","2 / 4","春寒料峭，河風仍利，萬物將動。",["短程暖身","河濱緩騎"],["逞強遠征"],"午後微陽","輪未轉熱，先養腿力。","spring"),
("雨水","2 / 19","細雨綿綿，路面常濕，木棉始綻街角。",["雨歇即出","市區慢遊"],["雨中急煞","下坡逞快"],"雨停初晴","濕路如薄冰，寧緩勿急。","spring"),
("驚蟄","3 / 5","春雷乍響，蟄蟲始振，苦楝冒紫。",["解凍遠騎","訪春之庭園"],["晨出未暖身"],"午後","身已解凍，心也該出門。","spring"),
("春分","3 / 20","晝夜均分，風溫日暖。",["全日長程","結伴同行"],["此格無忌"],"整日","晝夜各半，正好把路騎成一條中庸。","spring"),
("清明","4 / 4","天清氣明，梅雨未至，一年最穩。",["多日縱走","訪古道兼掃墓"],["辜負這片晴好"],"整日","此時不縱走，更待何時。","spring"),
("穀雨","4 / 20","雨生百穀，油桐落如五月雪。",["山區賞桐","雨前搶騎"],["輕忽午後雷陣"],"上午","把握梅雨前最後的乾爽。","spring"),
("立夏","5 / 5","暑氣初起，入梅在即。",["清晨出行","隨身備雨"],["正午曝騎"],"破曉","夏門已開，與雨賽跑的季節到了。","summer"),
("小滿","5 / 21","梅雨綿延，溪水漸漲。",["雨窗短騎","河濱看水"],["低地溪畔","雷雨將至"],"雨歇之間","水未滿則騎，水將滿則歸。","summer"),
("芒種","6 / 6","鳳凰始燃於路口，梅雨將盡。",["晨昏兩頭騎","賞鳳凰木"],["正午堤頂"],"清晨與黃昏","日頭毒了，騎乘往兩頭退。","summer"),
("夏至","6 / 21","白晝最長，暑氣方盛。",["極早出行","善用長日"],["午後曝曬"],"天未亮","日最長，影最短，人要躲著太陽走。","summer"),
("小暑","7 / 7","颱風季啟，溽暑悶熱。",["盯緊颱風","把握晴窗"],["風雨將至仍出"],"清晨","看天色，更要看氣象。","summer"),
("大暑","7 / 22","一年最熱，平地如灶。",["破曉出門","上山避暑（武嶺、中橫）"],["平地正午"],"日出前","平地如灶，把車騎上山去。","summer"),
("立秋","8 / 7","暑未消，颱風正盛。",["颱風空檔","傍晚乘涼"],["颱前颱後近溪"],"傍晚","秋字雖立，暑與颱猶在。","autumn"),
("處暑","8 / 23","暑氣將止，晚風初涼。",["黃昏騎乘","河濱納涼"],["輕信秋涼而曝曬"],"日落前後","暑氣退場，涼意排隊進來。","autumn"),
("白露","9 / 7","河面始霧，呼吸見白。",["晨霧河濱","添薄長袖"],["薄衫貪涼"],"清晨","露白了，該為手臂添一層。","autumn"),
("秋分","9 / 23","晝夜再均，季風前的黃金窗。",["長程縱走","結伴遠行"],["錯過這片清朗"],"整日","風起之前，把遠路騎個夠。","autumn"),
("寒露","10 / 8","東北季風初臨，轉涼起風。",["背風路線","向陽而行"],["迎風硬騎"],"午後向陽","風從東北來，路就往背風選。","autumn"),
("霜降","10 / 23","北風漸勁，氣溫下探。",["正午暖時","添件風衣"],["清晨迎風"],"正午","風利了，挑暖的時辰騎。","autumn"),
("立冬","11 / 7","季風穩定，台北濕冷。",["晴日把握","保暖層疊"],["濕冷迎風遠征"],"正午晴時","冬門已掩，騎乘趁晴。","winter"),
("小雪","11 / 22","北地飄雪，在台只是濕涼。",["向陽河段","短程暖身"],["陰雨迎風"],"午後","此地無雪，只有濕與風。","winter"),
("大雪","12 / 7","名為大雪，在台不過冬雨。",["晴窗短騎","溫熱收尾"],["貪遠受寒"],"正午","名與實之間，正是台灣的趣味。","winter"),
("冬至","12 / 22","白晝最短，與光賽跑。",["短程早歸","湯圓暖身"],["摸黑遠歸"],"正午前後","日最短，早歸早暖。","winter"),
("小寒","1 / 5","漸入嚴寒（台灣式）。",["南向追陽","台東暖騎"],["寒流迎風"],"正午","北邊冷了，車頭就往南偏。","winter"),
("大寒","1 / 20","一年最冷，然台灣猶可騎。",["南部逐暖","台東追陽"],["寒流高地"],"正午","最冷一格，也是輪將轉回春天的前夜。","winter"),
]
SEASON = {"spring":("春","Spring","#5FA046"),"summer":("夏","Summer","#CE8418"),
          "autumn":("秋","Autumn","#BE5027"),"winter":("冬","Winter","#34877C")}
# term start [month, day] for "today" detection (JS uses these)
TERM_STARTS = [[2,4],[2,19],[3,5],[3,20],[4,4],[4,20],[5,5],[5,21],[6,6],[6,21],[7,7],[7,22],
 [8,7],[8,23],[9,7],[9,23],[10,8],[10,23],[11,7],[11,22],[12,7],[12,22],[1,5],[1,20]]

# ================= build wheel SVG =================
cx,cy=240,240; r_label=222; r_rim_out=198; r_rim_in=183; r_spoke_out=181; r_hub=47
def pol(r,deg):
    a=math.radians(deg); return cx+r*math.cos(a), cy+r*math.sin(a)
def arc_path(r,a0,a1):
    x0,y0=pol(r,a0); x1,y1=pol(r,a1); large=1 if (a1-a0)%360>180 else 0
    return f"M {x0:.2f} {y0:.2f} A {r} {r} 0 {large} 1 {x1:.2f} {y1:.2f}"
sv=[f'<svg class="wheel" viewBox="0 0 480 480" role="img" aria-label="二十四節氣車輪">']
sv.append(f'<circle cx="{cx}" cy="{cy}" r="{r_rim_out+6}" fill="none" stroke="#2A2622" stroke-width="2" opacity="0.18"/>')
order=["spring","summer","autumn","winter"]
for si,sk in enumerate(order):
    a0=-90+si*90-7.5; a1=a0+90
    sv.append(f'<path d="{arc_path((r_rim_out+r_rim_in)/2,a0,a1)}" fill="none" stroke="{SEASON[sk][2]}" stroke-width="{r_rim_out-r_rim_in}" opacity="0.95"/>')
for si,sk in enumerate(order):
    am=-90+si*90+37.5; wx_,wy_=pol(118,am)
    sv.append(f'<text x="{wx_:.1f}" y="{wy_:.1f}" class="wmk" fill="{SEASON[sk][2]}" text-anchor="middle" dominant-baseline="central">{SEASON[sk][0]}</text>')
for i,row in enumerate(T):
    sk=row[7]; col=SEASON[sk][2]; deg=-90+i*15
    x1,y1=pol(r_hub+3,deg); x2,y2=pol(r_spoke_out,deg)
    sv.append(f'<line id="wsp-{i}" x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{col}" stroke-width="1.2" opacity="0.62"/>')
    dx,dy=pol(r_rim_in-2,deg); sv.append(f'<circle cx="{dx:.2f}" cy="{dy:.2f}" r="2.6" fill="{col}"/>')
    lx,ly=pol(r_label,deg)
    sv.append(f'<text id="wlbl-{i}" data-x="{lx:.2f}" data-y="{ly:.2f}" x="{lx:.2f}" y="{ly:.2f}" class="wlbl" text-anchor="middle" dominant-baseline="central">{row[0]}</text>')
sv.append(f'<circle cx="{cx}" cy="{cy}" r="{r_hub}" fill="#FBF8F0" stroke="#BE3D24" stroke-width="2.5"/>')
sv.append(f'<circle cx="{cx}" cy="{cy}" r="{r_hub-8}" fill="none" stroke="#BE3D24" stroke-width="1" opacity="0.4"/>')
sv.append(f'<text x="{cx}" y="{cy-12}" class="hubsm" text-anchor="middle" dominant-baseline="central">出發 ⟳ 歸來</text>')
sv.append(f'<text x="{cx}" y="{cy+10}" class="hubbig" text-anchor="middle" dominant-baseline="central">家</text>')
sv.append('</svg>')
WHEEL="\n".join(sv)

# ================= build almanac cards =================
def cards_for(sk):
    out=[]
    for idx,row in enumerate(T):
        if row[7]!=sk: continue
        name,date,scene,yi,ji,hour,verse,_=row
        out.append(f'''        <article class="term" id="term-{idx}">
          <div class="term__head"><span class="term__name">{name}</span><span class="term__date">{date}</span></div>
          <p class="term__scene">{scene}</p>
          <div class="yiji">
            <div class="row row--yi"><span class="seal seal--yi">宜</span><span class="row__txt">{" · ".join(yi)}</span></div>
            <div class="row row--ji"><span class="seal seal--ji">忌</span><span class="row__txt">{" · ".join(ji)}</span></div>
          </div>
          <p class="term__hour"><span class="hour__k">吉時</span>{hour}</p>
          <p class="term__verse">{verse}</p>
        </article>''')
    return "\n".join(out)
ICON = {
 "spring":'<svg class="season__ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22V10"/><path d="M12 12C12 8.5 9 6 5.5 6.5 5.1 10 7.5 12.4 12 12"/><path d="M12 14c0-2.8 2.4-5 5.5-4.5.3 2.9-2 5-5.5 4.5"/></svg>',
 "summer":'<svg class="season__ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4.3"/><path d="M12 2v2.6M12 19.4V22M2 12h2.6M19.4 12H22M4.9 4.9l1.9 1.9M17.2 17.2l1.9 1.9M19.1 4.9l-1.9 1.9M6.8 17.2l-1.9 1.9"/></svg>',
 "autumn":'<svg class="season__ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 4C10 4 4 10 4 20c10 0 16-6 16-16Z"/><path d="M4 20 13.5 10.5"/></svg>',
 "winter":'<svg class="season__ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18M4.2 7.5l15.6 9M19.8 7.5 4.2 16.5"/><path d="M9.2 4.7 12 6l2.8-1.3M9.2 19.3 12 18l2.8 1.3"/></svg>',
}
SECS=[]
for sk in order:
    ch,en,col=SEASON[sk]
    SECS.append(f'''      <section class="season" style="--season:{col}">
        <header class="season__head">{ICON[sk]}<span class="season__ch">{ch}</span><span class="season__en">{en}</span><span class="season__rule"></span></header>
        <div class="grid">
{cards_for(sk)}
        </div>
      </section>''')
ALMANAC="\n".join(SECS)
# almanac term data for JS (name, yi, ji, verse, season)
TERM_JS=[{"name":r[0],"yi":r[3],"ji":r[4],"verse":r[6],"season":r[7]} for r in T]

# ================= assemble HTML =================
TEMPLATE = r'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>單車騎行農民曆 · 路線天時</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="vendor/leaflet/leaflet.css">
<script src="vendor/leaflet/leaflet.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400;1,9..144,500&family=Noto+Serif+TC:wght@400;500;600;700;900&display=swap" rel="stylesheet">
<style>
  :root{
    --paper:#F3EEE2; --card:#FBF8F0; --ink:#2A2622; --body:#3A352E;
    --line:#DAD0BC; --muted:#857A66; --gold:#B08A3E;
    --good:#6F8A4D; --warn:#C7892F; --risk:#BE3D24; --pine:#4F6157; --yi:#BE3D24;
  }
  *{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%}
  body{margin:0; background:var(--paper); color:var(--body);
    font-family:"Noto Serif TC",serif; line-height:1.7;
    background-image:radial-gradient(circle at 50% -8%, rgba(0,0,0,0.025), transparent 55%);}
  .wrap{max-width:860px; margin:0 auto; padding:clamp(26px,5vw,52px) clamp(16px,4vw,34px) 72px}

  .mast{text-align:center}
  .mast__ey{font-family:"Fraunces",serif; font-style:italic; letter-spacing:.32em; text-transform:uppercase;
    font-size:12px; color:var(--muted); margin:0 0 12px}
  .mast__title{font-weight:900; font-size:clamp(30px,6.4vw,52px); letter-spacing:.12em; margin:0; color:var(--ink); line-height:1.1}
  .mast__sub{font-family:"Fraunces",serif; font-style:italic; font-size:clamp(13px,2.5vw,16px); color:var(--muted); margin:12px 0 0}

  /* today term card */
  .today{display:flex; gap:16px; align-items:center; margin:26px 0 0; background:var(--card);
    border:1px solid var(--line); border-left:5px solid var(--tc,var(--good)); border-radius:8px; padding:16px 20px}
  .today__badge{flex:none; width:70px; height:70px; border-radius:50%; display:grid; place-items:center;
    background:color-mix(in srgb,var(--tc,var(--good)) 12%, transparent); border:2px solid var(--tc,var(--good))}
  .today__ch{font-weight:900; font-size:30px; color:var(--tc,var(--good)); letter-spacing:.06em; line-height:1}
  .today__body{flex:1; min-width:0}
  .today__k{font-size:11px; letter-spacing:.2em; color:var(--muted); margin:0}
  .today__verse{margin:3px 0 8px; font-size:16px; color:var(--ink); font-weight:600}
  .today__yiji{display:flex; flex-wrap:wrap; gap:6px 8px; font-size:13px}
  .today__yiji .t{display:inline-flex; align-items:center; gap:5px}
  .today__yiji .sd{width:20px;height:20px;border-radius:3px;display:grid;place-items:center;color:#FBF8F0;font-weight:700;font-size:12px}

  /* route input */
  .panel{margin:22px 0 0; background:var(--card); border:1px solid var(--line); border-radius:8px; padding:18px 20px}
  .panel__k{font-family:"Fraunces",serif; font-style:italic; font-size:13px; letter-spacing:.06em; color:var(--muted); margin:0 0 10px}
  .searchbar{display:flex; gap:10px; align-items:stretch}
  .searchbar input{flex:1; font-family:"Noto Serif TC",serif; font-size:16px; color:var(--ink);
    border:1px solid var(--line); background:var(--paper); border-radius:8px; padding:12px 16px; min-width:0}
  .searchbar input:focus{outline:2px solid var(--gold); outline-offset:1px}
  .btn-go{font-family:"Noto Serif TC",serif; font-weight:700; font-size:16px; letter-spacing:.1em;
    border:0; background:var(--gold); color:#FBF8F0; border-radius:8px; padding:0 22px; cursor:pointer}
  .hint{font-size:12.5px; color:var(--muted); margin:10px 0 0; letter-spacing:.02em}
  .unresolved{margin:10px 0 0; font-size:13px; color:var(--risk)}
  .chips-k{font-size:12px; color:var(--muted); letter-spacing:.14em; margin:14px 0 8px}
  .chips{display:flex; flex-wrap:wrap; gap:8px}
  .chip{font-family:"Noto Serif TC",serif; font-size:13.5px; color:var(--body); cursor:pointer;
    border:1px solid var(--line); background:var(--paper); border-radius:999px; padding:6px 14px}
  .chip:hover{border-color:var(--gold); color:var(--ink)}
  .wp-list{display:flex; flex-wrap:wrap; gap:8px; margin:0 0 12px}
  .wp-list:empty{display:none}
  .wp-chip{display:inline-flex; align-items:center; gap:8px; font-size:14.5px; color:var(--ink);
    background:color-mix(in srgb,var(--gold) 13%, var(--card)); border:1px solid color-mix(in srgb,var(--gold) 42%, transparent);
    border-radius:999px; padding:6px 8px 6px 13px}
  .wp-chip .idx{font-family:"Fraunces",serif; font-size:12px; color:var(--muted)}
  .wp-chip button{border:0; background:color-mix(in srgb,var(--ink) 8%, transparent); color:var(--body); cursor:pointer;
    width:20px; height:20px; border-radius:50%; font-size:11px; line-height:1; display:grid; place-items:center}
  .wp-chip button:hover{background:var(--risk); color:#FBF8F0}
  .combo{position:relative}
  #wpInput{width:100%; font-family:"Noto Serif TC",serif; font-size:16px; color:var(--ink);
    border:1px solid var(--line); background:var(--paper); border-radius:8px; padding:12px 16px}
  #wpInput:focus{outline:2px solid var(--gold); outline-offset:1px}
  .suggest{position:absolute; left:0; right:0; top:calc(100% + 6px); z-index:30;
    background:var(--card); border:1px solid var(--line); border-radius:10px; overflow:hidden auto;
    box-shadow:0 12px 32px rgba(42,38,34,0.16); max-height:320px}
  .sug-item{display:flex; align-items:center; gap:10px; padding:11px 15px; cursor:pointer; border-bottom:1px solid var(--line)}
  .sug-item:last-child{border-bottom:0}
  .sug-item:hover,.sug-item.active{background:color-mix(in srgb,var(--gold) 10%, transparent)}
  .sug-item .nm{font-size:15.5px; color:var(--ink); flex:1}
  .sug-item .tag{font-size:11.5px; color:var(--muted); border:1px solid var(--line); border-radius:999px; padding:1px 9px; white-space:nowrap}
  .sug-item .tag.local{color:var(--good); border-color:color-mix(in srgb,var(--good) 42%, transparent)}
  .sug-item .tag.sta{color:var(--pine); border-color:color-mix(in srgb,var(--pine) 42%, transparent)}
  .sug-note{padding:9px 15px; font-size:12.5px; color:var(--muted); text-align:center}
  .sug-spin{display:inline-block; width:12px;height:12px;border-radius:50%; vertical-align:-2px; margin-right:6px;
    border:2px solid color-mix(in srgb,var(--gold) 30%,transparent); border-top-color:var(--gold); animation:spin .8s linear infinite}
  .wp-actions{display:flex; gap:10px; margin:8px 0 0}
  .mini-btn{font-family:"Noto Serif TC",serif; font-size:13px; color:var(--body); cursor:pointer;
    border:1px solid var(--line); background:var(--paper); border-radius:6px; padding:6px 14px}
  .mini-btn:hover{border-color:var(--gold)}
  #tripText{width:100%; font-family:"Noto Serif TC",serif; font-size:15px; color:var(--ink); line-height:1.7;
    border:1px solid var(--line); background:var(--paper); border-radius:8px; padding:12px 16px; resize:vertical}
  #tripText:focus{outline:2px solid var(--gold); outline-offset:1px}
  .btn-go{font-family:"Noto Serif TC",serif; font-weight:700; font-size:15px; letter-spacing:.08em;
    border:0; background:var(--gold); color:#FBF8F0; border-radius:8px; padding:9px 20px; cursor:pointer}
  .btn-go:disabled{opacity:.6; cursor:progress}
  .ai-note{font-size:12.5px; color:var(--muted)}
  .ai-note.err{color:var(--risk)}
  .sub-div{display:flex; align-items:center; gap:12px; margin:16px 0 10px; color:var(--muted)}
  .sub-div::before,.sub-div::after{content:""; flex:1; height:1px; background:var(--line)}
  .sub-div span{font-size:12px; letter-spacing:.16em}
  .map{height:340px; margin:16px 0 0; border:1px solid var(--line); border-radius:8px; overflow:hidden}
  .route-tools{display:flex; flex-wrap:wrap; align-items:center; gap:10px; margin:10px 0 0}
  .tools-note{font-size:12px; color:var(--muted)}
  a.mini-btn{text-decoration:none; display:inline-block}
  .grade-chips{display:flex; flex-wrap:wrap; align-items:center; gap:5px; margin-top:6px}
  .gk{font-size:11px; letter-spacing:.14em; color:var(--muted); margin-right:2px}
  .gchip{font-size:11.5px; padding:2px 8px; border-radius:999px; color:#FBF8F0; letter-spacing:.02em}
  .elevcv{display:block; width:100%; height:56px; margin-top:8px; border-bottom:1px solid var(--line)}
  .steps-tg{font-size:12px; color:var(--pine); cursor:pointer; background:none; border:0; padding:0; margin-top:8px;
    text-decoration:underline; text-underline-offset:3px; font-family:"Noto Serif TC",serif}
  .steps-list{margin:8px 0 0; padding:0 0 0 4px; list-style:none; font-size:12.5px; color:var(--body); line-height:1.8}
  .steps-list li{border-left:2px solid var(--line); padding-left:10px; margin-bottom:2px}
  .seg-est{color:var(--warn); font-size:11.5px}

  .controls{display:flex; flex-wrap:wrap; gap:14px 22px; align-items:center; margin:16px 0 0; padding-top:16px; border-top:1px dashed var(--line)}
  .ctl-group{display:flex; align-items:center; gap:8px}
  .ctl-label{font-size:12px; letter-spacing:.14em; color:var(--muted)}
  .time-input,.num-input{font-family:"Fraunces",serif; font-size:16px; color:var(--ink); letter-spacing:.03em;
    border:1px solid var(--line); background:var(--paper); border-radius:5px; padding:6px 10px}
  .num-input{width:66px}
  .time-input:focus,.num-input:focus{outline:2px solid var(--gold); outline-offset:1px}
  .toggle{font-family:"Noto Serif TC",serif; font-size:13px; letter-spacing:.08em; cursor:pointer;
    border:1px solid var(--line); background:var(--paper); color:var(--body); border-radius:5px; padding:6px 14px}
  .toggle.on{background:var(--pine); color:#FBF8F0; border-color:var(--pine)}
  .note-live{text-align:center; font-size:11.5px; color:var(--muted); letter-spacing:.04em; margin:10px 0 0}

  /* verdict */
  .verdict{margin:22px 0 0; background:var(--card); border:1px solid var(--line);
    border-left:5px solid var(--vc,var(--good)); border-radius:8px; padding:20px 22px}
  .route-title{font-size:15px; color:var(--ink); font-weight:600; margin:0 0 4px}
  .route-sub{font-size:13px; color:var(--muted); margin:0 0 14px}
  .verdict__top{display:flex; align-items:center; gap:12px; flex-wrap:wrap}
  .vdot{width:14px; height:14px; border-radius:50%; background:var(--vc,var(--good)); flex:none;
    box-shadow:0 0 0 4px color-mix(in srgb, var(--vc,var(--good)) 18%, transparent)}
  .vstatus{font-weight:900; font-size:clamp(20px,4vw,26px); letter-spacing:.06em; color:var(--ink)}
  .vsent{margin:12px 0 0; font-size:15.5px; color:var(--body)}
  .empty{margin:0; font-size:15px; color:var(--muted); text-align:center; padding:6px 0; line-height:1.7}
  .route-warn{margin:0 0 12px; padding:10px 13px; font-size:13.5px; color:var(--risk); line-height:1.6;
    background:color-mix(in srgb,var(--risk) 8%, transparent); border:1px solid color-mix(in srgb,var(--risk) 35%, transparent); border-radius:5px}
  .loading{display:flex; align-items:center; justify-content:center; gap:12px; padding:12px 0}
  .spinner{width:20px; height:20px; border-radius:50%; flex:none;
    border:3px solid color-mix(in srgb,var(--gold) 28%, transparent); border-top-color:var(--gold);
    animation:spin .8s linear infinite}
  @keyframes spin{to{transform:rotate(360deg)}}
  .loading__txt{font-size:15px; color:var(--body); letter-spacing:.02em}
  .btn-go:disabled{opacity:.6; cursor:progress}
  @media (prefers-reduced-motion:reduce){ .spinner{animation-duration:2.4s} }
  .vgrid{display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:16px}
  .vcell{background:var(--paper); border:1px solid var(--line); border-radius:5px; padding:11px 13px}
  .vcell__k{font-size:11px; letter-spacing:.16em; color:var(--muted); margin:0 0 4px}
  .vcell__v{font-size:14px; color:var(--ink); font-weight:500; line-height:1.5}
  .vrec{margin:16px 0 0; padding:12px 14px; background:color-mix(in srgb, var(--gold) 9%, transparent);
    border:1px dashed var(--gold); border-radius:5px; font-size:14.5px; color:var(--body)}
  .vrec b{color:var(--gold); font-weight:600}

  /* timeline */
  .timeline{position:relative; padding-left:8px; margin-top:22px}
  .tnode{position:relative; padding:0 0 4px 46px; margin-bottom:14px}
  .tnode::before{content:""; position:absolute; left:14px; top:26px; bottom:-18px; width:2px; background:var(--line)}
  .tnode:last-child::before{display:none}
  .tdot{position:absolute; left:6px; top:6px; width:18px; height:18px; border-radius:50%;
    background:var(--card); border:3px solid var(--sc,var(--good)); z-index:2}
  .tcard{background:var(--card); border:1px solid var(--line); border-left:4px solid var(--sc,var(--good)); border-radius:5px; padding:13px 15px}
  .tcard__top{display:flex; align-items:baseline; gap:10px; justify-content:space-between}
  .teta{font-family:"Fraunces",serif; font-size:22px; color:var(--ink); font-weight:600}
  .tname{font-weight:700; font-size:18px; color:var(--ink); letter-spacing:.06em; flex:1; text-align:right}
  .tmeta{display:flex; flex-wrap:wrap; gap:6px 8px; margin-top:10px}
  .pill{font-size:12.5px; padding:3px 9px; border-radius:999px; border:1px solid var(--line);
    background:var(--paper); color:var(--body); display:inline-flex; align-items:center; gap:5px}
  .pill--rain.hi{border-color:var(--risk); color:var(--risk)}
  .pill--rain.mid{border-color:var(--warn); color:#9a6a1e}
  .pill--uv.hi{border-color:var(--risk); color:var(--risk)}
  .pill--wind.head{border-color:var(--risk); color:var(--risk)}
  .pill--wind.tail{border-color:var(--good); color:#4c6234}
  .warr{display:inline-block; width:0;height:0; border-left:4px solid transparent; border-right:4px solid transparent; border-bottom:8px solid currentColor}
  .tesc{margin-top:9px; font-size:12.5px; color:var(--muted); display:flex; align-items:center; gap:6px}
  .tesc.hard{color:var(--risk); font-weight:500}
  .tseg{position:relative; padding:2px 0 2px 46px; margin:-8px 0 6px}
  .tseg__inner{font-size:12px; color:var(--muted)}
  .tseg__inner b{color:var(--body); font-weight:500}
  .regime{position:relative; padding:10px 0 10px 46px; margin:2px 0 10px}
  .regime__b{background:color-mix(in srgb,var(--pine) 10%, transparent); border:1px dashed var(--pine);
    border-radius:5px; padding:9px 13px; font-size:13px; color:var(--pine); font-weight:500}
  .legend{display:flex; flex-wrap:wrap; gap:10px 18px; justify-content:center; margin:22px 0 0; font-size:12px; color:var(--muted)}
  .legend i{display:inline-block; width:10px;height:10px;border-radius:50%;margin-right:6px}

  /* almanac */
  .section-div{display:flex; align-items:center; gap:16px; margin:56px 0 6px; color:var(--muted)}
  .section-div::before,.section-div::after{content:""; flex:1; height:1px; background:var(--line)}
  .section-div span{font-weight:700; font-size:16px; letter-spacing:.14em; color:var(--ink)}
  .wheel-wrap{display:flex; justify-content:center; margin:24px auto 6px; max-width:480px}
  .wheel{width:100%; height:auto; display:block}
  .wlbl{font-family:"Noto Serif TC",serif; font-weight:600; font-size:15px; fill:var(--ink)}
  .wlbl.today{font-weight:900; fill:var(--risk)}
  .wmk{font-family:"Noto Serif TC",serif; font-weight:900; font-size:54px; opacity:.16}
  .hubbig{font-family:"Noto Serif TC",serif; font-weight:900; font-size:26px; fill:var(--yi)}
  .hubsm{font-family:"Noto Serif TC",serif; font-weight:500; font-size:9px; fill:var(--muted); letter-spacing:.12em}
  .wheel-cap{text-align:center; color:var(--muted); font-size:13px; letter-spacing:.12em; margin:2px 0 26px}
  .season{margin-top:34px}
  .season__head{display:flex; align-items:center; gap:12px; margin:0 0 16px; padding:12px 18px;
    background:color-mix(in srgb,var(--season) 13%, var(--card));
    border:1px solid color-mix(in srgb,var(--season) 32%, transparent); border-radius:12px}
  .season__ico{width:26px; height:26px; color:var(--season); flex:none}
  .season__ch{font-weight:900; font-size:clamp(26px,5vw,38px); color:var(--season); letter-spacing:.1em; line-height:1}
  .season__en{font-family:"Fraunces",serif; font-style:italic; font-size:clamp(14px,2.5vw,18px); color:var(--season); opacity:.9}
  .season__rule{flex:1; height:2px; background:color-mix(in srgb,var(--season) 45%, transparent); align-self:center; border-radius:2px}
  .grid{display:grid; grid-template-columns:repeat(2,1fr); gap:16px; margin-top:14px}
  .term{background:color-mix(in srgb,var(--season) 7%, var(--card));
    border:1px solid color-mix(in srgb,var(--season) 24%, var(--line)); border-top:4px solid var(--season);
    padding:16px 18px 14px; border-radius:8px; transition:transform .2s ease, box-shadow .2s ease}
  .term:hover{transform:translateY(-3px); box-shadow:0 8px 20px color-mix(in srgb,var(--season) 22%, transparent)}
  .term.today{box-shadow:0 0 0 2px var(--risk); border-top-color:var(--risk)}
  .term.today .term__name::after{content:"　今日"; font-size:11px; color:var(--risk); font-weight:600; letter-spacing:.1em}
  .term__head{display:flex; align-items:baseline; justify-content:space-between; gap:10px}
  .term__name{font-weight:900; font-size:28px; letter-spacing:.14em; color:var(--season)}
  .term.today .term__name{color:var(--risk)}
  .term__date{font-family:"Fraunces",serif; font-size:15px; color:var(--muted); white-space:nowrap}
  .term__scene{margin:8px 0 12px; font-size:14px; color:var(--body); line-height:1.6}
  .yiji{display:flex; flex-direction:column; gap:8px; border-top:1px dashed var(--line); border-bottom:1px dashed var(--line); padding:11px 0; margin:0 0 11px}
  .row{display:flex; align-items:flex-start; gap:10px}
  .row__txt{font-size:14.5px; padding-top:1px}
  .row--yi .row__txt{color:var(--ink); font-weight:500}
  .row--ji .row__txt{color:var(--muted)}
  .seal{flex:none; width:23px; height:23px; border-radius:3px; display:grid; place-items:center; font-weight:700; font-size:14px; color:#FBF8F0}
  .seal--yi{background:var(--yi)} .seal--ji{background:var(--ink)}
  .term__hour{margin:0 0 9px; font-size:13.5px; color:var(--body)}
  .hour__k{display:inline-block; font-size:11px; letter-spacing:.2em; color:var(--muted); border:1px solid var(--line); border-radius:2px; padding:1px 6px; margin-right:8px}
  .term__verse{margin:0; font-size:14.5px; color:var(--season); font-weight:500; line-height:1.6}
  .term__verse::before{content:"〔語〕"; font-size:10px; color:var(--muted); margin-right:6px; vertical-align:1px}

  .colophon{margin-top:44px; padding-top:20px; border-top:1px solid var(--line); text-align:center; color:var(--muted); font-size:12px; line-height:1.9}
  .colophon b{color:var(--body); font-weight:600}

  @media (max-width:560px){
    .vgrid{grid-template-columns:1fr}
    .grid{grid-template-columns:1fr}
    .searchbar{flex-direction:column}
    .btn-go{padding:12px 0}
  }
</style>
</head>
<body>
  <div class="wrap">
    <header class="mast">
      <p class="mast__ey">A Cyclist&#39;s Almanac · Taiwan</p>
      <h1 class="mast__title">單車騎行農民曆</h1>
      <p class="mast__sub">Enter any waypoints in order — read the line through the day, and the season</p>
    </header>

    <div class="today" id="todayCard"></div>

    <div class="panel">
      <p class="panel__k">今日騎點 · 貼上整段行程，AI 讀出沿線地點</p>
      <textarea id="tripText" rows="3" placeholder="貼上路線敘述、遊記或地點清單，例如：花蓮車站出發，經七星潭、新城老街、佳興小吃店，進太魯閣到天祥…"></textarea>
      <div class="wp-actions">
        <button class="btn-go" id="aiBtn">AI 解析路線</button>
        <span class="ai-note" id="aiNote"></span>
      </div>
      <div class="sub-div"><span>或逐一挑選</span></div>
      <div class="wp-list" id="wpList"></div>
      <div class="combo">
        <input id="wpInput" type="text" autocomplete="off" placeholder="輸入地名，如 花蓮車站、淡水、太魯閣… 再從清單點選">
        <div class="suggest" id="suggest" hidden></div>
      </div>
      <div class="wp-actions">
        <button class="mini-btn" id="clearBtn">清空路線</button>
      </div>
      <p class="hint">每個地點都從清單挑選、帶有確定座標，所以不會認錯地名或定位到錯的地方。</p>

      <div class="controls">
        <div class="ctl-group"><span class="ctl-label">出發時間</span><input type="time" id="startTime" class="time-input" value="06:30" step="300"></div>
        <div class="ctl-group"><span class="ctl-label">每點停留</span><input type="number" id="dwell" class="num-input" value="15" min="0" max="120" step="5"><span class="ctl-label">分</span></div>
        <div class="ctl-group"><button class="toggle" id="revBtn">反轉方向 ⇄</button></div>
      </div>
      <p class="note-live">天氣為<strong>示範情境</strong>（依季節與地形估算），路徑／坡度／撤退依真實路網計算（需 API 金鑰）；天氣為示範情境，CWA 逐時預報為下一步</p>
    </div>

    <div class="verdict" id="verdict"></div>
    <div id="map" class="map" hidden></div>
    <div class="route-tools" id="routeTools" hidden>
      <button class="mini-btn" id="gpxBtn">下載 GPX</button>
      <a class="mini-btn" id="gmapsBtn" target="_blank" rel="noopener">在 Google 地圖開啟導航</a>
      <span class="tools-note" id="routeMode"></span>
    </div>
    <div class="timeline" id="timeline"></div>
    <div class="legend">
      <span><i style="background:var(--good)"></i>宜</span>
      <span><i style="background:var(--warn)"></i>留意</span>
      <span><i style="background:var(--risk)"></i>審慎</span>
      <span>頂風＝逆風而行 · 順風＝風助前進 · 轉進＝就近搭車撤退</span>
    </div>

    <footer class="colophon">
      <b>基地分析工作站</b> · 單車騎行農民曆（路線天時 + 節氣）原型<br>
      路線距離＝直線距離 × 1.3 迂迴係數；爬升＝海拔差 + 每公里起伏估算；ETA 依配速 15 km/h 與每點停留推算；頂／順風由每段方位角與當時風向相減。<br>
      地名座標來自 Open-Meteo Geocoding 與 OpenStreetMap Nominatim、海拔來自 Open-Meteo；天氣為示範情境，實際以出發當日之逐時預報與現場風雨為準。
    </footer>
  </div>

<script>
const GAZ = /*__GAZ__*/;
const TERMS = /*__TERMS__*/;
const TERM_STARTS = /*__TSTARTS__*/;
const STATIONS = /*__STATIONS__*/;
const SEASON_COLOR = {spring:"#5FA046",summer:"#CE8418",autumn:"#BE5027",winter:"#34877C"};

let START = 390, DWELL = 15, REVERSED = false;
let ROUTE = [];   // resolved gazetteer entries in order

// ---------- resolve place names (curated fast-path, then live geocode) ----------
const geoCache = new Map();
const sleep = ms => new Promise(r=>setTimeout(r,ms));

function inferZone(p){
  if(p.elev>=1500) return "exposed";
  if(p.elev>=400) return "exposed";
  if(/[海港灣濱漁岬嶼]/.test(p.n) && p.elev<80) return "coast";
  if(p.elev>=50) return "valley";
  return "basin";
}
// ---------- geocode search: return multiple suggestions (Open-Meteo, CORS-friendly) ----------
async function searchGeocode(q){
  try{
    const res=await fetch("https://geocoding-api.open-meteo.com/v1/search?count=6&language=zh&format=json&name="+encodeURIComponent(q));
    if(!res.ok) return {err:true};
    const j=await res.json();
    if(!j.results) return {results:[]};
    let rs=j.results.filter(r=>r.country_code==="TW"); if(!rs.length) rs=j.results;
    return {results: rs.map(r=>({
      n:r.name, lat:r.latitude, lng:r.longitude, elev:(r.elevation??null),
      region:[r.admin1,r.admin3,r.admin2].find(Boolean)||r.country||""
    }))};
  }catch(e){ return {err:true}; }
}

// ---------- fill elevation for selected waypoints that lack it ----------
async function fillElevations(list){
  const geo=list.filter(p=>p.elev===null);
  if(!geo.length) return;
  try{
    const lats=geo.map(p=>p.lat).join(","), lngs=geo.map(p=>p.lng).join(",");
    const res=await fetch("https://api.open-meteo.com/v1/elevation?latitude="+lats+"&longitude="+lngs);
    const j=await res.json();
    if(j&&j.elevation) geo.forEach((p,i)=>{ p.elev=Math.round(j.elevation[i]??0); p.wz=inferZone(p); });
    else geo.forEach(p=>{ p.elev=p.elev||0; p.wz=inferZone(p); });
  }catch(e){ geo.forEach(p=>{ p.elev=p.elev||0; p.wz=inferZone(p); }); }
}
function showLoading(txt){
  const v=document.getElementById('verdict');
  v.style.setProperty('--vc','var(--gold)');
  v.innerHTML='<div class="loading"><span class="spinner"></span><span class="loading__txt">'+(txt||'查詢地點中…')+'</span></div>';
  document.getElementById('timeline').innerHTML="";
}

// ---------- geo ----------
const rad=d=>d*Math.PI/180, deg=r=>r*180/Math.PI;
function haversine(a,b){
  const R=6371, dLat=rad(b.lat-a.lat), dLng=rad(b.lng-a.lng);
  const s=Math.sin(dLat/2)**2 + Math.cos(rad(a.lat))*Math.cos(rad(b.lat))*Math.sin(dLng/2)**2;
  return 2*R*Math.asin(Math.sqrt(s));
}
function bearing(a,b){
  const y=Math.sin(rad(b.lng-a.lng))*Math.cos(rad(b.lat));
  const x=Math.cos(rad(a.lat))*Math.sin(rad(b.lat))-Math.sin(rad(a.lat))*Math.cos(rad(b.lat))*Math.cos(rad(b.lng-a.lng));
  return (deg(Math.atan2(y,x))+360)%360;
}
function angDiff(a,b){ let d=Math.abs(a-b)%360; return d>180?360-d:d; }
const DETOUR=1.3, ROLL=6, SPEED=15, CLIMB=0.06;

// ---------- weather (illustrative, by zone + elevation) ----------
function lerp(pts,h){
  if(h<=pts[0][0])return pts[0][1];
  if(h>=pts[pts.length-1][0])return pts[pts.length-1][1];
  for(let i=0;i<pts.length-1;i++){const[h0,v0]=pts[i],[h1,v1]=pts[i+1];if(h>=h0&&h<=h1)return v0+(v1-v0)*(h-h0)/(h1-h0);}
  return pts[pts.length-1][1];
}
function wx(wz, elev, hour){
  elev = elev || 0;
  const h=hour;
  let temp = lerp([[5,25],[8,28],[11,31],[14,33],[16,32],[18,30]],h) - elev/1000*6.5;
  let uv   = lerp([[6,0],[8,3],[10,7],[12,10],[13,11],[15,8],[17,4],[18,1]],h) + elev/1000*1.2;
  const rainMap={
    basin:[[6,8],[11,12],[14,30],[16,38],[18,25]],
    valley:[[6,8],[11,14],[14,32],[16,38],[18,25]],
    coast:[[6,12],[11,18],[14,42],[16,48],[18,35]],
    exposed:[[6,10],[11,25],[13,55],[15,70],[16,65],[18,40]],
    lake:[[6,10],[11,20],[14,50],[16,55],[18,38]]
  };
  let rain=lerp(rainMap[wz]||rainMap.basin,h);
  const sea=lerp([[9,6],[12,14],[14,22],[16,24],[18,18]],h);
  let windFrom, windSpd;
  if(wz==="coast"||wz==="exposed"){ windFrom=h<11?225:112; windSpd=h<11?9:sea; }
  else { windFrom=225; windSpd=8; }
  if(wz==="exposed" && elev>1500) windSpd=Math.max(windSpd,16);
  if(wz==="valley"){ uv-=3; temp-=1; }
  if(wz==="coast"||wz==="lake"){ temp-=1; }
  if(wz==="basin"){ uv-=1; }
  uv=Math.max(0,Math.round(uv));
  return {temp:Math.round(temp), uv, rain:Math.round(rain), windFrom, windSpd:Math.round(windSpd)};
}
function cond(r){ return r>=60?"雷陣雨":r>=45?"陣雨機率高":r>=28?"多雲時陰":"多雲到晴"; }

// ---------- today's solar term ----------
function todayTerm(){
  const now=new Date(), ord=(now.getMonth()+1)*100+now.getDate();
  let best=-1, bestOrd=-1;
  for(let i=0;i<TERM_STARTS.length;i++){
    const o=TERM_STARTS[i][0]*100+TERM_STARTS[i][1];
    if(o<=ord && o>bestOrd){ best=i; bestOrd=o; }
  }
  return best<0 ? 21 : best;   // Jan 1–4 wraps back to 冬至 (started prev Dec 22)
}

// ---------- build itinerary ----------
function build(){
  const pts = REVERSED ? [...ROUTE].reverse() : ROUTE.slice();
  const rows=[]; let t=START;
  for(let i=0;i<pts.length;i++){
    let seg=null;
    if(i>0){
      seg = SEGDATA[i-1] || estSegment(pts[i-1],pts[i]);
      t += seg.dist/SPEED*60 + seg.up*CLIMB;
    }
    const arrMin=t, hour=arrMin/60;
    const w=wx(pts[i].wz, pts[i].elev, hour);
    let wind=null;
    if(i>0){
      const br=bearing(pts[i-1],pts[i]);
      const rel=angDiff(w.windFrom,br);
      const kind=rel<=60?"head":rel>=120?"tail":"cross";
      const windTo=(w.windFrom+180)%360; const rot=(windTo-br+360)%360;
      wind={kind,spd:w.windSpd,rot,label:kind==="head"?"頂風":kind==="tail"?"順風":"側風"};
    }
    let score=0;
    if(w.rain>=60)score+=3; else if(w.rain>=45)score+=2; else if(w.rain>=28)score+=1;
    if(w.uv>=10)score+=2; else if(w.uv>=8)score+=1;
    if(w.temp>=33)score+=1;
    if(w.temp<=8)score+=1;                       // cold exposure (alpine mornings)
    if(wind&&wind.kind==="head"&&wind.spd>=18)score+=1;
    if(pts[i].esc.hard)score+=1;
    const tier=score>=4?"risk":score>=2?"warn":"good";
    rows.push({pt:pts[i],seg,arrMin,w,wind,tier,score});
    if(i<pts.length-1) t+=DWELL;
  }
  return rows;
}

// ---------- render ----------
const fmt=m=>{m=Math.round(m);let h=Math.floor(m/60)%24,mm=((m%60)+60)%60;return String(h).padStart(2,'0')+":"+String(mm).padStart(2,'0');};
const fmtD=m=>{const d=Math.floor(Math.round(m)/1440); return fmt(m)+(d>=1?` <span style="color:var(--risk)">(+${d}日)</span>`:"");};
const COLOR={good:"var(--good)",warn:"var(--warn)",risk:"var(--risk)"};

function renderToday(){
  const ti=todayTerm(), tt=TERMS[ti], col=SEASON_COLOR[tt.season];
  const c=document.getElementById('todayCard');
  c.style.setProperty('--tc',col);
  c.innerHTML=`
    <div class="today__badge"><span class="today__ch">${tt.name}</span></div>
    <div class="today__body">
      <p class="today__k">今日節氣</p>
      <p class="today__verse">${tt.verse}</p>
      <div class="today__yiji">
        <span class="t"><span class="sd" style="background:var(--yi)">宜</span>${tt.yi.join(" · ")}</span>
        <span class="t"><span class="sd" style="background:var(--ink)">忌</span>${tt.ji.join(" · ")}</span>
      </div>
    </div>`;
  return tt;
}

function renderRoute(){
  const v=document.getElementById('verdict'), tl=document.getElementById('timeline');
  if(ROUTE.length<2){
    v.style.setProperty('--vc','var(--line)');
    v.innerHTML=`<p class="empty">打字搜尋地點、從清單挑選加入（或點熱門騎點）；加到兩個以上，就會分析今天這條路線的天時。</p>`;
    tl.innerHTML=""; return;
  }
  const rows=build();
  const tt=TERMS[todayTerm()];

  let worst=rows[0]; rows.forEach(r=>{if(r.score>worst.score)worst=r;});
  const heads=rows.filter(r=>r.wind&&r.wind.kind==="head");
  const tier=worst.tier;
  const statusText={good:"今日宜騎",warn:"可騎 · 留意時段",risk:"審慎 · 有高風險段"}[tier];

  const nameList=(REVERSED?[...ROUTE].reverse():ROUTE).map(p=>p.n);
  const totalKm=rows.reduce((s,r)=>s+(r.seg?r.seg.dist:0),0);
  const totalUp=rows.reduce((s,r)=>s+(r.seg?r.seg.up:0),0);
  const hasGeo=ROUTE.some(p=>p.src==="geo");
  const straight=rows.reduce((s,r,i)=>s+(i>0?haversine(rows[i-1].pt,rows[i].pt):0),0);
  const implausible = hasGeo && ROUTE.length>1 && straight/(ROUTE.length-1) > 40;

  let sent=`${worst.pt.n}於 <b>${fmtD(worst.arrMin)}</b> 抵達，正逢${cond(worst.w.rain)}（降雨 ${worst.w.rain}%）、UV ${worst.w.uv}、氣溫 ${worst.w.temp}°`
         +(worst.wind?`、${worst.wind.label} ${worst.wind.spd} km/h`:"")+`，為全程風險最高的一段。`;
  const headTxt=heads.length?heads.map(r=>r.pt.n).join("、")+" 頂風":"全程無明顯逆風";
  let rec;
  if(worst.tier==="risk"){
    rec=`風險集中在 <b>${fmtD(worst.arrMin)} 的${worst.pt.n}</b>。可試著 <b>提早出發</b>、<b>縮短每點停留</b>，或 <b>反轉方向</b>，把高風險點的抵達時刻挪開午後對流。`;
  } else {
    rec=`目前排程的節奏尚可；若要更保險，把暴露路段的抵達時刻壓在午前最穩妥。今日${tt.name}，${tt.verse}`;
  }

  v.style.setProperty('--vc', implausible?'var(--risk)':COLOR[tier]);
  v.innerHTML=`
    ${implausible?'<p class="route-warn">⚠ 路線總距離偏大（約 '+totalKm.toFixed(0)+' km），可能有地名被定位到錯誤位置。請在可疑地名後加上縣市或鄰近大地標，再查一次。</p>':''}
    <p class="route-title">${nameList.join(" → ")}</p>
    <p class="route-sub">${ROUTE.length} 點 · 約 ${totalKm.toFixed(0)} km · 估計爬升 ~${Math.round(totalUp/10)*10} m · 今日${tt.name}</p>
    <div class="verdict__top"><span class="vdot"></span><span class="vstatus">${statusText}</span></div>
    <p class="vsent">${sent}</p>
    <div class="vgrid">
      <div class="vcell"><p class="vcell__k">最糟時段 / 地點</p><p class="vcell__v">${fmtD(worst.arrMin)} · ${worst.pt.n}</p></div>
      <div class="vcell"><p class="vcell__k">風向</p><p class="vcell__v">${headTxt}</p></div>
      <div class="vcell"><p class="vcell__k">抵達終點</p><p class="vcell__v">${fmtD(rows[rows.length-1].arrMin)} · ${rows[rows.length-1].pt.n}</p></div>
    </div>
    <p class="vrec">${rec}</p>`;

  // timeline
  tl.innerHTML="";
  rows.forEach((r,i)=>{
    if(r.seg){
      const S=r.seg;
      const seg=document.createElement('div'); seg.className="tseg";
      let head=`<b>${S.dist.toFixed(1)} km</b> · ↑${Math.round(S.up)}m ↓${Math.round(S.down)}m`
        + (r.wind?` · ${r.wind.label} ${r.wind.spd}`:"")
        + (S.est?` · <span class="seg-est">直線推估</span>`:"");
      let gradeHtml="";
      if(S.bands){
        head += ` · 均坡 ${S.avgG}% · 最陡 ${S.maxG}%`;
        const B=S.bands, lbl={flat:"平路",gentle:"緩坡",steep:"陡坡",vsteep:"很陡",extreme:"極陡"},
              col={flat:"#5FA046",gentle:"#B08A3E",steep:"#CE8418",vsteep:"#BE5027",extreme:"#8C2318"};
        const km=m=> m>=950 ? (m/1000).toFixed(1)+" km" : Math.round(m/50)*50+" m";
        gradeHtml='<div class="grade-chips"><span class="gk">坡度組成</span>'+Object.keys(B).filter(k=>B[k]>=100)
          .map(k=>`<span class="gchip" style="background:${col[k]}">${lbl[k]} ${km(B[k])}</span>`).join("")+'</div>';
      }
      const cvId="cv"+i;
      const stepsHtml = S.steps && S.steps.length
        ? `<button class="steps-tg" data-tg="st${i}">逐步指示（${S.steps.length}）</button>
           <ul class="steps-list" id="st${i}" hidden>${S.steps.map(s=>`<li>${s.instruction}${s.distance?` <span style="color:var(--muted)">· ${s.distance>=1000?(s.distance/1000).toFixed(1)+" km":s.distance+" m"}</span>`:""}</li>`).join("")}</ul>`
        : "";
      seg.innerHTML=`<div class="tseg__inner">${head}${gradeHtml}`
        + (S.grades?`<canvas class="elevcv" id="${cvId}"></canvas>`:"")
        + stepsHtml + `</div>`;
      tl.appendChild(seg);
      if(S.grades) drawElev(cvId, S.grades);
      const tg=seg.querySelector('.steps-tg');
      if(tg) tg.addEventListener('click',()=>{ const el=document.getElementById(tg.dataset.tg); el.hidden=!el.hidden; });
    }
    const prevWz=i>0?rows[i-1].pt.wz:null, wz=r.pt.wz;
    const sheltered=["basin","valley","lake"], exposedZ=["coast","exposed"];
    if(i>0 && sheltered.includes(prevWz) && exposedZ.includes(wz)){
      const rg=document.createElement('div'); rg.className="regime";
      rg.innerHTML=`<div class="regime__b">⚑ 遮蔽 → 暴露：離開遮蔽地形，進入開闊／濱海／高地，風雨自此見真章</div>`;
      tl.appendChild(rg);
    }
    const w=r.w, wind=r.wind;
    const rainCls=w.rain>=60?"hi":w.rain>=28?"mid":"";
    const uvCls=w.uv>=10?"hi":"";
    const escSvg=`<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 15h16M6 15V7a2 2 0 012-2h8a2 2 0 012 2v8M8 19v2M16 19v2M9 11h6"/></svg>`;
    const windPill=wind?`<span class="pill pill--wind ${wind.kind}"><span class="warr" style="transform:rotate(${wind.rot}deg)"></span>${wind.label} ${wind.spd} km/h</span>`:"";
    const node=document.createElement('div'); node.className="tnode"; node.style.setProperty('--sc',COLOR[r.tier]);
    const rt = r.pt.retreat;
    const escTxt = rt
      ? `轉進機會：${rt.st}（${rt.road?"路網":"估"} ${rt.km} km）${rt.hard?" · 距離偏遠":""}`
      : `轉進機會：${r.pt.esc.st}${r.pt.esc.km>0&&!r.pt.esc.hard?`（${r.pt.esc.km} km）`:""}`;
    const escHard = rt ? rt.hard : r.pt.esc.hard;
    node.innerHTML=`
      <span class="tdot"></span>
      <div class="tcard">
        <div class="tcard__top"><span class="teta">${fmtD(r.arrMin)}</span><span class="tname">${r.pt.n}</span></div>
        <div class="tmeta">
          <span class="pill">${cond(w.rain)} · ${w.temp}°</span>
          <span class="pill pill--rain ${rainCls}">☂ ${w.rain}%</span>
          <span class="pill pill--uv ${uvCls}">UV ${w.uv}</span>
          ${windPill}
        </div>
        <div class="tesc ${escHard?'hard':''}">${escSvg}<span>${escTxt}</span></div>
      </div>`;
    tl.appendChild(node);
  });
}

// ================= waypoint builder (autocomplete + chips) =================
let ANALYZE_SEQ=0;
async function analyze(){
  const seq=++ANALYZE_SEQ;
  if(WAYPOINTS.length<2){ ROUTE=[]; SEGDATA=[]; renderRoute(); return; }
  if(WAYPOINTS.some(w=>w.elev===null)){ showLoading("整理海拔中…"); await fillElevations(WAYPOINTS); }
  if(seq!==ANALYZE_SEQ) return;
  ROUTE=WAYPOINTS.slice();
  await routeAll();            if(seq!==ANALYZE_SEQ) return;
  showLoading("計算各點撤退車站中…");
  await computeRetreats();     if(seq!==ANALYZE_SEQ) return;
  renderRoute();
  renderMap();
  const tools=document.getElementById('routeTools');
  tools.hidden = ROUTE.length<2;
  document.getElementById('gmapsBtn').href=gmapsUrl();
}

// ================= real routing engine (ORS via /api/route), gradients, retreat, AI, map, GPX =================
const API = p => p; // same-origin friendly paths (/api/...)
let SEGDATA = [];        // per consecutive pair: {dist(km), up, down, geom, grades, steps, est, maxG, avgG, bands}
let ROUTING = false;
let TDX_LOADED = false;

async function loadTdxStations(){
  if(TDX_LOADED) return; TDX_LOADED = true;
  try{
    const r = await fetch(API('/api/stations'));
    if(!r.ok) return;
    const j = await r.json();
    if(j.stations && j.stations.length > 20){
      const have = new Set(STATIONS.map(s=>s[0]));
      j.stations.forEach(s=>{ if(!have.has(s[0])) STATIONS.push(s); });
    }
  }catch(e){}
}

function estSegment(a,b){
  const dist = haversine(a,b)*DETOUR;
  const dE = (b.elev||0)-(a.elev||0);
  return { dist, up: Math.max(0,dE)+ROLL*dist, down: Math.max(0,-dE)+ROLL*dist,
           geom:[[a.lng,a.lat,(a.elev||0)],[b.lng,b.lat,(b.elev||0)]], grades:null, steps:[], est:true,
           maxG:null, avgG:null, bands:null };
}

function gradesFromGeom(geom){
  // geom: [[lng,lat,ele],...] → rolling ~100m gradient samples: [{d0,d1,g}]
  if(!geom || geom.length<3) return null;
  const pts=[]; let cum=0;
  for(let i=0;i<geom.length;i++){
    if(i>0) cum += haversine({lat:geom[i-1][1],lng:geom[i-1][0]},{lat:geom[i][1],lng:geom[i][0]})*1000;
    pts.push({d:cum, e:geom[i][2]||0});
  }
  const total=cum; if(total<50) return null;
  const eleAt=(d)=>{                       // linear interpolation along the profile
    if(d<=0) return pts[0].e;
    if(d>=total) return pts[pts.length-1].e;
    let lo=0, hi=pts.length-1;
    while(hi-lo>1){ const m=(lo+hi)>>1; (pts[m].d<=d)?lo=m:hi=m; }
    const a=pts[lo], b=pts[hi], f=(d-a.d)/Math.max(1e-6,b.d-a.d);
    return a.e+(b.e-a.e)*f;
  };
  const win=Math.max(80, Math.min(150, total/40));
  const out=[];
  for(let d0=0; d0<total; d0+=win){
    const d1=Math.min(total,d0+win);
    const run=Math.max(1,d1-d0);
    out.push({d0,d1,g:(eleAt(d1)-eleAt(d0))/run*100});
  }
  return {samples:out, total, profile:pts};
}

function summarizeGrades(gr){
  if(!gr) return {maxG:null,avgG:null,bands:null};
  const s=gr.samples;
  const climbs=s.filter(x=>x.g>0.5);
  const avgG = climbs.length ? climbs.reduce((a,x)=>a+x.g*(x.d1-x.d0),0)/climbs.reduce((a,x)=>a+(x.d1-x.d0),0) : 0;
  const sorted=[...s].sort((a,b)=>b.g-a.g);
  const maxG = sorted.length? sorted[Math.min(1,sorted.length-1)].g : 0; // 2nd highest ≈ robust max
  const bands={flat:0,gentle:0,steep:0,vsteep:0,extreme:0};
  s.forEach(x=>{ const L=x.d1-x.d0, g=Math.abs(x.g);
    if(g<=2)bands.flat+=L; else if(g<=5)bands.gentle+=L; else if(g<=8)bands.steep+=L;
    else if(g<=12)bands.vsteep+=L; else bands.extreme+=L; });
  return {maxG:Math.round(maxG*10)/10, avgG:Math.round(avgG*10)/10, bands}; // bands 為公尺
}

async function routeSegment(a,b){
  try{
    const r=await fetch(API('/api/route'),{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({coordinates:[[a.lng,a.lat],[b.lng,b.lat]]})});
    if(!r.ok) return null;
    const j=await r.json();
    if(!j.geometry) return null;
    const gr=gradesFromGeom(j.geometry);
    const sum=summarizeGrades(gr);
    return { dist:(j.distance||0)/1000, up:j.ascent||0, down:j.descent||0,
             geom:j.geometry, grades:gr, steps:j.steps||[], est:false, ...sum };
  }catch(e){ return null; }
}

async function routeAll(){
  SEGDATA=[]; let anyReal=false, anyEst=false;
  const pts = REVERSED ? [...ROUTE].reverse() : ROUTE.slice();
  for(let i=1;i<pts.length;i++){
    showLoading(`規劃路徑 ${i} / ${pts.length-1}：${pts[i-1].n} → ${pts[i].n}`);
    const seg = await routeSegment(pts[i-1],pts[i]) || estSegment(pts[i-1],pts[i]);
    seg.est ? anyEst=true : anyReal=true;
    SEGDATA.push(seg);
  }
  const modeEl=document.getElementById('routeMode');
  if(modeEl) modeEl.textContent = anyReal
    ? (anyEst? "部分路段為直線推估（路網服務未回應）" : "路徑、距離與坡度皆依真實路網計算")
    : "目前為直線推估模式 — 部署 ORS_API_KEY 後即為真實路網";
}

// ---------- retreat points via road-distance matrix ----------
async function computeRetreats(){
  const pts = REVERSED ? [...ROUTE].reverse() : ROUTE.slice();
  // candidates: 3 nearest stations (straight-line) per waypoint, deduped
  const cand=[]; const key=s=>s[0]+"@"+s[1].toFixed(3);
  const candKeys=new Set();
  const perWp = pts.map(p=>{
    const near=[...STATIONS].map(s=>({s, d:haversine(p,{lat:s[1],lng:s[2]})}))
      .sort((a,b)=>a.d-b.d).slice(0,3);
    near.forEach(x=>{ const k=key(x.s); if(!candKeys.has(k)){candKeys.add(k); cand.push(x.s);} });
    return near;
  });
  const capped = cand.slice(0, Math.max(1, 40 - pts.length));
  let dm=null;
  try{
    const r=await fetch(API('/api/matrix'),{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({sources:pts.map(p=>[p.lng,p.lat]), destinations:capped.map(s=>[s[2],s[1]])})});
    if(r.ok){ const j=await r.json(); if(j.distances) dm=j.distances; }
  }catch(e){}
  pts.forEach((p,i)=>{
    let best=null;
    if(dm && dm[i]){
      capped.forEach((s,k)=>{ const d=dm[i][k];
        if(d!=null && (best==null || d<best.d)) best={s, d, road:true}; });
    }
    if(!best){
      const n=perWp[i][0]; if(n) best={s:n.s, d:n.d*1000*DETOUR, road:false};
    }
    if(best){
      const km=best.d/1000;
      p.retreat={ st:`${best.s[3]} ${best.s[0]}站`, km:Math.round(km*10)/10,
                  road:best.road, hard:km>8 };
    }
  });
}

// ---------- AI extraction flow ----------
async function aiParse(){
  const ta=document.getElementById('tripText'), btn=document.getElementById('aiBtn'), note=document.getElementById('aiNote');
  const text=ta.value.trim(); if(!text) return;
  btn.disabled=true; btn.textContent="AI 解析中…"; note.className="ai-note"; note.textContent="";
  showLoading("AI 讀取路線中…");
  const fail=(msg)=>{ note.className="ai-note err"; note.textContent=msg;
    btn.disabled=false; btn.textContent="AI 解析路線"; ROUTE=[]; renderRoute(); };
  let resp;
  try{ resp=await fetch(API('/api/extract'),{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})}); }
  catch(e){ return fail("無法連線 AI 解析服務 — 請確認已部署 Netlify Functions"); }
  if(resp.status===404) return fail("AI 解析服務未部署 — 請依 README 部署 Functions 並設定 ANTHROPIC_API_KEY");
  const j=await resp.json().catch(()=>null);
  if(!j || j.error || !Array.isArray(j.waypoints)) return fail(j&&j.error ? j.error : "AI 回應格式異常");
  if(!j.waypoints.length) return fail("AI 沒有從文字中讀出地點，換段文字試試");

  const located=[], missed=[]; let last=null;
  for(let i=0;i<j.waypoints.length;i++){
    const wpt=j.waypoints[i];
    showLoading(`定位 ${i+1} / ${j.waypoints.length}：${wpt.name}`);
    let w=null;
    const loc=localMatches(wpt.name);
    if(loc.length){
      const top=loc[0], eq=normName(top.n)===normName(wpt.name)||top.n.includes(wpt.name)||wpt.name.includes(normName(top.n));
      if(eq) w = top.kind==='gaz'?wpFromGaz(top.g) : top.kind==='sta'?wpFromStation(top.s) : null;
    }
    if(!w){
      try{
        const q=new URLSearchParams({q:wpt.name}); if(wpt.region)q.set('region',wpt.region);
        if(last)q.set('near',last.lat+','+last.lng);
        const r=await fetch(API('/api/geocode?')+q.toString());
        if(r.ok){ const g=await r.json();
          if(g.results&&g.results[0]) w=wpFromGeo({n:wpt.name,lat:g.results[0].lat,lng:g.results[0].lng,elev:null}); }
      }catch(e){}
    }
    if(w){ located.push(w); last=w; } else missed.push(wpt.name);
  }
  WAYPOINTS=located; renderWaypoints();
  note.textContent = missed.length ? "認得但定不了位、已略過："+missed.join("、") : `已讀出 ${located.length} 個地點`;
  btn.disabled=false; btn.textContent="AI 解析路線";
  analyze();
}

// ---------- map ----------
let MAP=null, MAPLAYER=null;
function gradeColor(g){ const a=Math.abs(g);
  return a<=2?"#5FA046" : a<=5?"#B08A3E" : a<=8?"#CE8418" : a<=12?"#BE5027" : "#8C2318"; }
function drawElev(id, gr){
  const cv=document.getElementById(id); if(!cv) return;
  const W=cv.clientWidth||600, H=56; cv.width=W*2; cv.height=H*2;
  const ctx=cv.getContext('2d'); ctx.scale(2,2);
  const P=gr.profile, T=gr.total;
  let mn=Infinity,mx=-Infinity; P.forEach(p=>{mn=Math.min(mn,p.e);mx=Math.max(mx,p.e);});
  const pad=6, span=Math.max(20,mx-mn);
  const X=d=>pad+(W-2*pad)*d/T, Y=e=>H-4-(H-14)*(e-mn)/span;
  ctx.beginPath(); ctx.moveTo(X(0),H);
  P.forEach(p=>ctx.lineTo(X(p.d),Y(p.e))); ctx.lineTo(X(T),H); ctx.closePath();
  ctx.fillStyle="rgba(176,138,62,0.18)"; ctx.fill();
  ctx.beginPath(); P.forEach((p,i)=>i?ctx.lineTo(X(p.d),Y(p.e)):ctx.moveTo(X(p.d),Y(p.e)));
  ctx.strokeStyle="#B08A3E"; ctx.lineWidth=1.6; ctx.stroke();
  ctx.fillStyle="#857A66"; ctx.font="10px Fraunces, serif";
  ctx.fillText(Math.round(mx)+"m",4,10); ctx.fillText(Math.round(mn)+"m",4,H-6);
}
function renderMap(){
  const el=document.getElementById('map');
  if(!window.L){ el.hidden=true; return; }
  if(ROUTE.length<2 || !SEGDATA.length){ el.hidden=true; return; }
  el.hidden=false;
  if(!MAP){
    MAP=L.map('map',{scrollWheelZoom:false});
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',
      {attribution:'© OpenStreetMap', maxZoom:18}).addTo(MAP);
  }
  if(MAPLAYER) MAPLAYER.remove();
  MAPLAYER=L.layerGroup().addTo(MAP);
  const pts = REVERSED ? [...ROUTE].reverse() : ROUTE.slice();
  const all=[];
  SEGDATA.forEach(seg=>{
    const g=seg.geom; if(!g) return;
    if(seg.grades){
      // draw grade-coloured sub-polylines
      const P=seg.grades.profile;
      let cum=0, idx=0;
      seg.grades.samples.forEach(sm=>{
        const line=[];
        while(idx<g.length && cum<=sm.d1){
          line.push([g[idx][1],g[idx][0]]); all.push([g[idx][1],g[idx][0]]);
          idx++; if(idx<g.length) cum=P[idx].d;
        }
        if(idx<g.length) line.push([g[idx][1],g[idx][0]]);
        if(line.length>1) L.polyline(line,{color:gradeColor(sm.g),weight:4,opacity:.9}).addTo(MAPLAYER);
      });
    }else{
      const line=g.map(c=>[c[1],c[0]]); line.forEach(x=>all.push(x));
      L.polyline(line,{color:"#857A66",weight:3,dashArray:"6 6",opacity:.8}).addTo(MAPLAYER);
    }
  });
  pts.forEach((p,i)=>{
    L.circleMarker([p.lat,p.lng],{radius:7,color:"#FBF8F0",weight:2,fillColor:"#BE3D24",fillOpacity:1})
      .bindTooltip(`${i+1} ${p.n}`,{permanent:false}).addTo(MAPLAYER);
    all.push([p.lat,p.lng]);
  });
  if(all.length) MAP.fitBounds(all,{padding:[24,24]});
}

// ---------- GPX & Google Maps handoff ----------
function buildGpx(){
  const pts = REVERSED ? [...ROUTE].reverse() : ROUTE.slice();
  let wpts=pts.map(p=>`  <wpt lat="${p.lat}" lon="${p.lng}"><name>${xml(p.n)}</name></wpt>`).join("\n");
  let trk="";
  SEGDATA.forEach(seg=>{ (seg.geom||[]).forEach(c=>{
    trk+=`      <trkpt lat="${c[1]}" lon="${c[0]}">${c[2]!=null?`<ele>${Math.round(c[2])}</ele>`:""}</trkpt>\n`; });});
  return `<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="單車騎行農民曆" xmlns="http://www.topografix.com/GPX/1/1">
${wpts}
  <trk><name>${xml(pts[0]?.n||"")} → ${xml(pts[pts.length-1]?.n||"")}</name><trkseg>
${trk}    </trkseg></trk>
</gpx>`;
}
function xml(s){ return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }
function downloadGpx(){
  if(!SEGDATA.length) return;
  const blob=new Blob([buildGpx()],{type:"application/gpx+xml"});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob);
  a.download="騎行路線.gpx"; document.body.appendChild(a); a.click();
  setTimeout(()=>{URL.revokeObjectURL(a.href); a.remove();},500);
}
function gmapsUrl(){
  const pts = REVERSED ? [...ROUTE].reverse() : ROUTE.slice();
  if(pts.length<2) return "#";
  const o=pts[0], d=pts[pts.length-1];
  const mids=pts.slice(1,-1).slice(0,9).map(p=>p.lat+","+p.lng).join("|");
  return `https://www.google.com/maps/dir/?api=1&origin=${o.lat},${o.lng}&destination=${d.lat},${d.lng}`
       + (mids?`&waypoints=${encodeURIComponent(mids)}`:"") + `&travelmode=bicycling`;
}
let WAYPOINTS=[];
const wpInput=document.getElementById('wpInput');
const suggestEl=document.getElementById('suggest');
const wpListEl=document.getElementById('wpList');

function wpFromGaz(g){ return {n:g.n,lat:g.lat,lng:g.lng,elev:g.elev,wz:g.wz,esc:g.esc,src:"local"}; }
function wpFromStation(s){ return {n:s[0]+"站",lat:s[1],lng:s[2],elev:null,wz:"basin",
  esc:{st:s[3]+" "+s[0]+"站（即在此）",km:0,hard:false},src:"sta"}; }
function wpFromGeo(x){ const w={n:x.n,lat:x.lat,lng:x.lng,elev:(x.elev??null),wz:"basin",
  esc:{st:"—（附近車站待接 TDX）",km:0,hard:false},src:"geo"}; if(w.elev!==null) w.wz=inferZone(w); return w; }

function addWaypoint(w){
  WAYPOINTS.push(w);
  wpInput.value=""; hideSuggest(); renderWaypoints(); analyze();
  wpInput.focus();
}
function removeWaypoint(i){ WAYPOINTS.splice(i,1); renderWaypoints(); analyze(); }

function renderWaypoints(){
  wpListEl.innerHTML="";
  WAYPOINTS.forEach((w,i)=>{
    const c=document.createElement('span'); c.className="wp-chip";
    c.innerHTML=`<span class="idx">${i+1}</span>${w.n}<button aria-label="移除">✕</button>`;
    c.querySelector('button').addEventListener('click',()=>removeWaypoint(i));
    wpListEl.appendChild(c);
  });
}

// ----- suggestions -----
let sugSeq=0, sugTimer=null, activeItems=[];
function hideSuggest(){ suggestEl.hidden=true; suggestEl.innerHTML=""; activeItems=[]; }
function normName(s){ return s.replace(/(火車站|捷運站|車站|站)$/,'').trim(); }
function localMatches(q){
  const nq=normName(q);
  const out=[];
  const match=(nm)=>{
    if(nm.includes(q)||q.includes(nm)) return true;
    const nn=normName(nm);
    return nq.length>0 && (nn.includes(nq) || nq.includes(nn));
  };
  GAZ.forEach(g=>{ if([g.n,...g.a].some(match)) out.push({kind:"gaz",n:g.n,tag:"騎點",g}); });
  STATIONS.forEach(s=>{ if(match(s[0])) out.push({kind:"sta",n:s[0]+"站",tag:s[3],s}); });
  const seen=new Set();
  let list=out.filter(o=>{ if(seen.has(o.n))return false; seen.add(o.n); return true; });
  list.sort((a,b)=>{
    const na=normName(a.n), nb=normName(b.n);
    const sa=na===nq?0:na.startsWith(nq)?1:2, sb=nb===nq?0:nb.startsWith(nq)?1:2;
    return sa-sb || na.length-nb.length;
  });
  return list.slice(0,7);
}
function drawSuggest(items, loading, err){
  activeItems=items;
  let html="";
  items.forEach((it,idx)=>{
    const tagCls = it.kind==="gaz"?"local": it.kind==="sta"?"sta":"";
    html+=`<div class="sug-item${idx===0?' active':''}" data-i="${idx}"><span class="nm">${it.n}</span><span class="tag ${tagCls}">${it.tag||it.region||"地名"}</span></div>`;
  });
  if(loading) html+=`<div class="sug-note"><span class="sug-spin"></span>查詢更多地點…</div>`;
  else if(err) html+=`<div class="sug-note">外部地名查詢無回應，僅顯示內建騎點與車站</div>`;
  else if(!items.length) html+=`<div class="sug-note">找不到相符地點，換個關鍵字試試</div>`;
  suggestEl.innerHTML=html; suggestEl.hidden=false;
  suggestEl.querySelectorAll('.sug-item').forEach(el=>{
    el.addEventListener('click',()=>pick(+el.dataset.i));
  });
}
function pick(i){
  const it=activeItems[i]; if(!it) return;
  if(it.kind==="gaz") addWaypoint(wpFromGaz(it.g));
  else if(it.kind==="sta") addWaypoint(wpFromStation(it.s));
  else addWaypoint(wpFromGeo(it));
}
function onInput(){
  const q=wpInput.value.trim();
  clearTimeout(sugTimer);
  if(!q){ hideSuggest(); return; }
  const local=localMatches(q);
  drawSuggest(local, q.length>=2, false);
  if(q.length>=2){
    const myseq=++sugSeq;
    sugTimer=setTimeout(async()=>{
      const r=await searchGeocode(q);
      if(myseq!==sugSeq) return;
      let geo=(r.results||[]).map(x=>({kind:"geo",n:x.n,region:x.region,lat:x.lat,lng:x.lng,elev:x.elev}));
      geo=geo.filter(gi=> !local.some(l=> l.n===gi.n || l.n===gi.n+"站"));
      drawSuggest(local.concat(geo).slice(0,8), false, r.err);
    }, 300);
  }
}
wpInput.addEventListener('input', onInput);
wpInput.addEventListener('keydown', e=>{
  if(e.key==='Enter'){ e.preventDefault(); if(activeItems.length) pick(0); }
  else if(e.key==='Escape'){ hideSuggest(); }
});
document.addEventListener('click', e=>{ if(!e.target.closest('.combo')) hideSuggest(); });

// ----- controls -----
document.getElementById('clearBtn').addEventListener('click',()=>{ WAYPOINTS=[]; renderWaypoints(); ROUTE=[]; renderRoute(); });
document.getElementById('startTime').addEventListener('input',e=>{
  const v=e.target.value; if(!/^\d{1,2}:\d{2}$/.test(v))return;
  const [h,m]=v.split(':').map(Number); START=h*60+m; renderRoute();
});
document.getElementById('dwell').addEventListener('input',e=>{
  const n=parseInt(e.target.value,10); if(!isNaN(n)){DWELL=Math.max(0,n); renderRoute();}
});
document.getElementById('revBtn').addEventListener('click',e=>{
  REVERSED=!REVERSED; e.currentTarget.classList.toggle('on',REVERSED);
  e.currentTarget.textContent=REVERSED?"已反轉方向 ⇄":"反轉方向 ⇄";
  renderRoute();
});

document.getElementById('aiBtn').addEventListener('click', aiParse);
document.getElementById('gpxBtn').addEventListener('click', downloadGpx);
loadTdxStations();
renderWaypoints();
renderToday();
analyze();
</script>
</body>
</html>'''

html = (TEMPLATE
  .replace("/*__GAZ__*/", json.dumps(GAZ, ensure_ascii=False))
  .replace("/*__TERMS__*/", json.dumps(TERM_JS, ensure_ascii=False))
  .replace("/*__TSTARTS__*/", json.dumps(TERM_STARTS))
  .replace("/*__STATIONS__*/", json.dumps(STATIONS, ensure_ascii=False)))

import os
os.makedirs("public",exist_ok=True)
with open("public/index.html","w",encoding="utf-8") as f:
    f.write(html)
print("written", len(html), "bytes")

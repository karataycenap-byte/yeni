<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Noir Dedektif — Olgun Tema Metin Macerası (18+)</title>
<style>
  :root{--bg:#0f0f12;--card:#111216;--accent:#c68b5a;--muted:#999;}
  html,body{height:100%;margin:0;font-family:Inter,ui-sans-serif,system-ui,Segoe UI,Roboto,"Helvetica Neue",Arial;}
  body{background:
    radial-gradient(1200px 600px at 10% 10%, rgba(198,139,90,0.06), transparent 10%),
    radial-gradient(900px 400px at 90% 90%, rgba(0,0,0,0.25), transparent 10%),
    var(--bg);
    color:#e8e6e3; display:flex; align-items:center; justify-content:center; padding:24px;}
  .container{width:980px; max-width:100%; background:linear-gradient(180deg,rgba(255,255,255,0.02),transparent); border-radius:12px; box-shadow:0 8px 30px rgba(0,0,0,0.6); overflow:hidden; display:grid; grid-template-columns:1fr 340px; gap:0;}
  .main{padding:28px; min-height:520px; background:linear-gradient(180deg,rgba(0,0,0,0.02),transparent);}
  h1{margin:0 0 8px; font-size:22px; letter-spacing:0.6px;}
  p.lead{margin:0 0 18px; color:var(--muted); font-size:14px;}
  .story{background:rgba(0,0,0,0.12); padding:18px; border-radius:8px; max-height:360px; overflow:auto; line-height:1.6; font-size:15px;}
  .choices{margin-top:14px; display:flex; flex-direction:column; gap:10px;}
  .btn{background:transparent; border:1px solid rgba(255,255,255,0.06); padding:12px 14px; border-radius:8px; cursor:pointer; text-align:left; color:inherit;}
  .btn:hover{transform:translateY(-2px); box-shadow:0 6px 18px rgba(0,0,0,0.45);}
  .btn.primary{background:linear-gradient(90deg,var(--accent),#a86b3e); color:#111; border:none; font-weight:600;}
  .sidebar{padding:18px; border-left:1px solid rgba(255,255,255,0.03); background:linear-gradient(180deg, rgba(255,255,255,0.01), transparent);}
  .panel{background:var(--card); padding:12px; border-radius:8px; margin-bottom:12px;}
  .stat{display:flex; justify-content:space-between; margin-bottom:6px; font-size:13px;}
  .inv{display:flex; gap:8px; flex-wrap:wrap;}
  .chip{background:rgba(255,255,255,0.03); padding:6px 8px; border-radius:6px; font-size:13px;}
  .small{font-size:12px; color:var(--muted);}
  footer{padding:12px; text-align:center; color:var(--muted); font-size:12px;}
  .danger{color:#ff8b8b;}
  .hidden{display:none;}
  @media (max-width:880px){ .container{grid-template-columns:1fr; } .sidebar{border-left:none;border-top:1px solid rgba(255,255,255,0.03);} }
</style>
</head>
<body>
<div class="container" role="application" aria-label="Noir Dedektif oyunu">
  <div class="main">
    <h1>Noir Dedektif</h1>
    <p class="lead">Şehir yağmur altında. Bir dedektifin hikâyesi: seçimlerinle ilerle, ipuçları topla, gerçeği ortaya çıkar. <span class="small">Bu oyun olgun temalar içerir (şiddet, alkol, karanlık atmosfer) — cinsel içerik yok.</span></p>

    <div id="story" class="story" tabindex="0" aria-live="polite"></div>

    <div id="choices" class="choices" role="menu" aria-label="Seçimler"></div>

    <div style="margin-top:12px; display:flex; gap:8px;">
      <button id="saveBtn" class="btn">Kaydet</button>
      <button id="loadBtn" class="btn">Yükle</button>
      <button id="restartBtn" class="btn danger">Yeni Oyun</button>
    </div>
  </div>

  <aside class="sidebar" aria-label="Bilgiler">
    <div class="panel">
      <div class="stat"><strong>Karakter</strong><span id="playerName">Siz</span></div>
      <div class="stat"><span>Akıl</span><span id="statMind">10</span></div>
      <div class="stat"><span>Cesaret</span><span id="statGrit">10</span></div>
      <div class="stat"><span>İtibar</span><span id="statRep">5</span></div>
      <div class="stat"><span>Para</span><span id="statCash">25</span></div>
    </div>

    <div class="panel">
      <strong>Envanter</strong>
      <div id="inventory" class="inv" style="margin-top:8px;">
      </div>
    </div>

    <div class="panel small">
      <strong>İpuçları</strong>
      <ul id="clues" style="padding-left:18px; margin:8px 0 0 0;"></ul>
    </div>

    <div class="panel small">
      <strong>Notlar</strong>
      <div style="margin-top:6px;">Oyunu kaydetmek için "Kaydet", ilerlemeyi geri almak için "Yeni Oyun".</div>
    </div>
  </aside>
</div>

<footer>Noir Dedektif — Tek sayfa HTML oyun • Hazır</footer>

<script>
/*
  Tek sayfa metin macerası:
  - Oyun durumu (state) tek bir nesnede
  - Bölümler (scenes) seçimlerle ilerler
  - Basit test (random + stat) mekanikleri
  - Kaydet / yükle: localStorage
*/

const scenes = {
  start: {
    text: `Yağmur şehrin üzerine vuruyor. Lambaların altındaki yollar parlak, sigara dumanı kameranın yakın çekim gibi etrafı sarıyor. İsminiz bir zamanlar saygı görürdü — artık faturalar, birkaç yarım kalmış dava ve tek gecelik kahveler var.\n\nOfisteki çayı demleniyor. Masanın üzerindeki zarf ise dün gece gelen daveti hatırlatıyor: "Buluşma — Gece Yarısı, Eski Depo". Bir seçenek daha var: polis kayıtlarına bakmak, ya da kahvede dedikoduları dinlemek. Ne yapacaksınız?`,
    choices: [
      { txt: "Zarfa bak", to: "envelope" },
      { txt: "Polis kayıtlarına göz at", to: "police" },
      { txt: "Kahveye in, dedikodu topla", to: "cafe" }
    ]
  },

  envelope: {
    text: `Zarf kalın: içindekiler bir fotoğraf ve bir acık bir not. Fotoğrafta gecenin karanlığında belirsiz bir siluet, notta sadece bir saat: 00:00. Notun arkasında bir kod: "BR-13".`,
    onEnter: (s) => addClue(s, "Fotoğraf: belirsiz siluet; kod BR-13"),
    choices: [
      { txt: "Depoya doğru yola çık", to: "warehouseApproach" },
      { txt: "Polise götür", to: "police" },
      { txt: "Daha fazla araştır", to: "searchRecords" }
    ]
  },

  police: {
    text: `Polis kaydı karışık. BR-13 kodu daha önce küçük suç çetelerinin kullandığı bir işaret, ama kayıtlarda 2 sene öncesine kadar uzanıyor. Çıkışta memur sana bir şişe viski takdim ediyor — "Kederini iç, dostum."`,
    onEnter: (s) => addMoney(s, 10),
    choices: [
      { txt: "Depoya git", to: "warehouseApproach" },
      { txt: "Kayıtları daha derin tara", to: "searchRecords" },
      { txt: "Kahveye in, dedikodu topla", to: "cafe" }
    ]
  },

  cafe: {
    text: `Kahvede insanlar konuşuyor. Barmen seni tanır: "Gece hep aynı insanlar geliyor, bir takım eski depo işleri..." Bir kadın yanaşıyor, gözleri uykusuz. "BR-13'ten haberin var mı?" diye soruyor. Bize yardım karşılığında bir bilgi veriyor: depo kapısında bir bekçi var; ödeme yaparsan içeri alınabilirsin.`,
    choices: [
      { txt: "Ödemeyi yap (10₺)", to: "payGuard", cond: s => s.cash >= 10 },
      { txt: "İkna etmeye çalış", to: "persuadeBartender" },
      { txt: "Geri dön", to: "start" }
    ]
  },

  payGuard: {
    text: `Parayı ödüyorsun. Bilgi karşılığında adam, gece yarısı gelen aracı tarif ediyor: siyah bir sedan, plakası yarı okunur... İçeri girme planın şekilleniyor.`,
    onEnter: (s) => { addMoney(s, -10); addClue(s, "Kayıt: siyah sedan, yarı okunur plaka"); },
    choices: [
      { txt: "Depoya doğru yola çık", to: "warehouseApproach" },
      { txt: "İzleri takip et", to: "trackCar" }
    ]
  },

  persuadeBartender: {
    text: `İkna denemesi...`,
    onEnter: (s) => {
      const roll = rand() + s.mind/20;
      if (roll > 0.7){
        s.rep += 1; addClue(s, "Barmen bilgileri paylaştı: sabıkalı bekçi var."); s._last = "success";
      } else {
        s.mind -= 1; s._last = "fail";
      }
    },
    choices: [
      { txt: "Devam", to: (s) => s._last === "success" ? "warehouseApproach" : "start" }
    ]
  },

  searchRecords: {
    text: `Daha derin arama yapıyorsun. BR-13 aslında bir depo kodu ve 5 yıl önce burada kaybolan birkaç kişinin isimleriyle eşleşiyor. İş karışık, bazı polis dosyaları yanlışlıkla kapatılmış.`,
    onEnter: (s) => addClue(s, "BR-13 depo kodu; geçmişte kaybolmalar"),
    choices: [
      { txt: "Depoya git", to: "warehouseApproach" },
      { txt: "Bir kaynak bul", to: "informant" }
    ]
  },

  informant: {
    text: `Sokaktaki bir haberci seni bir köşeye çekiyor. "Girmeyi denersen bekçi var. Silahı 2-3 adım ötede sakladı."`,
    onEnter: (s) => addClue(s, "Bekçinin silahı gizli"),
    choices: [
      { txt: "Silahı al (risk var)", to: "takeGun" },
      { txt: "Depoya git", to: "warehouseApproach" }
    ]
  },

  takeGun: {
    text: `Silahı alıyorsun. Tetik soğuk. Bu eylem itibarını düşürebilir ama işine yarayabilir.`,
    onEnter: (s) => { addItem(s,"Tabanca"); s.rep -= 1; },
    choices: [
      { txt: "Depoya git", to: "warehouseApproach" }
    ]
  },

  trackCar: {
    text: `Siyah sedanın izini sürüyorsun. Park ettiği yer bir gece kulübü önü. İçeride tanınmış bir isim: "Marlo" — yeraltı dünyasının figürlerinden.`,
    onEnter: (s) => addClue(s, "Marlo: yeraltı figürü, gece kulübü"),
    choices: [
      { txt: "Marlo ile konuş (yüksek risk)", to: "confrontMarlo" },
      { txt: "Depoya geri dön", to: "warehouseApproach" }
    ]
  },

  confrontMarlo: {
    text: `Marlo kurnaz. Konuşma sabırlı olmayı gerektiriyor.`,
    onEnter: (s) => {
      const roll = rand() + s.grit/20;
      if (roll > 0.75){
        addClue(s, "Marlo: Depo işinde gizli işler var. Bir teslimat bekleniyor.");
        s.rep += 2; s._last="ok";
      } else {
        s.grit -= 2; s._last="bad";
      }
    },
    choices: [
      { txt: "Devam", to: (s)=> s._last==="ok" ? "warehouseApproach" : "start" }
    ]
  },

  warehouseApproach: {
    text: `Eski depo yakın. Kapı kilitli, bir gölge bekçi. Bir istek: paran mı, ikna mı, yoksa zor mu?`,
    choices: [
      { txt: "Para ver (20₺)", to: "payGuardAtDepot", cond: s => s.cash >= 20 },
      { txt: "İkna etmeye çalış", to: "talkToGuard" },
      { txt: "Zorla gir (silah varsa)", to: "forceEntry", cond: s => s.items.includes("Tabanca") },
      { txt: "Geri çekil", to: "start" }
    ]
  },

  payGuardAtDepot: {
    text: `Parayı veriyorsun. Bekçi içeri girmeni sağlıyor ancak içeride tuhaf bir sessizlik var — ışıklar sönük ve rütubet ağır.`,
    onEnter: (s)=> { addMoney(s,-20); addClue(s,"Depoda tuhaf sessizlik"); },
    choices: [
      { txt: "İçeri gir", to: "insideWarehouse" }
    ]
  },

  talkToGuard: {
    text: `İkna denemesi...`,
    onEnter: (s) => {
      const roll = rand() + s.mind/20;
      if (roll > 0.65) { addClue(s,"Bekçi yorgun; seni içeri alıyor."); s.rep += 1; s._last="in"; }
      else { s.grit -= 1; s._last="out"; }
    },
    choices: [
      { txt: "Devam", to: (s)=> s._last==="in" ? "insideWarehouse" : "start" }
    ]
  },

  forceEntry: {
    text: `Zorla içeri giriyorsun. Silahın var, ama her şey kontrolden çıkabilir.`,
    onEnter: (s) => {
      const roll = rand() + (s.grit + (s.items.includes("Tabanca")?2:0))/25;
      if (roll > 0.7) { addClue(s,"Zorla giriş: içeride bir gölge kaçtı."); s.rep -= 1; s._last="entered"; }
      else { s.grit -= 3; s._last="hurt"; }
    },
    choices: [
      { txt: "Devam", to: (s)=> s._last==="entered" ? "insideWarehouse" : "injured" }
    ]
  },

  injured: {
    text: `Hareket sırasında yara alıyorsun. Bir süre toparlanman gerekecek. İlerleme yavaşlar.`,
    onEnter: (s) => { s.health = (s.health||10)-4; if (s.health <= 0) s._last="dead"; else s._last="ok"; },
    choices: [
      { txt: "Devam", to: (s)=> s._last==="dead" ? "gameOver" : "start" }
    ]
  },

  insideWarehouse: {
    text: `Depo içinde eski sandıklar, paletler ve arka tarafta kilitli bir oda. Bir masanın üzerinde bir dosya ve bir küçük karanlık kutu var.`,
    choices: [
      { txt: "Dosyayı incele", to: "readFile" },
      { txt: "Kutuya bak", to: "openBox" },
      { txt: "Arka odaya bak", to: "lockedRoom" }
    ]
  },

  readFile: {
    text: `Dosya ismini veriyor: "BR-13 Operasyonu". İçinde isimler ve tarih: birkaç kişi iz bırakmadan kaybolmuş. Not: "Teslimat gecesi — saat 03:00".`,
    onEnter: (s) => addClue(s,"Dosya: Teslimat gecesi 03:00; isimler listesi"),
    choices: [
      { txt: "Kutuya bak", to: "openBox" },
      { txt: "Arka odaya bak", to: "lockedRoom" }
    ]
  },

  openBox: {
    text: `Kutu kırık; içinde bir anahtar ve eski bir madalya var. Madalyada bir logo: bir gemi çarkı.`,
    onEnter: (s) => { addItem(s,"Anahtar"); addClue(s,"Madalyada gemi çarkı logosu"); },
    choices: [
      { txt: "Arka odayı anahtarla aç", to: (s)=> s.items.includes("Anahtar") ? "lockedRoomOpen" : "insideWarehouse" },
      { txt: "Geri çık", to: "insideWarehouse" }
    ]
  },

  lockedRoom: {
    text: `Kapı kilitli. Bir anahtar gerek.`,
    choices: [
      { txt: "Geri", to: "insideWarehouse" }
    ]
  },

  lockedRoomOpen: {
    text: `Anahtarla açıyorsun. İçeride birkaç kişi bağlanmış, hayattalar ama bitkin. Onlar BR-13 mağdurları. Birisi mırıldanıyor: "Teslimat... rıhtım..."`,
    onEnter: (s) => { addClue(s,"Rıhtım bağlantısı: teslimat"); addItem(s,"Tanık"); },
    choices: [
      { txt: "Tanıkları al, rıhtıma git", to: "dock" },
      { txt: "Polise götür", to: "policeAfterRescue" }
    ]
  },

  policeAfterRescue: {
    text: `Polise götürdün. Resmi soruşturma başlar — ama bazı dosyalar kayıp olabilir. Marlo ve rıhtım bağlantısı resmi soruşturmaya çekildi.`,
    onEnter: (s) => { s.rep += 2; addClue(s,"Polis soruşturması başlatıldı"); },
    choices: [
      { txt: "Olayı basına ver", to: "expose" },
      { txt: "Marlo'ya git", to: "trackCar" }
    ]
  },

  dock: {
    text: `Rıhtımda gece yarısı soğuk bir sis. Paletler, konteynerler. Uzaktan bir ışık hareket ediyor. Bir teslimat bekleniyor — ve senin kararın kilit: gizlice izlemek mi, yoksa müdahale mi?`,
    choices: [
      { txt: "Gizlice izle", to: "stakeout" },
      { txt: "Müdahale et", to: "intervene" }
    ]
  },

  stakeout: {
    text: `Gözlemliyorsun. Siyah sedan geliyor. İçinden biri iniyor: Marlo'nun adamı. Teslimat bir çuvar; içinden insan sesi geliyor — kaçırılanlar mı? Polisi çağırmak bir seçenek ama Marlo kaçabilir.`,
    onEnter: (s) => addClue(s,"Rıhtımda teslimat: insan sesi"),
    choices: [
      { txt: "Polisi ara", to: "callPolice" },
      { txt: "Kendi başına müdahale et", to: "intervene" }
    ]
  },

  intervene: {
    text: `Müdahale riskli. İster sessizce, ister güç kullanarak yapabilirsin.`,
    choices: [
      { txt: "Sessiz müdahale (ikna/test)", to: "sneakIntervene" },
      { txt: "Gürültülü müdahale (çatışma)", to: "loudIntervene" }
    ]
  },

  sneakIntervene: {
    text: `Sessizce yaklaşıyorsun...`,
    onEnter: (s) => {
      const roll = rand() + s.mind/20;
      if (roll > 0.7) { addClue(s,"Sessiz müdahale başarılı: birkaç kişiyi kurtardın."); s.rep += 2; s._last="saved"; }
      else { s.grit -= 2; s._last="caught"; }
    },
    choices: [
      { txt: "Devam", to: (s)=> s._last==="saved" ? "resolutionGood" : "resolutionBad" }
    ]
  },

  loudIntervene: {
    text: `Çatışma başlıyor. Silah varsa avantajın olur, ama hasar riski yüksek.`,
    onEnter: (s) => {
      const power = (s.items.includes("Tabanca")?2:0) + s.grit/20 + rand();
      if (power > 1.2){ addClue(s,"Çatışma: başarılı, ancak yaralandın."); s.grit -= 1; s.rep += 1; s._last="saved"; }
      else { s.grit -= 3; s._last="bad"; }
    },
    choices: [
      { txt: "Devam", to: (s)=> s._last==="saved" ? "resolutionGood" : "resolutionBad" }
    ]
  },

  callPolice: {
    text: `Polisi arıyorsun; sirenler uzaktan geliyor. Teslimat anında kesintiye uğruyor, birkaç kişi kaçıyor ama mağdurlar kurtarılıyor. Marlo serbest kalabilir; bazı izler kaybolacak.`,
    onEnter: (s) => { addClue(s,"Polis müdahalesi: bazı failler kaçtı"); s.rep += 1; },
    choices: [
      { txt: "Soruşturmayı sürdür", to: "resolutionMixed" },
      { txt: "İşi polise bırak", to: "resolutionPolice" }
    ]
  },

  resolutionGood: {
    text: `Cesaretin ve aklınla birçok kişiyi kurtardın. Marlo'nın çarkı çatladı; birkaç küçük figür tutuklandı. Senin saygınlık arttı; ama yeraltı seni unutmayacak.`,
    onEnter: (s) => { s.rep += 3; s.cash += 50; },
    choices: [
      { txt: "Oyun Sonu: Başarılı", to: "endGood" }
    ]
  },

  resolutionMixed: {
    text: `Bazı failler kaçtı ama onlar için daha küçük ipuçları kaldı. Sen yaşadın, ama zafer tam değil.`,
    onEnter: (s) => { s.rep += 1; s.cash += 20; },
    choices: [
      { txt: "Oyun Sonu: Karışık", to: "endMixed" }
    ]
  },

  resolutionBad: {
    text: `Plan istediğin gibi gitmedi. Birkaç kişi zarar gördü ve bazı deliller kayboldu. İşin tehlikeli tarafı ağır bastı.`,
    onEnter: (s) => { s.rep -= 2; s.grit -= 2; },
    choices: [
      { txt: "Oyun Sonu: Kötü", to: "endBad" }
    ]
  },

  resolutionPolice: {
    text: `İşi polise bıraktın. Resmi raporlar hazırlanıyor; bazı kesimler tatmin olur, birkaç dosya eksik kalır. Sen rüşvet ya da ilişkilerle daha az konuşulan yolculuğuna devam ediyorsun.`,
    onEnter: (s) => { s.rep += 0; },
    choices: [
      { txt: "Oyun Sonu: Resmi", to: "endPolice" }
    ]
  },

  gameOver: {
    text: `Yaraların ağır. İlerleyemiyorsun. Oyun burada sona erdi.`,
    choices: [
      { txt: "Yeni Oyun", to: "start" }
    ]
  },

  endGood: { text: "Şehirde küçük bir zafer kazandın. İsimlerin bir kısmı kurtuldu. Gece biterken ufak bir huzur—ama işin bir tarafı hep eksik.", choices:[{txt:"Yeni Oyun", to:"start"}] },
  endMixed: { text: "İş kısmen başarılı. Bazı sorular cevapsız kaldı. Dedektif bazen kazandığını, bazen kaybettiğini bilir.", choices:[{txt:"Yeni Oyun", to:"start"}] },
  endBad: { text: "İş kötü bitti. Şehrin karanlığı biraz daha derinleşti. Yeni başlangıçlar zor olacak.", choices:[{txt:"Yeni Oyun", to:"start"}] },
  endPolice: { text: "Olaya resmi bir çözüm geldi; bazı gerçekler gömüldü. Sen işini yaptın ama vicdan farklı çarpar.", choices:[{txt:"Yeni Oyun", to:"start"}] }
};

// Oyun state
let state = {
  scene: "start",
  mind: 10,
  grit: 10,
  rep: 5,
  cash: 25,
  items: [],
  clues: [],
  health: 10,
  playerName: "Sen"
};

const storyEl = document.getElementById('story');
const choicesEl = document.getElementById('choices');
const inventoryEl = document.getElementById('inventory');
const cluesEl = document.getElementById('clues');
const nameEl = document.getElementById('playerName');
const sMind = document.getElementById('statMind');
const sGrit = document.getElementById('statGrit');
const sRep = document.getElementById('statRep');
const sCash = document.getElementById('statCash');

function rand(){ return Math.random(); }

function render(){
  const sc = scenes[state.scene];
  if(!sc) { storyEl.textContent = "Bilinmeyen sahne."; return; }

  // Metin
  storyEl.innerText = sc.text;

  // onEnter etkinleştirilmeleri sahneye girişte değilse çalıştır
  if (!state._entered || state._entered !== state.scene) {
    if (typeof sc.onEnter === 'function') sc.onEnter(state);
    state._entered = state.scene;
  }

  // Seçimler
  choicesEl.innerHTML = '';
  (sc.choices || []).forEach((c, idx) => {
    let allowed = true;
    if (typeof c.cond === 'function') allowed = c.cond(state);
    if (!allowed) return;
    const btn = document.createElement('button');
    btn.className = 'btn' + (idx===0 ? ' primary' : '');
    btn.innerText = c.txt;
    btn.onclick = ()=> {
      let dest = c.to;
      if (typeof dest === 'function') dest = dest(state);
      changeScene(dest);
    };
    choicesEl.appendChild(btn);
  });

  // Sidebar güncelle
  nameEl.innerText = state.playerName;
  sMind.innerText = Math.max(0, Math.round(state.mind));
  sGrit.innerText = Math.max(0, Math.round(state.grit));
  sRep.innerText = Math.max(-10, Math.round(state.rep));
  sCash.innerText = Math.max(0, Math.round(state.cash));
  inventoryEl.innerHTML = '';
  state.items.forEach(it => {
    const span = document.createElement('div'); span.className='chip'; span.innerText = it;
    inventoryEl.appendChild(span);
  });
  cluesEl.innerHTML = '';
  state.clues.forEach(cl=> {
    const li = document.createElement('li'); li.innerText = cl; cluesEl.appendChild(li);
  });

  // Oyun sonu durumu kontrolü
  if (state.health <= 0) {
    changeScene('gameOver');
  }
}

function changeScene(name){
  if(!scenes[name]) { console.warn("Sahne yok:", name); return; }
  state.scene = name;
  // Temizlik: sahneye tekrar girerse onEnter yeniden çalışsın
  state._entered = null;
  render();
}

function addItem(s, item){
  if (!s.items.includes(item)) s.items.push(item);
}
function addClue(s, clue){
  if (!s.clues.includes(clue)) s.clues.push(clue);
}
function addMoney(s, amt){
  s.cash = (s.cash||0) + amt;
}

// Kaydet / yükle
const saveBtn = document.getElementById('saveBtn');
const loadBtn = document.getElementById('loadBtn');
const restartBtn = document.getElementById('restartBtn');

saveBtn.onclick = ()=> {
  localStorage.setItem('noir_save', JSON.stringify(state));
  alert('Oyun kaydedildi.');
};
loadBtn.onclick = ()=> {
  const raw = localStorage.getItem('noir_save');
  if (!raw) { alert('Kayıt bulunamadı.'); return; }
  try {
    const obj = JSON.parse(raw);
    state = Object.assign(state, obj);
    alert('Oyun yüklendi.');
    render();
  } catch(e){ alert('Yükleme başarısız.'); }
};
restartBtn.onclick = ()=> {
  if(!confirm("Yeni oyun başlatılsın mı? (Mevcut ilerleme kaybolacak)")) return;
  state = {
    scene: "start",
    mind: 10,
    grit: 10,
    rep: 5,
    cash: 25,
    items: [],
    clues: [],
    health: 10,
    playerName: "Sen"
  };
  render();
};

// Başlangıç render
render();

// Klavye erişilebilirlik (1-9 ile seçim)
document.addEventListener('keydown', e=>{
  if (e.key >= '1' && e.key <= '9'){
    const idx = parseInt(e.key)-1;
    const btns = Array.from(choicesEl.querySelectorAll('button'));
    if (btns[idx]) btns[idx].click();
  }
});
</script>
</body>
</html>

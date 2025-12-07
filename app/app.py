import streamlit as st
import random

# -------------------- GENEL AYARLAR -------------------- #

st.set_page_config(page_title="NOX: Gizli Bağ", page_icon="🖤", layout="centered")

# Karanlık / gizemli atmosfer için basit CSS
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top, #1f0b3a 0, #070411 40%, #020105 100%);
        color: #f5e6ff;
    }
    h1, h2, h3, h4 {
        color: #f7ecff !important;
        font-family: "Trebuchet MS", sans-serif;
    }
    .dark-card {
        background: rgba(8, 4, 20, 0.85);
        padding: 1.2rem 1.4rem;
        border-radius: 12px;
        border: 1px solid rgba(180, 120, 255, 0.35);
        box-shadow: 0 0 25px rgba(70, 0, 120, 0.6);
    }
    .label-pill {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        background: rgba(140, 70, 255, 0.22);
        color: #f8e8ff;
        font-size: 0.8rem;
        margin-right: 0.3rem;
    }
    .subtle {
        color: #c3a9ff;
        font-size: 0.9rem;
    }
    .big-btn button {
        width: 100% !important;
        border-radius: 999px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- OYUN VERİLERİ -------------------- #

MAX_SCORE = 10  # klasik modlarda kazanan eşiği
MAX_BOND = 20   # roulette / genel bağ seviyesi

CARDS = [
    # ---- CESARET MODU ----
    {
        "mode": "Cesaret",
        "category": "Cesaret",
        "type": "görev",
        "text": "Karanlıktan bir istek çıkar: Partnerine söylemekten çekindiğin bir şeyi, doğrudan değil dolaylı bir dille anlat."
    },
    {
        "mode": "Cesaret",
        "category": "Cesaret",
        "type": "görev",
        "text": "Dokunmadan, sadece yaklaşarak bir mesaj ver. Partnerin ne istediğini tahmin etmeye çalışsın."
    },
    {
        "mode": "Cesaret",
        "category": "Cesaret",
        "type": "görev",
        "text": "Sadece bakışlarınla bir davet oluştur. Kelime yok, işaret yok; yalnızca gözlerin konuşsun."
    },
    {
        "mode": "Cesaret",
        "category": "Cesaret",
        "type": "soru",
        "text": "Şu an aranızdaki havayı bir kelimeyle tanımlasan ne olurdu? Aynı soruyu partnerine de sor."
    },

    # ---- İTİRAF MODU ----
    {
        "mode": "İtiraf",
        "category": "İtiraf",
        "type": "soru",
        "text": "Partnerinin enerjisinde seni en çok çeken 'gölge' yönü nedir? Beden, ses, bakış, tavır… hangisi sende en çok iz bırakıyor?"
    },
    {
        "mode": "İtiraf",
        "category": "İtiraf",
        "type": "soru",
        "text": "Onunla ilgili daha önce paylaşmadığın gizli bir merakını söyle; ama detaya girmeden, sadece hissini tarif ederek."
    },
    {
        "mode": "İtiraf",
        "category": "İtiraf",
        "type": "görev",
        "text": "Partnerinle ilgili aklına gelen en çarpıcı hayali anlat; doğrudan sahneyi değil, sahnenin atmosferini tarif et."
    },
    {
        "mode": "İtiraf",
        "category": "İtiraf",
        "type": "soru",
        "text": "Onun senin üzerinde bıraktığı etkiyi, bir şarkı adı veya film sahnesiyle anlat. Nedenini kısa bir cümle ile açıklayın."
    },

    # ---- GİZLİ KART MODU ----
    {
        "mode": "Gizli Kart",
        "category": "Gizli Kart",
        "type": "görev",
        "text": "Bu kart yalnızca senin. Partnerin gözlerini kapatsın. Sessizce yanına git ve sadece nefesinle varlığını hissettir."
    },
    {
        "mode": "Gizli Kart",
        "category": "Gizli Kart",
        "type": "görev",
        "text": "Sadece sen okuyorsun: Partnerine üç küçük dokunuş yap. Bunlardan yalnızca biri gerçek mesajın. Hangisinin olduğunu bulmasını iste."
    },
    {
        "mode": "Gizli Kart",
        "category": "Gizli Kart",
        "type": "görev",
        "text": "Bu kartı gösterme. Partnerine sadece bir cümle kur: 'Tam olarak ne düşündüğümü bilseydin…' ve cümleyi içinden tamamla."
    },
    {
        "mode": "Gizli Kart",
        "category": "Gizli Kart",
        "type": "soru",
        "text": "İçinden bir cümle kur ve sadece ona bak. Partnerin, senin ne düşündüğünü tahmin etmeye çalışsın."
    },

    # ---- GENEL / KARIŞIK ATMOSFER ----
    {
        "mode": "Genel",
        "category": "Derin",
        "type": "soru",
        "text": "Bu anda, senden yayılan hangi enerji en baskın: sakinlik, merak, gerilim, tutku? Aynı soruyu partnerine de sor."
    },
    {
        "mode": "Genel",
        "category": "Bağ",
        "type": "görev",
        "text": "Üç nefes boyunca aynı ritimde nefes alın. Gözlerinizi kapatın ve yalnızca birbirinizin sesini ve nefesini dinleyin."
    },
    {
        "mode": "Genel",
        "category": "Bağ",
        "type": "görev",
        "text": "Odanın ışığını olabildiğince kısın. Karanlıkta sadece ellerinizle birbirinizi tanımlamaya çalışın."
    },
]

# Roulette / Türbülans Çarkı bileşenleri
ROULETTE_CONTROLLERS = ["Sen", "Partnerin", "İkiniz de", "Rastgele değişsin"]
ROULETTE_LEVELS = ["Yumuşak", "Yoğun", "Tutkulu", "Karanlık"]
ROULETTE_ACTIONS = ["Sinyal", "Fısıltı", "Yakınlık", "Gizemli Jest"]

ROULETTE_HINTS = [
    "Bu kombinasyonu kendi aranızda, yalnızca sizin bildiğiniz bir ritüele dönüştürün.",
    "Detaya girmeden, yalnızca hisleri paylaşın. Gerisini sessizliğe bırakın.",
    "Sözleri minimumda tutun; bakışlar ve küçük jestler konuşsun.",
    "Bu turu, ileride hatırladığınızda sizi gülümsetecek küçük bir sır gibi düşünün."
]

# -------------------- SESSION STATE BAŞLANGIÇ -------------------- #

if "step" not in st.session_state:
    st.session_state.step = "start"

defaults = {
    "player1": "",
    "player2": "",
    "players": [],
    "scores": {},
    "deck": [],
    "turn": 0,
    "current_card": None,
    "mode": "Karışık",
    "winner": None,
    "bond_points": 0,
    "roulette_result": None,
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# -------------------- ORTAK FONKSİYONLAR -------------------- #

def reset_game(full=False):
    st.session_state.deck = []
    st.session_state.turn = 0
    st.session_state.current_card = None
    st.session_state.winner = None
    if full:
        st.session_state.player1 = ""
        st.session_state.player2 = ""
        st.session_state.players = []
        st.session_state.scores = {}
        st.session_state.bond_points = 0
        st.session_state.roulette_result = None
    st.session_state.step = "start"


def init_deck_for_mode(mode: str):
    if mode == "Karışık":
        st.session_state.deck = random.sample(CARDS, len(CARDS))
    else:
        filtered = [c for c in CARDS if c["mode"] == mode or c["mode"] == "Genel"]
        if not filtered:
            filtered = CARDS[:]
        st.session_state.deck = random.sample(filtered, len(filtered))


def draw_card():
    if len(st.session_state.deck) == 0:
        init_deck_for_mode(st.session_state.mode)
    st.session_state.current_card = st.session_state.deck.pop()


def increment_bond(by: int = 1):
    st.session_state.bond_points = min(MAX_BOND, st.session_state.bond_points + by)


def show_scores_and_bond():
    st.markdown("### 💖 Skorlar")
    for p, s in st.session_state.scores.items():
        st.write(f"**{p}:** {s} puan")

    total = sum(st.session_state.scores.values())
    max_total = MAX_SCORE * max(1, len(st.session_state.players))
    ratio = 0 if max_total == 0 else min(1.0, total / max_total)

    st.markdown("### 🔥 Bağ Seviyesi")
    st.progress(min(1.0, (st.session_state.bond_points / MAX_BOND) * 0.5 + ratio * 0.5))
    st.caption("Bağ seviyesi, hem tamamlanan görevlerden hem de birlikte yaşadığınız turlardan beslenir.")


def show_header():
    st.markdown(
        "<h1 style='text-align:center;'>NOX: Gizli Bağ</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='subtle' style='text-align:center;'>karanlık, tutkulu ve sadece ikinizin bildiği bir oyun</p>",
        unsafe_allow_html=True,
    )

# -------------------- EKRAN: BAŞLANGIÇ -------------------- #

show_header()

if st.session_state.step == "start":
    st.markdown("### 🖤 Oyuncular")

    col1, col2 = st.columns(2)
    with col1:
        p1 = st.text_input("1. Oyuncu Adı", value=st.session_state.player1)
    with col2:
        p2 = st.text_input("2. Oyuncu Adı", value=st.session_state.player2)

    st.markdown("### 🎭 Mod Seçimi")

    mode = st.selectbox(
        "Oyun havasını seçin",
        ["Karışık", "Cesaret", "İtiraf", "Gizli Kart", "Roulette (Türbülans Çarkı)"],
        index=["Karışık", "Cesaret", "İtiraf", "Gizli Kart", "Roulette (Türbülans Çarkı)"].index(
            st.session_state.mode if st.session_state.mode != "Roulette" else "Roulette (Türbülans Çarkı)"
        ),
    )

    st.markdown(
        "<div class='subtle'>"
        "• <b>Cesaret:</b> daha gözü kara, direkt ama yine de imalı görevler<br>"
        "• <b>İtiraf:</b> duygusal + tensel gerilimi besleyen itiraf kartları<br>"
        "• <b>Gizli Kart:</b> kartı sadece biriniz okur, diğeri tahmin eder<br>"
        "• <b>Roulette:</b> Türbülans Çarkı; kontrol, seviye ve eylem rastgele belirlenir"
        "</div>",
        unsafe_allow_html=True,
    )

    start_clicked = st.button("Oyuna Başla", type="primary")

    if start_clicked:
        if not p1.strip() or not p2.strip():
            st.warning("İki oyuncu adı da dolu olmalı.")
        else:
            st.session_state.player1 = p1.strip()
            st.session_state.player2 = p2.strip()
            st.session_state.players = [st.session_state.player1, st.session_state.player2]
            st.session_state.scores = {st.session_state.player1: 0, st.session_state.player2: 0}
            st.session_state.bond_points = 0
            st.session_state.turn = 0
            st.session_state.winner = None
            st.session_state.current_card = None
            st.session_state.roulette_result = None

            if mode.startswith("Roulette"):
                st.session_state.mode = "Roulette"
                st.session_state.step = "roulette"
            else:
                st.session_state.mode = mode
                init_deck_for_mode(mode)
                st.session_state.step = "game"

# -------------------- EKRAN: KLASİK KART MODLARI (CESARET / İTİRAF / GİZLİ / KARIŞIK) -------------------- #

if st.session_state.step == "game" and st.session_state.mode != "Roulette":
    current_player = st.session_state.players[st.session_state.turn]

    st.markdown(f"### 🎲 Sıra: **{current_player}**")
    st.markdown(
        f"<span class='label-pill'>Mod: {st.session_state.mode}</span>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p class='subtle'>İkiniz de ekrana bakıyorsanız, "
        "Gizli Kart çıkarsa biriniz gözlerini kapatmayı unutmasın.</p>",
        unsafe_allow_html=True,
    )

    st.markdown("")

    col_btn = st.container()
    with col_btn:
        st.markdown("<div class='big-btn'>", unsafe_allow_html=True)
        draw_clicked = st.button("Kart Çek")
        st.markdown("</div>", unsafe_allow_html=True)

    if draw_clicked:
        draw_card()
        st.session_state.step = "card"

    show_scores_and_bond()

    st.markdown("---")
    if st.button("🔁 Mod / Oyuncu Ayarlarına Dön"):
        reset_game(full=False)

# -------------------- EKRAN: KART GÖRÜNTÜLEME -------------------- #

if st.session_state.step == "card" and st.session_state.current_card is not None:
    card = st.session_state.current_card
    current_player = st.session_state.players[st.session_state.turn]

    st.markdown(
        f"<div class='dark-card'>"
        f"<span class='label-pill'>{card['category']}</span>"
        f"<span class='label-pill'>{card['type'].capitalize()}</span>"
        f"<p class='subtle' style='margin-top:0.4rem;'>Bu turu başlatan: <b>{current_player}</b></p>"
        f"<h3>Kart</h3>"
        f"<p>{card['text']}</p>"
        f"<p class='subtle'>Kartı uygularken detayları siz belirleyin; oyun sadece atmosferi fısıldar.</p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown("")

    col1, col2 = st.columns(2)
    with col1:
        completed = st.button("Görev / Soru Yaşandı (+1 puan)", key="completed_card")
    with col2:
        skipped = st.button("Bu Turu Atla", key="skipped_card")

    if completed or skipped:
        if completed:
            st.session_state.scores[current_player] += 1
            increment_bond(1)

        # Kazanan kontrolü
        for p, s in st.session_state.scores.items():
            if s >= MAX_SCORE:
                st.session_state.winner = p
                st.session_state.step = "end"
                break
        else:
            # sırayı değiştir
            st.session_state.turn = (st.session_state.turn + 1) % len(st.session_state.players)
            st.session_state.current_card = None
            st.session_state.step = "game"

    show_scores_and_bond()

    st.markdown("---")
    if st.button("🔁 Mod / Oyuncu Ayarlarına Dön", key="back_from_card"):
        reset_game(full=False)

# -------------------- EKRAN: ROULETTE / TÜRBÜLANS ÇARKI -------------------- #

if st.session_state.step == "roulette" and st.session_state.mode == "Roulette":
    st.markdown("### 🎡 Türbülans Çarkı")
    st.markdown(
        "<div class='subtle'>Kontrol, seviye ve eylem türü rastgele belirlenir. "
        "Detaylar size kalır; oyun sadece çerçeveyi çizer.</div>",
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown("<div class='big-btn'>", unsafe_allow_html=True)
    spin = st.button("Çarkı Çevir")
    st.markdown("</div>", unsafe_allow_html=True)

    if spin:
        controller = random.choice(ROULETTE_CONTROLLERS)
        level = random.choice(ROULETTE_LEVELS)
        action = random.choice(ROULETTE_ACTIONS)
        hint = random.choice(ROULETTE_HINTS)
        st.session_state.roulette_result = (controller, level, action, hint)
        increment_bond(1)

    if st.session_state.roulette_result:
        controller, level, action, hint = st.session_state.roulette_result

        st.markdown(
            f"""
            <div class='dark-card'>
                <h3>Bu Turun Enerjisi</h3>
                <p><span class='label-pill'>Kontrol</span> <b>{controller}</b></p>
                <p><span class='label-pill'>Seviye</span> <b>{level}</b></p>
                <p><span class='label-pill'>Eylem</span> <b>{action}</b></p>
                <p class='subtle' style='margin-top:0.6rem;'>{hint}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("")
        done = st.button("Bu turu yaşadık (+Bağ)", key="roulette_done")
        if done:
            increment_bond(1)

    st.markdown("### 🔥 Bağ Seviyesi")
    st.progress(min(1.0, st.session_state.bond_points / MAX_BOND))
    st.caption("Her çevirdiğiniz çark, yalnızca ikinizin bildiği küçük bir sır bırakabilir.")

    st.markdown("---")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        if st.button("🎴 Kart Modlarına Geç"):
            st.session_state.mode = "Karışık"
            init_deck_for_mode("Karışık")
            st.session_state.step = "game"
    with col_r2:
        if st.button("🔁 Oyuncu Ayarlarına Dön"):
            reset_game(full=False)

# -------------------- EKRAN: BİTİŞ -------------------- #

if st.session_state.step == "end":
    st.markdown("## 🖤 Oyun Bitti")

    if st.session_state.winner:
        st.success(f"🎉 Kazanan: **{st.session_state.winner}**")
    else:
        st.info("Bu turda belirgin bir kazanan yok; ama asıl kazanç aranızdaki bağ oldu.")

    show_scores_and_bond()

    st.markdown("")
    col_end1, col_end2 = st.columns(2)
    with col_end1:
        if st.button("Aynı Modla Yeni Tur"):
            # sadece skor & desteyi sıfırla, isimleri koru
            init_deck_for_mode(st.session_state.mode)
            st.session_state.scores = {p: 0 for p in st.session_state.players}
            st.session_state.turn = 0
            st.session_state.current_card = None
            st.session_state.winner = None
            st.session_state.step = "game"
    with col_end2:
        if st.button("Oyuncu / Mod Ayarlarına Dön"):
            reset_game(full=False)

import streamlit as st
import random

# -------------------- VERİLER -------------------- #

CARDS = [
    # TANIMA
    {"category": "Tanıma", "type": "soru", "text": "Partnerinde seni en çok şaşırtan özellik ne oldu?"},
    {"category": "Tanıma", "type": "soru", "text": "Hayatını etkileyen bir çocukluk anını paylaş."},
    {"category": "Tanıma", "type": "görev", "text": "Birbirinize ilk tanışma anınızı film sahnesi gibi anlatın."},

    # DERİN
    {"category": "Derin Sohbet", "type": "soru", "text": "Bu ilişkide en çok ne zaman güvende hissettin?"},
    {"category": "Derin Sohbet", "type": "soru", "text": "Partnerinden duyduğunda seni en çok şifalandıran cümle neydi?"},
    {"category": "Derin Sohbet", "type": "görev", "text": "Şu cümleyi tamamla: 'Sende en çok sevdiğim şey...'"},
    
    # ROMANTİK / FLÖRTÖZ
    {"category": "Romantik & Flörtöz", "type": "görev", "text": "30 saniye boyunca yalnızca göz göze bakın."},
    {"category": "Romantik & Flörtöz", "type": "görev", "text": "Partnerine bugün için minnettar olduğun 3 şeyi söyle."},
    {"category": "Romantik & Flörtöz", "type": "mini-oyun", "text": "Taş-kağıt-makas oynayın. Kaybeden kazanana küçük bir jest yapar."},
]

# Buraya özgürce kendi (+18 size özel) kartlarınızı ekleyebilirsiniz.
CUSTOM_CARDS = []

ALL_CARDS = CARDS + CUSTOM_CARDS

# -------------------- UYGULAMA -------------------- #

st.set_page_config(page_title="Çift Oyunu", page_icon="💞", layout="centered")

st.markdown("<h1 style='text-align:center;'>💞 Bağlantı: Çift Oyunu 💞</h1>", unsafe_allow_html=True)

# Oturum durumu hazırlığı
if "step" not in st.session_state:
    st.session_state.step = "start"
if "player1" not in st.session_state:
    st.session_state.player1 = ""
if "player2" not in st.session_state:
    st.session_state.player2 = ""
if "scores" not in st.session_state:
    st.session_state.scores = {}
if "deck" not in st.session_state:
    st.session_state.deck = []
if "turn" not in st.session_state:
    st.session_state.turn = 0


# -------------------- GİRİŞ -------------------- #
if st.session_state.step == "start":

    st.subheader("Oyuncu İsimleri")

    p1 = st.text_input("1. Oyuncu Adı", "")
    p2 = st.text_input("2. Oyuncu Adı", "")

    if st.button("Başla"):
        if p1.strip() == "" or p2.strip() == "":
            st.warning("Lütfen iki oyuncu adı da girilsin.")
        else:
            st.session_state.player1 = p1
            st.session_state.player2 = p2
            st.session_state.players = [p1, p2]
            st.session_state.scores = {p1: 0, p2: 0}
            st.session_state.deck = random.sample(ALL_CARDS, len(ALL_CARDS))
            st.session_state.step = "game"


# -------------------- OYUN EKRANI -------------------- #
if st.session_state.step == "game":

    current_player = st.session_state.players[st.session_state.turn]

    st.markdown(f"### 🎲 Sıra: **{current_player}**")

    if st.button("Kart Çek"):
        if len(st.session_state.deck) == 0:
            st.session_state.deck = random.sample(ALL_CARDS, len(ALL_CARDS))

        st.session_state.current_card = st.session_state.deck.pop()
        st.session_state.step = "card"


# -------------------- KART EKRANI -------------------- #
if st.session_state.step == "card":

    card = st.session_state.current_card

    st.markdown(f"### 📌 Kategori: **{card['category']}**")
    st.markdown(f"### 🎴 Tür: **{card['type']}**")

    st.info(card["text"])

    st.markdown("---")
    st.write("Görevi/Soruyu birlikte uyguladıktan sonra ilerleyin.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Tamamlandı (+1 puan)"):
            current_player = st.session_state.players[st.session_state.turn]
            st.session_state.scores[current_player] += 1
            st.session_state.turn = (st.session_state.turn + 1) % 2
            st.session_state.step = "game"

    with col2:
        if st.button("Atla"):
            st.session_state.turn = (st.session_state.turn + 1) % 2
            st.session_state.step = "game"

    # Skor Tablosu
    st.markdown("### 💖 Skorlar")
    for p, s in st.session_state.scores.items():
        st.write(f"**{p}:** {s} puan")

    # Yakınlık oranı
    total = sum(st.session_state.scores.values())
    st.progress(min(total / 20, 1.0))

    # Kazanan kontrolü
    for p, s in st.session_state.scores.items():
        if s >= 10:
            st.success(f"🎉 **Kazanan: {p}!**")
            st.session_state.step = "end"


# -------------------- BİTİŞ -------------------- #
if st.session_state.step == "end":
    st.markdown("## 💞 Oyun Bitti!")
    st.write("Dilerseniz oyuna yeni kartlar ekleyerek kendi ilişkinize göre özelleştirebilirsiniz.")
    if st.button("Başa Dön"):
        st.session_state.step = "start"
        st.session_state.scores = {}
        st.session_state.deck = []

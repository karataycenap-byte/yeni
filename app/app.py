import streamlit as st
import random
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Vicdan Pusulası", page_icon="⚖️", layout="centered")

# --- CSS İLE ATMOSFERİK TASARIM ---
st.markdown("""
<style>
    /* Genel Arka Plan ve Yazı Tipi */
    .main {
        background-color: #0E1117;
        color: #FAFAFA;
        font-family: 'Georgia', serif;
    }
    
    /* Başlık */
    .title-text {
        font-size: 36px;
        font-weight: 300;
        text-align: center;
        letter-spacing: 2px;
        color: #E0E0E0;
        margin-bottom: 30px;
        text-transform: uppercase;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
    }
    
    /* Soru Kartı */
    .question-card {
        background-color: #161B22;
        padding: 30px;
        border-radius: 8px;
        border-left: 4px solid #8e44ad; /* Mor vurgu */
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    .question-text {
        font-size: 24px;
        font-weight: 500;
        line-height: 1.5;
        color: #ffffff;
    }
    
    /* Sonuç Analizi */
    .analysis-box {
        background-color: #2c3e50;
        padding: 20px;
        border-radius: 8px;
        margin-top: 20px;
        border: 1px solid #8e44ad;
    }
    
    /* Butonlar */
    .stButton>button {
        height: 60px;
        font-size: 18px;
        border-radius: 4px;
        transition: all 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# --- FELSEFİ İKİLEMLER VERİTABANI ---
# Format: [Soru, Seçenek A, Seçenek B, Analiz A, Analiz B]
IKILEMLER = [
    (
        "Mükemmel bir simülasyonda sonsuza dek mutlu yaşamak mı, yoksa acı dolu gerçek dünyada uyanmak mı?",
        "💊 Mükemmel Simülasyon (Mutluluk)",
        "🛑 Acı Dolu Gerçek (Hakikat)",
        "Hedonizmi seçtin. Senin için önemli olan deneyimin kalitesi, kaynağı değil. Cypher (Matrix) gibi düşünüyorsun.",
        "Varoluşçuluğu seçtin. Senin için özgürlük ve gerçeklik, mutluluktan daha değerli. Sokrates'in dediği gibi: 'Sorgulanmamış bir hayat yaşamaya değmez.'"
    ),
    (
        "Sevdiğin tek bir kişiyi kurtarmak için tanımadığın 100 kişinin ölmesine izin verir misin?",
        "❤️ Sevdiğimi Kurtarırım",
        "⚖️ 100 Kişiyi Kurtarırım",
        "Duygusal Etik. Senin için kişisel bağlar, evrensel matematiksel doğrulardan daha güçlü. İnsan olmanın trajedisi budur.",
        "Faydacı Etik (Utilitarianism). Jeremy Bentham gibi düşünüyorsun: 'En fazla kişi için en büyük iyilik'. Ama kalbini feda ettin."
    ),
    (
        "Geçmişindeki tüm kötü anıları sildirme şansın olsa, sildirir miydin? (Kişiliğin değişecek olsa bile)",
        "🧹 Evet, Sildiririm",
        "🧠 Hayır, Kalsın",
        "Tabula Rasa'yı arzuluyorsun. Acının seni engellediğini düşünüyorsun, ama unuttuğun şey şu: Acı, büyümenin tek yoludur.",
        "Nietzsche'nin 'Amor Fati' (Kaderini Sev) anlayışındasın. Seni sen yapan şeyin sadece zaferlerin değil, yaraların olduğunu biliyorsun."
    ),
    (
        "Ölümsüz olmak ama insanlığını kaybetmek mi (duygu yok), yoksa anlamlı ama kısa bir insan ömrü mü?",
        "🤖 Ölümsüzlük (Duygusuz)",
        "🥀 Kısa ve Anlamlı Ömür",
        "Transhümanizm. Varlığın devamlılığını, varlığın içeriğinden üstün tutuyorsun. Ölüm korkun, yaşam arzundan büyük.",
        "Stoacı Bakış. Ölümün yaşamı anlamlı kıldığını biliyorsun. Bir şeyin değerli olması için, onun bitecek olması gerekir."
    ),
    (
        "Bir suçluyu cezalandırmanın amacı ne olmalı: İntikam almak mı, onu topluma geri kazandırmak mı?",
        "🔥 İntikam / Adalet",
        "🌿 Rehabilitasyon / İyileştirme",
        "Retributivizm. Göze göz. Senin için adalet, evrensel bir denge meselesidir. Suç cezasız kalamaz.",
        "Hümanizm. İnsanın değişebileceğine inanıyorsun. Suçu bir hastalık, suçluyu ise hasta olarak görüyorsun."
    ),
    (
        "Dünyadaki tüm savaşları bitirecek bir düğme var, ama basarsan tüm sanat ve edebiyat da yok olacak. Basar mısın?",
        "🕊️ Evet, Barış İçin Basarım",
        "🎨 Hayır, Sanat İçin Basmam",
        "Mutlak Pragmatizm. Yaşam hakkını, yaşamın estetiğinden üstün tuttun. Güvenli ama renksiz bir dünya seçtin.",
        "Romantizm. İnsanı insan yapan şeyin sadece nefes almak değil, yaratmak olduğunu düşünüyorsun. Acı olmadan sanat olmaz."
    )
]

# --- SESSION STATE (DURUM YÖNETİMİ) ---
if 'index' not in st.session_state:
    st.session_state.index = random.randint(0, len(IKILEMLER)-1)
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
if 'choice' not in st.session_state:
    st.session_state.choice = None

def next_question():
    st.session_state.index = random.randint(0, len(IKILEMLER)-1)
    st.session_state.show_result = False
    st.session_state.choice = None
    st.rerun()

def make_choice(choice_idx):
    st.session_state.choice = choice_idx
    st.session_state.show_result = True
    st.rerun()

# --- ARAYÜZ ---

st.markdown('<p class="title-text">🪐 VİCDAN PUSULASI</p>', unsafe_allow_html=True)

# Mevcut Soru Verisi
soru, secenek_a, secenek_b, analiz_a, analiz_b = IKILEMLER[st.session_state.index]

# SORU KARTI
st.markdown(f"""
<div class="question-card">
    <p class="question-text">{soru}</p>
</div>
""", unsafe_allow_html=True)

# SEÇİM EKRANI
if not st.session_state.show_result:
    col1, col2 = st.columns(2)
    with col1:
        st.button(secenek_a, on_click=make_choice, args=(0,), use_container_width=True)
    with col2:
        st.button(secenek_b, on_click=make_choice, args=(1,), use_container_width=True)
    
    st.markdown("<br><p style='text-align:center; color:gray; font-size:14px;'><i>Dürüst ol. Kimse seni yargılamıyor, sadece sen.</i></p>", unsafe_allow_html=True)

# SONUÇ EKRANI
else:
    # Rastgele istatistik üretimi (Simülasyon)
    oran_a = random.randint(30, 70)
    oran_b = 100 - oran_a
    
    secilen_analiz = analiz_a if st.session_state.choice == 0 else analiz_b
    secilen_oran = oran_a if st.session_state.choice == 0 else oran_b
    
    st.markdown(f"### 👁️ Analiz")
    st.markdown(f"""
    <div class="analysis-box">
        <p style='font-size: 18px; color: #E0E0E0;'>{secilen_analiz}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🌍 Toplumsal Yansıma")
    st.write(f"İnsanların **%{secilen_oran}** kadarı seninle aynı seçimi yaptı.")
    
    # Görsel İlerleme Çubuğu
    if st.session_state.choice == 0:
        st.progress(oran_a / 100)
        st.caption(f"{secenek_a} (%{oran_a}) vs {secenek_b} (%{oran_b})")
    else:
        st.progress(oran_b / 100)
        st.caption(f"{secenek_b} (%{oran_b}) vs {secenek_a} (%{oran_a})")

    st.markdown("---")
    st.button("✨ Başka Bir İkilem Getir", on_click=next_question, type="primary", use_container_width=True)

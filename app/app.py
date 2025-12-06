import streamlit as st
import random
import time

# --- OYUN İÇERİĞİ (TELEPATİ SENARYOLARI) ---
# Buraya yüzlerce eğlenceli, absürt ve zorlayıcı başlık ekledik.
SENARYOLAR = [
    "Buzdolabında duran bozulmuş bir şey?",
    "Eski sevgiliye atılacak tek kelimelik mesaj?",
    "Zombi istilasında ilk ölecek kişi tipi?",
    "Polis seni çevirse bagajda bulacağı en saçma şey?",
    "Bir süper kahramanın en gereksiz süper gücü?",
    "Düğünde takılacak en kötü takı?",
    "Issız adaya düşsen yanına alacağın, hayatta kalmana yaramayacak bir eşya?",
    "Bir korku filminde asla girmemen gereken oda?",
    "İnsanların gizlice yaptığı iğrenç bir alışkanlık?",
    "Sadece zenginlerin yediği saçma bir yiyecek?",
    "Bir hayvan konuşabilseydi, hangisi en küfürbaz olurdu?",
    "Sevgilinin telefonunda görmemen gereken bir uygulama?",
    "Mezar taşına yazılacak komik bir söz?",
    "Uzaylılar gelse ilk kaçıracağı ünlü?",
    "Pizzanın üzerine konulabilecek en kötü malzeme?",
    "Bir öğretmenin derste söylemekten bıktığı cümle?",
    "Sadece Türkiye'de görebileceğin bir olay?",
    "Gece 3'te mutfakta yenen şey?",
    "Birinin yüzüne söylenmeyecek bir iltifat?",
    "Çocuğuna asla koymayacağın bir isim?",
    "Cehenneme gitsen çalacak şarkı?",
    "İnternet geçmişin silinmese açıklayamayacağın arama?",
    "En kötü hediye?",
    "Bir erkeğin/kadının en itici özelliği?",
    "Sarhoşken atılan mesajın konusu?",
    "Hayatın bir film olsa türü ne olurdu?",
    "En gereksiz icat?",
    "Bir vampir olsan kanını içmeyeceğin kişi?",
    "Asansörde yapılmayacak hareket?",
    "Patronuna söylemek isteyip söyleyemediğin şey?",
    "İlk buluşmada yapılmaması gereken bir hata?",
    "Diyeti bozduran yiyecek?",
    "Sihirli bir değneğin olsa yapacağın ilk saçmalık?",
    "Bir rock grubun olsa adı ne olurdu?",
    "Tuvalette kağıt bitse kullanacağın şey?",
    "En sinir bozucu ses?",
    "Bir renk söyle (Kırmızı ve Mavi hariç)?",
    "3 harfli bir hayvan?",
    "Babaannenin en çok kullandığı kelime?",
    "Yere düşse bile alıp yiyeceğin şey?",
    "Titanic batarken çalacak neşeli şarkı?",
] * 5 # Listeyi uzatmak için çoğaltıyoruz
random.shuffle(SENARYOLAR)

# --- ARAYÜZ VE MANTIK ---

# Sayfa Yapılandırması
st.set_page_config(page_title="Telepati Testi", page_icon="🧠", layout="centered")

# CSS ile Modern Tasarım
st.markdown("""
<style>
    .main-header {
        font-size: 40px; 
        font-weight: 800; 
        text-align: center; 
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    .card {
        background-color: #262730;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border: 2px solid #4B4B4B;
        margin-bottom: 20px;
    }
    .prompt-text {
        font-size: 28px;
        font-weight: bold;
        color: #ffffff;
        line-height: 1.4;
    }
    .score-box {
        font-size: 20px;
        font-weight: bold;
        color: #FFD700;
        text-align: center;
        padding: 10px;
        border: 1px dashed #FFD700;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    /* Butonları büyütme */
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Session State
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'rounds' not in st.session_state:
    st.session_state.rounds = 0
if 'current_prompt' not in st.session_state:
    st.session_state.current_prompt = None
if 'game_active' not in st.session_state:
    st.session_state.game_active = False

# Fonksiyonlar
def new_round():
    st.session_state.current_prompt = random.choice(SENARYOLAR)
    st.session_state.game_active = True

def result(match):
    st.session_state.rounds += 1
    if match:
        st.session_state.score += 1
        st.balloons()
    st.session_state.game_active = False
    st.rerun()

# --- OYUN GÖRÜNÜMÜ ---

st.markdown('<p class="main-header">🧠 AYNI FREKANS</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Aynı anda aynı cevabı verin!</p>", unsafe_allow_html=True)

# Skor Tablosu (Uyum Oranı)
if st.session_state.rounds > 0:
    uyum_orani = int((st.session_state.score / st.session_state.rounds) * 100)
    st.markdown(f'<div class="score-box">UYUM ORANI: %{uyum_orani} <br> ({st.session_state.score} / {st.session_state.rounds})</div>', unsafe_allow_html=True)
    st.progress(uyum_orani / 100)
else:
    st.markdown('<div class="score-box">HENÜZ BAŞLAMADI</div>', unsafe_allow_html=True)

# Oyun Alanı
if not st.session_state.game_active:
    # Başlat Butonu
    if st.button("🚀 FREKANSI YAKALA (BAŞLA)", type="primary"):
        new_round()
        st.rerun()
else:
    # Soru Kartı
    st.markdown(f"""
    <div class="card">
        <p style="color: #FF4B4B; font-weight: bold; font-size: 18px;">3 SANİYE İÇİNDE SÖYLE!</p>
        <p class="prompt-text">{st.session_state.current_prompt}</p>
    </div>
    """, unsafe_allow_html=True)

    # Geri Sayım Efekti (Metin olarak)
    st.info("💡 İPUCU: 3'ten geriye sesli sayın ve aynı anda bağırın!")

    # Sonuç Butonları
    col1, col2 = st.columns(2)
    with col1:
        st.button("✅ AYNI ŞEYİ DEDİK!", on_click=lambda: result(True), type="primary")
    with col2:
        st.button("❌ FARKLI ŞEYLER...", on_click=lambda: result(False))

# Sıfırlama
st.markdown("---")
if st.button("🔄 Skoru Sıfırla"):
    st.session_state.score = 0
    st.session_state.rounds = 0
    st.session_state.game_active = False
    st.rerun()

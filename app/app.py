import streamlit as st
import random
import time

# --- 1. AYARLAR VE SABİTLER ---

# Kelimeler (Türkçe anlamları) ve karşılık gelen HEX kodları
COLORS = {
    "KIRMIZI": "#FF0000",
    "MAVİ": "#0000FF",
    "YEŞİL": "#00AA00",
    "SARI": "#CCCC00",
    "MOR": "#800080",
    "TURUNCU": "#FF8C00"
}
COLOR_NAMES = list(COLORS.keys())
TOTAL_TIME = 60 # Saniye

# --- 2. CSS ve Görsel Ayarlar ---

def inject_custom_css():
    st.markdown("""
        <style>
        .stApp {
            background-color: #1a1a1a;
            color: #f0f0f0;
            text-align: center;
        }
        h1 {
            color: #00ffcc;
            font-size: 3em;
        }
        /* Oyundaki merkezi kelime için özel stil */
        .color-word {
            font-family: 'Arial Black', sans-serif;
            font-size: 70px !important;
            font-weight: 900;
            text-shadow: 2px 2px 5px rgba(0,0,0,0.5);
            margin: 50px 0;
            line-height: 1.2;
        }
        /* Buton stili */
        div.stButton > button {
            height: 80px;
            font-size: 24px;
            font-weight: bold;
        }
        .stSuccess {
            background-color: #00AA00;
            color: white;
            padding: 10px;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 3. OYUN MANTIĞI FONKSİYONLARI ---

def init_state():
    """Oyun durumunu başlatır/sıfırlar."""
    if 'game_running' not in st.session_state:
        st.session_state.game_running = False
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = 0
    if 'current_word' not in st.session_state:
        st.session_state.current_word = None
    if 'current_color' not in st.session_state:
        st.session_state.current_color = None
    if 'feedback' not in st.session_state:
        st.session_state.feedback = ""
    if 'correct_answer' not in st.session_state:
        st.session_state.correct_answer = None

def generate_puzzle():
    """Yeni bir kelime ve renk kombinasyonu oluşturur."""
    
    # 1. Kelimeyi rastgele seç (MAVİ, KIRMIZI, vb.)
    word = random.choice(COLOR_NAMES)
    
    # 2. Kelimenin gösterileceği rengi rastgele seç
    displayed_color_name = random.choice(COLOR_NAMES)
    hex_code = COLORS[displayed_color_name]
    
    # 3. Doğru cevabı belirle
    # Eşleşiyor: Kelimenin ANLAMI ile RENGİ aynı ise (örn: Yazı 'MAVİ', Renk MAVİ)
    is_match = (word == displayed_color_name)
    
    st.session_state.current_word = word
    st.session_state.current_color = hex_code
    st.session_state.correct_answer = "match" if is_match else "no_match"
    st.session_state.feedback = ""
    st.rerun()

def handle_answer(user_answer):
    """Kullanıcının cevabını kontrol eder ve skoru günceller."""
    
    # Oyuncunun cevabı doğru mu?
    is_correct = (user_answer == st.session_state.correct_answer)
    
    if is_correct:
        st.session_state.score += 1
        st.session_state.feedback = "✅ DOĞRU!"
    else:
        st.session_state.feedback = "❌ YANLIŞ!"
        # Yanlış cevapta puan düşürmeyerek daha motive edici yapalım.
    
    # Yeni bulmaca oluştur
    generate_puzzle()


# --- 4. ANA ARAYÜZ ---

def main_game():
    inject_custom_css()
    init_state()

    st.markdown("<h1>🧠 RENK FIRTINASI</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Hızlı karar ver, beynini test et!</h2>", unsafe_allow_html=True)

    if not st.session_state.game_running:
        st.markdown("""
        <div style="background-color: #222; padding: 20px; border-radius: 10px; margin-top: 30px;">
            <h3>OYUN KURALLARI</h3>
            <p>Ekranda beliren kelimeyi (örn: SARI) ve onun rengini (örn: Kırmızı) inceleyin.</p>
            <ul>
                <li><span style="color:#00ffcc; font-weight:bold;">Eşleşiyor</span> butonuna, kelimenin anlamı ile rengi AYNI ise basın.</li>
                <li><span style="color:#ff5555; font-weight:bold;">Eşleşmiyor</span> butonuna, kelimenin anlamı ile rengi FARKLI ise basın.</li>
            </ul>
            <p style="font-size: 1.2em; font-weight: bold;">Amaç: 60 saniyede en yüksek skoru yapmak!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("OYUNA BAŞLA (60 Saniye) 🚀", key="start_btn", type="primary", use_container_width=True):
            st.session_state.game_running = True
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            generate_puzzle() # İlk bulmacayı oluştur
            st.rerun()
        return

    # --- OYUN ÇALIŞIYOR ---
    
    elapsed_time = time.time() - st.session_state.start_time
    time_left = max(0, TOTAL_TIME - int(elapsed_time))

    if time_left == 0:
        st.session_state.game_running = False
        st.markdown(f"<h2>ZAMAN DOLDU! ⏱️</h2>")
        st.markdown(f"<h1>FİNAL SKORUN: {st.session_state.score}</h1>", unsafe_allow_html=True)
        if st.button("TEKRAR OYNA"):
            init_state() # Durumu sıfırla
            st.rerun()
        return
        
    # --- Skor ve Süre Gösterimi ---
    
    col1, col2, col3 = st.columns([1, 1, 1])
    col1.metric("SKOR", st.session_state.score)
    col2.metric("SÜRE", f"{time_left} s", delta_color="off")
    col3.metric("GERİ BİLDİRİM", st.session_state.feedback if st.session_state.feedback else "Hazır Ol")
    
    st.markdown("---")
    
    # --- Kelime Gösterimi ---
    
    if st.session_state.current_word:
        # Kelimeyi ve rengi merkezde göster
        st.markdown(
            f"<p class='color-word' style='color: {st.session_state.current_color};'>{st.session_state.current_word}</p>",
            unsafe_allow_html=True
        )
    
    # --- Cevap Butonları ---
    
    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        # Kırmızı butonu yanlış/olumsuz durumlar için kullanalım
        if st.button("EŞLEŞMİYOR ❌", key="no_match_btn", type="secondary", use_container_width=True):
            handle_answer("no_match")
            
    with btn_col2:
        # Yeşil butonu doğru/olumlu durumlar için kullanalım
        if st.button("EŞLEŞİYOR ✅", key="match_btn", type="primary", use_container_width=True):
            handle_answer("match")
    
    # Streamlit'i sürekli güncel tutmak için
    if st.session_state.game_running:
        time.sleep(0.1)
        st.rerun()


if __name__ == "__main__":
    main_game()

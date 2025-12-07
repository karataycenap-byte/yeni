import streamlit as st
import random
import time
from itertools import permutations

# --- 1. AYARLAR VE SABİTLER ---

CODE_LENGTH = 4   # Şifre hanesi
MAX_ATTEMPTS = 10 # Maksimum deneme hakkı

# --- 2. ŞİFRE MANTIĞI VE KONTROL FONKSİYONLARI ---

def generate_secret_code():
    """Benzersiz rakamlardan oluşan gizli şifreyi üretir."""
    # 0'dan 9'a kadar rakamları karıştır ve ilk CODE_LENGTH kadarını al
    digits = [str(i) for i in range(10)]
    random.shuffle(digits)
    return "".join(digits[:CODE_LENGTH])

def get_feedback(guess, secret):
    """Tahmine karşı 'Dahil' ve 'Konum' geri bildirimlerini hesaplar."""
    
    # 1. Dahil (Benzersiz rakamlar şifrede var mı?)
    included = 0
    for digit in guess:
        if digit in secret:
            included += 1
            
    # 2. Konum (Hem dahil hem de doğru pozisyonda mı?)
    position = 0
    for i in range(CODE_LENGTH):
        if guess[i] == secret[i]:
            position += 1
            
    return included, position

# --- 3. ARAYÜZ VE DURUM YÖNETİMİ ---

def init_state():
    """Oyun durumunu başlatır/sıfırlar."""
    
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False
    
    if 'secret_code' not in st.session_state:
        st.session_state.secret_code = generate_secret_code()
        
    if 'attempts_left' not in st.session_state:
        st.session_state.attempts_left = MAX_ATTEMPTS
        
    if 'history' not in st.session_state:
        st.session_state.history = [] # [(tahmin, dahil, konum), ...]
        
    if 'message' not in st.session_state:
        st.session_state.message = "Şifre Çözücü Hazır. İlk tahmini girin."

def start_game():
    """Yeni oyunu başlatır."""
    st.session_state.secret_code = generate_secret_code()
    st.session_state.attempts_left = MAX_ATTEMPTS
    st.session_state.history = []
    st.session_state.game_active = True
    st.session_state.message = "Yeni Şifre Oluşturuldu. Başlayın."
    st.rerun()

def handle_guess():
    """Kullanıcının tahminini işler."""
    
    guess = st.session_state.guess_input
    
    # Giriş Kontrolleri
    if not guess or len(guess) != CODE_LENGTH or not guess.isdigit():
        st.session_state.message = f"Hata: Lütfen {CODE_LENGTH} haneli sayısal bir giriş yapın."
        return

    if len(set(guess)) != CODE_LENGTH:
        st.session_state.message = "Hata: Rakamlar tekrarlanamaz."
        return

    # Geri Bildirimi Hesapla
    secret = st.session_state.secret_code
    included, position = get_feedback(guess, secret)
    
    # Tarihçeye Ekle
    st.session_state.history.append((guess, included, position))
    st.session_state.attempts_left -= 1
    
    # Kazanma Durumu
    if position == CODE_LENGTH:
        st.session_state.game_active = False
        st.session_state.message = f"✅ ŞİFRE ÇÖZÜLDÜ! ({secret}) {MAX_ATTEMPTS - st.session_state.attempts_left} denemede başarıldı."
        st.balloons()
    elif st.session_state.attempts_left == 0:
        st.session_state.game_active = False
        st.session_state.message = f"❌ DENEME HAKKI BİTTİ. Şifre: {secret}"
    else:
        st.session_state.message = "Geri bildirimi analiz edin ve yeni bir tahmin yapın."
    
    # Girişi temizle ve yeniden çiz
    st.session_state.guess_input = ""
    st.rerun()

# --- 4. ANA ARAYÜZ FONKSİYONU ---

def main_app():
    
    # CSS ve Başlık
    st.set_page_config(page_title="Sıralı Şifre Çözücü", layout="centered")
    st.markdown("<h1>🔐 Sıralı Şifre Çözücü (Sequential Decryption)</h1>", unsafe_allow_html=True)
    st.markdown("### Kısıtlı Optimizasyon ve Tümdengelim Oyunu")
    st.markdown("---")

    init_state()

    # Oyun Dışı Durum (Başlangıç veya Son)
    if not st.session_state.game_active:
        
        st.markdown(f"""
        <div style='background-color: #333; padding: 20px; border-radius: 10px;'>
            <h4>ANALİZ PROTOKOLÜ</h4>
            <p>Gizli {CODE_LENGTH} haneli (rakamları benzersiz) şifreyi en fazla {MAX_ATTEMPTS} denemede çözmelisiniz.</p>
            <p><b>Geri Bildirim Anahtarı:</b></p>
            <ul>
                <li><b>Dahil (Rakam):</b> Tahmininizdeki kaç rakam şifrede mevcuttur.</li>
                <li><b>Konum (Rakam):</b> Dahil olan rakamlardan kaç tanesi doğru yerdedir.</li>
            </ul>
            <p style='color: #00ffcc;'>{st.session_state.message}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔴 YENİ ŞİFRE OLUŞTUR / BAŞLA", type="primary", use_container_width=True):
            start_game()
        
        # Eğer oyun bitmişse, sonuç mesajını göster
        if st.session_state.history and 'ŞİFRE ÇÖZÜLDÜ' in st.session_state.message:
            st.success(st.session_state.message)
        elif st.session_state.history and 'DENEME HAKKI BİTTİ' in st.session_state.message:
            st.error(st.session_state.message)
        
        return

    # --- OYUN İÇİ DURUM ---
    
    st.markdown(f"**Kalan Deneme Hakkı:** `{st.session_state.attempts_left} / {MAX_ATTEMPTS}`")
    st.info(st.session_state.message)

    # Tahmin Girişi
    with st.form(key='guess_form', clear_on_submit=True):
        st.text_input(
            f"Tahmininizi Girin ({CODE_LENGTH} Benzersiz Rakam):",
            max_chars=CODE_LENGTH,
            key='guess_input'
        )
        st.form_submit_button("Tahmin Et ➡️", on_click=handle_guess, type="secondary")

    st.markdown("---")
    
    # Tarihçe ve Geri Bildirim Tablosu
    st.subheader("İşlem Kaydı (Feedback History)")
    
    if st.session_state.history:
        
        # Tabloyu ters çevirerek en yeni tahmini en üste getir
        history_reversed = st.session_state.history[::-1] 
        
        # Veri yapısını DataFrame'e uygun hale getir
        data = [{"Deneme": MAX_ATTEMPTS - st.session_state.attempts_left - i, 
                 "Tahmin": h[0], 
                 "Dahil": h[1], 
                 "Konum": h[2]} for i, h in enumerate(history_reversed)]
        
        st.dataframe(
            data,
            hide_index=True,
            column_order=("Deneme", "Tahmin", "Dahil", "Konum"),
            column_config={
                "Deneme": st.column_config.NumberColumn(format="%d"),
                "Tahmin": st.column_config.TextColumn(),
                "Dahil": st.column_config.NumberColumn("✅ Dahil", help="Doğru rakam sayısı"),
                "Konum": st.column_config.NumberColumn("📍 Konum", help="Doğru konumdaki rakam sayısı")
            }
        )
    else:
        st.caption("Henüz bir işlem yapılmadı.")

if __name__ == "__main__":
    main_app()

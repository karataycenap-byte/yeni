import streamlit as st
import random

# --- OYUN AYARLARI ---

KISILER = ["Sana", "Karşındakine", "İkiniz de"]

# (Önceki 100+ görevinizin listesi burada yer alıyor, tekrar yazmıyorum.)
GOREVLER_LISTESI = [
    ("30 saniye boyunca karşındakine bir 'superstar' gibi imza dağıt.", 1),
    ("Karşındakinin en sevdiği yemeği 5 saniye boyunca taklit et.", 1),
    ("Karşındakine içten bir iltifat et (aynı iltifat daha önce yapılmamış olmalı).", 2),
    ("Eğer bir film çekseydiniz, başlık, ana karakter ve konusu ne olurdu?", 3),
    ("Hayatında yaptığın ve şu an gülerek hatırladığın bir hatayı anlat.", 3),
    ("1 dakika boyunca karşıdakinin sana verdiği bir kelimeyi kullanmadan, bir konu hakkında konuş.", 2),
    ("En utanç verici anını kısaca, ama çok neşeli bir şekilde anlat.", 1),
] * 20 
random.shuffle(GOREVLER_LISTESI)

# --- OYUN MANTIĞI VE WEB ARAYÜZÜ (Streamlit) ---

# Session State (Veri Koruma)
if 'puanlar' not in st.session_state:
    st.session_state.puanlar = {"Oyuncu 1": 0, "Oyuncu 2": 0}
if 'sira' not in st.session_state:
    st.session_state.sira = 1
if 'gorev_aktif' not in st.session_state:
    st.session_state.gorev_aktif = False
if 'kullanilmis_gorevler_indeks' not in st.session_state:
    st.session_state.kullanilmis_gorevler_indeks = set()
if 'son_gorev_tuple' not in st.session_state:
    st.session_state.son_gorev_tuple = (None, 0)

def gorev_sonucu(basarili):
    """Görevi tamamlar, puanı ekler ve sırayı değiştirir."""
    puan_ekle = st.session_state.son_gorev_tuple[1] if basarili else 0
    oyuncu_key = f"Oyuncu {st.session_state.sira}"
    st.session_state.puanlar[oyuncu_key] += puan_ekle
    
    # Sıra değişimi ve sıfırlama
    st.session_state.sira = 3 - st.session_state.sira
    st.session_state.gorev_aktif = False
    
    st.rerun()

def zar_at():
    """Zar atar ve yeni görevi seçer."""
    
    if st.session_state.gorev_aktif:
        st.warning("Lütfen önce mevcut görevi tamamlayın!")
        return

    st.session_state.gorev_aktif = True
    
    # Kullanılmamış görev bulma mantığı
    kullanilmayan_gorev_indeksleri = [i for i in range(len(GOREVLER_LISTESI)) if i not in st.session_state.kullanilmis_gorevler_indeks]

    if not kullanilmayan_gorev_indeksleri:
        st.balloons()
        st.success("🎉 Tüm görevler tamamlandı! Oyun bitti!")
        return

    secilen_indeks = random.choice(kullanilmayan_gorev_indeksleri)
    st.session_state.kullanilmis_gorevler_indeks.add(secilen_indeks)
    
    secilen_gorev_tuple = GOREVLER_LISTESI[secilen_indeks]
    
    secilen_kisi = random.choice(KISILER)
    gorev_metni, gorev_puani = secilen_gorev_tuple
    st.session_state.son_gorev_tuple = secilen_gorev_tuple

    # GÖREVİ GÖSTEREN ESTETİK KISIM
    st.markdown("<br>", unsafe_allow_html=True) 
    
    # Kişi ve Puan Bilgisi (Daha Dikkat Çekici)
    if st.session_state.sira == 1:
        kisi_rengi = "#ff6b6b" # Parlak Kırmızı
        sira_rengi = "#e74c3c"
    else:
        kisi_rengi = "#4cd137" # Parlak Yeşil
        sira_rengi = "#2ecc71"
        
    st.markdown(f"""
    <div style='background-color: #34495e; padding: 10px; border-radius: 10px; border-left: 5px solid {sira_rengi};'>
        <p style='font-size: 16px; margin: 0; color: #ecf0f1;'>GÖREV PUANI: <span style='font-weight: bold; color: yellow;'>{gorev_puani}</span></p>
        <h4 style='color: {kisi_rengi}; margin: 5px 0 0 0;'>KİŞİ: {secilen_kisi}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Ana Görev Metni (Büyük ve Vurgulu)
    st.markdown(f"## 💥 {gorev_metni}", unsafe_allow_html=True)
    st.markdown("---")


# --- ARAYÜZ BAŞLANGICI VE STİL AYARLARI ---

# Sayfa ayarları (Koyu Tema ve Genişlik)
st.set_page_config(layout="wide", page_title="🌟 Eğlenceli Görev Zarı")

# Başlık ve Açıklama (Gradient ile)
st.markdown("""
<style>
    .big-title {
        font-size: 36px;
        font-weight: bold;
        color: #f1c40f; /* Altın Rengi */
        text-shadow: 2px 2px #34495e;
    }
    .stButton>button {
        height: 3em;
        font-weight: bold;
        font-size: 16px;
    }
</style>
<p class='big-title'>🌟 EĞLENCELİ GÖREV ZARI 🌟</p>
""", unsafe_allow_html=True)


# Puanlar Tablosu (Daha Estetik ve Emojili)
col1, col2 = st.columns(2)
col1.markdown(f"### 🔴 P1: **{st.session_state.puanlar['Oyuncu 1']}** Puan", unsafe_allow_html=True)
col2.markdown(f"### 🟢 P2: **{st.session_state.puanlar['Oyuncu 2']}** Puan", unsafe_allow_html=True)


# Sıra Bilgisi
sira_rengi = "#e74c3c" if st.session_state.sira == 1 else "#2ecc71"
st.markdown(f"""
<div style='text-align: center; padding: 10px; background-color: {sira_rengi}; border-radius: 10px; margin-bottom: 20px;'>
    <h3 style='color: white; margin: 0;'>➡️ SIRA: OYUNCU {st.session_state.sira}</h3>
</div>
""", unsafe_allow_html=True)


# Zar Atma Butonu veya Görev Kontrol Butonları
if not st.session_state.gorev_aktif:
    # Zar At butonu
    st.button(f"✨ ZAR AT & GÖREV BUL", on_click=zar_at, use_container_width=True, type="primary")
else:
    # Görev aktifken, görev detaylarını ve puanlama butonlarını göster
    zar_at() 

    col_basarili, col_basarisiz = st.columns(2)
    with col_basarili:
        st.button("✅ GÖREV BAŞARILI (+Puan)", on_click=lambda: gorev_sonucu(True), use_container_width=True, type="primary")
    with col_basarisiz:
        st.button("❌ GÖREV BAŞARISIZ (0 Puan)", on_click=lambda: gorev_sonucu(False), use_container_width=True, type="secondary")

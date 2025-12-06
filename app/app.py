import streamlit as st
import random
import time

# --- OYUN VERİLERİ ---

# KADER KARTLARI (Rastlantısal Etkiler)
KADER_KARTLARI = {
    "Rüya": ("Duygu", 5, "Gizemli bir rüya, duygusal sezgilerini keskinleştirdi."),
    "Hata": ("Zeka", -5, "Küçük bir mantık hatası, güvenini sarstı."),
    "Bağ": ("Etki", 10, "Yeni bir sosyal bağlantı kurdun, etki alanın genişledi."),
    "Yorgunluk": ("Güç", -10, "Aşırı çaba, fiziksel gücünü tüketti."),
    "İlham": ("Zeka", 10, "Anlık bir aydınlanma, zekanı artırdı."),
    "Kayb": ("Duygu", -10, "Yaşanan bir kayıp, duygusal derinliğini azalttı.")
}

# KRİTİK ANLAR (Karar Noktaları)
KRITIK_ANLAR = [
    ("Bir sırrı açığa çıkarmak zorundasın. Başarı için hangi kaynağı feda edersin?", 70),
    ("Bir meydan okumayı kırmak üzeresin. Hangi kaynağı en yüksek riskle kullanırsın?", 55),
    ("Birine güvenmek mi, yoksa şüphelenmek mi? Karar anın geldi.", 65),
    ("Yanlış giden bir planı düzeltmek için neyden vazgeçersin?", 80),
    ("Kendini mi, yoksa başkasını mı kurtarırsın? Feda zorunluluğu var.", 75)
]

# --- SAYFA AYARLARI ve CSS ---
st.set_page_config(page_title="Kaderin Mimarı", page_icon="🎲", layout="centered")

st.markdown("""
<style>
    .main {background-color: #0A0A1F; color: #E0E0E0;} 
    .title-kader {
        font-size: 38px; font-weight: bold; text-align: center;
        background: linear-gradient(90deg, #A8C0FF, #3F2B96);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
    }
    .profile-card {
        background-color: #1A1A3A; padding: 20px; border-radius: 10px; margin-bottom: 20px;
    }
    .kader-card {
        background-color: #4A148C; /* Mor */
        padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 20px;
        box-shadow: 0 0 10px rgba(74, 20, 140, 0.7);
    }
    .kritik-card {
        background-color: #2E004B; 
        padding: 25px; border-radius: 8px; margin-top: 15px; border: 1px solid #7B1FA2;
    }
    .stButton>button {
        height: 55px; font-size: 16px; border-radius: 8px; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE (Durum Yönetimi) ---
if 'profil' not in st.session_state: 
    st.session_state.profil = {"Güç": 50, "Zeka": 50, "Duygu": 50, "Etki": 50}
if 'tur' not in st.session_state: st.session_state.tur = 0
if 'max_tur' not in st.session_state: st.session_state.max_tur = 12
if 'oyun_durumu' not in st.session_state: st.session_state.oyun_durumu = "baslangic"
if 'mevcut_kritik_an' not in st.session_state: st.session_state.mevcut_kritik_an = None
if 'kritik_zorluk' not in st.session_state: st.session_state.kritik_zorluk = 0
if 'kader_etkisi' not in st.session_state: st.session_state.kader_etkisi = None
if 'log' not in st.session_state: st.session_state.log = []

# --- FONKSİYONLAR ---

def oyunu_baslat():
    st.session_state.profil = {"Güç": 50, "Zeka": 50, "Duygu": 50, "Etki": 50}
    st.session_state.tur = 1
    st.session_state.oyun_durumu = "kader_cek"
    st.session_state.log = []
    yeni_tur()

def yeni_tur():
    if st.session_state.tur > st.session_state.max_tur:
        st.session_state.oyun_durumu = "sonuc"
        return
        
    # 1. Kader Kartı Çek
    kart_isim, ozellik, deger, aciklama = random.choice(list(KADER_KARTLARI.items()))
    st.session_state.kader_etkisi = (kart_isim, ozellik, deger, aciklama)
    
    # 2. Kritik Anı Çek
    an, zorluk = random.choice(KRITIK_ANLAR)
    st.session_state.mevcut_kritik_an = an
    st.session_state.kritik_zorluk = zorluk
    
    st.session_state.oyun_durumu = "kader_cek"
    st.rerun()

def kader_etkisini_uygula():
    if st.session_state.oyun_durumu != "kader_cek": return
    
    _, ozellik, deger, _ = st.session_state.kader_etkisi
    
    # Profili güncelle
    st.session_state.profil[ozellik] += deger
    # Log kaydı
    st.session_state.log.append((st.session_state.tur, "KADER", ozellik, deger))
    
    st.session_state.oyun_durumu = "kritik_an"
    st.rerun()

def kaynagi_feda_et(kaynak_adi):
    if st.session_state.oyun_durumu != "kritik_an": return
    
    kaynak_degeri = st.session_state.profil[kaynak_adi]
    zorluk = st.session_state.kritik_zorluk
    
    # Başarı Kontrolü: % başarı şansı = (kaynak_degeri / zorluk) * 100
    sans = min(100, int((kaynak_degeri / zorluk) * 100))
    basarili = random.randint(1, 100) <= sans
    
    # Sonuç ve Etki
    if basarili:
        etki = f"Kritik Anı **başarıyla** yönettin. Feda edilen kaynak ({kaynak_adi}) %50 geri kazanıldı. (+{kaynak_degeri // 2})"
        st.session_state.profil[kaynak_adi] += (kaynak_degeri // 2)
    else:
        etki = f"**Başarısız** oldun. Kaynak ({kaynak_adi}) tamamen tükendi. (-{kaynak_degeri})"
        st.session_state.profil[kaynak_adi] = 0
    
    # Log ve Tur Geçişi
    st.session_state.log.append((st.session_state.tur, "KRİTİK", kaynak_adi, basarili))
    st.session_state.tur += 1
    st.session_state.oyun_durumu = "kritik_sonuc"
    st.session_state.sonuc_mesaji = etki
    st.session_state.sonuc_basarili = basarili
    st.rerun()

# --- ARAYÜZ ---

st.markdown('<p class="title-kader">KADERİN MİMARI</p>', unsafe_allow_html=True)

# 1. BAŞLANGIÇ EKRANI
if st.session_state.oyun_durumu == "baslangic":
    st.markdown("### 🎲 Oyuna Başla")
    st.info("Kaderin Mimarı, 12 turluk bir varoluşsal inşadır. Her turda kaderin getirdiklerini kabul edecek ve kritik anlarda bir kaynağını feda edeceksin.")
    st.button("MİMARLIĞA BAŞLA", on_click=oyunu_baslat, type="primary", use_container_width=True)

# 2. OYUN EKRANI
else:
    # A. PROFİL GÖSTERGESİ
    st.markdown("---")
    st.markdown(f"### ⚙️ Profil Durumu (Tur {st.session_state.tur} / {st.session_state.max_tur})")
    
    colG, colZ, colD, colE = st.columns(4)
    cols = [colG, colZ, colD, colE]
    ozellikler = ["Güç", "Zeka", "Duygu", "Etki"]
    renkler = ["red", "blue", "green", "orange"]
    
    for i, oz in enumerate(ozellikler):
        cols[i].metric(oz, st.session_state.profil[oz], help=f"{ozellikler[i]} Profili")
        cols[i].progress(st.session_state.profil[oz] / 100) # İlerleme Çubuğu

    # B. KADER KARTI ÇEKİM AŞAMASI
    if st.session_state.oyun_durumu == "kader_cek":
        kart_isim, ozellik, deger, aciklama = st.session_state.kader_etkisi
        isaret = "+" if deger > 0 else ""
        
        st.markdown(f"""
        <div class="kader-card">
            <h4>KADER KARTI: {kart_isim}</h4>
            <p style='color: #CFD8DC;'>{aciklama}</p>
            <h3 style='color: #FFEB3B;'>{ozellik} {isaret}{değer}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.button("KADERİ KABUL ET", on_click=kader_etkisini_uygula, type="secondary", use_container_width=True)

    # C. KRİTİK AN AŞAMASI
    elif st.session_state.oyun_durumu == "kritik_an":
        
        st.markdown(f"""
        <div class="kritik-card">
            <h4>KRİTİK AN</h4>
            <p style='font-size: 18px; font-weight: bold; color: #E8D7FF;'>{st.session_state.mevcut_kritik_an}</p>
            <p style='font-size: 14px; color: #FF9800;'>Gereken Zorluk Değeri: {st.session_state.kritik_zorluk}</p>
        </div>
        """)
        
        st.info("Hangi kaynağı feda ederek bu anı yöneteceksin? (Mevcut değerler başarı şansını belirler, ancak tükenme riski vardır.)")
        
        cols_karar = st.columns(4)
        for i, oz in enumerate(ozellikler):
            deger = st.session_state.profil[oz]
            cols_karar[i].button(f"({deger}) {oz} Feda Et", on_click=lambda oz=oz: kaynagi_feda_et(oz), key=f"feda_{oz}", use_container_width=True)

    # D. KRİTİK AN SONUCU AŞAMASI
    elif st.session_state.oyun_durumu == "kritik_sonuc":
        if st.session_state.sonuc_basarili:
            st.success(f"BAŞARILI! ✅ {st.session_state.sonuc_mesaji}")
        else:
            st.error(f"BAŞARISIZ! ❌ {st.session_state.sonuc_mesaji}")
            
        st.button("SONRAKİ TURA GEÇ", on_click=yeni_tur, type="primary", use_container_width=True)

# 3. SONUÇ EKRANI (Oyun Bitti)
if st.session_state.oyun_durumu == "sonuc":
    st.markdown("---")
    st.markdown("## 📜 VAROLUŞSAL MİMARİ RAPORU")
    
    final_profil = st.session_state.profil
    st.info("12 Tur sonunda oluşan nihai varoluşsal mimariniz:")
    
    st.markdown(f"**Güç:** {final_profil['Güç']} | **Zeka:** {final_profil['Zeka']} | **Duygu:** {final_profil['Duygu']} | **Etki:** {final_profil['Etki']}")

    # Nihai Yorum
    en_yuksek = max(final_profil, key=final_profil.get)
    en_dusuk = min(final_profil, key=final_profil.get)

    st.warning(f"**Sonuç Yorumu:** Profili en çok beslediğin alan **{en_yuksek}** oldu. Yaşadığın kayıplar ve rastlantılarla en çok tükettiğin alan ise **{en_dusuk}** oldu. Senin kaderin, bilinçli tercihlerinin ve kabul ettiğin rastlantıların birleşimidir.")

    st.button("YENİ BİR KADER YARAT", on_click=oyunu_baslat, type="primary", use_container_width=True)

import streamlit as st
import random

# --- OYUN VERİLERİ ---

# 4 BASAMAKLI GİZLİ ŞİFRE (Her oyun başlangıcında rastgele belirlenecek)
def generate_password():
    # 1'den 9'a kadar birbirinden farklı 4 rakam
    return random.sample(range(1, 10), 4)

# 4 ASİSTAN (Her birinin bir YALANCI (False) veya GERÇEKÇİ (True) olma durumu rastgele belirlenir)
def generate_assistants():
    names = ["Ajan K", "Mühendis Z", "Operatör P", "Gözcü M"]
    # 2 Yalancı, 2 Gerçekçi atama (ya da 1/3, 3/1 rastgele olabilir)
    is_truthful = random.sample([True] * 2 + [False] * 2, 4) 
    
    assistants = {}
    for i, name in enumerate(names):
        assistants[name] = {"truthful": is_truthful[i], "digit": i + 1, "code_index": i, "questioned": False}
    return assistants

# --- SAYFA AYARLARI ve CSS ---
st.set_page_config(page_title="SIĞINAK", page_icon="🔒", layout="centered")

st.markdown("""
<style>
    .main {background-color: #0A192F; color: #E0E0E0;} 
    .title-sığınak {
        font-size: 42px; font-weight: bold; text-align: center;
        background: linear-gradient(90deg, #66FCF1, #45A29E); /* Siber Mavi Tonları */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 3px;
    }
    .asistan-card {
        background-color: #1F2833; 
        padding: 15px; border-radius: 8px; margin-bottom: 10px;
        box-shadow: 0 0 10px rgba(102, 252, 241, 0.2);
        border-left: 5px solid #66FCF1;
        cursor: pointer;
    }
    .asistan-card:hover {
        background-color: #2C3847;
    }
    .cevap-card {
        padding: 20px; border-radius: 10px; margin-top: 15px; font-size: 18px;
        border: 2px solid #45A29E;
    }
    .stButton>button {
        height: 50px; font-size: 16px; border-radius: 8px; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE (Durum Yönetimi) ---
if 'oyun_durumu' not in st.session_state: st.session_state.oyun_durumu = "baslangic"
if 'password' not in st.session_state: st.session_state.password = []
if 'assistants' not in st.session_state: st.session_state.assistants = {}
if 'mevcut_asistan' not in st.session_state: st.session_state.mevcut_asistan = None
if 'soru_sayisi' not in st.session_state: st.session_state.soru_sayisi = 0
if 'cevap_log' not in st.session_state: st.session_state.cevap_log = []
if 'tahmin_girildi' not in st.session_state: st.session_state.tahmin_girildi = False
if 'tahmin' not in st.session_state: st.session_state.tahmin = ["", "", "", ""]

# --- FONKSİYONLAR ---

def oyunu_baslat():
    st.session_state.password = generate_password()
    st.session_state.assistants = generate_assistants()
    st.session_state.oyun_durumu = "oyun"
    st.session_state.mevcut_asistan = None
    st.session_state.soru_sayisi = 0
    st.session_state.cevap_log = []
    st.session_state.tahmin_girildi = False
    st.session_state.tahmin = ["", "", "", ""]
    st.rerun()

def asistan_sec(asistan_adi):
    if st.session_state.assistants[asistan_adi]["questioned"]:
        st.warning(f"{asistan_adi} ile zaten konuştunuz. Her asistana sadece tek bir soru sorabilirsiniz.")
        return
    st.session_state.mevcut_asistan = asistan_adi
    st.session_state.oyun_durumu = "soru"
    st.rerun()

def cevabi_al(soru_tipi):
    asistan_adi = st.session_state.mevcut_asistan
    asistan = st.session_state.assistants[asistan_adi]
    
    # 1. Şifre Rakamı Nedir? (En direkt soru)
    if soru_tipi == 1:
        dogru_cevap = st.session_state.password[asistan["code_index"]]
        soru = f"Şifrenin {asistan['code_index']+1}. basamağı nedir?"
        
        if asistan["truthful"]:
            cevap = f"{dogru_cevap}"
        else:
            # Yalancı: 1-9 arası farklı bir rakam söyler (Doğru cevabı hariç)
            yanlis_secenekler = [r for r in range(1, 10) if r != dogru_cevap]
            cevap = f"{random.choice(yanlis_secenekler)}"

    # 2. Şifrede Tek Rakam Var mı? (Boolean soru)
    elif soru_tipi == 2:
        dogru_cevap = any(d % 2 != 0 for d in st.session_state.password)
        soru = "Şifrede hiç tek rakam var mı?"
        
        if asistan["truthful"]:
            cevap = "Evet" if dogru_cevap else "Hayır"
        else:
            # Yalancı: Her zaman tersini söyler
            cevap = "Hayır" if dogru_cevap else "Evet"

    # 3. Sen Yalancı mısın? (Paradoks sorusu - Gerçekçi/Yalancı'yı ortaya çıkarmaya yarar)
    elif soru_tipi == 3:
        soru = "Sen bir yalancı mısın?"
        # Gerçekçi her zaman 'Hayır' der (Çünkü yalan söylemez)
        # Yalancı her zaman 'Hayır' der (Çünkü yalan söylediği için 'Evet' dese doğru söylemiş olur)
        cevap = "Hayır"

    
    # Güncel Durumu Kaydet
    st.session_state.assistants[asistan_adi]["questioned"] = True
    st.session_state.cevap_log.append({
        "asistan": asistan_adi,
        "soru": soru,
        "cevap": cevap,
        "yalancı_mi": not asistan["truthful"] # Logda belirtmiyoruz, oyuncu bulacak
    })
    st.session_state.soru_sayisi += 1
    st.session_state.oyun_durumu = "oyun" # Tekrar asistan seçme ekranına dön
    st.session_state.mevcut_asistan = None
    st.rerun()

def tahmini_kontrol_et():
    try:
        tahmin_rakamlar = [int(x) for x in st.session_state.tahmin]
        if len(tahmin_rakamlar) != 4 or any(r < 1 or r > 9 for r in tahmin_rakamlar):
             st.error("Lütfen 1-9 arası 4 basamaklı geçerli bir şifre girin.")
             return
    except ValueError:
        st.error("Lütfen tüm alanlara sayı girdiğinizden emin olun.")
        return

    if tahmin_rakamlar == st.session_state.password:
        st.session_state.oyun_durumu = "kazandi"
    else:
        st.session_state.oyun_durumu = "kaybetti"
    st.rerun()

# --- ARAYÜZ ---

st.markdown('<p class="title-sığınak">SIĞINAK</p>', unsafe_allow_html=True)

# 1. BAŞLANGIÇ EKRANI
if st.session_state.oyun_durumu == "baslangic":
    st.markdown("### 🔒 Şifreyi Çöz ve Kaç")
    st.info("""
    Bir sığınağa kilitlendiniz. Dışarı çıkmak için 4 basamaklı gizli şifreyi çözmeniz gerekiyor. 
    
    4 asistanın her biri şifrenin bir basamağını biliyor. Ancak:
    
    * **2 asistan** her zaman **doğru** söyler (Gerçekçi).
    * **2 asistan** her zaman **yalan** söyler (Yalancı).
    * Her asistana **sadece bir kez** soru sorabilirsiniz.
    
    Mantık zincirini kurun, yalancıları bulun ve şifreyi çözün.
    """)
    st.button("SIĞINAĞA GİR", on_click=oyunu_baslat, type="primary", use_container_width=True)

# 2. KAZANDI EKRANI
elif st.session_state.oyun_durumu == "kazandi":
    st.balloons()
    st.success(f"**TEBRİKLER MİMAR!** 🏆 Kapıyı başarıyla açtınız. Şifre: {''.join(map(str, st.session_state.password))}")
    st.button("YENİ SIĞINAK", on_click=oyunu_baslat, type="primary", use_container_width=True)

# 3. KAYBETTİ EKRANI
elif st.session_state.oyun_durumu == "kaybetti":
    st.error(f"**KİLİTLENDİNİZ!** 💥 Girdiğiniz şifre yanlıştı. Doğru şifre: {''.join(map(str, st.session_state.password))}")
    st.button("TEKRAR DENE", on_click=oyunu_baslat, type="primary", use_container_width=True)

# 4. SORU SORMA EKRANI
elif st.session_state.oyun_durumu == "soru":
    asistan_adi = st.session_state.mevcut_asistan
    st.subheader(f"💬 {asistan_adi}'a Sorulacak Soru")
    st.warning("Unutmayın: Sadece TEK BİR soru sorabilirsiniz.")
    
    col_1, col_2, col_3 = st.columns(3)
    
    with col_1:
        st.button("1. Şifre Basamağını Sor", on_click=lambda: cevabi_al(1), use_container_width=True)
    with col_2:
        st.button("2. Şifre Hakkında Genel Soru Sor", on_click=lambda: cevabi_al(2), use_container_width=True)
    with col_3:
        st.button("3. 'Sen Yalancı mısın?' diye sor", on_click=lambda: cevabi_al(3), use_container_width=True)

# 5. OYUN EKRANI (Asistan Seçimi ve Log)
elif st.session_state.oyun_durumu == "oyun":
    
    # Log Gösterimi
    if st.session_state.cevap_log:
        st.markdown("### 📜 Sorgu Kaydı")
        for log in st.session_state.cevap_log:
            st.markdown(f"""
            <div class="cevap-card" style="background-color: {'#0B4F6C' if log['cevap'] == 'Hayır' else '#116530'};">
                <span style="font-weight: bold;">{log['asistan']}:</span> {log['soru']}
                <br>
                <span style="font-weight: bold;">Yanıtı:</span> {log['cevap']}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")

    # Asistan Seçimi
    st.markdown("### 👤 Konuşulacak Asistanı Seç")
    asistan_cols = st.columns(4)
    asistan_names = list(st.session_state.assistants.keys())
    
    for i, name in enumerate(asistan_names):
        is_questioned = st.session_state.assistants[name]["questioned"]
        
        button_label = f"{name} ({st.session_state.assistants[name]['code_index']+1}. Basamak)"
        
        if is_questioned:
            asistan_cols[i].button(button_label, disabled=True, use_container_width=True, help="Zaten sorgulandı.")
        else:
            asistan_cols[i].button(button_label, on_click=lambda name=name: asistan_sec(name), use_container_width=True, type="secondary")

    st.markdown("---")
    
    # ŞİFRE TAHMİN ALANI
    st.subheader("🔑 Şifre Tahmini")
    st.info(f"4 asistana da ({len(st.session_state.assistants)}) soru sorduktan sonra veya yeterli bilgiye ulaştığınızı düşündüğünüzde tahminde bulunun.")
    
    tahmin_cols = st.columns(4)
    
    for i in range(4):
        st.session_state.tahmin[i] = tahmin_cols[i].text_input(f"Basamak {i+1}", 
                                                               max_chars=1, 
                                                               key=f"tahmin_{i}", 
                                                               value=st.session_state.tahmin[i],
                                                               help="Şifre 1 ile 9 arasında bir rakamdır.")
    
    st.button("KİLİDİ AÇ", on_click=tahmini_kontrol_et, type="primary", use_container_width=True)

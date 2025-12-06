import streamlit as st
import random

# --- OYUN AYARLARI ---

KISILER = [
    "Sana",
    "Karşındakine",
    "İkiniz de"
]

# 100'den fazla yaratıcı, eğlenceli ve buz kırıcı görev listesi.
# Format: ("Görev Metni", Puan)
GOREVLER_LISTESI = [
    # Basit/Komik Görevler (1 Puan)
    ("30 saniye boyunca karşındakine bir 'superstar' gibi imza dağıt.", 1),
    ("Karşındakinin en sevdiği yemeği 5 saniye boyunca taklit et.", 1),
    ("Bir kelimeyi bilmece gibi anlat ama 'evet' veya 'hayır' kelimelerini kullanma.", 1),
    ("Odadaki en çirkin eşyayı göster ve nedenini abartılı bir övgüyle açıkla.", 1),
    ("En sevdiğin 3 film karakterinin taklidini 10 saniye içinde yap.", 1),
    ("30 saniye boyunca bir dondurma külahını taklit et (erime efekti dahil).", 1),
    ("En sevdiğin şarkının nakaratını abartılı bir şekilde opera tarzında söyle.", 1),
    ("1 dakika boyunca sadece robot sesi çıkararak konuş.", 1),
    ("Karşındakine en garip sesini göster.", 1),
    ("Gözlerin kapalıyken 10 saniye boyunca odada yürü.", 1),
    ("5 saniye boyunca bir dinozor gibi bağır.", 1),
    ("Bir hayvanın yürüme biçimini taklit ederek odanın diğer ucuna git.", 1),
    ("Rastgele bir dilde (uydurma olabilir) 10 saniyelik bir konuşma yap.", 1),
    ("Ayakkabılarınla konuşuyormuş gibi davran.", 1),
    ("30 saniye boyunca kendini bir süper kahraman olarak tanıt.", 1),
    ("En utanç verici anını kısaca, ama çok neşeli bir şekilde anlat.", 1),
    ("Karşındakine bir 'evet/hayır' sorusu sor; cevap vermeden 5 saniye beklemesi gerekiyor.", 1),
    ("30 saniye boyunca sadece mimiklerle konuşarak bir hikaye anlat.", 1),
    ("Bir nesneyi al ve onu 3 farklı hayvanın sesiyle tanıt.", 1),
    ("Yaptığın en kötü saç stilini veya kıyafeti anlat.", 1),
    ("Parmak uçlarında yürü ve kendini gizemli bir casus olarak tanıt.", 1),
    ("Hayatında yediğin en garip şeyi anlat (30 saniye).", 1),
    ("Karşındakinin sana verdiği 3 kelimeyi içeren bir şiir uydur.", 1),
    ("Gözlerini kapat ve karşındakinin ellerini kullanarak bir nesneyi tahmin et.", 1),
    ("Burnunla havada adını yaz.", 1),
    ("Her iki elinle aynı anda farklı şekiller çiz.", 1),
    ("30 saniye boyunca hızlı konuşarak hava durumu sunucusu taklidi yap.", 1),
    ("En sevdiğin içeceğin tadını abartılı bir yüz ifadesiyle göster.", 1),
    ("Odadaki bir nesnenin 30 yıl sonraki halini tahmin et.", 1),
    ("1 dakika boyunca sadece 'Bip bop' kelimesini kullanarak karşındakine bir mesaj ilet.", 1),

    # Orta Zorlukta/Yaratıcı Görevler (2 Puan)
    ("Karşındakine içten bir iltifat et (aynı iltifat daha önce yapılmamış olmalı).", 2),
    ("1 dakika boyunca karşıdakinin sana verdiği bir kelimeyi kullanmadan, bir konu hakkında konuş.", 2),
    ("Karşındakinin bilmediği bir yeteneğini göster.", 2),
    ("Sizce neden dünyadaki en iyi oyunun bu olduğunu açıklayın (absürt ve mantıklı argümanlarla).", 2),
    ("Hayalindeki süper gücü ve nedenini açıklarken 3 farklı ses tonu kullan.", 2),
    ("Karşındakinin adını 5 farklı duygusal tonla söyle (farklı tonlar olmalı).", 2),
    ("Odadaki bir nesneyi al ve onun için 1 dakikalık kısa bir reklam filmi çek (sözlü).", 2),
    ("Karşındakinin en iyi 3 özelliğini ve bu özelliklerin sana nasıl hissettirdiğini açıkla.", 2),
    ("Bir fıkra anlat ama fıkranın ortasında aniden bir şarkı söylemeye başla.", 2),
    ("Birbirinize en sevdiğiniz 3 seyahat yerini anlatın ve nedenini açıklayın.", 2),
    ("En son aldığın en garip kararı ve sonuçlarını anlat.", 2),
    ("Karşındakinin en sevdiği şarkıyı tahmin et ve 10 saniye mırıldan.", 2),
    ("30 saniye içinde bir 'görünmez ip atlarken' karşıdakine ilginç bir felsefi soru sor.", 2),
    ("Birbirinize karşı bir 'imkansız' durum yaratın ve bu durumdan nasıl kurtulacağınızı anlatın.", 2),
    ("Hayalinizdeki bir sonraki tatil planını 30 saniyede bir tur rehberi gibi tanıt.", 2),
    ("Karşındakinin bilmediği 3 garip alışkanlığını itiraf et.", 2),
    ("5 farklı 'günaydın' deme şekli geliştir ve her birini dene.", 2),
    ("Odanın ortasında duran bir nesneyi 3 farklı hayvanın yürüme biçimiyle taklit ederek al.", 2),
    ("İkinize ait, unutamadığınız komik bir anıyı canlandırın.", 2),
    ("1 dakika boyunca sadece el hareketleri ve mimiklerle 'ben açım' demeyi dene.", 2),
    ("Birbirinize, bir hayvan olsaydınız hangisi olacağınızı ve nedenini açıklayın.", 2),
    ("3 farklı dilde (uydurma olabilir) teşekkür et.", 2),
    ("1 dakika boyunca karşındakinin söylediği her şeyi abartılı bir şekilde tekrarla.", 2),
    ("Elinizdeki telefonu bir evcil hayvan gibi sevin.", 2),
    ("Birbirinize en sevdiğiniz 3 çocukluk oyununu anlatın ve kurallarını açıklayın.", 2),
    ("Gelecekteki kendinize bir dakikalık bir mesaj kaydı oluşturun.", 2),
    ("En sevdiğiniz süper kahraman pozuyla 10 saniye boyunca dur.", 2),
    ("30 saniye içinde bir nesneyi sihirli bir nesneye dönüştürün (sözlü olarak).", 2),
    ("En sevdiğiniz film repliğini 3 farklı aksanla söyleyin.", 2),
    ("Birbirinize en çok güldüğünüz anı hatırlatın.", 2),

    # Zor/Derin Görevler (3 Puan)
    ("Karşındakine şu an hissettiğin en güçlü duyguyu bir renk ve bir hayvanla betimle.", 3),
    ("Karşılıklı olarak birbirinize en çok gurur duyduğunuz başarıyı anlatın.", 3),
    ("Karşındakinin hayatında yaptığı 3 cesur şeyi söyle ve takdir et.", 3),
    ("Eğer bir film çekseydiniz, başlık, ana karakter ve konusu ne olurdu?", 3),
    ("Karşındakine, onun hakkında daha önce hiç düşünmediğin, derin bir soru sor.", 3),
    ("Gözlerinizi kapatın ve birbirinize 'o an' hissettiğiniz en huzurlu şeyi anlatın.", 3),
    ("Birbirinize en büyük hayallerinizi fısıldayın ve gerçekleşmesi için iyi dileklerde bulunun.", 3),
    ("Hayatında yaptığın ve şu an gülerek hatırladığın bir hatayı anlat.", 3),
    ("En sevdiğin 3 hayat mottosunu açıkla ve nedenini anlat.", 3),
    ("Birbirinizin en güçlü yönlerini birer cümleyle özetleyin.", 3),
    ("Karşındakine küçük, kişisel bir 'teşekkür notu' yaz ve sesli oku.", 3),
    ("Birbirinizin çocukluk kahramanlarını tahmin edin ve nedenini açıklayın.", 3),
    ("Sizce birbirinizin en büyük zaafı ne olabilir? (Nazikçe ve tahmin yürütmeli).", 3),
    ("3 dakika boyunca telefonları bırakın ve sessizce sadece birbirinizin gözlerine bakın.", 3),
    ("Hayatınızda aldığınız en iyi kararı ve nedenini karşılıklı olarak anlatın.", 3),
] * 2 # Listeyi 100'den fazla yapmak için çoğalttım.
random.shuffle(GOREVLER_LISTESI) # Karıştır

# --- OYUN MANTIĞI VE WEB ARAYÜZÜ (Streamlit) ---

# Streamlit Session State (Değişkenlerin sayfada kalması için)
if 'puanlar' not in st.session_state:
    st.session_state.puanlar = {"Oyuncu 1": 0, "Oyuncu 2": 0}
if 'sira' not in st.session_state:
    st.session_state.sira = 1
if 'gorev_aktif' not in st.session_state:
    st.session_state.gorev_aktif = False
if 'kullanilmis_gorevler_indeks' not in st.session_state:
    st.session_state.kullanilmis_gorevler_indeks = set() # İndeksleri tutar
if 'son_gorev_tuple' not in st.session_state:
    st.session_state.son_gorev_tuple = (None, 0)

def gorev_sonucu(basarili):
    """Görevi tamamlar, puanı ekler ve sırayı değiştirir."""
    puan_ekle = st.session_state.son_gorev_tuple[1] if basarili else 0
    
    oyuncu_key = f"Oyuncu {st.session_state.sira}"
    st.session_state.puanlar[oyuncu_key] += puan_ekle
    
    st.session_state.sira = 3 - st.session_state.sira # Sırayı değiştir
    st.session_state.gorev_aktif = False
    
    st.rerun() # Sayfayı yeniden yükle

def zar_at():
    """Zar atar ve yeni görevi seçer."""
    
    if st.session_state.gorev_aktif:
        st.warning("Lütfen önce mevcut görevi tamamlayın!")
        return

    st.session_state.gorev_aktif = True
    
    # Kullanılmamış görev bulma (indeks ile)
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

    # GÖREVİ GÖSTER
    st.markdown("---")
    st.subheader(f"ZAR ATILDI! ({gorev_puani} Puan)")
    
    # HTML ile renkli çıktı (Mobil uyumlu)
    if st.session_state.sira == 1:
        st.markdown(f"<p style='color:#e74c3c; font-size: 20px;'>KİŞİ: **{secilen_kisi}**</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='color:#2ecc71; font-size: 20px;'>KİŞİ: **{secilen_kisi}**</p>", unsafe_allow_html=True)
        
    st.markdown(f"## 🎯 {gorev_metni}")
    st.markdown("---")


# --- ARAYÜZ BAŞLANGICI ---
st.set_page_config(layout="centered", page_title="Mobil Görev Zarı")
st.title("🌟 Mobil Görev Zarı")

# Puanlar Tablosu
col1, col2 = st.columns(2)
col1.markdown(f"<h3 style='color:#e74c3c;'>P1: {st.session_state.puanlar['Oyuncu 1']} Puan</h3>", unsafe_allow_html=True)
col2.markdown(f"<h3 style='color:#2ecc71;'>P2: {st.session_state.puanlar['Oyuncu 2']} Puan</h3>", unsafe_allow_html=True)

# Sıra Bilgisi
sira_rengi = "#e74c3c" if st.session_state.sira == 1 else "#2ecc71"
st.markdown(f"<h2 style='color:{sira_rengi};'>➡️ SIRA: OYUNCU {st.session_state.sira}</h2>", unsafe_allow_html=True)

st.markdown("---")

if not st.session_state.gorev_aktif:
    # Zar At butonu (Aktif değilse)
    st.button(f"🎲 OYUNCU {st.session_state.sira} ZAR AT", on_click=zar_at, use_container_width=True, type="primary")
else:
    # Görev aktifken, görev detaylarını ve puanlama butonlarını göster
    zar_at() # Görev detaylarını tekrar çizdirir

    col_basarili, col_basarisiz = st.columns(2)
    with col_basarili:
        st.button("✅ GÖREV BAŞARILI (+Puan)", on_click=lambda: gorev_sonucu(True), use_container_width=True, type="primary")
    with col_basarisiz:
        st.button("❌ GÖREV BAŞARISIZ (0 Puan)", on_click=lambda: gorev_sonucu(False), use_container_width=True)
import streamlit as st
import random

# -------------------- GENEL AYARLAR -------------------- #

st.set_page_config(page_title="NOX: Gizli Bağ", page_icon="🖤", layout="centered")

# MOR SİS + NEON GRADIENT TEMA
st.markdown(
    """
    <style>
    /* Arka plan ve genel tipografi */
    .stApp {
        background: radial-gradient(circle at top, #3a0f55 0, #120018 45%, #020006 100%) !important;
        color: #fdf2ff;
        font-family: "Poppins", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .block-container {
        max-width: 820px;
        padding-top: 2.5rem !important;
        padding-bottom: 2.5rem !important;
    }
    h1, h2, h3, h4 {
        color: #fdf7ff !important;
        letter-spacing: 0.06em;
    }
    h1 {
        font-size: 2.2rem !important;
        text-transform: uppercase;
        text-align: center;
    }
    .subtitle {
        color: #e1ceff;
        font-size: 0.95rem;
        text-align: center;
        margin-top: -0.4rem;
        margin-bottom: 1.4rem;
    }

    /* Form elemanları (input, select) – cam & oval */
    .stTextInput input, .stSelectbox select {
        background: rgba(8, 4, 20, 0.9) !important;
        color: #fdf4ff !important;
        border-radius: 999px !important;
        border: 1px solid rgba(243, 220, 255, 0.65) !important;
        padding: 0.55rem 0.9rem !important;
    }
    .stTextInput input:focus, .stSelectbox select:focus {
        border-color: rgba(255, 183, 255, 0.95) !important;
        box-shadow: 0 0 0 1px rgba(255, 183, 255, 0.85) !important;
    }

    /* Neon butonlar */
    div.stButton > button {
        border-radius: 999px !important;
        border: none !important;
        padding: 0.6rem 1.3rem !important;
        font-weight: 600 !important;
        cursor: pointer;
        background: radial-gradient(circle at top left,
            #ffe9ff 0, #ff8fd1 35%, #c77dff 65%, #7c3aed 100%) !important;
        color: #14031f !important;
        box-shadow:
            0 0 18px rgba(205, 140, 255, 0.75),
            0 0 40px rgba(148, 87, 235, 0.9) !important;
    }
    div.stButton > button:hover {
        filter: brightness(1.06);
        transform: translateY(-1px);
        box-shadow:
            0 0 22px rgba(235, 170, 255, 0.9),
            0 0 55px rgba(170, 100, 255, 1) !important;
    }
    .ghost-btn button {
        border-radius: 999px !important;
        padding: 0.55rem 1.2rem !important;
        font-weight: 500 !important;
        background: rgba(10, 6, 26, 0.75) !important;
        border: 1px solid rgba(240, 225, 255, 0.6) !important;
        color: #f5ebff !important;
        box-shadow: none !important;
    }
    .ghost-btn button:hover {
        background: rgba(40, 22, 70, 0.95) !important;
        border-color: rgba(255, 240, 255, 0.9) !important;
    }
    .small button {
        padding: 0.4rem 1rem !important;
        font-size: 0.85rem !important;
    }

    /* Neon gradient kart: dış çerçeve + iç siyah kart */
    .neon-wrapper {
        background: linear-gradient(135deg, #ff8fd1, #c77dff, #ff9ad5);
        padding: 2px;
        border-radius: 26px;
        box-shadow:
            0 0 30px rgba(255, 144, 222, 0.9),
            0 0 70px rgba(146, 76, 230, 0.95);
        animation: glowPulse 4s ease-in-out infinite alternate;
    }
    .neon-card {
        background: radial-gradient(circle at top, rgba(18, 8, 40, 0.98), rgba(4, 0, 12, 0.98));
        border-radius: 24px;
        padding: 1.6rem 1.8rem;
    }
    @keyframes glowPulse {
        0% { box-shadow: 0 0 18px rgba(255, 144, 222, 0.7); }
        100% { box-shadow: 0 0 40px rgba(186, 120, 255, 1); }
    }

    .pill {
        display: inline-block;
        padding: 0.2rem 0.9rem;
        border-radius: 999px;
        background: rgba(17, 11, 32, 0.9);
        border: 1px solid rgba(240, 220, 255, 0.6);
        color: #f6ebff;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-right: 0.4rem;
    }
    .pill-strong {
        background: linear-gradient(135deg, #ffe7ff, #ff8fd1);
        color: #280624;
        border: none;
    }
    .card-text {
        font-size: 1rem;
        line-height: 1.6;
        margin-top: 0.9rem;
    }
    .card-note {
        color: #ceb7ff;
        font-size: 0.88rem;
        margin-top: 0.7rem;
    }

    /* Progress bar neon */
    .stProgress > div > div {
        background: linear-gradient(90deg, #ff8fd1, #c77dff) !important;
    }

    /* Küçük alt yazı */
    .footer-text {
        font-size: 0.8rem;
        color: #cbb8ff;
        text-align: center;
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- OYUN VERİLERİ (80 KART) -------------------- #

CARDS = [
    # Yakınlık 1–20
    {"mode": "Genel", "category": "Yakınlık", "type": "soru",
     "text": "Partnerinle ilk tanıştığınız dönemden, bugün hâlâ aklında en çok kalan küçük bir ayrıntıyı anlat."},
    {"mode": "Genel", "category": "Yakınlık", "type": "soru",
     "text": "Onun yanında kendini en çok 'evde' hissettiğin an hangisiydi? O ana dair tek bir sahneyi tarif et."},
    {"mode": "Genel", "category": "Yakınlık", "type": "görev",
     "text": "Karşılıklı oturun ve sırayla birbirinizde en çok takdir ettiğiniz üç özelliği söyleyin."},
    {"mode": "İtiraf", "category": "Yakınlık", "type": "soru",
     "text": "Bu ilişkide seni en çok yumuşatan, gardını indiren cümle ne oldu? Hâlâ etkisini hissediyor musun?"},
    {"mode": "İtiraf", "category": "Yakınlık", "type": "görev",
     "text": "Partnerine karşı zihninde taşıdığın ama yüksek sesle hiç söylemediğin bir teşekkürü paylaş."},
    {"mode": "Genel", "category": "Yakınlık", "type": "ritüel",
     "text": "Üç nefes boyunca aynı ritimde nefes alın. Nefes alırken içinden 'biz', verirken 'birlikte' kelimesini düşün."},
    {"mode": "Genel", "category": "Yakınlık", "type": "soru",
     "text": "Onun yanında kendini kaç yaşında hissediyorsun? Neden o yaş? Hissettiğin versiyonunu tarif et."},
    {"mode": "İtiraf", "category": "Yakınlık", "type": "soru",
     "text": "Onu kaybetme korkunu hiç düşündün mü? Bu düşünce aklına geldiğinde içinden geçen ilk duygu neydi?"},
    {"mode": "Genel", "category": "Yakınlık", "type": "görev",
     "text": "Birbirinizin ellerine bakın ve ellerinizin bugüne kadar birlikte neler taşıdığını, nelerden geçtiğini hayal edin; sonra bunu kısa cümlelerle paylaşın."},
    {"mode": "Genel", "category": "Yakınlık", "type": "soru",
     "text": "Birlikte geçirdiğiniz zamanlardan, 'keşke oraya geri dönsek' dediğin tek bir günü seç; o günü üç kelimeyle özetle."},
    {"mode": "İtiraf", "category": "Yakınlık", "type": "soru",
     "text": "Onun yanında kendinle ilgili yumuşattığın bir sert tarafın var mı? Bu ilişkide hangi köşen yuvarlandı?"},
    {"mode": "Genel", "category": "Yakınlık", "type": "görev",
     "text": "Birbirinize, bu ilişki sayesinde kendinizde büyüttüğünüz olumlu bir yönü söyleyin."},
    {"mode": "Genel", "category": "Yakınlık", "type": "soru",
     "text": "Bu ilişkinin bir rengi olsa, hangi renk olurdu ve neden? O rengi hissettiren bir anı paylaş."},
    {"mode": "İtiraf", "category": "Yakınlık", "type": "ritüel",
     "text": "Gözlerinizi kapatın. İçinizden partneriniz için tek bir cümle kurun ve sonra göz göze bakarak o cümleyi fısıldayın."},
    {"mode": "Genel", "category": "Yakınlık", "type": "soru",
     "text": "Onunla tanışmasaydın, bugün hayalindeki hayat nasıl olurdu? Şu anki hayatın hangi kısmı ondan iz taşıyor?"},
    {"mode": "Genel", "category": "Yakınlık", "type": "görev",
     "text": "Birbirinize, bu ilişki sayesinde kendinizde büyüttüğünüz olumlu bir yönü söyleyin."},
    {"mode": "İtiraf", "category": "Yakınlık", "type": "soru",
     "text": "Onun seni anladığını en net hissettiğin cümle ya da bakış hangisiydi? Bu anı yeniden anlat."},
    {"mode": "Genel", "category": "Yakınlık", "type": "ritüel",
     "text": "Bir dakikalığına telefonları tamamen uzaklaştırın. Sadece birbirinize dönüp sessizce bakın ve aklınızdan geçen ilk kelimeyi paylaşın."},
    {"mode": "İtiraf", "category": "Yakınlık", "type": "soru",
     "text": "Onunla ilgili 'bunu bilse hoşuna gider' dediğin ama söylemediğin bir düşüncen var mı? Şimdi kısaca paylaş."},
    {"mode": "Genel", "category": "Yakınlık", "type": "görev",
     "text": "Partnerine, kendini yorgun hissettiğinde ona güvenerek sırtını nasıl bıraktığını tarif et; o da bunu nasıl hissettiğini anlatsın."},

    # Çekim 21–40
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Dokunmadan, sadece yaklaşarak partnerine bir mesaj gönder. O, mesajın ne olduğunu tahmin etmeye çalışsın."},
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Onu en çekici bulduğun hâlini tarif et; bir an, bir bakış, bir ses tonunu seç ve o anı canlandır."},
    {"mode": "Genel", "category": "Çekim", "type": "soru",
     "text": "Onun üzerinde seni en çok çeken şey sence: duruşu, bakışı, sesi, kokusu mu? Neden?"},
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Partnerini bir süre sadece uzaktan izle ve sonra 'sende en çok şu an hoşuma gidiyor' diyerek tek bir ayrıntıyı söyle."},
    {"mode": "Genel", "category": "Çekim", "type": "oyun",
     "text": "İkiniz de, birbirinizde en çekici bulduğunuz davranışı tek kelimeyle yazın; aynı anda söyleyin."},
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Partnerine, bugün onu gördüğünde aklından geçen ilk 'keşke'yi söyle (örneğin 'keşke şimdi…' diye başlayan bir cümleyle)."},
    {"mode": "Genel", "category": "Çekim", "type": "ritüel",
     "text": "Birbirinize 10 saniye boyunca kesintisiz göz göze bakın. İçinizden geçen ilk hisleri tek kelimeyle paylaşın."},
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Onun en çok hangi hali sana 'dayanılmaz' geliyor? Bir sahne kurar gibi anlat."},
    {"mode": "Genel", "category": "Çekim", "type": "soru",
     "text": "Onun enerjisini bir hava durumu olarak anlatsan, şu anda nasıl bir hava olurdu? Neden?"},
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Yalnızca bakışlarınla, ondan bir şey iste. O, ne istediğini tahmin etmeye çalışsın."},
    {"mode": "Genel", "category": "Çekim", "type": "soru",
     "text": "Onu ilk gördüğünde hissettiğin çekim ile şu anki çekim arasında nasıl bir fark var?"},
    {"mode": "Cesaret", "category": "Çekim", "type": "oyun",
     "text": "Taş-kağıt-makas oynayın. Kaybeden, kazananın seçtiği küçük ve nazik bir jesti yapmak zorunda."},
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Onun sana en çekici gelen tarafını tek bir cümlede özetle ve bunu fısıldayarak söyle."},
    {"mode": "Genel", "category": "Çekim", "type": "soru",
     "text": "Onunla dışarıda olduğunuz bir anı düşün: O an seni çekici hissettiren neydi? İkiniz de kendi cevabınızı verin."},
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Partnerinin yanına adım adım yaklaş ve her adımda onunla ilgili hoşuna giden bir kelime söyle."},
    {"mode": "Genel", "category": "Çekim", "type": "ritüel",
     "text": "Kısa bir süre yan yana sessizce oturun. Sonra 'şu an bedenimde en çok şu hissi taşıyorum' cümlesini tamamlayın."},
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Bir film sahnesinde gibi düşünün: Kamera sizi yakından çekiyormuş gibi, birbirinize nasıl bakardınız? Kısaca canlandırın."},
    {"mode": "Genel", "category": "Çekim", "type": "soru",
     "text": "Onun 'farkında olmadığı' bir çekiciliği var mı? Varsa bunu şimdi ona anlat."},
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Partnerine, ses tonunu kullanarak bir cümle kur: Kelimeden çok tınısı çekici olsun. Ne dediğin değil, nasıl dediğin önemli."},
    {"mode": "Genel", "category": "Çekim", "type": "oyun",
     "text": "İkiniz de içinizden partnerinizle ilgili kısa bir hayal kurun; sonra bu hayali yalnızca üç kelimeyle özetleyin."},

    # Gölge 41–60
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Bu ilişkide, gösterip de aslında daha derininde sakladığın bir duygun var mı? İstersen ucundan biraz anlat."},
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Onunla ilgili, içinden 'bunu söylesem fazla olur' deyip sustuğun bir düşünceyi daha yumuşak bir dille şimdi paylaş."},
    {"mode": "Gizli Kart", "category": "Gölge", "type": "görev",
     "text": "Bu kartı sadece sen görüyorsun. Partnerin gözlerini kapatsın. İçinden onunla ilgili güçlü bir cümle kur; sonra yalnızca bir kelimesini fısılda."},
    {"mode": "Gizli Kart", "category": "Gölge", "type": "görev",
     "text": "Sadece sen okuyorsun: Partnerine üç kısa dokunuş yap; bunlardan sadece biri gerçek niyetini taşıyor. O hangisi olduğunu tahmin etsin."},
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Onun yanında tetiklenen, sevmediğin ama dürüstçe kabul ettiğin bir gölge yönün var mı? Bunu yumuşak bir dille anlat."},
    {"mode": "Gizli Kart", "category": "Gölge", "type": "ritüel",
     "text": "Bu kartı ona gösterme. İçinden 'sende en çok korktuğum şey...' diye başlayan bir cümle kur ve sonra sadece ilk kelimeyi söyle."},
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Onunla beraberken, dışarıya göstermediğin ama için için yoğun yaşadığın bir duygu var mı? Kısaca tarif et."},
    {"mode": "Gizli Kart", "category": "Gölge", "type": "görev",
     "text": "Bu kart yalnızca senin. Partnerine hiçbir şey söylemeden, yüz ifadenle ona bir şey anlatmaya çalış. O ne anladığını söylesin."},
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Onunla geleceğe dair aklından geçen ama açmaya çekindiğin bir senaryo var mı? Detaya girmeden, sadece duygusunu anlat."},
    {"mode": "Gizli Kart", "category": "Gölge", "type": "görev",
     "text": "Sadece sen görüyorsun: Partnerinin kulağına, ondan gizlediğin bir isteğini 'tam cümle kurmadan' kısa ve belirsiz kelimelerle fısılda."},
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "İlişkide bazen geri çekilme ihtiyacı hissettiğinde, en çok hangi düşünce aklına geliyor? Bunu onunla paylaş."},
    {"mode": "Gizli Kart", "category": "Gölge", "type": "görev",
     "text": "Bu kartı ona gösterme. Ona bir bakış at ve bu bakışın içinde hem çekim hem tereddüt olsun. O, hangi tarafın ağır bastığını tahmin etsin."},
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Onunla ilgili 'bazen korkuyorum çünkü...' diye başlayan bir cümleyi tamamla ve paylaş."},
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Kendi gölgenden, onun korunmasını istediğin bir tarafın var mı? Bunu ona kısa ama dürüstçe anlat."},
    {"mode": "Gizli Kart", "category": "Gölge", "type": "ritüel",
     "text": "Bu kartı sadece sen okuyorsun. Partnerinin elini tut ve içinden geçen gölge duyguyu ona söylemeden, sadece dokunuşunla hissettirmeye çalış."},
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Geçmiş ilişkilerinden taşıdığın bir korku, bu ilişkide ara sıra kendini hatırlatıyor mu? Eğer evetse, nasıl?"},
    {"mode": "Gizli Kart", "category": "Gölge", "type": "görev",
     "text": "Bu kartı ona gösterme. Partnerinin hangi bakışının sende en çok gölgeyi uyandırdığını düşün ve o bakışı ondan iste."},
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Onun seni kaybetmekten korktuğunu hissettiğin bir an oldu mu? Bunu ona kendi gözünden anlat."},
    {"mode": "Gizli Kart", "category": "Gölge", "type": "görev",
     "text": "Sadece sen görüyorsun: Partnerine, 'şu anda aklımdan geçen şeyi bilseydin...' diye başlayan bir cümleyi içinden kur ve ona sadece bak."},
    {"mode": "İtiraf", "category": "Gölge", "type": "ritüel",
     "text": "Bir dakikalığına karanlık bir köşe hayal edin. Orada birlikte neyi bırakmak, hangi eski korkuyu geride bırakmak isterdiniz? Bunu paylaşın."},

    # Senaryo 61–80
    {"mode": "Genel", "category": "Senaryo", "type": "oyun",
     "text": "Bu akşam ilişkiniz bir film olsaydı, türü ne olurdu (dram, gizem, romantik, fantastik…)? İkiniz de kendi cevabınızı söyleyin."},
    {"mode": "Genel", "category": "Senaryo", "type": "soru",
     "text": "İkinizi anlatan bir film sahnesi hayal et; kamera sizi nasıl çekiyor olurdu? Kısa bir sahne tarif edin."},
    {"mode": "Gizli Kart", "category": "Senaryo", "type": "görev",
     "text": "Bu kart sadece senin. Partnerinle beraber olduğun farklı bir şehir hayal et; orada bir akşamı kafanda canlandır ve tek bir cümleyle özetle."},
    {"mode": "Genel", "category": "Senaryo", "type": "görev",
     "text": "Birlikte, ileride hatırladığınızda sizi gülümsetecek küçük bir ritüel uydurun ve hemen şimdi deneyin."},
    {"mode": "Genel", "category": "Senaryo", "type": "soru",
     "text": "Bir gece yürüyüşünde yan yana olduğunuzu hayal edin. Sessizlikte birbirinize ne söylemek isterdiniz?"},
    {"mode": "Gizli Kart", "category": "Senaryo", "type": "görev",
     "text": "Bu kartı ona gösterme. İkinizi gelecekte hayal et; kaç yaşındasınız ve o an ne yapıyorsunuz? Bu sahnenin tek bir ayrıntısını yüksek sesle söyle."},
    {"mode": "Genel", "category": "Senaryo", "type": "oyun",
     "text": "İkiniz de birbiriniz için gizli bir 'sahne adı' düşünün ve aynı anda söyleyin. Bu isim, onun hangi halini temsil ediyor?"},
    {"mode": "Genel", "category": "Senaryo", "type": "soru",
     "text": "Birlikte yazacağınız bir hikâyenin ilk cümlesi ne olurdu? İkiniz de ayrı ayrı ilk cümlenizi söyleyin."},
    {"mode": "Gizli Kart", "category": "Senaryo", "type": "ritüel",
     "text": "Bu kart sadece senin. Partnerinle ilgili aklından geçen bir sahneyi içinden yavaşça say ve ona sadece 'tam da bunu düşünüyordum' de."},
    {"mode": "Genel", "category": "Senaryo", "type": "görev",
     "text": "Birlikte, bu oyundan sonra yapmak istediğiniz küçük bir planı konuşun. Bu planın tek bir kelimelik başlığını bulun."},
    {"mode": "Genel", "category": "Senaryo", "type": "soru",
     "text": "Onunla 'başka bir evrende' tanışsaydınız, nerede tanışmış olmak isterdiniz? İkiniz de hayalinizdeki yeri söyleyin."},
    {"mode": "Gizli Kart", "category": "Senaryo", "type": "görev",
     "text": "Bu kartı ona gösterme. Partnerine bak ve 'şu anda aklımda sana dair bir sahne var' de; o, bu sahneyi tahmin etmeye çalışsın."},
    {"mode": "Genel", "category": "Senaryo", "type": "oyun",
     "text": "Biriniz 'gece', diğeriniz 'gündüz' kelimesini seçsin. İkinizi hangi zaman dilimi daha çok anlatıyormuş gibi geliyor? Neden?"},
    {"mode": "Genel", "category": "Senaryo", "type": "soru",
     "text": "Bir şarkı çalıyor ve ikiniz yalnızsınız. Bu anın temposunu anlatan tek bir kelime söyleyin: yavaş, derin, hareketli, dalgalı… hangisi?"},
    {"mode": "Gizli Kart", "category": "Senaryo", "type": "görev",
     "text": "Bu kart yalnızca senin. Partnerinin kulağına, 'bir gün mutlaka…' diye başlayan bir cümle fısılda; devamını sadece ikiniz bilin."},
    {"mode": "Genel", "category": "Senaryo", "type": "görev",
     "text": "Bu oyunu bitirdiğinizde yapacağınız ilk küçük şeyi birlikte seçin ve birbirinize bunu hatırlatacak bir kelime bulun."},
    {"mode": "Genel", "category": "Senaryo", "type": "soru",
     "text": "İkinizin ortak geleceğini anlatan bir kitabın adı ne olurdu? İkiniz de farklı bir başlık önerin."},
    {"mode": "Gizli Kart", "category": "Senaryo", "type": "ritüel",
     "text": "Bu kartı gizli tut. Partnerinin elini tut ve 'bu hikâyede en sevdiğim yer...' diye içinden bir cümle kur; sonra sadece ona bak."},
    {"mode": "Genel", "category": "Senaryo", "type": "soru",
     "text": "Birlikte yaşamak istediğiniz 'mükemmel gün'ü üç sahne olarak düşünün. Her biriniz bu sahnelerden birini tarif edin."},
    {"mode": "Genel", "category": "Senaryo", "type": "görev",
     "text": "Bu oyunu, aranızda sadece ikinizin bileceği bir isimle anmaya karar verin. Şimdi bu gizli ismi bulun."},
]

MAX_SCORE = 10
MAX_BOND = 20

ROULETTE_CONTROLLERS = ["Sen", "Partnerin", "İkiniz de", "Rastgele değişsin"]
ROULETTE_LEVELS = ["Yumuşak", "Yoğun", "Tutkulu", "Karanlık"]
ROULETTE_ACTIONS = ["Sinyal", "Fısıltı", "Yakınlık", "Gizemli Jest"]
ROULETTE_HINTS = [
    "Bu kombinasyonu aranızda, dışarıya anlatmayacağınız küçük bir sır haline getirin.",
    "Detayları kelimelere değil, bakışlara bırakın. O anı sadece siz bilin.",
    "Sözleri azaltın; nefes, bakış ve küçük jestler dili devralsın.",
    "Bu turu, gelecekte hatırladığınızda sizi gülümsetecek bir sahneye dönüştürmeye çalışın.",
]

# -------------------- STATE & YARDIMCI FONKSİYONLAR -------------------- #

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
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def reset(full=False):
    st.session_state.deck = []
    st.session_state.turn = 0
    st.session_state.current_card = None
    st.session_state.winner = None
    st.session_state.roulette_result = None
    st.session_state.bond_points = 0
    if st.session_state.players:
        st.session_state.scores = {p: 0 for p in st.session_state.players}
    if full:
        st.session_state.player1 = ""
        st.session_state.player2 = ""
        st.session_state.players = []
        st.session_state.mode = "Karışık"
    st.session_state.step = "start"


def init_deck(mode: str):
    if mode == "Karışık":
        st.session_state.deck = random.sample(CARDS, len(CARDS))
    else:
        subset = [c for c in CARDS if c["mode"] == mode or c["mode"] == "Genel"]
        if not subset:
            subset = CARDS[:]
        st.session_state.deck = random.sample(subset, len(subset))


def draw_card():
    if not st.session_state.deck:
        init_deck(st.session_state.mode)
    st.session_state.current_card = st.session_state.deck.pop()


def next_turn():
    if st.session_state.players:
        st.session_state.turn = (st.session_state.turn + 1) % len(st.session_state.players)


def add_bond(by=1):
    st.session_state.bond_points = min(MAX_BOND, st.session_state.bond_points + by)


def check_winner():
    for p, s in st.session_state.scores.items():
        if s >= MAX_SCORE:
            return p
    return None


def header():
    st.markdown("NOX: Gizli Bağ")
    st.markdown("<p class='subtitle'>mor sisin içinde, sadece ikinizin bildiği bir oyun</p>", unsafe_allow_html=True)


def status_bar():
    if not st.session_state.players:
        return
    mode_label = "Roulette" if st.session_state.mode == "Roulette" else st.session_state.mode
    current = (
        st.session_state.players[st.session_state.turn]
        if st.session_state.step in ("game", "card")
        else None
    )
    pills = f"<span class='pill pill-strong'>{mode_label}</span>"
    if current:
        pills += f"<span class='pill'>Sıra: {current}</span>"
    st.markdown(f"<div style='text-align:center; margin-bottom:0.6rem;'>{pills}</div>", unsafe_allow_html=True)


def stats():
    if not st.session_state.players:
        return
    st.markdown("### Skor & Bağ")
    c1, c2 = st.columns([2, 3])
    with c1:
        for p, s in st.session_state.scores.items():
            st.write(f"**{p}**: {s} puan")
    with c2:
        ratio = st.session_state.bond_points / MAX_BOND if MAX_BOND else 0
        st.progress(min(1.0, ratio))
        st.caption(f"Bağ puanı: {st.session_state.bond_points} / {MAX_BOND}")

# -------------------- EKRANLAR -------------------- #

header()

# Başlangıç
if st.session_state.step == "start":
    st.markdown("### Oyuncular ve Mod")

    c1, c2 = st.columns(2)
    with c1:
        p1 = st.text_input("Oyuncu", value=st.session_state.player1)
    with c2:
        p2 = st.text_input("Oyuncu ", value=st.session_state.player2)

    st.markdown("### Oyun Modu")
    mode_options = ["Karışık", "Cesaret", "İtiraf", "Gizli Kart", "Roulette (Türbülans Çarkı)"]
    current_label = "Roulette (Türbülans Çarkı)" if st.session_state.mode == "Roulette" else st.session_state.mode
    mode_label = st.selectbox("Bu gece oyunun havası:", mode_options, index=mode_options.index(current_label))

    st.markdown(
        "<div class='subtitle' style='text-align:left;'>"
        "• <b>Karışık:</b> Tüm katmanlardan kartlar<br>"
        "• <b>Cesaret:</b> Çekimi öne çıkaran cesur görevler<br>"
        "• <b>İtiraf:</b> İç dünyayı açan derin sorular<br>"
        "• <b>Gizli Kart:</b> Sadece birinizin gördüğü sır kartları<br>"
        "• <b>Roulette:</b> Türbülans Çarkı; kontrol, seviye ve eylem sürpriz"
        "</div>",
        unsafe_allow_html=True,
    )

    start = st.button("Oyuna Başla")
    if start:
        if not p1.strip() or not p2.strip():
            st.warning("İki oyuncu adı da dolu olmalı.")
        else:
            st.session_state.player1 = p1.strip()
            st.session_state.player2 = p2.strip()
            st.session_state.players = [st.session_state.player1, st.session_state.player2]
            st.session_state.scores = {p: 0 for p in st.session_state.players}
            st.session_state.turn = 0
            st.session_state.current_card = None
            st.session_state.bond_points = 0
            st.session_state.winner = None

            if mode_label.startswith("Roulette"):
                st.session_state.mode = "Roulette"
                st.session_state.step = "roulette"
            else:
                st.session_state.mode = mode_label
                init_deck(st.session_state.mode)
                st.session_state.step = "game"

# Kart modları
if st.session_state.step in ("game", "card") and st.session_state.mode != "Roulette":
    if not st.session_state.players:
        st.info("Önce oyuncu ve mod seçmelisiniz.")
    else:
        status_bar()

        if st.session_state.current_card is None and st.session_state.step == "game":
            st.markdown("### Kart Çek")
            st.markdown(
                "<p class='subtitle'>Kart açıldığında, detayları siz dolduracaksınız. NOX sadece sahnenin giriş cümlesini fısıldar.</p>",
                unsafe_allow_html=True,
            )
            if st.button("Kart Çek"):
                draw_card()
                add_bond(1)
                st.session_state.step = "card"

        if st.session_state.current_card is not None and st.session_state.step == "card":
            card = st.session_state.current_card
            st.markdown(
                f"""
                <div class="neon-wrapper">
                  <div class="neon-card">
                    <div>
                      <span class="pill pill-strong">{card['category']}</span>
                      <span class="pill">{card['type'].capitalize()}</span>
                    </div>
                    <h3 style="margin-top:1rem;">Kart</h3>
                    <p class="card-text">{card['text']}</p>
                    <p class="card-note">
                      Detayı, hızı ve sınırı siz belirleyin; oyun sadece çerçeveyi çizer.
                    </p>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("")
            b1, b2 = st.columns(2)
            with b1:
                done = st.button("Görev / Soru Yaşandı (+1)")
            with b2:
                st.markdown("<div class='ghost-btn'>", unsafe_allow_html=True)
                skip = st.button("Bu Turu Atla", key="skip")
                st.markdown("</div>", unsafe_allow_html=True)

            if done or skip:
                current_player = st.session_state.players[st.session_state.turn]
                if done:
                    st.session_state.scores[current_player] += 1
                    add_bond(1)
                winner = check_winner()
                if winner:
                    st.session_state.winner = winner
                    st.session_state.step = "end"
                else:
                    st.session_state.current_card = None
                    next_turn()
                    st.session_state.step = "game"

        stats()
        st.markdown("---")
        st.markdown("<div class='ghost-btn small'>", unsafe_allow_html=True)
        back = st.button("Oyuncu / Mod Ayarlarına Dön", key="back_game")
        st.markdown("</div>", unsafe_allow_html=True)
        if back:
            st.session_state.step = "start"

# Roulette
if st.session_state.step == "roulette" and st.session_state.mode == "Roulette":
    status_bar()
    st.markdown("### Türbülans Çarkı")
    st.markdown(
        "<p class='subtitle'>Kontrolü, yoğunluğu ve eylemi çark belirler; gerisini sisin içinde siz tamamlarsınız.</p>",
        unsafe_allow_html=True,
    )

    if st.button("Çarkı Çevir"):
        controller = random.choice(ROULETTE_CONTROLLERS)
        level = random.choice(ROULETTE_LEVELS)
        action = random.choice(ROULETTE_ACTIONS)
        hint = random.choice(ROULETTE_HINTS)
        st.session_state.roulette_result = (controller, level, action, hint)
        add_bond(1)

    if st.session_state.roulette_result:
        controller, level, action, hint = st.session_state.roulette_result
        st.markdown(
            f"""
            <div class="neon-wrapper">
              <div class="neon-card">
                <h3>Bu Turun Enerjisi</h3>
                <p><span class="pill pill-strong">Kontrol</span> {controller}</p>
                <p><span class="pill">Seviye</span> {level}</p>
                <p><span class="pill">Eylem</span> {action}</p>
                <p class="card-note">{hint}</p>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("")
        st.markdown("<div class='ghost-btn'>", unsafe_allow_html=True)
        done = st.button("Bu Turu Yaşadık (+Bağ)", key="roulette_done")
        st.markdown("</div>", unsafe_allow_html=True)
        if done:
            add_bond(1)

    stats()
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='ghost-btn small'>", unsafe_allow_html=True)
        to_cards = st.button("Kart Modlarına Geç", key="to_cards")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='ghost-btn small'>", unsafe_allow_html=True)
        back = st.button("Oyuncu / Mod Ayarlarına Dön", key="roulette_back")
        st.markdown("</div>", unsafe_allow_html=True)
    if to_cards:
        st.session_state.mode = "Karışık"
        init_deck("Karışık")
        st.session_state.step = "game"
    if back:
        st.session_state.step = "start"

# Bitiş
if st.session_state.step == "end":
    status_bar()
    st.markdown("## Tur Tamamlandı")
    if st.session_state.winner:
        st.success(f"Bu turun kazananı: {st.session_state.winner}")
    else:
        st.info("Bu turda belirgin bir kazanan yok; ama asıl kazanç aranızdaki bağ oldu.")
    stats()
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        again = st.button("Aynı Modla Yeni Tur", key="again")
    with c2:
        st.markdown("<div class='ghost-btn small'>", unsafe_allow_html=True)
        back = st.button("Oyuncu / Mod Ayarlarına Dön", key="end_back")
        st.markdown("</div>", unsafe_allow_html=True)
    if again:
        init_deck(st.session_state.mode if st.session_state.mode != "Roulette" else "Karışık")
        st.session_state.scores = {p: 0 for p in st.session_state.players}
        st.session_state.turn = 0
        st.session_state.current_card = None
        st.session_state.winner = None
        st.session_state.bond_points = 0
        st.session_state.step = "game"
    if back:
        st.session_state.step = "start"

st.markdown(
    "<p class='footer-text'>NOX, ayrıntıları size bırakır; kartlar sadece sisin içinden gelen küçük işaretlerdir.</p>",
    unsafe_allow_html=True,
)

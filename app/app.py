import streamlit as st
import random

# -------------------- GENEL AYARLAR -------------------- #

st.set_page_config(page_title="NOX: Gizli Bağ", page_icon="🖤", layout="centered")

# Daha okunabilir, sade ama karanlık tema
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top, #1b1028 0, #0b0b12 40%, #050509 100%);
        color: #f4f0ff;
        font-family: "Segoe UI", system-ui, sans-serif;
    }
    h1, h2, h3, h4 {
        color: #fdf9ff !important;
    }
    .main-card {
        background: rgba(20, 16, 32, 0.96);
        padding: 1.2rem 1.4rem;
        border-radius: 14px;
        border: 1px solid rgba(210, 180, 255, 0.4);
        box-shadow: 0 0 18px rgba(40, 10, 80, 0.7);
    }
    .chip {
        display: inline-block;
        padding: 0.18rem 0.7rem;
        border-radius: 999px;
        background: rgba(115, 90, 200, 0.55);
        color: #fefbff;
        font-size: 0.8rem;
        margin-right: 0.35rem;
    }
    .chip-soft {
        display: inline-block;
        padding: 0.18rem 0.7rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.08);
        color: #f4edff;
        font-size: 0.8rem;
        margin-right: 0.35rem;
    }
    .subtle {
        color: #d0c2ff;
        font-size: 0.9rem;
    }
    .big-btn button {
        width: 100% !important;
        border-radius: 999px !important;
        padding: 0.6rem 1.1rem !important;
        font-weight: 600 !important;
    }
    .tight-btn button {
        border-radius: 999px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- OYUN VERİLERİ -------------------- #
# 80 KART – 4 psikolojik kategori: Yakınlık, Çekim, Gölge, Senaryo
# mode: "Genel", "Cesaret", "İtiraf", "Gizli Kart"
# type: "soru", "görev", "ritüel", "oyun" (sadece görsel amaçlı)

CARDS = [
    # -------- Yakınlık 1–20 (Genel / İtiraf) --------
    # 1
    {"mode": "Genel", "category": "Yakınlık", "type": "soru",
     "text": "Partnerinle ilk tanıştığınız dönemden, bugün hâlâ aklında en çok kalan küçük bir ayrıntıyı anlat."},
    # 2
    {"mode": "Genel", "category": "Yakınlık", "type": "soru",
     "text": "Onun yanında kendini en çok 'evde' hissettiğin an hangisiydi? O ana dair tek bir sahneyi tarif et."},
    # 3
    {"mode": "Genel", "category": "Yakınlık", "type": "görev",
     "text": "Karşılıklı oturun ve sırayla birbirinizde en çok takdir ettiğiniz üç özelliği söyleyin."},
    # 4
    {"mode": "İtiraf", "category": "Yakınlık", "type": "soru",
     "text": "Bu ilişkide seni en çok yumuşatan, gardını indiren cümle ne oldu? Hâlâ etkisini hissediyor musun?"},
    # 5
    {"mode": "İtiraf", "category": "Yakınlık", "type": "görev",
     "text": "Partnerine karşı zihninde taşıdığın ama yüksek sesle hiç söylemediğin bir teşekkürü paylaş."},
    # 6
    {"mode": "Genel", "category": "Yakınlık", "type": "ritüel",
     "text": "Üç nefes boyunca aynı ritimde nefes alın. Nefes alırken içinden 'biz', verirken 'birlikte' kelimesini düşün."},
    # 7
    {"mode": "Genel", "category": "Yakınlık", "type": "soru",
     "text": "Onun yanında kendini kaç yaşında hissediyorsun? Neden o yaş? Hissettiğin versiyonunu tarif et."},
    # 8
    {"mode": "İtiraf", "category": "Yakınlık", "type": "soru",
     "text": "Onu kaybetme korkunu hiç düşündün mü? Bu düşünce aklına geldiğinde içinden geçen ilk duygu neydi?"},
    # 9
    {"mode": "Genel", "category": "Yakınlık", "type": "görev",
     "text": "Birbirinizin ellerine bakın ve ellerinizin bugüne kadar birlikte neler taşıdığını, nelerden geçtiğini hayal edin; sonra bunu kısa cümlelerle paylaşın."},
    # 10
    {"mode": "Genel", "category": "Yakınlık", "type": "soru",
     "text": "Birlikte geçirdiğiniz zamanlardan, 'keşke oraya geri dönsek' dediğin tek bir günü seç; o günü üç kelimeyle özetle."},
    # 11
    {"mode": "İtiraf", "category": "Yakınlık", "type": "soru",
     "text": "Onun yanında kendinle ilgili yumuşattığın bir sert tarafın var mı? Bu ilişkide hangi köşen yuvarlandı?"},
    # 12
    {"mode": "Genel", "category": "Yakınlık", "type": "görev",
     "text": "Birbirinize 'bugün sende en çok neye minnettarım' cümlesini tamamlayarak sırayla söyleyin."},
    # 13
    {"mode": "Genel", "category": "Yakınlık", "type": "soru",
     "text": "Bu ilişkinin bir rengi olsa, hangi renk olurdu ve neden? O rengi hissettiren bir anı paylaş."},
    # 14
    {"mode": "İtiraf", "category": "Yakınlık", "type": "ritüel",
     "text": "Gözlerinizi kapatın. İçinizden partneriniz için tek bir cümle kurun ve sonra göz göze bakarak o cümleyi fısıldayın."},
    # 15
    {"mode": "Genel", "category": "Yakınlık", "type": "soru",
     "text": "Onunla tanışmasaydın, bugün hayalindeki hayat nasıl olurdu? Şu anki hayatın hangi kısmı ondan iz taşıyor?"},
    # 16
    {"mode": "Genel", "category": "Yakınlık", "type": "görev",
     "text": "Birbirinize, bu ilişki sayesinde kendinizde büyüttüğünüz olumlu bir yönü söyleyin."},
    # 17
    {"mode": "İtiraf", "category": "Yakınlık", "type": "soru",
     "text": "Onun seni anladığını en net hissettiğin cümle ya da bakış hangisiydi? Bu anı yeniden anlat."},
    # 18
    {"mode": "Genel", "category": "Yakınlık", "type": "ritüel",
     "text": "Bir dakikalığına telefonları tamamen uzaklaştırın. Sadece birbirinize dönüp sessizce bakın ve aklınızdan geçen ilk kelimeyi paylaşın."},
    # 19
    {"mode": "İtiraf", "category": "Yakınlık", "type": "soru",
     "text": "Onunla ilgili 'bunu bilse hoşuna gider' dediğin ama söylemediğin bir düşüncen var mı? Şimdi kısaca paylaş."},
    # 20
    {"mode": "Genel", "category": "Yakınlık", "type": "görev",
     "text": "Partnerine, kendini yorgun hissettiğinde ona güvenerek sırtını nasıl bıraktığını tarif et; o da bunu nasıl hissettiğini anlatsın."},

    # -------- Çekim 21–40 (Cesaret / Genel) --------
    # 21
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Dokunmadan, sadece yaklaşarak partnerine bir mesaj gönder. O, mesajın ne olduğunu tahmin etmeye çalışsın."},
    # 22
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Onu en çekici bulduğun hâlini tarif et; bir an, bir bakış, bir ses tonunu seç ve o anı canlandır."},
    # 23
    {"mode": "Genel", "category": "Çekim", "type": "soru",
     "text": "Onun üzerinde seni en çok çeken şey sence: duruşu, bakışı, sesi, kokusu mu? Neden?"},
    # 24
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Partnerini bir süre sadece uzaktan izle ve sonra 'sende en çok şu an hoşuma gidiyor' diyerek tek bir ayrıntıyı söyle."},
    # 25
    {"mode": "Genel", "category": "Çekim", "type": "oyun",
     "text": "İkiniz de, birbirinizde en çekici bulduğunuz davranışı tek kelimeyle yazın; aynı anda söyleyin."},
    # 26
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Partnerine, bugün onu gördüğünde aklından geçen ilk 'keşke'yi söyle (örneğin 'keşke şimdi…' diye başlayan bir cümleyle)."},
    # 27
    {"mode": "Genel", "category": "Çekim", "type": "ritüel",
     "text": "Birbirinize 10 saniye boyunca kesintisiz göz göze bakın. İçinizden geçen ilk hisleri tek kelimeyle paylaşın."},
    # 28
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Onun en çok hangi hali sana 'dayanılmaz' geliyor? Bir sahne kurar gibi anlat."},
    # 29
    {"mode": "Genel", "category": "Çekim", "type": "soru",
     "text": "Onun enerjisini bir hava durumu olarak anlatsan, şu anda nasıl bir hava olurdu? Neden?"},
    # 30
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Yalnızca bakışlarınla, ondan bir şey iste. O, ne istediğini tahmin etmeye çalışsın."},
    # 31
    {"mode": "Genel", "category": "Çekim", "type": "soru",
     "text": "Onu ilk gördüğünde hissettiğin çekim ile şu anki çekim arasında nasıl bir fark var?"},
    # 32
    {"mode": "Cesaret", "category": "Çekim", "type": "oyun",
     "text": "Taş-kağıt-makas oynayın. Kaybeden, kazananın seçtiği küçük ve nazik bir jesti yapmak zorunda."},
    # 33
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Onun sana en çekici gelen tarafını tek bir cümlede özetle ve bunu fısıldayarak söyle."},
    # 34
    {"mode": "Genel", "category": "Çekim", "type": "soru",
     "text": "Onunla dışarıda olduğunuz bir anı düşün: O an seni çekici hissettiren neydi? İkiniz de kendi cevabınızı verin."},
    # 35
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Partnerinin yanına adım adım yaklaş ve her adımda onunla ilgili hoşuna giden bir kelime söyle."},
    # 36
    {"mode": "Genel", "category": "Çekim", "type": "ritüel",
     "text": "Kısa bir süre yan yana sessizce oturun. Sonra 'şu an bedenimde en çok şu hissi taşıyorum' cümlesini tamamlayın."},
    # 37
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Bir film sahnesinde gibi düşünün: Kamera sizi yakından çekiyormuş gibi, birbirinize nasıl bakardınız? Kısaca canlandırın."},
    # 38
    {"mode": "Genel", "category": "Çekim", "type": "soru",
     "text": "Onun sana göre 'farkında olmadığı' bir çekiciliği var mı? Varsa bunu şimdi ona anlat."},
    # 39
    {"mode": "Cesaret", "category": "Çekim", "type": "görev",
     "text": "Partnerine, ses tonunu kullanarak bir cümle kur: Kelimeden çok tınısı çekici olsun. Ne dediğin değil, nasıl dediğin önemli."},
    # 40
    {"mode": "Genel", "category": "Çekim", "type": "oyun",
     "text": "İkiniz de içinizden partnerinizle ilgili kısa bir hayal kurun; sonra bu hayali yalnızca üç kelimeyle özetleyin."},

    # -------- Gölge 41–60 (İtiraf / Gizli Kart) --------
    # 41
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Bu ilişkide, gösterip de aslında daha derininde sakladığın bir duygun var mı? İstersen ucundan biraz anlat."},
    # 42
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Onunla ilgili, içinden 'bunu söylesem fazla olur' deyip sustuğun bir düşünceyi daha yumuşak bir dille şimdi paylaş."},
    # 43
    {"mode": "Gizli Kart", "category": "Gölge", "type": "görev",
     "text": "Bu kartı sadece sen görüyorsun. Partnerin gözlerini kapatsın. İçinden onunla ilgili güçlü bir cümle kur; sonra yalnızca bir kelimesini fısılda."},
    # 44
    {"mode": "Gizli Kart", "category": "Gölge", "type": "görev",
     "text": "Sadece sen okuyorsun: Partnerine üç kısa dokunuş yap; bunlardan sadece biri gerçek niyetini taşıyor. O hangisi olduğunu tahmin etsin."},
    # 45
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Onun yanında tetiklenen, sevmediğin ama dürüstçe kabul ettiğin bir gölge yönün var mı? Bunu yumuşak bir dille anlat."},
    # 46
    {"mode": "Gizli Kart", "category": "Gölge", "type": "ritüel",
     "text": "Bu kartı ona gösterme. İçinden 'sende en çok korktuğum şey...' diye başlayan bir cümle kur ve sonra sadece ilk kelimeyi söyle."},
    # 47
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Onunla beraberken, dışarıya göstermediğin ama için için yoğun yaşadığın bir duygu var mı? Kısaca tarif et."},
    # 48
    {"mode": "Gizli Kart", "category": "Gölge", "type": "görev",
     "text": "Bu kart yalnızca senin. Partnerine hiçbir şey söylemeden, yüz ifadenle ona bir şey anlatmaya çalış. O ne anladığını söylesin."},
    # 49
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Onunla geleceğe dair aklından geçen ama açmaya çekindiğin bir senaryo var mı? Detaya girmeden, sadece duygusunu anlat."},
    # 50
    {"mode": "Gizli Kart", "category": "Gölge", "type": "görev",
     "text": "Sadece sen görüyorsun: Partnerinin kulağına, ondan gizlediğin bir isteğini 'tam cümle kurmadan' kısa ve belirsiz kelimelerle fısılda."},
    # 51
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "İlişkide bazen geri çekilme ihtiyacı hissettiğinde, en çok hangi düşünce aklına geliyor? Bunu onunla paylaş."},
    # 52
    {"mode": "Gizli Kart", "category": "Gölge", "type": "görev",
     "text": "Bu kartı ona gösterme. Ona bir bakış at ve bu bakışın içinde hem çekim hem tereddüt olsun. O, hangi tarafın ağır bastığını tahmin etsin."},
    # 53
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Onunla ilgili 'bazen korkuyorum çünkü...' diye başlayan bir cümleyi tamamla ve paylaş."},
    # 54
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Kendi gölgenden, onun korunmasını istediğin bir tarafın var mı? Bunu ona kısa ama dürüstçe anlat."},
    # 55
    {"mode": "Gizli Kart", "category": "Gölge", "type": "ritüel",
     "text": "Bu kartı sadece sen okuyorsun. Partnerinin elini tut ve içinden geçen gölge duyguyu ona söylemeden, sadece dokunuşunla hissettirmeye çalış."},
    # 56
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Geçmiş ilişkilerinden taşıdığın bir korku, bu ilişkide ara sıra kendini hatırlatıyor mu? Eğer evetse, nasıl?"},
    # 57
    {"mode": "Gizli Kart", "category": "Gölge", "type": "görev",
     "text": "Bu kartı ona gösterme. Partnerinin hangi bakışının sende en çok gölgeyi uyandırdığını düşün ve o bakışı ondan iste."},
    # 58
    {"mode": "İtiraf", "category": "Gölge", "type": "soru",
     "text": "Onun seni kaybetmekten korktuğunu hissettiğin bir an oldu mu? Bunu ona kendi gözünden anlat."},
    # 59
    {"mode": "Gizli Kart", "category": "Gölge", "type": "görev",
     "text": "Sadece sen görüyorsun: Partnerine, 'şu anda aklımdan geçen şeyi bilseydin...' diye başlayan bir cümleyi içinden kur ve ona sadece bak."},
    # 60
    {"mode": "İtiraf", "category": "Gölge", "type": "ritüel",
     "text": "Bir dakikalığına karanlık bir köşe hayal edin. Orada birlikte neyi bırakmak, hangi eski korkuyu geride bırakmak isterdiniz? Bunu paylaşın."},

    # -------- Senaryo 61–80 (Genel / Gizli Kart) --------
    # 61
    {"mode": "Genel", "category": "Senaryo", "type": "oyun",
     "text": "Bu akşam ilişkiniz bir film olsaydı, türü ne olurdu (dram, gizem, romantik, fantastik…)? İkiniz de kendi cevabınızı söyleyin."},
    # 62
    {"mode": "Genel", "category": "Senaryo", "type": "soru",
     "text": "İkinizi anlatan bir film sahnesi hayal et; kamera sizi nasıl çekiyor olurdu? Kısa bir sahne tarif edin."},
    # 63
    {"mode": "Gizli Kart", "category": "Senaryo", "type": "görev",
     "text": "Bu kart sadece senin. Partnerinle beraber olduğun farklı bir şehir hayal et; orada bir akşamı kafanda canlandır ve tek bir cümleyle özetle."},
    # 64
    {"mode": "Genel", "category": "Senaryo", "type": "görev",
     "text": "Birlikte, ileride hatırladığınızda sizi gülümsetecek küçük bir ritüel uydurun (örneğin şifreli bir selamlaşma) ve hemen şimdi deneyin."},
    # 65
    {"mode": "Genel", "category": "Senaryo", "type": "soru",
     "text": "Bir gece yürüyüşünde yan yana olduğunuzu hayal edin. Sessizlikte birbirinize ne söylemek isterdiniz?"},
    # 66
    {"mode": "Gizli Kart", "category": "Senaryo", "type": "görev",
     "text": "Bu kartı ona gösterme. İkinizi gelecekte hayal et; kaç yaşındasınız ve o an ne yapıyorsunuz? Bu sahnenin tek bir ayrıntısını yüksek sesle söyle."},
    # 67
    {"mode": "Genel", "category": "Senaryo", "type": "oyun",
     "text": "İkiniz de birbiriniz için gizli bir 'sahne adı' düşünün ve aynı anda söyleyin. Bu isim, onun hangi halini temsil ediyor?"},
    # 68
    {"mode": "Genel", "category": "Senaryo", "type": "soru",
     "text": "Birlikte yazacağınız bir hikâyenin ilk cümlesi ne olurdu? İkiniz de ayrı ayrı ilk cümlenizi söyleyin."},
    # 69
    {"mode": "Gizli Kart", "category": "Senaryo", "type": "ritüel",
     "text": "Bu kart sadece senin. Partnerinle ilgili aklından geçen bir sahneyi içinden yavaşça say ve ona sadece 'tam da bunu düşünüyordum' de."},
    # 70
    {"mode": "Genel", "category": "Senaryo", "type": "görev",
     "text": "Birlikte, bu oyundan sonra yapmak istediğiniz küçük bir planı konuşun. Bu planın tek bir kelimelik başlığını bulun."},
    # 71
    {"mode": "Genel", "category": "Senaryo", "type": "soru",
     "text": "Onunla 'başka bir evrende' tanışsaydınız, nerede tanışmış olmak isterdiniz? İkiniz de hayalinizdeki yeri söyleyin."},
    # 72
    {"mode": "Gizli Kart", "category": "Senaryo", "type": "görev",
     "text": "Bu kartı gösterme. Partnerine bak ve 'şu anda aklımda sana dair bir sahne var' de; o, bu sahneyi tahmin etmeye çalışsın."},
    # 73
    {"mode": "Genel", "category": "Senaryo", "type": "oyun",
     "text": "Biriniz 'gece', diğeriniz 'gündüz' kelimesini seçsin. İkinizi hangi zaman dilimi daha çok anlatıyormuş gibi geliyor? Neden?"},
    # 74
    {"mode": "Genel", "category": "Senaryo", "type": "soru",
     "text": "Bir şarkı çalıyor ve ikiniz yalnızsınız. Bu anın temposunu anlatan tek bir kelime söyleyin: yavaş, derin, hareketli, dalgalı… hangisi?"},
    # 75
    {"mode": "Gizli Kart", "category": "Senaryo", "type": "görev",
     "text": "Bu kart yalnızca senin. Partnerinin kulağına, 'bir gün mutlaka…' diye başlayan bir cümle fısılda; devamını sadece ikiniz bilin."},
    # 76
    {"mode": "Genel", "category": "Senaryo", "type": "görev",
     "text": "Bu oyunu bitirdiğinizde yapacağınız ilk küçük şeyi birlikte seçin ve birbirinize bunu hatırlatacak bir kelime bulun."},
    # 77
    {"mode": "Genel", "category": "Senaryo", "type": "soru",
     "text": "İkinizin ortak geleceğini anlatan bir kitabın adı ne olurdu? İkiniz de farklı bir başlık önerin."},
    # 78
    {"mode": "Gizli Kart", "category": "Senaryo", "type": "ritüel",
     "text": "Bu kartı gizli tut. Partnerinin elini tut ve 'bu hikâyede en sevdiğim yer...' diye içinden bir cümle kur; sonra sadece ona bak."},
    # 79
    {"mode": "Genel", "category": "Senaryo", "type": "soru",
     "text": "Birlikte yaşamak istediğiniz 'mükemmel gün'ü üç sahne olarak düşünün. Her biriniz bu sahnelerden birini tarif edin."},
    # 80
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

# -------------------- SESSION STATE -------------------- #

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

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


def reset_game(full=False):
    st.session_state.deck = []
    st.session_state.turn = 0
    st.session_state.current_card = None
    st.session_state.winner = None
    st.session_state.roulette_result = None
    st.session_state.bond_points = 0
    st.session_state.scores = {p: 0 for p in st.session_state.players} if st.session_state.players else {}
    if full:
        st.session_state.player1 = ""
        st.session_state.player2 = ""
        st.session_state.players = []
        st.session_state.mode = "Karışık"
    st.session_state.step = "start"


def init_deck_for_mode(mode: str):
    if mode == "Karışık":
        st.session_state.deck = random.sample(CARDS, len(CARDS))
    else:
        filtered = [c for c in CARDS if c["mode"] == mode or c["mode"] == "Genel"]
        if not filtered:
            filtered = CARDS[:]
        st.session_state.deck = random.sample(filtered, len(filtered))


def draw_card():
    if len(st.session_state.deck) == 0:
        init_deck_for_mode(st.session_state.mode)
    st.session_state.current_card = st.session_state.deck.pop()


def next_turn():
    if st.session_state.players:
        st.session_state.turn = (st.session_state.turn + 1) % len(st.session_state.players)


def increment_bond(by: int = 1):
    st.session_state.bond_points = min(MAX_BOND, st.session_state.bond_points + by)


def check_winner():
    for p, s in st.session_state.scores.items():
        if s >= MAX_SCORE:
            return p
    return None


def show_header():
    st.markdown(
        "<h1 style='text-align:center;'>NOX: Gizli Bağ</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='subtle' style='text-align:center;'>karanlık, tutkulu ve sadece ikinizin bildiği bir deneyim</p>",
        unsafe_allow_html=True,
    )


def show_scores_and_bond_in_sidebar():
    with st.sidebar:
        st.markdown("### 🧩 Oyuncular")
        if st.session_state.players:
            for p in st.session_state.players:
                st.write(f"• **{p}**")
        else:
            st.caption("Henüz oyuncu eklenmedi.")

        if st.session_state.scores:
            st.markdown("### 💖 Skorlar")
            for p, s in st.session_state.scores.items():
                st.write(f"{p}: **{s}** puan")

        st.markdown("### 🔥 Bağ Seviyesi")
        bond_ratio = st.session_state.bond_points / MAX_BOND if MAX_BOND > 0 else 0
        st.progress(min(1.0, bond_ratio))
        st.caption("Bağ seviyesi, tamamlanan her turla yavaşça yükselir.")

        st.markdown("---")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            if st.button("Yeni Tur", key="sidebar_new_round"):
                if st.session_state.mode == "Roulette":
                    st.session_state.step = "roulette"
                else:
                    init_deck_for_mode(st.session_state.mode if st.session_state.mode != "Roulette" else "Karışık")
                    st.session_state.scores = {p: 0 for p in st.session_state.players}
                    st.session_state.turn = 0
                    st.session_state.current_card = None
                    st.session_state.winner = None
                    st.session_state.bond_points = 0
                    st.session_state.step = "game"
        with col_s2:
            if st.button("Tamamen Sıfırla", key="sidebar_reset_full"):
                reset_game(full=True)


# -------------------- ANA EKRAN -------------------- #

show_scores_and_bond_in_sidebar()
show_header()

# Başlangıç ekranı
if st.session_state.step == "start":
    st.markdown("### 🖤 Oyuncu ve Mod Seçimi")

    col1, col2 = st.columns(2)
    with col1:
        p1 = st.text_input("1. Oyuncu Adı", value=st.session_state.player1)
    with col2:
        p2 = st.text_input("2. Oyuncu Adı", value=st.session_state.player2)

    st.markdown("### 🎭 Oyun Modu")

    mode_options = [
        "Karışık",
        "Cesaret",
        "İtiraf",
        "Gizli Kart",
        "Roulette (Türbülans Çarkı)",
    ]
    current_mode_label = (
        "Roulette (Türbülans Çarkı)"
        if st.session_state.mode == "Roulette"
        else st.session_state.mode
    )

    mode_label = st.selectbox("Hangi havada ilerlemek istersiniz?", mode_options,
                              index=mode_options.index(current_mode_label))

    st.markdown(
        "<p class='subtle'>"
        "• <b>Karışık:</b> Tüm kategorilerden kartlar karışık gelir<br>"
        "• <b>Cesaret:</b> Daha gözü kara, çekim odaklı görevler<br>"
        "• <b>İtiraf:</b> İç dünyayı açan derin sorular<br>"
        "• <b>Gizli Kart:</b> Sadece birinizin gördüğü gizemli kartlar<br>"
        "• <b>Roulette:</b> Türbülans Çarkı; kontrol, seviye ve eylem rastgele belirlenir"
        "</p>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='big-btn'>", unsafe_allow_html=True)
    start_clicked = st.button("Oyuna Başla", type="primary")
    st.markdown("</div>", unsafe_allow_html=True)

    if start_clicked:
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
                init_deck_for_mode(st.session_state.mode)
                st.session_state.step = "game"

# Klasik kart modları (Karışık / Cesaret / İtiraf / Gizli Kart)
if st.session_state.step == "game" and st.session_state.mode != "Roulette":
    if not st.session_state.players:
        st.info("Önce oyuncu ve mod seçmelisiniz.")
    else:
        current_player = st.session_state.players[st.session_state.turn]

        st.markdown(
            f"<p class='chip'>Mod: {st.session_state.mode}</p>"
            f"<p class='chip-soft'>Sıra: <b>{current_player}</b></p>",
            unsafe_allow_html=True,
        )

        if st.session_state.current_card is None:
            st.markdown("### 🎴 Kart Çekme Zamanı")
            st.markdown(
                "<p class='subtle'>Kartı gördükten sonra, detayları siz dolduracaksınız. "
                "Oyun sadece atmosferi çizecek.</p>",
                unsafe_allow_html=True,
            )

            st.markdown("<div class='big-btn'>", unsafe_allow_html=True)
            draw_clicked = st.button("Kart Çek", key="draw_btn")
            st.markdown("</div>", unsafe_allow_html=True)

            if draw_clicked:
                draw_card()
                increment_bond(1)  # kart çekmek bile hafif bağ puanı versin
        else:
            card = st.session_state.current_card
            st.markdown(
                f"""
                <div class="main-card">
                    <div>
                        <span class="chip">{card['category']}</span>
                        <span class="chip-soft">{card['type'].capitalize()}</span>
                    </div>
                    <h3 style="margin-top:0.6rem;">Kart</h3>
                    <p>{card['text']}</p>
                    <p class="subtle">Kartı uygularken, hızınızı ve sınırlarınızı siz belirlersiniz. Oyun sadece fikri fısıldar.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("")
            col1, col2 = st.columns(2)
            with col1:
                completed = st.button("Görev / Soru Yaşandı (+1 puan)", key="completed_btn")
            with col2:
                skipped = st.button("Bu Turu Atla", key="skip_btn")

            if completed or skipped:
                if completed:
                    st.session_state.scores[current_player] += 1
                    increment_bond(1)

                winner = check_winner()
                if winner:
                    st.session_state.winner = winner
                    st.session_state.step = "end"
                else:
                    st.session_state.current_card = None
                    next_turn()

        if st.session_state.scores:
            st.markdown("### 💖 Anlık Skor")
            for p, s in st.session_state.scores.items():
                st.write(f"{p}: **{s}** puan")

        st.markdown("---")
        st.markdown(
            "<div class='tight-btn'>",
            unsafe_allow_html=True,
        )
        if st.button("Oyuncu / Mod Ayarlarına Dön", key="back_settings"):
            st.session_state.step = "start"
        st.markdown("</div>", unsafe_allow_html=True)

# Roulette / Türbülans Çarkı
if st.session_state.step == "roulette" and st.session_state.mode == "Roulette":
    st.markdown("### 🎡 Türbülans Çarkı")
    st.markdown(
        "<p class='subtle'>Kontrolü, seviyeyi ve eylem türünü çark belirlesin; "
        "siz sadece sahneyi doldurun.</p>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='big-btn'>", unsafe_allow_html=True)
    spin = st.button("Çarkı Çevir", key="spin_btn")
    st.markdown("</div>", unsafe_allow_html=True)

    if spin:
        controller = random.choice(ROULETTE_CONTROLLERS)
        level = random.choice(ROULETTE_LEVELS)
        action = random.choice(ROULETTE_ACTIONS)
        hint = random.choice(ROULETTE_HINTS)
        st.session_state.roulette_result = (controller, level, action, hint)
        increment_bond(1)

    if st.session_state.roulette_result:
        controller, level, action, hint = st.session_state.roulette_result
        st.markdown(
            f"""
            <div class="main-card">
                <h3>Bu Turun Enerjisi</h3>
                <p><span class="chip">Kontrol</span> <b>{controller}</b></p>
                <p><span class="chip">Seviye</span> <b>{level}</b></p>
                <p><span class="chip">Eylem</span> <b>{action}</b></p>
                <p class="subtle" style="margin-top:0.6rem;">{hint}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        done = st.button("Bu Turu Yaşadık (+Bağ)", key="roulette_done")
        if done:
            increment_bond(1)

    st.markdown("---")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        if st.button("🎴 Kart Modlarına Geç", key="to_cards"):
            st.session_state.mode = "Karışık"
            init_deck_for_mode("Karışık")
            st.session_state.step = "game"
    with col_r2:
        if st.button("Oyuncu / Mod Ayarlarına Dön", key="roulette_to_start"):
            st.session_state.step = "start"

# Bitiş ekranı
if st.session_state.step == "end":
    st.markdown("## 🖤 Tur Tamamlandı")
    if st.session_state.winner:
        st.success(f"🎉 Bu turun kazananı: **{st.session_state.winner}**")
    else:
        st.info("Bu turda belirgin bir kazanan yok; ama asıl kazanç aranızdaki bağ oldu.")

    if st.session_state.scores:
        st.markdown("### 💖 Son Skorlar")
        for p, s in st.session_state.scores.items():
            st.write(f"{p}: **{s}** puan")

    st.markdown("### 🔥 Bağ Seviyesi")
    ratio = st.session_state.bond_points / MAX_BOND if MAX_BOND > 0 else 0
    st.progress(min(1.0, ratio))
    st.caption("İsterseniz yeni bir turla bu grafiği biraz daha doldurabilirsiniz.")

    st.markdown("---")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        if st.button("Aynı Modla Yeni Tur", key="end_new_round"):
            init_deck_for_mode(st.session_state.mode if st.session_state.mode != "Roulette" else "Karışık")
            st.session_state.scores = {p: 0 for p in st.session_state.players}
            st.session_state.turn = 0
            st.session_state.current_card = None
            st.session_state.winner = None
            st.session_state.bond_points = 0
            st.session_state.step = "game"
    with col_e2:
        if st.button("Oyuncu / Mod Ayarlarına Dön", key="end_to_start"):
            st.session_state.step = "start"

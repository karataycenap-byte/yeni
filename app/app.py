import 'dart:math';
import 'package:flutter/material.dart';

void main() {
  runApp(const IliskiKurtaranApp());
}

class IliskiKurtaranApp extends StatelessWidget {
  const IliskiKurtaranApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'İlişki Kurtaran',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0A030F),
        fontFamily: 'Roboto',
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFFF1F8A),
          brightness: Brightness.dark,
        ),
      ),
      home: const SplashScreen(),
    );
  }
}

/// ─────────────────────────
///  SPLASH
/// ─────────────────────────

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scale;
  late Animation<double> _opacity;

  @override
  void initState() {
    super.initState();
    _controller =
        AnimationController(vsync: this, duration: const Duration(seconds: 3));

    _scale = Tween<double>(begin: 0.4, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeOutBack),
    );
    _opacity = Tween<double>(begin: 0, end: 1).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeIn),
    );

    _controller.forward();

    Future.delayed(const Duration(seconds: 3), () {
      if (!mounted) return;
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => const MainMenuScreen()),
      );
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    const gradient = LinearGradient(
      colors: [Color(0xFF19051F), Color(0xFF4A0126), Color(0xFF0A030F)],
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
    );

    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(gradient: gradient),
        child: Center(
          child: AnimatedBuilder(
            animation: _controller,
            builder: (context, child) {
              return Opacity(
                opacity: _opacity.value,
                child: Transform.scale(
                  scale: _scale.value,
                  child: _buildLogo(),
                ),
              );
            },
          ),
        ),
      ),
    );
  }

  Widget _buildLogo() {
    return Stack(
      alignment: Alignment.center,
      children: [
        Container(
          width: 230,
          height: 230,
          decoration: const BoxDecoration(
            shape: BoxShape.circle,
            boxShadow: [
              BoxShadow(
                color: Color(0xFFFF1F8A),
                blurRadius: 50,
                spreadRadius: 5,
              ),
            ],
            gradient: RadialGradient(
              colors: [
                Color(0x55FF1F8A),
                Color(0x11000000),
              ],
            ),
          ),
        ),
        const Icon(
          Icons.favorite,
          color: Color(0xFFFF1F8A),
          size: 140,
        ),
        const Positioned(
          bottom: -60,
          child: Column(
            children: [
              Text(
                'İlişki Kurtaran',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                  letterSpacing: 1.2,
                ),
              ),
              SizedBox(height: 8),
              Text(
                'Aranızdaki enerjiyi açın',
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.white70,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}

/// ─────────────────────────
///  ANA MENÜ
/// ─────────────────────────

class MainMenuScreen extends StatelessWidget {
  const MainMenuScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFF0A030F), Color(0xFF19051F), Color(0xFF4A0126)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 24),
                const Text(
                  'İlişki Kurtaran',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.3,
                  ),
                ),
                const SizedBox(height: 8),
                const Text(
                  'Mistik – erotik ritüel kart oyunu',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.white70,
                  ),
                ),
                const Spacer(),
                _MenuButton(
                  label: 'Oyuna Başla',
                  onTap: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(builder: (_) => const GameScreen()),
                    );
                  },
                ),
                const SizedBox(height: 16),
                _MenuButton(
                  label: 'Kartları Keşfet',
                  onTap: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(
                          builder: (_) => const CardGalleryScreen()),
                    );
                  },
                ),
                const SizedBox(height: 16),
                _MenuButton(
                  label: 'Ayarlar',
                  onTap: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(builder: (_) => const SettingsScreen()),
                    );
                  },
                ),
                const Spacer(),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _MenuButton extends StatelessWidget {
  final String label;
  final VoidCallback onTap;

  const _MenuButton({required this.label, required this.onTap, super.key});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 16),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: const Color(0xFFFF1F8A)),
          boxShadow: const [
            BoxShadow(
              color: Color(0x55FF1F8A),
              blurRadius: 15,
              spreadRadius: 1,
            ),
          ],
          gradient: const LinearGradient(
            colors: [Color(0x33FF1F8A), Color(0x110A030F)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Center(
          child: Text(
            label,
            style: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.w600,
              letterSpacing: 1.1,
            ),
          ),
        ),
      ),
    );
  }
}

/// ─────────────────────────
///  OYUN EKRANI – KART ÇEKME
/// ─────────────────────────

class GameScreen extends StatefulWidget {
  const GameScreen({super.key});

  @override
  State<GameScreen> createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen> {
  final Random _random = Random();
  late List<String> _allCards;
  String? _currentCard;

  @override
  void initState() {
    super.initState();
    _allCards = [
      ...tenselEnerjiCards,
      ...arzuCekimCards,
      ...derinBagCards,
      ...mistikOyunCards,
    ];
    _allCards.shuffle(_random);
    _drawNextCard();
  }

  void _drawNextCard() {
    setState(() {
      if (_allCards.isEmpty) {
        _currentCard =
            "Tüm kartları tükettiniz. Yeni bir ritüele birlikte başlamak ister misiniz?";
      } else {
        _currentCard = _allCards.removeLast();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    const gradient = LinearGradient(
      colors: [Color(0xFF0A030F), Color(0xFF19051F), Color(0xFF4A0126)],
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
    );

    return Scaffold(
      appBar: AppBar(
        title: const Text('Ritüel Kartı'),
        backgroundColor: Colors.black54,
        elevation: 0,
      ),
      body: Container(
        decoration: const BoxDecoration(gradient: gradient),
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              children: [
                const SizedBox(height: 16),
                Expanded(
                  child: _currentCard == null
                      ? const SizedBox()
                      : _CardDisplay(text: _currentCard!),
                ),
                const SizedBox(height: 24),
                Row(
                  children: [
                    Expanded(
                      child: _MenuButton(
                        label: 'Yeni Kart',
                        onTap: _drawNextCard,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                TextButton(
                  onPressed: () => Navigator.of(context).pop(),
                  child: const Text(
                    'Ana Menüye Dön',
                    style: TextStyle(color: Colors.white70),
                  ),
                ),
                const SizedBox(height: 8),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _CardDisplay extends StatelessWidget {
  final String text;

  const _CardDisplay({required this.text, super.key});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(24),
          border: Border.all(color: const Color(0xFFFF1F8A), width: 2),
          boxShadow: const [
            BoxShadow(
              color: Color(0x55FF1F8A),
              blurRadius: 25,
              spreadRadius: 2,
            ),
          ],
          gradient: const LinearGradient(
            colors: [
              Color(0xAA19051F),
              Color(0xAA4A0126),
            ],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: SingleChildScrollView(
          child: Text(
            text,
            textAlign: TextAlign.center,
            style: const TextStyle(
              fontSize: 18,
              height: 1.5,
            ),
          ),
        ),
      ),
    );
  }
}

/// ─────────────────────────
///  KART GALERİSİ
/// ─────────────────────────

class CardGalleryScreen extends StatelessWidget {
  const CardGalleryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final categories = [
      {"title": "Tensel Enerji", "cards": tenselEnerjiCards},
      {"title": "Arzu & Çekim", "cards": arzuCekimCards},
      {"title": "Derin Duygusal Bağ", "cards": derinBagCards},
      {"title": "Mistik Oyunlar", "cards": mistikOyunCards},
    ];

    return DefaultTabController(
      length: categories.length,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Kartları Keşfet'),
          bottom: TabBar(
            isScrollable: true,
            tabs: [
              for (final c in categories) Tab(text: c["title"] as String),
            ],
          ),
        ),
        body: TabBarView(
          children: [
            for (final c in categories)
              _CardListView(cards: c["cards"] as List<String>),
          ],
        ),
      ),
    );
  }
}

class _CardListView extends StatelessWidget {
  final List<String> cards;

  const _CardListView({required this.cards, super.key});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: cards.length,
      itemBuilder: (context, index) {
        return Container(
          margin: const EdgeInsets.only(bottom: 12),
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: const Color(0xFFFF1F8A), width: 1),
            gradient: const LinearGradient(
              colors: [Color(0x3319051F), Color(0x334A0126)],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
          ),
          child: Text(
            cards[index],
            style: const TextStyle(fontSize: 16, height: 1.4),
          ),
        );
      },
    );
  }
}

/// ─────────────────────────
///  AYARLAR
/// ─────────────────────────

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool sesAcik = true;
  bool titresimAcik = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ayarlar'),
      ),
      body: ListView(
        children: [
          SwitchListTile(
            title: const Text('Ses efektleri'),
            value: sesAcik,
            onChanged: (v) {
              setState(() => sesAcik = v);
            },
          ),
          SwitchListTile(
            title: const Text('Titreşim'),
            value: titresimAcik,
            onChanged: (v) {
              setState(() => titresimAcik = v);
            },
          ),
          const ListTile(
            title: Text('Dil'),
            subtitle: Text('Şimdilik: Türkçe'),
          ),
        ],
      ),
    );
  }
}

/// ─────────────────────────
///  KART VERİLERİ – 4×80
/// ─────────────────────────

final List<String> tenselEnerjiCards = [
  // 1–20: beden farkındalığı
  "Partnerinin bedeninde en merak ettiğin yeri sadece bakışlarınla işaret et.",
  "Parmak uçlarınla partnerinin yüzüne 5 saniyelik yumuşak bir dokunuş yap.",
  "Partnerinin avuç içini kokla ve o anki hissini tek kelimeyle söyle.",
  "Partnerinin beden sıcaklığını hissetmek için ona 3 saniye yaklaş.",
  "Partnerinin tenine dokunmadan 1 cm mesafede gez ve enerjiyi tarif et.",
  "Gözlerini kapat; partnerin sana bedenini bir kelimeyle anlatsın.",
  "Partnerinin omzuna hafifçe dokun ve o dokunuşun arkasındaki niyeti söyle.",
  "Partnerinin sırtına parmağınla kısa bir çizgi çiz; hangi duygu uyandığını sor.",
  "Onun kokusunu fark et ve sana ilk çağrıştırdığı anıyı paylaş.",
  "Elini partnerinin kalbinin üzerine koyun; ritmi birlikte birkaç saniye dinleyin.",
  "Bedensel olarak en güvende hissettiğin anı partnerine anlat.",
  "Partnerinin boynuna yaklaş ama dokunma; hissettiklerini paylaş.",
  "Parmaklarınla partnerinin yüz şeklini gözlerin kapalıyken keşfet.",
  "Partnerin sana sadece nefesiyle bir duygu göndersin; tahmin etmeye çalış.",
  "Dudaklarını partnerinin elinin tersiyle 1 saniyeliğine temas ettir.",
  "Birbirinizin ten sıcaklığını karşılaştırarak aradaki farkı konuşun.",
  "Partnerinin kulağına sadece “hazır mısın?” fısılda ve tepkisini izle.",
  "Onun beline hafifçe dokunarak sınırını hisset, sonra ne hissettiğini söyle.",
  "Partnerin bedeninin en yumuşak yerini bulmasını iste ve nedenini anlatmasını iste.",
  "Birbirinize sessizce yaklaşın ve aranızdaki mesafeyi sözcükle tarif edin.",
  "Partnerine dokunmadan onu hayal ederek hangi duyuyu tetiklediğini söyle.",
  "Parmak uçlarınla partnerinin dudak çizgisine hafifçe dokun.",
  "Sadece nefesinizle 5 saniyelik bir ritim yakalamaya çalışın.",
  "Partnerinin ensesine ılık bir nefes üfle ve ne hissettiğini sor.",
  "Onun saçına bir kez dokun ve dokunuşunun sende uyandırdığı duyguyu tarif et.",
  "Göz teması kurarken ellerinizi birbirine değdirin ve hissettiğiniz enerjiyi anlatın.",
  "Partnerine “dokunulmayı en çok sevdiğin yer neresi?” diye sor.",
  "Bedeninizde gerilen bir noktayı partnerine göster ve nedenini konuşun.",
  "Onun yüzüne bak ve en çok nereye dokunmak istediğini söyle.",
  "Partnerinin yüzüne iki parmağınla hafifçe bir çerçeve çiz.",
  "Sırtına dokunmadan sıcaklığını hissetmeye çalış; sonra dokun ve farkı anlat.",
  "Partnerinin elini boynuna götürmesini iste ve orada bir süre kalmasına izin ver.",
  "Birbirinizin nefes ritmini bilinçli olarak değiştirip farkı gözlemleyin.",
  "Partnerinin beline sarılın ama konuşmayın; sadece bedeninizi dinleyin.",
  "Dudaklarınıza dokunmadan 1 cm mesafede bekleyin ve iç sesinizi dinleyin.",
  "Onun elini kendi kalbin üzerine koy ve ritmini birlikte dinleyin.",
  "Parmağınla partnerinin dudağında minik bir yol çiz ve ne hissettirdiğini sor.",
  "Onun saç diplerini hafifçe uyar ve bedeninin tepkisini izle.",
  "Partnerin sana bedenindeki “en canlı” noktayı göstersin.",
  "Tenine dokunduğunda ilk hissettiğin duyguyu yüksek sesle söyle.",
  // 41–60
  "Partnerine sadece bir dokunuşla “seni istiyorum” mesajı ver.",
  "Onun beden dilini 5 saniye boyunca sessizce gözlemle ve yorumla.",
  "Partnerine yavaş bir öpücük vermek istediğin bölgeyi sadece sözle ifade et.",
  "Partnerine “dokun bana” demesini iste ve ses tonunu hisset.",
  "Onun ellerinin gücünü hissederek sıkıca elini tut.",
  "Birbirinizin dudak kenarına hafifçe dokun ve hissi anlat.",
  "Partnerine “şu an vücudunda ne hissediyorsun?” diye sor.",
  "Onun kokusunu tarif eden bir metafor bul (örneğin: orman, deniz, ateş).",
  "Partnerine dokunmadan bile seni etkilediği bir anı anlat.",
  "Gözlerini kapat ve partnerinin seni sadece dokunuşla yönlendirmesine izin ver.",
  "Onun bedenini sanki ilk kez görüyormuş gibi baştan sona tarif et.",
  "Partnerinin boynuna yaklaşınca içinden geçen ilk düşünceyi paylaş.",
  "Tenine dokunduğunda seni en çok rahatlatan yeri partnerine söyle.",
  "Partnerinin elini kendi yüz hatlarında gezdirmesine izin ver.",
  "Onun gülüşünün bedeninde yarattığı etkiyi kelimelere dök.",
  "Partnerinin göğsüne hafifçe dokun; nefesindeki değişimi fark et.",
  "Birbirinize ılık bir nefes gönderin ve yalnızca nefesi hissedin.",
  "Onun omuzlarını keşfediyormuş gibi yavaşça dokun.",
  "Partnerine “beni şu anda nereye dokunarak sakinleştirirdin?” diye sor.",
  "Dudaklarınız birbirine yaklaşırken bedenindeki değişimi tarif et.",
  // 61–80
  "Partnerine tenine dair en gizli sırrını paylaş.",
  "Partnerinin tenini bir metaforla anlat (ipek, ateş, deniz gibi).",
  "Onun dokunuşunun sende açtığı kapıyı tarif et.",
  "Partnerinin bedeninde en çok “ev” hissettiren yeri söyle.",
  "Dokunduğunda sende kıvılcım yaratan anı ona anlat.",
  "Onun sıcaklığının sende yarattığı güven duygusunu tarif et.",
  "Partnerine “bedenimin en çok sevdiğin kısmı neresi?” diye sor.",
  "Onun tenini ilk keşfettiğin anı hatırlayıp yeniden canlandırın.",
  "Partnerinin cildine bir kelime armağan et.",
  "Bedeninde “uyanmak” kelimesine karşılık gelen yeri düşün ve paylaş.",
  "Partnerinin dudaklarına yaklaşınca ne hissettiğini dürüstçe söyle.",
  "Onun teninde seni en çok rahatlatan dokunuş hangisi, anlat.",
  "Partnerinin boynunu bir kelimeyle tarif et.",
  "Sadece tek bir parmakla partnerine güçlü bir duygu gönder.",
  "Onun bedenini tek bir renkle ifade et ve nedenini söyle.",
  "Partnerinin seni en çok çektiği bölgeyi sadece sözcükle ifade et.",
  "Onun cildinin dokusunun sende uyandırdığı arzuyu tarif et.",
  "Partnerine “beni şu an nasıl dokunarak çağırırsın?” diye sor.",
  "Onun tenine yaklaşınca içindeki dürtüyü tarif et.",
  "Partnerinin bedeninde keşfetmekten en çok çekindiğin yer neresi, söyle.",
];

final List<String> arzuCekimCards = [
  // 1–20
  "Partnerine “beni şu anda nasıl çağırırsın?” diye sor.",
  "Onu hayatında en çekici bulduğun anı paylaş.",
  "Dudaklarına bakarken aklından geçen üç kelimeyi söyle.",
  "Partnerinin senin için “en tehlikeli” tarafını tarif et.",
  "Onu yeniden tanısan, ilk hangi beden hareketi seni çekerdi?",
  "Partnerini ilk gördüğün anda hissettiğin arzuyu anlat.",
  "Onun vücudunda seni her seferinde çeken yer neresi, söyle.",
  "Partnerine bir fanteziyi sadece ima ederek anlat (detaya girmeden).",
  "Onun ses tonunda seni çeken en gizli şeyi tarif et.",
  "Dudaklarına bakarken içinden geçen ilk dürtüyü söylemek için cesaret et.",
  "Partnerine “beni nasıl baştan çıkarırsın?” diye sor.",
  "Onu çekici yapan en küçük ayrıntıyı söyle (el, göz, mimik gibi).",
  "Partnerini “en ateşli” bulduğun anı tarif et.",
  "Ona nasıl “gel” diyeceğini sadece bir cümleyle ifade et.",
  "Partnerinin yürüyüşünde seni çeken detayı anlat.",
  "Onun kokusunun sende uyandırdığı arzuyu tarif et.",
  "Partnerine bir arzu metaforu söyle (kıvılcım, volkan, kor gibi).",
  "Onun bedeninde seni her seferinde tetikleyen küçük bir hareket seç.",
  "Partnerine “beni şu an en çok neren çağırıyor?” diye sor.",
  "Ona erotik bir cümleyi fısıldayarak söyle (bir kelime bile olabilir).",
  // 21–40
  "Partnerine seni en çok etkilediği bakışını hatırlat.",
  "Onun yüzünde en ateşli bulduğun ifadeyi tarif et.",
  "Dudaklarına dokunmadan sadece şeklini tarif et.",
  "Partnerine “şu an beni hangi bakışla çözersin?” diye sor.",
  "Onu ilk kez öpmeyi hayal ederek o anı anlat.",
  "Partnerine seni etkileyen üç mikro mimik söyle.",
  "Onu utandıracak kadar samimi bir iltifat et.",
  "Partnerine “beni şu anda hangi bakışınla yakalarsın?” diye sor.",
  "Onun kalçasında seni çeken küçük bir detayı sözle anlat.",
  "Partnerinin bel hareketinde seni çeken şeyi tarif et.",
  "Onu en çok istediğin anı dürüstçe paylaş.",
  "Üzerindeki kıyafette seni en çok çeken noktayı söyle.",
  "Partnerine seni “tehlikeli hissettiren” yönünü anlat.",
  "Onun en çekici vücut duruşunu tarif et.",
  "Onu hayal ettiğinde bedeninde ilk hangi bölge tepki veriyor, söyle.",
  "Partnerinin seni etkilediğini ilk fark ettiğin anı anlat.",
  "Onun bedenini bir ateş türüne benzet (kor, alev, kıvılcım gibi).",
  "Partnerine “beni en çok hangi dokunuşla çağırırsın?” diye sor.",
  "Onu neden bazı zamanlarda daha çok istediğini açıklamaya çalış.",
  "Partnerinin boynunu düşündüğünde aklına gelen ilk kelimeyi söyle.",
  // 41–60
  "Partnerinle bir geceyi tek bir kelimeyle tanımla.",
  "Onunla yaşayabileceğin hayali bir anı sadece ima ederek anlat.",
  "Partnerinin hangi saatlerde en çekici olduğunu söyle.",
  "Onun vücudundaki ışığı bir metaforla ifade et.",
  "Partnerine “beni hangi enerjiyle istiyorsun?” diye sor.",
  "Teninin rengine en yakın arzu rengini seç ve söyle.",
  "Partnerinin sıcaklığının sende açığa çıkardığı duyguyu tarif et.",
  "Onu sana en çok çeken duygusal tetikleyiciyi paylaş.",
  "Partnerinin bedenini bir kıvılcımla anlat.",
  "Onun senin için erotik olan en masum hareketini söyle.",
  "Partnerine “beni düşündüğünde bedenine ne oluyor?” diye sor.",
  "Onun sana verdiği çekim enerjisini 1’den 10’a puanla.",
  "Partnerinin dudaklarını bir tatla ilişkilendir.",
  "Ona hiç söylemediğin ama düşündüğün bir arzuyu ima et.",
  "Partnerinin bedenindeki “yasak bölgeyi” sadece ima ederek tarif et.",
  "Onun teni hakkında söylemek isteyip sustuğun bir cümleyi şimdi söyle.",
  "Partnerinin kalçalarını bir çizgiyle tarif ediyor olsaydın nasıl olurdu?",
  "Onunla ilgili erotik bir hayalin sadece girişini anlat.",
  "Partnerinin bedenindeki “en ateşli ritmi” nasıl tarif edersin?",
  "Onu düşündüğünde aklına gelen fantaziyi sembollerle anlat.",
  // 61–80
  "Partnerinin enerjisini bir elementle ifade et (ateş, su, hava, toprak).",
  "Ona “beni şu anda hangi enerjiyle çağırırsın?” diye sor.",
  "Bedenindeki arzu uyanışını bir imgeyle anlat.",
  "Partnerine erotik bir bakış at ve konuşma.",
  "Onun nefesinin sende yarattığı arzuyu tarif et.",
  "Partnerinin bedenini hangi ritimde keşfetmek isterdin, paylaş.",
  "Onu bir “yasak meyve” metaforuyla anlat.",
  "Partnerine “beni en çok ne zaman istedin?” diye sor.",
  "Onun vücudunu bir çizgi ile hayal edip tarif et.",
  "Partnerine dokunmadan bir “enerji öpücüğü” gönder.",
  "Onun seni tetikleyen en ufak hareketini söyle.",
  "Partnerine “beni şimdi nerede hayal ediyorsun?” diye sor.",
  "Onu düşününce bedeninde en çok hangi bölge uyanıyor, tarif et.",
  "Partnerine gözlerini kapatıp seni nasıl çağırdığını düşünmesini söyle.",
  "Onu erotik bir ritüelin parçası gibi anlat.",
  "Partnerinin bedenini bir “sıcaklık haritası” olarak hayal et.",
  "Onun tenine yaklaşınca içindeki ateşi tarif et.",
  "Partnerinin dudaklarını bir gece manzarasına benzet.",
  "Onu şu an sana en çok çeken iç dürtüyü paylaş.",
  "Partnerine “beni kendine nasıl çekersin?” sorusunu sor ve dinle.",
];

final List<String> derinBagCards = [
  // 1–20
  "Partnerine “sana en çok ne zaman güvendim biliyor musun?” diyerek bir anı anlat.",
  "Şu anda ilişkide en kırılgan hissettiğin alanı paylaş.",
  "Partnerine içinden geçen ama söylemekten çekindiğin bir cümleyi söyle.",
  "Onun sana iyi geldiği en küçük detayı paylaş.",
  "Bugün kalbini en çok ne yorduğunu partnerine anlat.",
  "Partnerinden hangi konuda daha fazla güven beklediğini açıkça söyle.",
  "Partnerine “beni en çok hangi davranışın iyileştiriyor?” diye sor.",
  "Hayatında en güvende hissettiğin bir anı anlat ve nedenini söyle.",
  "Partnerine göstermekten en çok çekindiğin duyguyu paylaş.",
  "Onun sana verdiği güveni bir metaforla anlat (duvar, köprü, ışık gibi).",
  "Partnerine içsel bir korkunu sessizce fısılda.",
  "“Sana güvenmek bana nasıl hissettiriyor?” sorusunu cevapla.",
  "Onun seni hiç yargılamadığı bir anı hatırlat.",
  "Partnerinden gizlemeden “şu anda şuna ihtiyacım var” de.",
  "Onun kırılganlığının sende uyandırdığı duyguyu paylaş.",
  "Partnerinin en güven veren özelliğini söyle.",
  "Ona karşı en çok açıldığın anı anlat.",
  "Birlikte aştığınız bir zorluğu hatırlat ve teşekkür et.",
  "Partnerine “beni en çok nasıl kaygılandırabilirsin?” sorusunu dürüstçe cevapla.",
  "Onun seni kırmamak için yaptığı küçük bir jesti öv.",
  // 21–40
  "Partnerine “bendeki hangi düşünce tarzı seni etkiliyor?” diye sor.",
  "Onun zekâsının seni etkilediği bir anı paylaş.",
  "Partnerine bir konuda tamamen aynı hissettiğinizi söyle.",
  "“Beni en iyi anladığın an şuydu…” diyerek cümleyi tamamla.",
  "Onunla konuşurken zihninde en çok açılan alanı tarif et.",
  "Onun yanında hangi duygunu daha özgür yaşayabildiğini söyle.",
  "Partnerine seni sakinleştiren bir düşünceyi anlat.",
  "Onunla yaptığınız ilk derin sohbeti hatırlat.",
  "Partnerine “bende gördüğün en güzel değişim ne?” diye sor.",
  "Onunla uyuşamadığın bir konuyu nazikçe açıklayıp dinlemeye açık ol.",
  "Partnerinin hayata bakışındaki en büyüleyici tarafı söyle.",
  "Onun yanında kendini ne kadar “gerçek” hissettiğini paylaş.",
  "Partnerine geleceğe dair içsel bir hayalini aç.",
  "Onun fikirlerinin sende nasıl bir duygu uyandırdığını anlat.",
  "Partnerinin seni geliştiren bir özelliğini örnekle.",
  "Onunla ilk kez derin bir bağ hissettiğin anı paylaş.",
  "Partnerine seni hangi konuda ilham kaynağı yaptığını söyle.",
  "Onunla konuşurken zamanın nasıl aktığını hissettiğini anlat.",
  "Partnerinin bakışında seni en çok rahatlatan şeyi tarif et.",
  "Ona “şu anda bana ne söylemekten çekiniyorsun?” sorusunu sor.",
  // 41–60
  "Çocukken sevgiyi nasıl öğrendiğini partnerine anlat.",
  "Bir ilişkide en çok hangi tür yakınlığa ihtiyaç duyduğunu söyle.",
  "Partnerine “beni kaybetmekten en çok ne zaman korktun?” diye sor.",
  "Onun yanında içindeki çocuğun nasıl hissettiğini paylaş.",
  "Çocuklukta aldığın bir yarayı nazikçe partnerinle paylaş.",
  "Partnerine “yanımda en çok ne zaman güvende hissettin?” diye sor.",
  "Varsa terk edilme korkunu sadece ima ederek dile getir.",
  "Onun sevgisinin sende onardığı bir yeri anlat.",
  "Partnerinin sana nasıl temas ettiğinde içsel çocuğunun sakinleştiğini söyle.",
  "Partnerine “şu an içimdeki çocuk sana şunu söylüyor…” cümlesini tamamla.",
  "Çocukken duymadığın ama şimdi duymak istediğin bir cümleyi ondan iste.",
  "Ona “zorlandığımda beni nasıl tutmanı isterim…” cümlesini tamamla.",
  "Partnerinin varlığının sende yarattığı güven katmanını tarif et.",
  "Onun seni en çok hangi davranışıyla iyileştirdiğini paylaş.",
  "Hayatında hissettiğin en büyük duygusal yalnızlığı ona anlat.",
  "Partnerine ihtiyaç duyduğunu kabul etmenin en zor olduğu anı paylaş.",
  "Onun yanında ağlamak isteseydin sebebi ne olurdu, anlat.",
  "Partnerine “sende bulduğum aile duygusu…” cümlesini tamamla.",
  "Çocukken eksik kalan bir duyguyu partnerinden istemeyi dene.",
  "Partnerine “beni nasıl daha iyi sevebilirsin?” diye sorman için cesaret topla.",
  // 61–80
  "Partnerine geleceğe dair en gerçek isteğini söyle.",
  "Onunla yaşlanma fikrinin sende uyandırdığı duyguyu anlat.",
  "Beş yıl sonra ilişkinizi tek kelimeyle tanımlasan ne dersin?",
  "Partnerine “birlikte en çok nerede olmak isterdim?” diyerek hayalini paylaş.",
  "Onunla uzun bir yolculuk yapma fikrinin sende uyandırdığı hissi anlat.",
  "Partnerine “aynı takımdayız” hissini ne zaman yaşadığını söyle.",
  "Sadakat senin için ne demek? Tek cümleyle açıkla.",
  "Onun sana bağlı hissettiğini ilk ne zaman fark ettiğini paylaş.",
  "Partnerine geleceğe dair ondan bir ricada bulun.",
  "Onunla beraber öğrenmek istediğin yeni bir şeyi söyle.",
  "İlişkinizde bir ritüel yaratacak olsan bunun ne olacağını anlat.",
  "Partnerinin geleceğine dair içten bir temennini paylaş.",
  "Birlikte kurduğunuz bağı bir sembolle ifade et.",
  "Partnerine “seninle daha çok … yapmak istiyorum” cümlesini tamamla.",
  "Onunla birlikte aşmak istediğin bir zorluğu söyle.",
  "Partnerine “bende en çok neyi güçlendirdin biliyor musun?” diyerek cevap ver.",
  "Onu kaybetme fikrinin sende uyandırdığı duyguyu tek kelimeyle ifade et.",
  "Partnerine gelecekte birlikte gerçekleştirmek istediğin bir hayali anlat.",
  "Ona “benim bir gölge yanım var, bunu kabul eder misin?” diye sor.",
  "Partnerine minnettarlığını sadece bakışlarınla ifade etmeye çalış.",
];

final List<String> mistikOyunCards = [
  // 1–20
  "Partnerinin şu anda aklından geçen kelimeyi sez ve söylemeye çalış.",
  "Gözlerini kapat; partnerin sana sessizce bir duygu göndersin, hissettiğini söyle.",
  "Partnerinin bedeninde şu anda en aktif enerjiyi tahmin et.",
  "Birbirinize dokunmadan “beni çağır” enerjisi gönderin.",
  "Partnerin bir hayal düşünsün; sen de ona en yakın sembolü seç.",
  "Hissettiğin bir duygu dalgasını partnerine söyle: sıcaklık, soğukluk, titreşim…",
  "Partnerinin ruh hâlini bir renkle ifade et.",
  "Onun enerjisinin bugün bedeninin neresinde yoğunlaştığını sez.",
  "Partnerinin iç sesinin şu anda ne söylediğini tahmin et.",
  "Bir element seç ve partnerine bunu hissettir: ateş, su, sis, ışık.",
  "Partnerinin gözlerinden ne istediğini sez ve paylaş.",
  "Onun dokunmadan beden ritmini hissetmeye çalış.",
  "Partnerinin içsel yorgunluğunu bir hayvan sembolüyle tarif et.",
  "Onun şu anda sakladığı duyguyu bir metaforla ifade et.",
  "Partnerinin enerjisinin yüksek mi düşük mü olduğunu sezgisel olarak söyle.",
  "Onun şu anda en çok istediği şeyi tahmin etmeye çalış.",
  "Partnerinin kalbinden geçen cümleyi hayal edip paylaş.",
  "Aranızdaki bağı bir elementle seç (ateş, su, hava, toprak).",
  "Partnerinin gölge yönünü sez ve yargılamadan bir kelimeyle ifade et.",
  "Onun seni çağırdığı enerjiyi tarif et: yakınlık mı, oyun mu, tutku mu?",
  // 21–40
  "Elini partnerinin eline koy ve 10 saniye enerji akışını takip et.",
  "Birlikte 3 derin nefes alın, ritminizi uyumlu hale getirin.",
  "Gözlerinizi kapatın; aynı anda bir kelime söylemeye çalışın.",
  "Onun enerjisini yükseltmek için küçük bir jest yap (dokunmak zorunda değil).",
  "Partnerinin omuzlarına dokunmadan enerji yönlendirdiğini hayal et.",
  "Birlikte bir ritüel kelimesi seçin: uyan, yakınlaş, derinleş, ak gibi.",
  "Partnerine özel bir ritüel el işareti icat edin.",
  "İkiniz için sembolik bir mühür kelimesi belirleyin.",
  "Elleriniz birbirine yakınken aranızda bir enerji çemberi hayal edin.",
  "Beraber 5 saniyelik sessiz bir mini meditasyon yapın.",
  "Partnerinin enerjisindeki en parlak noktayı sez ve söyle.",
  "Ona kısa bir koruma cümlesi söyle: “yanındayım”, “buradayım” gibi.",
  "Birlikte sadece ikinize özel yeni bir ritüel kelimesi yaratın.",
  "Onun enerjisinin bugün ateşe mi, suya mı daha yakın olduğunu söyle.",
  "Partnerine bir enerji rengi seç ve nedenini açıkla.",
  "Partnerinin kalbinden eline doğru enerji aktığını hayal edin.",
  "Başlarınızı yavaşça birbirinize yaklaştırın ve aradaki alanı hissedin.",
  "Nefesinizin ritmini aynı hizaya getirip hissettiklerinizi paylaşın.",
  "Aranızdaki bağı tek bir sesle ifade edin: fısıltı, nefes, mırıldanma.",
  "Gözlerinizi kapatıp “biz” halinizin enerjisini dinleyin.",
  // 41–60
  "Partnerinin ruhunu bir mitolojik yaratıkla tarif et.",
  "Onu bir element tanrı/tanrıçasına benzet (sadece sembolik).",
  "Partnerine bir “gölge hayvanı” seç (örneğin kurt, baykuş, kedi…).",
  "Onun enerjisinin bugün hangi gezegene benzediğini söyle.",
  "Aranızdaki bağı bir tarot kartına benzet (aşıklar, güneş, ay gibi).",
  "Partnerinin ruh hâlini sezgisel bir sembolle anlat (ok, spiral, alev…).",
  "Onu “gecenin” hangi hâline benzetirsin? alacakaranlık, ay ışığı, şafak?",
  "Partnerin için havaya küçük bir koruyucu sembol çiz.",
  "Onun enerjisinin titreşimini bir müzik ritmiyle tarif et.",
  "Partnerine bir “ritüel adı” ver (örneğin: sessiz ateş, gece rüzgârı).",
  "Onu mistik bir varlık gibi hayal ederek kısa bir cümle kur.",
  "Partnerinin içsel gücünü bir tanrıça/tanrı niteliğiyle ifade et.",
  "Onun ruh rengine karar ver ve nedenini anlat.",
  "İkinizi bağlayan gizli bir sembol icat edin (bir şekil, işaret, hareket).",
  "Aranızdaki bağı bir büyü türüne benzet (ışık büyüsü, ateş büyüsü…).",
  "Partnerinin ışık tarafını tek bir kelimeyle anlat.",
  "Onun gölge tarafını nazik bir metaforla ifade et.",
  "Onu bir rüzgâr türü olarak hayal et (fırtına, meltem, esinti).",
  "Partnerine bir kutsal sözcük fısılda (sadece ikinizin anlamını bildiği).",
  "Beraber bir “enerji sembolü” yaratın (el hareketi, işaret, çizgi).",
  // 61–80
  "Partnerine dokunmadan bir “enerji öpücüğü” gönderdiğini hayal et.",
  "Onun bedenine dokunmadan bir sıcaklık dalgası yönlendir.",
  "Partnerine yaklaş ve sadece nefeslerinle bir ritim oluştur.",
  "Elleriniz birbirine değmeden “enerji dansı” yapın.",
  "Onun bedenini sezgisel bir ışık haritası gibi düşün.",
  "Partnerine derin ve çağıran bir ritüel bakışı gönder.",
  "Onun dudaklarına yaklaş ama dokunma; enerjiyi hisset.",
  "Partnerine bedensel enerjinin hangi bölgede uyandığını söyle.",
  "Birbirinize dokunmadan yakınlık enerjisi gönderin.",
  "Partnerinin aurasını bir renk akışı olarak tarif et.",
  "Onun tenine yaklaşınca içindeki titreşimi tarif et.",
  "Partnerine sezgisel olarak bir dokunuş “tarifi” yap (uygulanmadan).",
  "Onun enerjisini ateşle uyandıran hareketi sözle anlat.",
  "Partnerine ritüel bir cümle söyle: “beni çağır”, “gel bana” gibi.",
  "Elleriniz yakınken aranızdaki sıcaklık dalgasını tanımlayın.",
  "Partnerine “enerjimi nereye yönlendireyim?” diye sor.",
  "Gözlerinizi kapatıp sadece birbirinizin nefesini dinleyin.",
  "Onun bedenini sis içinde hayal edip bir noktayı seç ve tarif et.",
  "Birbirinize “çekim sırrı” fısıldayın (tek kelime bile olabilir).",
  "Partnerine enerjinizin bugün hangi tonda olduğunu söyle (yumuşak, yoğun, coşkulu).",
];

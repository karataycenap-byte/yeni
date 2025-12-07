# Noir Dedektif - Olgun Tema Macera Oyunu
# +18 = sadece karanlik/siddet/gerilim temalari. Cinsel icerik yoktur.
# Tek dosya Python oyunu.

import sys
import time
import random

# Oyuncu durumu
state = {
    "scene": "start",
    "mind": 10,
    "grit": 10,
    "rep": 5,
    "cash": 25,
    "items": [],
    "clues": [],
    "health": 10
}

def slow_print(text, delay=0.02):
    """Ekrana yavas yazim efekti."""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def choice(options):
    """Kullanicidan secim al."""
    while True:
        try:
            sec = int(input("\nSeciminiz: "))
            if 1 <= sec <= len(options):
                return options[sec - 1]
        except:
            pass
        print("Gecerli bir secim girin.")

def add_clue(c):
    if c not in state["clues"]:
        state["clues"].append(c)

def add_item(i):
    if i not in state["items"]:
        state["items"].append(i)

def change_scene(s):
    state["scene"] = s

# SAHNELER
def scene_start():
    slow_print("Yagmur sokaklara vuruyor. Ofisinde tek basinasi oturan bir dedektifsin.")
    slow_print("Masanin ustunde bir zarf, bir de soğumus kahve var.")
    print("\n1) Zarfa bak")
    print("2) Polis kayitlarina goz at")
    print("3) Kahveye inip dedikodulari dinle")

    sec = choice([1,2,3])
    if sec == 1:
        change_scene("envelope")
    elif sec == 2:
        change_scene("police")
    else:
        change_scene("cafe")

def scene_envelope():
    slow_print("Zarfin icinden bir foto ve kisacik bir not cikiyor.")
    slow_print("Not: Saat 00:00 - BR13 kodlu depo.")
    add_clue("BR13 depo ve gizli bulusma")
    print("\n1) Depoya git")
    print("2) Polise goster")
    print("3) Daha fazla arastir")

    sec = choice([1,2,3])
    if sec == 1:
        change_scene("warehouse")
    elif sec == 2:
        change_scene("police")
    else:
        change_scene("records")

def scene_police():
    slow_print("Polis kayitlarinda BR13 gecmisten kayip insanlar ile baglantili.")
    slow_print("Memur sana 10 lira veriyor: 'Isine yarar belki.'")
    state["cash"] += 10
    print("\n1) Depoya git")
    print("2) Kayitlari derin incele")
    print("3) Kahveye git")

    sec = choice([1,2,3])
    if sec == 1:
        change_scene("warehouse")
    elif sec == 2:
        change_scene("records")
    else:
        change_scene("cafe")

def scene_cafe():
    slow_print("Kahvede insanlar BR13 kodlu eski depoyu konusuyor.")
    slow_print("Barmen: Bekci var. Para verirsen alir iceri.")
    print("\n1) 10 TL ode (paran varsa)")
    print("2) Ikna etmeye calis")
    print("3) Geri don")

    options = []
    if state["cash"] >= 10:
        options = [1,2,3]
    else:
        options = [2,3]

    sec = choice(options)

    if sec == 1:
        state["cash"] -= 10
        add_clue("Bekci para ile ikna oluyor")
        change_scene("warehouse")
    elif sec == 2:
        roll = random.random() + state["mind"]/20
        if roll > 0.7:
            slow_print("Barmeni ikna ettin. Bekci seni birakacak.")
            add_clue("Bekci yorgun ve kolay ikna olur.")
            change_scene("warehouse")
        else:
            slow_print("Barmen sinirlendi. Bir sey anlatmadi.")
            state["mind"] -= 1
            change_scene("start")
    else:
        change_scene("start")

def scene_records():
    slow_print("Kayitlarda BR13 gecmiste kaybolan insanlar ile baglantili.")
    add_clue("BR13 gecmiste kaybolan insanlar")
    print("\n1) Depoya git")
    print("2) Sokak haberci bul")

    sec = choice([1,2])
    if sec == 1:
        change_scene("warehouse")
    else:
        change_scene("informant")

def scene_informant():
    slow_print("Sokak habercisi: Bekcinin silahi var ama yerini gizli sakliyor.")
    add_clue("Bekcinin gizli silahi var")
    print("\n1) Silahi almaya calis (risk)")
    print("2) Depoya git")

    sec = choice([1,2])
    if sec == 1:
        slow_print("Silahi aldin ama itibar kaybettin.")
        add_item("Tabanca")
        state["rep"] -= 1
        change_scene("warehouse")
    else:
        change_scene("warehouse")

def scene_warehouse():
    slow_print("Depo onundeki bekci seni durduruyor.")
    print("\n1) 20 TL ode")
    print("2) Ikna et")
    print("3) Zorla gir (silahin varsa)")
    print("4) Geri don")

    options = []
    mapping = []

    # eslestirme
    cnt = 1
    if state["cash"] >= 20:
        print(f"{cnt}) 20 TL ode")
        options.append("pay")
        cnt += 1
    print(f"{cnt}) Ikna et")
    options.append("talk")
    cnt += 1
    if "Tabanca" in state["items"]:
        print(f"{cnt}) Zorla gir")
        options.append("force")
        cnt += 1
    print(f"{cnt}) Geri don")
    options.append("back")

    sec = choice(list(range(1, len(options)+1)))
    act = options[sec-1]

    if act == "pay":
        state["cash"] -= 20
        add_clue("Bekci parayla birakti")
        change_scene("inside")
    elif act == "talk":
        roll = random.random() + state["mind"]/20
        if roll > 0.6:
            add_clue("Bekci seni birakti")
            change_scene("inside")
        else:
            slow_print("Bekci seni geri gonderdi.")
            state["grit"] -= 1
            change_scene("start")
    elif act == "force":
        roll = random.random() + state["grit"]/20
        if roll > 0.7:
            slow_print("Zorla iceri girdin.")
            add_clue("Bekci kacarken bir sey soylenedi")
            change_scene("inside")
        else:
            slow_print("Yaralandin.")
            state["health"] -= 4
            if state["health"] <= 0:
                change_scene("dead")
            else:
                change_scene("start")
    else:
        change_scene("start")

def scene_inside():
    slow_print("Depo icinde kutular, sandiklar ve kilitli bir oda var.")
    print("\n1) Dosyayi incele")
    print("2) Kutuya bak")
    print("3) Kilitli odaya bak")

    sec = choice([1,2,3])
    if sec == 1:
        add_clue("BR13 dosyasi: 03:00 teslimat")
        change_scene("inside")
        slow_print("Dosyada teslimatin saat 03:00 oldugu yaziyor.")
    elif sec == 2:
        slow_print("Kutunun icinde anahtar ve eski bir madalya var.")
        add_item("Anahtar")
        add_clue("Gemi logosu olan madalya")
        change_scene("inside")
    else:
        if "Anahtar" in state["items"]:
            change_scene("room")
        else:
            slow_print("Oda kilitli.")
            change_scene("inside")

def scene_room():
    slow_print("Odayi actin. Iceride kayip insanlar var. Bitkin ama hayattalar.")
    add_clue("Rhtim baglantisi")
    add_item("Tanik")
    print("\n1) Taniklari alip rihtima git")
    print("2) Polise gotur")

    sec = choice([1,2])
    if sec == 1:
        change_scene("dock")
    else:
        change_scene("police_after")

def scene_police_after():
    slow_print("Polis resmi sorusturma acti. Bazi dosyalar kaybolabilir.")
    add_clue("Resmi sorusturma basladi")
    print("\n1) Basina haber ver")
    print("2) Marloya git")

    sec = choice([1,2])
    if sec == 1:
        change_scene("end_mixed")
    else:
        change_scene("dock")

def scene_dock():
    slow_print("Rihtim sisli. Bir teslimat bekleniyor.")
    print("\n1) Gizlice izle")
    print("2) Mudahale et")

    sec = choice([1,2])
    if sec == 1:
        change_scene("stakeout")
    else:
        change_scene("intervene")

def scene_stakeout():
    slow_print("Siyah sedan geliyor. Bir cuvarda insan sesi var.")
    add_clue("Teslimatta insanlar var")
    print("\n1) Polisi ara")
    print("2) Kendin mudahale et")

    sec = choice([1,2])
    if sec == 1:
        change_scene("end_mixed")
    else:
        change_scene("intervene")

def scene_intervene():
    slow_print("Mudahale etmek uzere hazirlaniyorsun...")
    print("\n1) Sessiz mudahale")
    print("2) Gurultulu mudahale")

    sec = choice([1,2])
    roll = random.random() + state["grit"]/20

    if roll > 0.7:
        change_scene("end_good")
    else:
        change_scene("end_bad")

def scene_end_good():
    slow_print("Basarili oldun. Insanlari kurtardin. Sehir bir nebze daha iyi.")
    sys.exit()

def scene_end_bad():
    slow_print("Isler kotu bitti. Bazi insanlar zarar gordu.")
    sys.exit()

def scene_end_mixed():
    slow_print("Sonuc karisik. Bazi seyler cozuldu, bazi seyler ortada kaldi.")
    sys.exit()

def scene_dead():
    slow_print("Aldigin yaralar ilk degil ama bu sefer son. Oyun bitti.")
    sys.exit()

# SAHNE HARITASI
scenes = {
    "start": scene_start,
    "envelope": scene_envelope,
    "police": scene_police,
    "cafe": scene_cafe,
    "records": scene_records,
    "informant": scene_informant,
    "warehouse": scene_warehouse,
    "inside": scene_inside,
    "room": scene_room,
    "police_after": scene_police_after,
    "dock": scene_dock,
    "stakeout": scene_stakeout,
    "intervene": scene_intervene,
    "end_good": scene_end_good,
    "end_bad": scene_end_bad,
    "end_mixed": scene_end_mixed,
    "dead": scene_dead
}

# OYUN DONGUSU
while True:
    scene = state["scene"]
    if scene in scenes:
        scenes[scene]()
    else:
        slow_print("Bilinmeyen sahne: " + scene)
        break

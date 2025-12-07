import streamlit as st

# --- STATE INIT ---
if "scene" not in st.session_state:
    st.session_state.scene = "start"
if "mind" not in st.session_state:
    st.session_state.mind = 10
if "grit" not in st.session_state:
    st.session_state.grit = 10
if "rep" not in st.session_state:
    st.session_state.rep = 5
if "cash" not in st.session_state:
    st.session_state.cash = 25
if "items" not in st.session_state:
    st.session_state.items = []
if "clues" not in st.session_state:
    st.session_state.clues = []
if "health" not in st.session_state:
    st.session_state.health = 10


def goto(scene):
    st.session_state.scene = scene
    st.rerun()  # DÜZELTİLMİŞ


def add_clue(c):
    if c not in st.session_state.clues:
        st.session_state.clues.append(c)


def add_item(i):
    if i not in st.session_state.items:
        st.session_state.items.append(i)


# --- SCENES ---
def scene_start():
    st.title("Noir Dedektif - Streamlit Metin Oyunu")
    st.write("Yagmur sokaklara vuruyor. Masanda bir zarf duruyor.")

    if st.button("Zarfa bak"):
        goto("envelope")

    if st.button("Polis kayitlarina bak"):
        goto("police")

    if st.button("Kahveye in"):
        goto("cafe")


def scene_envelope():
    st.write("Zarfin icinden bir foto ve bir not cikiyor: 'BR13 depo - 00:00'")
    add_clue("BR13 depo notu")

    if st.button("Depoya git"):
        goto("warehouse")

    if st.button("Polise goster"):
        goto("police")

    if st.button("Geri dön"):
        goto("start")


def scene_police():
    st.write("Polis memuru BR13'un kayip insanlar ile baglantili oldugunu soyluyor.")
    st.session_state.cash += 10
    st.info("Memur sana 10 TL verdi.")

    if st.button("Depoya git"):
        goto("warehouse")

    if st.button("Kahveye git"):
        goto("cafe")

    if st.button("Geri don"):
        goto("start")


def scene_cafe():
    st.write("Kahvede insanlar BR13 deposunu konusuyor. Barmen bilgi verebilir.")

    if st.session_state.cash >= 10:
        if st.button("10 TL ver (ipucu al)"):
            st.session_state.cash -= 10
            add_clue("Bekci para ile ikna olur")
            goto("warehouse")

    if st.button("Ikna etmeye calis"):
        add_clue("Barmen seni pek sevmedi")
        goto("start")

    if st.button("Geri don"):
        goto("start")


def scene_warehouse():
    st.write("Depo onunde bir bekci var.")

    if st.session_state.cash >= 20:
        if st.button("20 TL ver ve iceri gir"):
            st.session_state.cash -= 20
            goto("inside")

    if st.button("Ikna et"):
        goto("inside")

    if "Tabanca" in st.session_state.items:
        if st.button("Zorla gir"):
            goto("inside")

    if st.button("Geri don"):
        goto("start")


def scene_inside():
    st.write("Depo icinde kutular ve kilitli bir oda var.")

    if st.button("Kutuyu ac"):
        add_item("Anahtar")
        add_clue("Kutudan anahtar cikti")
        st.success("Anahtar alindi!")

    if st.button("Dosyayi incele"):
        add_clue("Teslimat saati 03:00")

    if st.button("Kilitli odayi ac"):
        if "Anahtar" in st.session_state.items:
            goto("room")
        else:
            st.error("Anahtar yok.")

    if st.button("Geri don"):
        goto("warehouse")


def scene_room():
    st.write("Odayi actin. Iceride kayip insanlar var.")
    add_item("Tanik")

    if st.button("Taniklari alip rihtima git"):
        goto("dock")

    if st.button("Polise teslim et"):
        goto("police_after")


def scene_police_after():
    st.write("Polis resmi sorusturma acti.")

    if st.button("Basina haber ver"):
        goto("end_mixed")

    if st.button("Rihtima git"):
        goto("dock")


def scene_dock():
    st.write("Sisli bir rihtim. Bir teslimat bekleniyor.")

    if st.button("Gizlice izle"):
        goto("stakeout")

    if st.button("Mudahale et"):
        goto("intervene")


def scene_stakeout():
    st.write("Siyah bir sedan geliyor. Cuvallarda ses var.")

    if st.button("Polisi ara"):
        goto("end_mixed")

    if st.button("Kendin mudahale et"):
        goto("intervene")


def scene_intervene():
    st.write("Mudahale ediyorsun...")

    if st.button("Sessiz mudahale"):
        goto("end_good")

    if st.button("Gurultulu mudahale"):
        goto("end_bad")


def scene_end_good():
    st.success("Basarili oldun. Insanlari kurtardin. Oyun bitti.")


def scene_end_bad():
    st.error("Mudahale basarisiz oldu. Oyun bitti.")


def scene_end_mixed():
    st.warning("Son karisik. Bazi seyler cozuldu, bazi seyler havada kaldi.")


# --- ROUTER ---
scene_map = {
    "start": scene_start,
    "envelope": scene_envelope,
    "police": scene_police,
    "cafe": scene_cafe,
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
}

scene_map[st.session_state.scene]()

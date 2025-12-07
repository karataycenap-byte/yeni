import random
import time
import os

# ---------------------- YARDIMCI FONKSİYONLAR ---------------------- #

def clear_screen():
    # Ekranı temizler (Windows / Mac / Linux)
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.015):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def wait_enter(msg="\nDevam etmek için Enter'a basın..."):
    input(msg)

# ---------------------- OYUN VERİLERİ ---------------------- #

# Kategoriler: TANIMA, DERIN, ROMANTIK
CARDS = [
    # TANIMA
    {
        "category": "Tanıma",
        "type": "soru",
        "text": "Partnerinde seni en çok şaşırtan özellik ne oldu?"
    },
    {
        "category": "Tanıma",
        "type": "soru",
        "text": "Çocukluğundan bugününü etkilediğini düşündüğün bir anını paylaş."
    },
    {
        "category": "Tanıma",
        "type": "görev",
        "text": "Birbirinize ilk tanışma anınızı, sanki film sahnesini anlatır gibi yeniden anlatın."
    },
    # DERIN
    {
        "category": "Derin Sohbet",
        "type": "soru",
        "text": "Bu ilişkide en çok ne zaman kendini gerçekten 'güvende' hissettin?"
    },
    {
        "category": "Derin Sohbet",
        "type": "soru",
        "text": "Partnerinden duyduğunda seni en çok şifalandıran cümle neydi?"
    },
    {
        "category": "Derin Sohbet",
        "type": "görev",
        "text": "Birbiriniz için şu cümleyi tamamlayın: 'Sende en çok sevdiğim şey...'"
    },
    # ROMANTIK (buradakileri daha flörtöz yapabilir, istersen kendin +18'leştirebilirsin)
    {
        "category": "Romantik & Flörtöz",
        "type": "görev",
        "text": "Partnerine 30 saniye boyunca sadece gözlerinin içine bak ve hiçbir şey söyleme."
    },
    {
        "category": "Romantik & Flörtöz",
        "type": "görev",
        "text": "Partnerine bugün için minnettar olduğun 3 şeyi sırayla söyle."
    },
    {
        "category": "Romantik & Flörtöz",
        "type": "mini-oyun",
        "text": "Taş-kâğıt-makas oynayın. Kaybeden, kazananın seçtiği küçük bir jesti yapmak zorunda."
    },
]

# Buraya kendi özel kartlarını ekleyebilirsin.
# Örn: 'text' kısmını kendin çok daha cesur hale getirebilirsin.
CUSTOM_CARDS = [
    # ÖRNEK (bunu istediğin gibi değiştirebilirsin)
    # {
    #     "category": "Özel",
    #     "type": "görev",
    #     "text": "Buraya sadece sizin bildiğiniz özel bir görev yazın. ;)"
    # }
]

ALL_CARDS = CARDS + CUSTOM_CARDS

# ---------------------- OYUN SINIFI ---------------------- #

class CiftOyunu:
    def __init__(self):
        self.player1 = ""
        self.player2 = ""
        self.scores = {}
        self.deck = []
        self.current_player_index = 0
        self.players = []
        self.max_score = 10  # İstenirse değiştirilebilir

    def setup_players(self):
        clear_screen()
        slow_print("Bağlantı: Çift Oyunu'na hoş geldiniz 💫\n")
        self.player1 = input("1. oyuncunun adı/nick'i: ").strip() or "Oyuncu 1"
        self.player2 = input("2. oyuncunun adı/nick'i: ").strip() or "Oyuncu 2"
        self.players = [self.player1, self.player2]
        self.scores = {self.player1: 0, self.player2: 0}

    def choose_mode(self):
        clear_screen()
        slow_print("Oyun modu seçin:\n")
        print("1) Karışık kartlar (tümü)")
        print("2) Sadece Tanıma")
        print("3) Sadece Derin Sohbet")
        print("4) Sadece Romantik & Flörtöz")
        print("5) Özel + Karışık (varsa CUSTOM_CARDS ile birlikte)\n")

        choice = input("Seçiminiz (1-5): ").strip()
        categories = []

        if choice == "2":
            categories = ["Tanıma"]
        elif choice == "3":
            categories = ["Derin Sohbet"]
        elif choice == "4":
            categories = ["Romantik & Flörtöz"]
        elif choice == "5":
            categories = ["Tanıma", "Derin Sohbet", "Romantik & Flörtöz", "Özel"]
        else:
            # 1 veya geçersiz ise karışık tümü
            categories = ["Tanıma", "Derin Sohbet", "Romantik & Flörtöz", "Özel"]

        # Deste oluştur
        self.deck = [
            card for card in ALL_CARDS
            if card["category"] in categories
        ]

        if not self.deck:
            slow_print("Bu kategori seçimiyle hiç kart yok. Varsayılan olarak tüm kartlar seçildi.")
            self.deck = ALL_CARDS[:]

        random.shuffle(self.deck)

    def show_scores(self):
        print("\n--- SKOR TABLOSU ---")
        for p, s in self.scores.items():
            print(f"{p}: {s} puan")
        self.show_bond_level()

    def show_bond_level(self):
        # Yakınlık seviyesi (maks skora göre basit bir bar)
        total = sum(self.scores.values())
        max_total = self.max_score * 2
        ratio = total / max_total if max_total > 0 else 0
        bar_length = 20
        filled = int(bar_length * ratio)
        bar = "█" * filled + "-" * (bar_length - filled)
        print(f"\nYakınlık Seviyesi: [{bar}] {int(ratio * 100)}%")

    def draw_card(self):
        if not self.deck:
            # Kartlar biterse tekrar karıştır
            self.deck = ALL_CARDS[:]
            random.shuffle(self.deck)
        return self.deck.pop()

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def play_round(self):
        clear_screen()
        current = self.players[self.current_player_index]
        slow_print(f"Sıra sende: {current} ✨\n")
        wait_enter("Kart çekmek için Enter'a bas...")

        card = self.draw_card()

        slow_print(f"\nKategori: {card['category']}")
        slow_print(f"Tür: {card['type'].capitalize()}")
        slow_print("\nKart:")
        slow_print(f"{card['text']}")

        print("\nBu kartı birlikte uyguladıktan/cevapladıktan sonra 'bitti' diyebilirsiniz.")
        done = input("Kartı uyguladınız mı? (e/h): ").strip().lower()

        if done == "e":
            self.scores[current] += 1
            slow_print(f"\nHarika! {current} +1 puan kazandı. 🎉")
        else:
            slow_print(f"\nSorun değil, bazen beklemek de oyunun parçası. 🙂")

        self.show_scores()
        wait_enter()
        self.next_player()

    def check_winner(self):
        for p, s in self.scores.items():
            if s >= self.max_score:
                return p
        return None

    def end_game_message(self, winner):
        clear_screen()
        slow_print("Oyun bitti! 💖\n")
        if winner:
            slow_print(f"Kazanan: {winner} 🎉")
        else:
            slow_print("Bu turda belirgin bir kazanan yok, ama asıl kazanan aranızdaki bağ oldu. 💫")
        self.show_scores()
        print("\nİsterseniz kod içindeki kartları değiştirerek oyunu kendi ilişkinize göre 'özelleştirebilirsiniz'. 😉")

    def main_menu(self):
        while True:
            clear_screen()
            slow_print("Bağlantı: Çift Oyunu 💞\n")
            print("1) Oyuna Başla")
            print("2) Kurallar")
            print("3) Çıkış\n")
            choice = input("Seçiminiz (1-3): ").strip()

            if choice == "1":
                self.setup_players()
                self.choose_mode()
                self.game_loop()
            elif choice == "2":
                self.show_rules()
            elif choice == "3":
                clear_screen()
                slow_print("Görüşmek üzere, aranızdaki bağ hep güçlensin. 💫")
                break
            else:
                slow_print("Geçersiz seçim, lütfen tekrar deneyin.")
                time.sleep(1.3)

    def show_rules(self):
        clear_screen()
        slow_print("Kurallar / Mantık:\n")
        slow_print("- Oyun iki kişiyle, aynı cihazdan oynanır.")
        slow_print("- Sırası gelen oyuncu bir kart çeker.")
        slow_print("- Kart; soru, görev veya mini oyun içerebilir.")
        slow_print("- Kartı birlikte uyguladıktan sonra 'e' derseniz o oyuncu +1 puan alır.")
        slow_print(f"- İlk {self.max_score} puana ulaşan kazanır (isterseniz koddan değiştirebilirsiniz).")
        slow_print("- Kod içindeki CARDS ve CUSTOM_CARDS listelerini değiştirerek kendi özel kartlarınızı ekleyebilirsiniz.")
        wait_enter()

    def game_loop(self):
        winner = None
        while not winner:
            self.play_round()
            winner = self.check_winner()
        self.end_game_message(winner)
        wait_enter()

# ---------------------- ÇALIŞTIR ---------------------- #

if __name__ == "__main__":
    game = CiftOyunu()
    game.main_menu()

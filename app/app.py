import streamlit as st
import random
import time
from collections import deque

# --- 1. AYARLAR VE CSS TASARIMI ---
st.set_page_config(page_title="Logic Grid Flow", page_icon="⚡", layout="centered")

def inject_custom_css():
    st.markdown("""
        <style>
        /* Ana Arka Plan: Cyberpunk Siyah */
        .stApp {
            background-color: #050505;
        }
        
        /* Başlık Stili */
        h1 {
            color: #00ffcc;
            text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
            font-family: 'Courier New', monospace;
            text-align: center;
        }
        
        /* Oyun Alanı Konteyneri */
        .block-container {
            padding-top: 2rem;
        }

        /* Buton Genel Stili */
        div.stButton > button {
            width: 100%;
            height: 60px;
            font-size: 28px !important;
            font-weight: bold;
            background-color: #1a1a1a;
            color: #444;
            border: 2px solid #333;
            border-radius: 8px;
            transition: all 0.3s ease;
            line-height: 1 !important;
        }
        
        /* Hover Efekti */
        div.stButton > button:hover {
            border-color: #00ffcc;
            color: #00ffcc;
            box-shadow: 0 0 8px #00ffcc;
        }

        /* AKTİF AKIŞ (Primary Butonlar) - Neon Yeşil */
        div.stButton > button[kind="primary"] {
            background-color: #003300 !important;
            color: #00ff00 !important;
            border-color: #00ff00 !important;
            box-shadow: 0 0 15px #00ff00;
        }

        /* KİLİTLİ PARÇALAR - Kırmızı Çerçeve */
        div.stButton > button:disabled {
            background-color: #1a0000;
            color: #ff0000;
            border-color: #ff0000;
            opacity: 0.8;
            cursor: not-allowed;
        }
        
        /* Bilgilendirme Kutusu */
        .info-box {
            background-color: #111;
            padding: 10px;
            border-radius: 5px;
            border-left: 5px solid #00ffcc;
            color: #ddd;
            font-family: monospace;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 2. OYUN MANTIĞI VE SINIFLAR ---

class Piece:
    def __init__(self, p_type, rotation=0, is_locked=False):
        self.type = p_type          # Straight, Corner, T-Shape, Cross, Start, End
        self.rotation = rotation    # 0, 90, 180, 270
        self.is_locked = is_locked
        self.is_flow_active = False

    def rotate(self):
        if not self.is_locked:
            self.rotation = (self.rotation + 90) % 360

    def get_connections(self):
        """
        Parçanın mevcut rotasyonuna göre hangi yönlere (N, E, S, W) açık olduğunu döndürür.
        Yönler: N=0, E=1, S=2, W=3
        """
        # Temel Bağlantılar (Rotasyon 0 için)
        base_connections = {
            "Straight": [0, 2],       # N, S (Dikey)
            "Corner":   [0, 1],       # N, E (L Şekli)
            "T-Shape":  [1, 2, 3],    # E, S, W (T Şekli - Aşağı Bakan)
            "Cross":    [0, 1, 2, 3], # Hepsi
            "Start":    [1],          # Sadece Doğu (Varsayılan)
            "End":      [3],          # Sadece Batı (Varsayılan)
            "Empty":    []
        }
        
        base = base_connections.get(self.type, [])
        
        # Rotasyona göre yönleri kaydır: (Yön + (Rotasyon/90)) % 4
        rotation_steps = self.rotation // 90
        current_connections = set()
        for direction in base:
            new_dir = (direction + rotation_steps) % 4
            current_connections.add(new_dir)
            
        return current_connections

class Grid:
    def __init__(self, size=5):
        self.size = size
        self.grid_state = []
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)

    def load_level(self, level_data):
        self.size = level_data["size"]
        self.start_pos = tuple(level_data["start_pos"])
        self.end_pos = tuple(level_data["end_pos"])
        self.grid_state = []

        raw_grid = level_data["grid"]
        for r in range(self.size):
            row_pieces = []
            for c in range(self.size):
                code = raw_grid[r][c]
                # Kod ayrıştırma (Örn: "C90L" -> Corner, 90 deg, Locked)
                p_type_map = {'S': 'Straight', 'C': 'Corner', 'T': 'T-Shape', 'X': 'Cross', 'A': 'Start', 'Z': 'End', '.': 'Empty'}
                
                char_type = code[0]
                p_type = p_type_map.get(char_type, 'Empty')
                
                # Rotasyon ve Kilit parsing
                rotation = 0
                is_locked = False
                
                # Basit parsing: stringin geri kalanını analiz et
                if '90' in code: rotation = 90
                elif '180' in code: rotation = 180
                elif '270' in code: rotation = 270
                
                if 'L' in code: is_locked = True
                if p_type in ['Start', 'End']: is_locked = True # Başlangıç/Bitiş hep kilitli
                
                # Rastgelelik (Oyun başında karıştırma)
                if not is_locked and p_type not in ['Start', 'End', 'Empty']:
                    rotation = random.choice([0, 90, 180, 270])

                piece = Piece(p_type, rotation, is_locked)
                
                # Start ve End rotasyonlarını manuel düzelt (Level tasarımına göre)
                if p_type == 'Start': piece.rotation = int(code[1:]) if code[1:].isdigit() else 0
                if p_type == 'End': piece.rotation = int(code[1:]) if code[1:].isdigit() else 0
                
                row_pieces.append(piece)
            self.grid_state.append(row_pieces)
        
        self.check_flow()

    def rotate_piece(self, r, c):
        self.grid_state[r][c].rotate()
        # ÖZGÜN MEKANİK: Dinamik Blokaj
        self.apply_dynamic_blockage(r, c)
        self.check_flow()

    def apply_dynamic_blockage(self, last_r, last_c):
        """Her hamlede başka bir parçayı rastgele kilitle veya kilidini aç."""
        candidates = []
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) != (last_r, last_c) and (r, c) != self.start_pos and (r, c) != self.end_pos:
                     if self.grid_state[r][c].type != 'Empty':
                        candidates.append((r, c))
        
        if candidates and random.random() < 0.4: # %40 ihtimalle tetiklenir
            tr, tc = random.choice(candidates)
            target = self.grid_state[tr][tc]
            target.is_locked = not target.is_locked # Durumu tersine çevir

    def check_flow(self):
        """BFS ile akışı hesapla"""
        # 1. Reset
        for r in range(self.size):
            for c in range(self.size):
                self.grid_state[r][c].is_flow_active = False
        
        # 2. Start
        queue = deque([self.start_pos])
        sr, sc = self.start_pos
        self.grid_state[sr][sc].is_flow_active = True
        
        while queue:
            cr, cc = queue.popleft()
            curr_piece = self.grid_state[cr][cc]
            curr_conns = curr_piece.get_connections()
            
            # Komşuları kontrol et (0:N, 1:E, 2:S, 3:W)
            directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
            opposite_map = {0: 2, 1: 3, 2: 0, 3: 1} # Kuzey'in zıttı Güney vb.
            
            for direction in curr_conns:
                dr, dc = directions[direction]
                nr, nc = cr + dr, cc + dc
                
                # Izgara içi kontrolü
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    neighbor = self.grid_state[nr][nc]
                    if not neighbor.is_flow_active:
                        # Bağlantı Kontrolü: Komşunun bana bakan portu açık mı?
                        needed_port = opposite_map[direction]
                        if needed_port in neighbor.get_connections():
                            neighbor.is_flow_active = True
                            queue.append((nr, nc))

    def is_solved(self):
        er, ec = self.end_pos
        return self.grid_state[er][ec].is_flow_active

# --- 3. SEVİYE VERİLERİ (Hardcoded JSON) ---
LEVELS = {
    1: {
        "name": "Eğitim",
        "size": 4,
        "start_pos": [0, 0],
        "end_pos": [3, 3],
        "grid": [
            ["A90", "C", "S", "C"],
            ["S", "T", "C", "S"],
            ["C", "S", "T", "C"],
            ["C", "C", "S", "Z270"]
        ]
    },
    2: {
        "name": "Karışık Sinyaller",
        "size": 5,
        "start_pos": [2, 0],
        "end_pos": [2, 4],
        "grid": [
            ["C", "S", "T", "S", "C"],
            ["S", "C", "X", "C", "S"],
            ["A0", "T", "X", "T", "Z180"],
            ["S", "C", "X", "C", "S"],
            ["C", "S", "T", "S", "C"]
        ]
    },
    3: {
        "name": "Kilitli Labirent",
        "size": 5,
        "start_pos": [0, 2],
        "end_pos": [4, 2],
        "grid": [
            ["C", "C", "A180", "C", "C"],
            ["S", "T", "S", "T", "S"],
            ["T", "XL", "XL", "XL", "T"],
            ["S", "C", "S", "C", "S"],
            ["C", "S", "Z0", "S", "C"]
        ]
    }
}

# --- 4. YARDIMCI FONKSİYONLAR (Unicode Grafikleri) ---
def get_symbol(p_type, rotation):
    # Box Drawing Characters
    chars = {
        "Straight": {0: "║", 90: "═", 180: "║", 270: "═"},
        "Corner":   {0: "╚", 90: "╔", 180: "╗", 270: "╝"},
        "T-Shape":  {0: "╠", 90: "╦", 180: "╣", 270: "╩"},
        "Cross":    {0: "╬", 90: "╬", 180: "╬", 270: "╬"},
        "Start":    {0: "⚡", 90: "⚡", 180: "⚡", 270: "⚡"},
        "End":      {0: "🔋", 90: "🔋", 180: "🔋", 270: "🔋"},
        "Empty":    {0: " ", 90: " ", 180: " ", 270: " "}
    }
    return chars.get(p_type, {}).get(rotation, "?")

# --- 5. STREAMLIT ARAYÜZÜ ---

def main():
    inject_custom_css()
    
    st.title("⚡ LOGIC GRID FLOW")
    
    # Session State Başlatma
    if 'level_id' not in st.session_state:
        st.session_state.level_id = 1
        st.session_state.grid_obj = Grid()
        st.session_state.grid_obj.load_level(LEVELS[1])
        st.session_state.moves = 0

    # Yan Panel (Sidebar)
    with st.sidebar:
        st.header("🎛 Kontrol Paneli")
        st.write(f"**Seviye:** {LEVELS[st.session_state.level_id]['name']}")
        st.write(f"**Hamle:** {st.session_state.moves}")
        
        st.markdown("---")
        st.markdown("**Nasıl Oynanır?**")
        st.markdown("1. Parçaları döndürmek için **tıklayın**.")
        st.markdown("2. Enerjiyi (⚡) Bataryaya (🔋) ulaştırın.")
        st.markdown("3. **Dikkat:** Bazı hamleler diğer parçaları kilitleyebilir! (🔒)")
        
        if st.button("🔄 Seviyeyi Yeniden Başlat"):
            st.session_state.grid_obj.load_level(LEVELS[st.session_state.level_id])
            st.session_state.moves = 0
            st.rerun()

        level_selection = st.selectbox("Seviye Seç:", list(LEVELS.keys()), index=st.session_state.level_id-1)
        if level_selection != st.session_state.level_id:
            st.session_state.level_id = level_selection
            st.session_state.grid_obj.load_level(LEVELS[level_selection])
            st.session_state.moves = 0
            st.rerun()

    # Oyun Alanı Render
    grid = st.session_state.grid_obj
    
    # Kazanma Durumu
    if grid.is_solved():
        st.balloons()
        st.success(f"🎉 TEBRİKLER! Seviye Tamamlandı! Toplam Hamle: {st.session_state.moves}")
        if st.session_state.level_id < len(LEVELS):
            if st.button("Sonraki Seviye ➡️"):
                st.session_state.level_id += 1
                st.session_state.grid_obj.load_level(LEVELS[st.session_state.level_id])
                st.session_state.moves = 0
                st.rerun()
        else:
            st.write("🏆 Tüm seviyeleri bitirdiniz! Harika bir yazılım mühendisi zekası!")

    # Grid Çizimi
    # Ortalamak için kolonlar
    c1, c2, c3 = st.columns([1, 6, 1])
    
    with c2:
        for r in range(grid.size):
            cols = st.columns(grid.size)
            for c in range(grid.size):
                piece = grid.grid_state[r][c]
                
                # Görsel Hazırlığı
                symbol = get_symbol(piece.type, piece.rotation)
                btn_type = "primary" if piece.is_flow_active else "secondary"
                label = symbol
                
                # Buton Oluşturma
                # Kilitli ise ve akış yoksa disabled yapılabilir, ama tıklayıp "Kilitli" uyarısı vermek daha iyi hissettirebilir.
                # Bizim tasarımımızda kilitli parçalar disabled olacak.
                
                with cols[c]:
                    # CSS tanımları için key ve disabled durumu yeterli
                    is_disabled = piece.is_locked
                    
                    # Eğer kilitli ama akış varsa, görünmeli ama tıklanamamalı
                    # Streamlit disabled butonları gri yapar, bunu CSS ile düzelttik.
                    
                    clicked = st.button(
                        label,
                        key=f"btn_{r}_{c}_{st.session_state.moves}", # Key her hamlede değişmeli ki UI yenilensin
                        type=btn_type,
                        disabled=is_disabled,
                        help="Döndürmek için tıkla" if not is_disabled else "KİLİTLİ"
                    )
                    
                    if clicked and not is_disabled:
                        grid.rotate_piece(r, c)
                        st.session_state.moves += 1
                        st.rerun()

if __name__ == "__main__":
    main()

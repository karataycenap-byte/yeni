import streamlit as st
import random
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
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #333;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 2. OYUN MANTIĞI VE SINIFLAR ---

class Piece:
    def __init__(self, p_type, rotation=0, is_locked=False):
        self.type = p_type
        self.rotation = rotation
        self.is_locked = is_locked
        self.is_flow_active = False

    def rotate(self):
        if not self.is_locked:
            self.rotation = (self.rotation + 90) % 360

    def get_connections(self):
        """ Parçanın rotasyonuna göre açık bağlantı yönlerini (0:N, 1:E, 2:S, 3:W) döndürür. """
        base_connections = {
            "Straight": [0, 2],
            "Corner":   [0, 1],
            "T-Shape":  [1, 2, 3],
            "Cross":    [0, 1, 2, 3],
            "Start":    [1], # Default
            "End":      [3], # Default
            "Empty":    []
        }
        base = base_connections.get(self.type, [])
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
        """ JSON'daki çözülmüş hali yükler ve rastgele kilitler ekler (Karıştırma yok). """
        self.size = level_data["size"]
        self.start_pos = tuple(level_data["start_pos"])
        self.end_pos = tuple(level_data["end_pos"])
        self.grid_state = []

        raw_grid = level_data["grid"]
        for r in range(self.size):
            row_pieces = []
            for c in range(self.size):
                code = raw_grid[r][c]
                p_type_map = {'S': 'Straight', 'C': 'Corner', 'T': 'T-Shape', 'X': 'Cross', 'A': 'Start', 'Z': 'End', '.': 'Empty'}
                
                char_type = code[0]
                p_type = p_type_map.get(char_type, 'Empty')
                rotation = 0
                is_locked = False
                
                # Rotasyon ve Kilit parsing (JSON'dan gelen çözülmüş rotasyon)
                if '90' in code: rotation = 90
                elif '180' in code: rotation = 180
                elif '270' in code: rotation = 270
                
                if 'L' in code: is_locked = True
                if p_type in ['Start', 'End']: is_locked = True
                
                piece = Piece(p_type, rotation, is_locked)
                
                # Start ve End rotasyonlarını düzelt
                if p_type == 'Start': piece.rotation = int(code[1:]) if len(code) > 1 and code[1:].isdigit() else 0
                if p_type == 'End': piece.rotation = int(code[1:]) if len(code) > 1 and code[1:].isdigit() else 0
                
                # Çözülebilirliği bozmamak için rastgele karıştırmayı kaldırıyoruz.
                # SADECE rastgele kilit ekliyoruz (Çözümün karmaşıklık seviyesi).
                if not is_locked and p_type not in ['Start', 'End', 'Empty']:
                    if random.random() < 0.3: # %30 ihtimalle ilk başta kilitli başlasın
                         piece.is_locked = True 

                row_pieces.append(piece)
            self.grid_state.append(row_pieces)
        self.check_flow()

    def rotate_piece(self, r, c):
        self.grid_state[r][c].rotate()
        self.apply_dynamic_blockage(r, c)
        self.check_flow()

    def apply_dynamic_blockage(self, last_r, last_c):
        """ GÜNCELLENMİŞ VE YUMUŞATILMIŞ Dinamik Blokaj Mekaniği. """
        candidates = []
        for r in range(self.size):
            for c in range(self.size):
                # Başlangıç, Bitiş, Boş ve Son Oynanan yerleri hariç tut
                if (r, c) != (last_r, last_c) and (r, c) != self.start_pos and (r, c) != self.end_pos:
                     if self.grid_state[r][c].type not in ['Start', 'End', 'Empty']:
                        candidates.append((r, c))
        
        if candidates and random.random() < 0.5: # %50 tetiklenme ihtimali
            tr, tc = random.choice(candidates)
            target = self.grid_state[tr][tc]
            
            # %60 Kilit Açma / %40 Kilitleme (Oyuncuyu ödüllendiren denge)
            if random.random() < 0.6:
                if target.is_locked:
                    target.is_locked = False
            else:
                if not target.is_locked:
                    target.is_locked = True

    def check_flow(self):
        # BFS (Genişlik Öncelikli Arama) ile akışı hesapla
        for r in range(self.size):
            for c in range(self.size):
                self.grid_state[r][c].is_flow_active = False
        
        queue = deque([self.start_pos])
        sr, sc = self.start_pos
        self.grid_state[sr][sc].is_flow_active = True
        
        while queue:
            cr, cc = queue.popleft()
            curr_piece = self.grid_state[cr][cc]
            curr_conns = curr_piece.get_connections()
            directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
            opposite_map = {0: 2, 1: 3, 2: 0, 3: 1} # Karşı yön haritası
            
            for direction in curr_conns:
                dr, dc = directions[direction]
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    neighbor = self.grid_state[nr][nc]
                    if not neighbor.is_flow_active:
                        needed_port = opposite_map[direction]
                        if needed_port in neighbor.get_connections():
                            neighbor.is_flow_active = True
                            queue.append((nr, nc))

    def is_solved(self):
        er, ec = self.end_pos
        return self.grid_state[er][ec].is_flow_active

# --- 3. SEVİYE VERİLERİ (Çözülmüş Durumda Verilmiştir) ---
LEVELS = {
    1: {"name": "Başlangıç Sinyali", "size": 4, "start_pos": [0, 0], "end_pos": [3, 3], "grid": [["A1", "S90", "C90", "C180"], ["C180", "T270", "S", "C90"], ["S", "C180", "T", "C270"], ["C90", "C", "S90", "Z270"]]},
    2: {"name": "Çapraz Ateş", "size": 5, "start_pos": [2, 0], "end_pos": [2, 4], "grid": [["C", "S", "T", "S", "C"], ["S", "C90", "X", "C270", "S"], ["A1", "T90", "X", "T270", "Z3"], ["S", "C180", "X", "C", "S"], ["C", "S", "T", "S", "C"]]},
    3: {"name": "Siber Labirent", "size": 5, "start_pos": [0, 2], "end_pos": [4, 2], "grid": [["C270", "S", "A0", "S", "C90"], ["S", "T270", "S", "T90", "S"], ["T", "X", "S", "X", "T"], ["S", "C", "S", "C", "S"], ["C", "S90", "Z2", "S90", "C"]]}}

def get_symbol(p_type, rotation):
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

# --- 4. KARŞILAMA EKRANI VE OYUN MANTIĞI ---

def show_welcome_screen():
    st.markdown("<h1 style='font-size: 60px;'>⚡ LOGIC GRID FLOW</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #888;'>Siber Enerji Hatlarını Onar</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>🎮 Nasıl Oynanır?</h4>
            <ol style="line-height: 1.8; color: #ccc;">
                <li><b>Amacın:</b> Enerji kaynağından (⚡) çıkan neon ışığını bataryaya (🔋) ulaştırmak.</li>
                <li><b>Kontrol:</b> Boru parçalarına tıklayarak onları <b>90 derece döndür</b> ve yolu tamamla.</li>
                <li><b>Yeşil Işık:</b> Eğer bir parçadan elektrik geçiyorsa rengi <span style="color:#00ff00;"><b>Neon Yeşil</b></span> olur.</li>
            </ol>
            <hr style="border-color: #333;">
            <h4>⚠️ Kritik Uyarı: "Kaos Faktörü"</h4>
            <p style="color: #ff5555;">Bu sıradan bir bulmaca değil! Her hamlenizde sistemin <b>Güvenlik Protokolü</b> devreye girebilir:</p>
            <ul>
                <li>Bir parçayı döndürdüğünüzde, haritadaki başka bir parça <b>aniden kilitlenebilir</b> (🔒) veya kilidi açılabilir (Daha sık).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        start_btn = st.button("SİSTEMİ BAŞLAT [START] 🚀", type="primary", use_container_width=True)
        if start_btn:
            st.session_state.game_active = True
            st.rerun()

def render_game_ui():
    grid = st.session_state.grid_obj

    with st.sidebar:
        st.header("🎛 Kontrol Paneli")
        st.write(f"**Seviye:** {LEVELS[st.session_state.level_id]['name']}")
        st.write(f"**Hamle Sayısı:** {st.session_state.moves}")
        
        st.progress(st.session_state.level_id / len(LEVELS), text="Oyun İlerlemesi")
        
        if st.button("🏠 Ana Menüye Dön"):
            st.session_state.game_active = False
            st.rerun()
            
        if st.button("🔄 Seviyeyi Sıfırla"):
            st.session_state.grid_obj.load_level(LEVELS[st.session_state.level_id])
            st.session_state.moves = 0
            st.rerun()

    st.title(f"Seviye {st.session_state.level_id}: {LEVELS[st.session_state.level_id]['name']}")
    
    # Kazanma Kontrolü
    if grid.is_solved():
        st.balloons()
        st.success(f"🎉 SİSTEM ONARILDI! Toplam Hamle: {st.session_state.moves}")
        
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            if st.session_state.level_id < len(LEVELS):
                if st.button("SONRAKİ SEVİYEYE GEÇ ➡️", type="primary"):
                    st.session_state.level_id += 1
                    st.session_state.grid_obj.load_level(LEVELS[st.session_state.level_id])
                    st.session_state.moves = 0
                    st.rerun()
            else:
                st.info("🏆 Tebrikler! Tüm protokolleri başarıyla tamamladınız.")
                if st.button("Başa Dön"):
                    st.session_state.level_id = 1
                    st.session_state.game_active = False
                    st.rerun()

    # Grid Render
    c1, c2, c3 = st.columns([1, 6, 1])
    with c2:
        for r in range(grid.size):
            cols = st.columns(grid.size)
            for c in range(grid.size):
                piece = grid.grid_state[r][c]
                symbol = get_symbol(piece.type, piece.rotation)
                btn_type = "primary" if piece.is_flow_active else "secondary"
                
                with cols[c]:
                    is_disabled = piece.is_locked
                    label = symbol
                    
                    clicked = st.button(
                        label,
                        key=f"btn_{r}_{c}_{st.session_state.moves}",
                        type=btn_type,
                        disabled=is_disabled,
                        help="Döndürmek için tıkla" if not is_disabled else "KİLİTLİ - Kaos Faktörü Devrede!"
                    )
                    
                    if clicked and not is_disabled:
                        grid.rotate_piece(r, c)
                        st.session_state.moves += 1
                        st.rerun()

def main():
    inject_custom_css()
    
    # Session State Başlatma ve Durum Kontrolü
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False
        
    if 'level_id' not in st.session_state:
        st.session_state.level_id = 1
        st.session_state.grid_obj = Grid()
        st.session_state.grid_obj.load_level(LEVELS[1])
        st.session_state.moves = 0

    if not st.session_state.game_active:
        show_welcome_screen()
    else:
        render_game_ui()

if __name__ == "__main__":
    main()

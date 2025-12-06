import streamlit as st
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict
import plotly.graph_objects as go

# ============================================================================
# GAME CONSTANTS & ENUMS (Aynı)
# ============================================================================

class CellType(Enum):
    EMPTY = "empty"
    THOUGHT_CREATIVE = "creative"
    THOUGHT_ANALYTIC = "analytic"
    THOUGHT_EMOTIONAL = "emotional"
    THOUGHT_INTUITIVE = "intuitive"
    ANXIETY = "anxiety"
    JOY = "joy"
    TRAUMA = "trauma"
    FLOWER = "flower"
    WISDOM = "wisdom"

class TimeOfDay(Enum):
    MORNING = "Sabah"
    NOON = "Öğle"
    EVENING = "Akşam"
    NIGHT = "Gece"

# ============================================================================
# DATA CLASSES (Aynı)
# ============================================================================

@dataclass
class Cell:
    type: CellType
    health: int = 50
    energy: int = 0
    age: int = 0
    x: int = 0
    y: int = 0

@dataclass
class GameState:
    day: int = 1
    action_points: int = 3
    total_energy: int = 100
    consciousness_level: int = 1
    consciousness_xp: int = 0
    grid_size: int = 7
    grid: List[List[Cell]] = None
    time_of_day: TimeOfDay = TimeOfDay.MORNING
    event_log: List[str] = None
    achievements: List[str] = None
    flowers_bloomed: int = 0
    total_thoughts: int = 0
    anxieties_cleared: int = 0
    
    def __post_init__(self):
        if self.grid is None:
            self.grid = [[Cell(CellType.EMPTY, x=x, y=y) for x in range(self.grid_size)] 
                         for y in range(self.grid_size)]
        if self.event_log is None:
            self.event_log = []
        if self.achievements is None:
            self.achievements = []

# ============================================================================
# GAME CONFIGURATION, UTILITY & ENGINE (Aynı)
# ============================================================================
# (Bu kısımlar uzun olduğu için yer tutmaması amacıyla kısaltıldı, 
#  ancak tam kodunuzda aynı kalmalıdır.)
# ... (CELL_CONFIGS, initialize_game, MindGardenEngine sınıfları ve methodları aynı kalmıştır)

CELL_CONFIGS = {
    CellType.EMPTY: {
        'emoji': '⬜', 'color': '#F8F9FA', 'name': 'Boş Alan'
    },
    CellType.THOUGHT_CREATIVE: {
        'emoji': '🌸', 'color': '#FF6B9D', 'name': 'Yaratıcı Düşünce',
        'growth_rate': 15, 'energy_gen': 2, 'cost': 1,
        'desc': 'Hızlı büyür, çiçek açabilir'
    },
    CellType.THOUGHT_ANALYTIC: {
        'emoji': '🌿', 'color': '#4ECDC4', 'name': 'Analitik Düşünce',
        'growth_rate': 8, 'energy_gen': 1, 'cost': 1,
        'desc': 'Kaygılara dirençli'
    },
    CellType.THOUGHT_EMOTIONAL: {
        'emoji': '🌻', 'color': '#FFE66D', 'name': 'Duygusal Düşünce',
        'growth_rate': 12, 'energy_gen': 3, 'cost': 1,
        'desc': 'Komşuları güçlendirir'
    },
    CellType.THOUGHT_INTUITIVE: {
        'emoji': '🌙', 'color': '#A29BFE', 'name': 'Sezgisel Düşünce',
        'growth_rate': 10, 'energy_gen': 2, 'cost': 2,
        'desc': 'Gizli bağlantıları açar'
    },
    CellType.ANXIETY: {
        'emoji': '🐛', 'color': '#C44569', 'name': 'Kaygı',
        'desc': 'Yayılır ve zayıflatır'
    },
    CellType.JOY: {
        'emoji': '✨', 'color': '#FFA502', 'name': 'Sevinç',
        'desc': 'Enerji verir'
    },
    CellType.TRAUMA: {
        'emoji': '🌑', 'color': '#2C3A47', 'name': 'Travma Kökü',
        'desc': 'Dönüştürülmeyi bekliyor'
    },
    CellType.FLOWER: {
        'emoji': '🌺', 'color': '#FD79A8', 'name': 'Bilinç Çiçeği',
        'desc': 'Güçlü enerji kaynağı'
    },
    CellType.WISDOM: {
        'emoji': '🌳', 'color': '#00B894', 'name': 'Bilgelik Ağacı',
        'desc': 'Dönüşmüş travma - Tüm bahçeyi güçlendirir'
    }
}

class MindGardenEngine:
    def __init__(self, state: GameState):
        self.state = state
    
    def get_neighbors(self, x: int, y: int) -> List[Cell]:
        neighbors = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.state.grid_size and 0 <= ny < self.state.grid_size:
                neighbors.append(self.state.grid[ny][nx])
        return neighbors
    
    def plant_thought(self, x: int, y: int, thought_type: CellType) -> tuple[bool, str]:
        """Düşünce ek"""
        cell = self.state.grid[y][x]
        
        if cell.type != CellType.EMPTY:
            # KRİTİK: Hücre tipi kontrolü yapılıyor.
            return False, f"Bu alan dolu! ({CELL_CONFIGS[cell.type]['name']})"
        
        cost = CELL_CONFIGS[thought_type].get('cost', 1)
        if self.state.action_points < cost:
            return False, f"Yeterli AP yok! ({cost} AP gerekli)"
        
        cell.type = thought_type
        cell.health = 50
        cell.energy = 10
        cell.age = 0
        
        self.state.action_points -= cost
        self.state.total_thoughts += 1
        self.add_event(f"🌱 {CELL_CONFIGS[thought_type]['name']} ekildi ({x},{y})")
        return True, "Başarılı! Düşünce ekildi."
    
    # Diğer aksiyon metodları (water_cell, prune_anxiety, meditate, focus_joy, transform_trauma, end_turn, vb.) aynı kalmıştır.
    def water_cell(self, x: int, y: int) -> tuple[bool, str]:
        if self.state.action_points < 1:
            return False, "Yeterli AP yok!"
        cell = self.state.grid[y][x]
        if cell.type == CellType.EMPTY:
            return False, "Boş alan sulanamaz!"
        if cell.type == CellType.ANXIETY:
            return False, "Kaygı sulanamaz!"
        cell.health = min(100, cell.health + 30)
        cell.energy = min(100, cell.energy + 20)
        self.state.action_points -= 1
        self.add_event(f"💧 ({x},{y}) sulandı (+30 sağlık, +20 enerji)")
        return True, "Başarılı! Alan sulandı."
    
    def prune_anxiety(self, x: int, y: int) -> tuple[bool, str]:
        if self.state.action_points < 2:
            return False, "Yeterli AP yok! (2 AP gerekli)"
        cell = self.state.grid[y][x]
        if cell.type != CellType.ANXIETY:
            return False, "Burası kaygı değil!"
        self.state.action_points -= 2
        if random.random() < 0.75:
            cell.type = CellType.EMPTY
            cell.health = 0
            cell.energy = 0
            self.state.anxieties_cleared += 1
            self.state.consciousness_xp += 10 
            self.add_event(f"✂️ Kaygı tamamen temizlendi ({x},{y})")
            return True, "Başarılı! Kaygı yok edildi."
        else:
            cell.health = max(0, cell.health - 40)
            if cell.health == 0:
                cell.type = CellType.EMPTY
                self.state.anxieties_cleared += 1
                self.state.consciousness_xp += 10
                self.add_event(f"✂️ Kaygı budandı ve eridi ({x},{y})")
                return True, "Başarılı! Kaygı budandı ve eridi."
            self.add_event(f"✂️ Kaygı zayıflatıldı ({x},{y})")
            return True, "Başarılı! Kaygı zayıfladı."
            
    def meditate(self) -> tuple[bool, str]:
        if self.state.action_points < 3:
            return False, "Yeterli AP yok! (3 AP gerekli)"
        healed = 0
        for row in self.state.grid:
            for cell in row:
                if cell.type != CellType.EMPTY and cell.type != CellType.ANXIETY:
                    cell.energy = min(100, cell.energy + 15)
                    cell.health = min(100, cell.health + 10)
                    healed += 1
        self.state.action_points -= 3
        self.add_event(f"🧘 Meditasyon - {healed} hücre iyileşti")
        return True, f"Başarılı! {healed} hücre iyileşti."

    def focus_joy(self, x: int, y: int) -> tuple[bool, str]:
        if self.state.action_points < 2:
            return False, "Yeterli AP yok! (2 AP gerekli)"
        cell = self.state.grid[y][x]
        if cell.type != CellType.EMPTY:
            return False, "Bu alan dolu!"
        neighbors = self.get_neighbors(x, y)
        strong_thoughts = [n for n in neighbors 
                             if n.type in [CellType.THOUGHT_CREATIVE, CellType.THOUGHT_EMOTIONAL, CellType.THOUGHT_ANALYTIC, CellType.THOUGHT_INTUITIVE]
                             and n.health > 60]
        if len(strong_thoughts) < 2:
            return False, "En az 2 güçlü düşünce (sağlık > 60) gerekli!"
        cell.type = CellType.JOY
        cell.health = 80
        cell.energy = 50
        self.state.action_points -= 2
        self.add_event(f"✨ Sevinç ışığı oluşturuldu ({x},{y})")
        return True, "Başarılı! Sevinç yarattın."

    def transform_trauma(self, x: int, y: int) -> tuple[bool, str]:
        if self.state.action_points < 3:
            return False, "Yeterli AP yok! (3 AP gerekli)"
        cell = self.state.grid[y][x]
        if cell.type != CellType.TRAUMA:
            return False, "Burası travma değil!"
        neighbors = self.get_neighbors(x, y)
        strong_support = [n for n in neighbors 
                          if n.type in [CellType.THOUGHT_ANALYTIC, CellType.THOUGHT_EMOTIONAL, CellType.THOUGHT_CREATIVE, CellType.THOUGHT_INTUITIVE]
                          and n.health > 70]
        if len(strong_support) < 3:
            return False, "En az 3 güçlü destek düşünce (sağlık > 70) gerekli!"
        cell.type = CellType.WISDOM
        cell.health = 100
        cell.energy = 100
        cell.age = 0
        self.state.action_points -= 3
        self.state.consciousness_xp += 100
        self.add_event(f"🌳 TRAVMA DÖNÜŞTÜRÜLDÜ! Bilgelik Ağacı oldu ({x},{y})")
        return True, "Başarılı! Travma iyileşti."

    def end_turn(self):
        # ... (Tüm tur sonu işlemleri)
        self.state.action_points = 3
        self.add_event(f"--- Tur Bitti. Gün {self.state.day}, {self.state.time_of_day.value} ---")
        # Diğer end_turn alt methodları burada devam eder...
        self._grow_thoughts()
        self._spread_anxiety()
        self._apply_neighbor_effects()
        self._apply_joy_effects()
        self._apply_wisdom_effects()
        self._check_flower_bloom()
        self._age_cells()
        self._advance_time()
        self._calculate_total_energy()
        self._update_consciousness()
        
        if random.random() < 0.25:
            self._trigger_random_event()
        
        self._check_achievements()
        self.add_event(f"--- Tur Bitti. Gün {self.state.day}, {self.state.time_of_day.value} ---")

    def add_event(self, message: str):
        self.state.event_log.append(message)
        if len(self.state.event_log) > 15:
            self.state.event_log.pop(0)

# (Diğer yardımcı fonksiyonlar aynı kalmıştır)

def initialize_game():
    state = GameState()
    engine = MindGardenEngine(state)
    size = state.grid_size
    # Düşünce, Kaygı, Travma ekleme...
    for _ in range(2):
        x, y = get_random_empty_coords(state.grid, size)
        thought_type = random.choice([CellType.THOUGHT_CREATIVE, CellType.THOUGHT_ANALYTIC])
        state.grid[y][x].type = thought_type
        state.grid[y][x].health = 60
        state.grid[y][x].energy = 20
    x, y = get_random_empty_coords(state.grid, size)
    state.grid[y][x].type = CellType.ANXIETY
    state.grid[y][x].health = 45
    x, y = get_random_empty_coords(state.grid, size)
    state.grid[y][x].type = CellType.TRAUMA
    state.grid[y][x].health = 100
    engine.add_event("🌱 Zihin bahçesi oluşturuldu")
    engine.add_event("💡 İlk düşünceler ekildi")
    engine.add_event("⚠️ Bir kaygı ve bir travma var")
    return state

# ============================================================================
# VISUALIZATION (Aynı)
# ============================================================================

def create_garden_visualization(state: GameState):
    # ... (Plotly görselleştirme kodu aynı kalmıştır)
    z_data = []
    hover_text = []
    
    color_map = {
        CellType.EMPTY: 0,
        CellType.ANXIETY: 1,
        CellType.TRAUMA: 2,
        CellType.THOUGHT_CREATIVE: 3,
        CellType.THOUGHT_ANALYTIC: 4,
        CellType.THOUGHT_EMOTIONAL: 5,
        CellType.THOUGHT_INTUITIVE: 6,
        CellType.JOY: 7,
        CellType.FLOWER: 8,
        CellType.WISDOM: 9
    }

    z_colors = [[color_map.get(cell.type, 0) for cell in row] for row in state.grid]

    for y, row in enumerate(state.grid):
        z_row = []
        hover_row = []
        
        for x, cell in enumerate(row):
            config = get_cell_config(cell.type)
            z_value = color_map.get(cell.type, 0)
            z_row.append(z_value)
            
            hover_row.append(
                f"{config['emoji']} {config['name']}<br>"
                f"Konum: ({x},{y})<br>"
                f"Sağlık: {cell.health}/100<br>"
                f"Enerji: {cell.energy}/100<br>"
                f"Yaş: {cell.age} tur"
            )
        
        z_data.append(z_row)
        hover_text.append(hover_row)
    
    colorscale_values = [
        [0.0, CELL_CONFIGS[CellType.EMPTY]['color']],
        [0.1, CELL_CONFIGS[CellType.ANXIETY]['color']],
        [0.2, CELL_CONFIGS[CellType.TRAUMA]['color']],
        [0.3, CELL_CONFIGS[CellType.THOUGHT_CREATIVE]['color']],
        [0.4, CELL_CONFIGS[CellType.THOUGHT_ANALYTIC]['color']],
        [0.5, CELL_CONFIGS[CellType.THOUGHT_EMOTIONAL]['color']],
        [0.6, CELL_CONFIGS[CellType.THOUGHT_INTUITIVE]['color']],
        [0.7, CELL_CONFIGS[CellType.JOY]['color']],
        [0.8, CELL_CONFIGS[CellType.FLOWER]['color']],
        [1.0, CELL_CONFIGS[CellType.WISDOM]['color']]
    ]
    
    max_val = max(color_map.values()) if max(color_map.values()) > 0 else 1
    normalized_z = [[val / max_val for val in row] for row in z_colors]


    fig = go.Figure(data=go.Heatmap(
        z=normalized_z,
        text=[[get_cell_config(cell.type)['emoji'] for cell in row] for row in state.grid],
        hovertext=hover_text,
        hoverinfo='text',
        colorscale=colorscale_values,
        showscale=False,
        texttemplate='%{text}',
        textfont={"size": 28}
    ))
    
    fig.update_layout(
        width=600,
        height=600,
        xaxis=dict(showgrid=True, zeroline=False, showticklabels=True, 
                   tickmode='linear', tick0=0, dtick=1, side='top'),
        yaxis=dict(showgrid=True, zeroline=False, showticklabels=True,
                   tickmode='linear', tick0=0, dtick=1, autorange='reversed'),
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='#E8F4F8'
    )
    
    return fig

# ============================================================================
# ACTION HANDLER & CALLBACKS (Aynı)
# ============================================================================

def handle_action(action_type, x, y, thought_type=None):
    """Merkezi aksiyon tetikleyici."""
    state = st.session_state.game_state
    engine = MindGardenEngine(state)
    
    success, msg = False, "Bilinmeyen aksiyon."
    
    if action_type == "plant" and thought_type:
        success, msg = engine.plant_thought(x, y, thought_type)
    elif action_type == "water":
        success, msg = engine.water_cell(x, y)
    elif action_type == "prune":
        success, msg = engine.prune_anxiety(x, y)
    elif action_type == "meditate":
        success, msg = engine.meditate()
    elif action_type == "focus_joy":
        success, msg = engine.focus_joy(x, y)
    elif action_type == "transform":
        success, msg = engine.transform_trauma(x, y)
    elif action_type == "end_turn":
        engine.end_turn()
        msg = "Tur bitti! Bahçe gelişti."
        success = True 

    st.session_state.message = msg
    return success

def set_action_callback(action_type: str, thought_type: CellType = None):
    """Buton aksiyonunu session state'e kaydeder ve formu submit etmeye zorlar."""
    st.session_state.action_clicked = True
    st.session_state.next_action = action_type
    st.session_state.thought_type = thought_type

# ============================================================================
# COORDINATE UPDATE CALLBACK (Yeni Yardımcı Fonksiyon)
# ============================================================================

def update_selected_cell():
    """X ve Y girişleri değiştiğinde seçili hücreyi günceller."""
    # new_x ve new_y, st.number_input'ların key'leri aracılığıyla session_state'den alınır.
    if 'inp_x' in st.session_state and 'inp_y' in st.session_state:
        st.session_state.selected_cell = (st.session_state.inp_x, st.session_state.inp_y)
        # Sadece koordinat değiştiğinde mesajı temizlemeye gerek yok, bu kullanıcının bilgiyi okumasını engeller.


# ============================================================================
# MAIN APPLICATION LOGIC (Güncellenmiş)
# ============================================================================

def main():
    st.set_page_config(page_title="Zihin Bahçesi", page_icon="🌱", layout="wide")
    
    # CSS (Aynı)
    st.markdown("""
        <style>
        .main {background-color: #F5F7FA;}
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            height: 3em;
            font-size: 15px;
            font-weight: 500;
        }
        .metric-card {
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stPlotlyChart {
            border: 2px solid #DDDDDD; 
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # **KRİTİK BAŞLANGIÇ DURUMU KONTROLÜ**
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
        st.session_state.game_state = None 
        st.session_state.message = "Yeni bir zihin bahçesi kurmaya hazır mısınız?"
        st.session_state.selected_cell = (3, 3) # Varsayılan başlangıç hücresi
        st.session_state.next_action = None 
        st.session_state.thought_type = None 
        st.session_state.action_clicked = False 

    
    # Yeni Oyun Başlatma Düğmesi (Aynı)
    st.sidebar.title("Kontrol")
    if st.sidebar.button("🔄 Yeni Oyun Başlat", help="Mevcut oyunu sıfırlar.", type="secondary"):
        st.session_state.clear()
        st.session_state.game_started = False
        st.session_state.selected_cell = (3, 3)
        st.session_state.message = "Yeni bir zihin bahçesi kurmaya hazır mısınız?"
        st.session_state.next_action = None
        st.session_state.thought_type = None
        st.session_state.action_clicked = False
        st.rerun()

    # Oyun Başlangıç Ekranı (Aynı)
    if not st.session_state.game_started:
        display_how_to_play() 
        return

    # Oyun Başladı
    state = st.session_state.game_state
    
    st.title("🌱 ZİHİN BAHÇESİ")
    st.caption("Zihninizi büyütün, kaygıları yönetin, bilincinizi yükseltin")
    
    # Üst Bilgi Metrikleri (Aynı)
    xp_needed = state.consciousness_level * 100
    xp_progress = min(1.0, state.consciousness_xp / xp_needed) 
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Gün", state.day)
    with col2:
        st.metric("Bilinç", f"Lvl {state.consciousness_level}", f"{xp_progress*100:.0f}% XP")
    with col3:
        st.metric("Enerji", f"{state.total_energy}")
    with col4:
        st.metric("AP", f"{state.action_points}/3")
    with col5:
        st.metric("Zaman", state.time_of_day.value)
    
    # Aksiyon Mesajları (Aynı)
    if st.session_state.message:
        if "Başarılı" in st.session_state.message or "iyileşti" in st.session_state.message or "yok edildi" in st.session_state.message or "yarattın" in st.session_state.message or "dönüştürüldü" in st.session_state.message or "Tur bitti" in st.session_state.message:
            st.success(st.session_state.message)
        elif "Yeterli AP" in st.session_state.message or "dolu" in st.session_state.message or "gerekli" in st.session_state.message or "değil" in st.session_state.message:
            st.warning(st.session_state.message)
        else:
            st.info(st.session_state.message)
            
    
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.subheader("🗺️ Zihin Haritası")
        fig = create_garden_visualization(state)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("📜 Olay Günlüğü")
        log_html = ""
        for entry in reversed(state.event_log):
            log_html += f"<li>{entry}</li>"
        st.markdown(f"<ul style='font-size: 14px; list-style-type: none; padding-left: 0;'>{log_html}</ul>",
                    unsafe_allow_html=True)
    
    with col_right:
        st.subheader("🎯 Seçili Alan Kontrolü")
        
        # **KRİTİK DÜZELTME: KOORDİNAT SEÇİMİ**
        # Kullanıcının en son seçtiği koordinatı al
        x, y = st.session_state.selected_cell
        
        with st.expander("Koordinat Seç", expanded=True):
            col_x, col_y = st.columns(2)
            with col_x:
                # X Koordinatını güncelleyen input. on_change ile update_selected_cell'i çağırır.
                st.number_input("X Koordinat", 0, state.grid_size-1, x, key="inp_x", on_change=update_selected_cell)
            with col_y:
                # Y Koordinatını güncelleyen input. on_change ile update_selected_cell'i çağırır.
                st.number_input("Y Koordinat", 0, state.grid_size-1, y, key="inp_y", on_change=update_selected_cell)
            
            # Koordinat güncellenmiş olabilir, tekrar alıyoruz
            x, y = st.session_state.selected_cell 

        cell = state.grid[y][x]
        config = get_cell_config(cell.type)
        
        # Hücre Bilgisi (Aynı)
        st.markdown(f"""
        <div style='background: white; padding: 15px; border-radius: 10px; border-left: 4px solid {config['color']}'>
            <h3>{config['emoji']} {config['name']}</h3>
            <p><b>Konum:</b> ({x}, {y})</p>
            <p><b>Sağlık:</b> {cell.health}/100</p>
            <p><b>Enerji:</b> {cell.energy}/100</p>
            <p><b>Yaş:</b> {cell.age} tur</p>
            <p><i>{config.get('desc', '')}</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")

        # AKSİYON FORMU (Aynı, çünkü sorun burada değildi)
        
        with st.form(key="action_form"):
            st.markdown("### 🛠️ Aksiyon Seç")
            tab_plant, tab_action, tab_special = st.tabs(["🌱 EKME", "💧 TEMEL AKSİYON", "✨ İLERİ TEKNİKLER"])
            
            with tab_plant:
                st.write("Düşünce Türü Seç (Boş Alan Gerekir):")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.form_submit_button("🌸 Yaratıcı (1 AP)", help="Yaratıcı Düşünce Eker", use_container_width=True, 
                                          on_click=set_action_callback, args=("plant", CellType.THOUGHT_CREATIVE), key="btn_plant_c")
                    
                    st.form_submit_button("🌻 Duygusal (1 AP)", help="Duygusal Düşünce Eker", use_container_width=True,
                                          on_click=set_action_callback, args=("plant", CellType.THOUGHT_EMOTIONAL), key="btn_plant_e")
                
                with col_b:
                    st.form_submit_button("🌿 Analitik (1 AP)", help="Analitik Düşünce Eker", use_container_width=True,
                                          on_click=set_action_callback, args=("plant", CellType.THOUGHT_ANALYTIC), key="btn_plant_a")
                    
                    st.form_submit_button("🌙 Sezgisel (2 AP)", help="Sezgisel Düşünce Eker (Yüksek AP)", use_container_width=True,
                                          on_click=set_action_callback, args=("plant", CellType.THOUGHT_INTUITIVE), key="btn_plant_i")
            
            with tab_action:
                st.write("Temel Bakım ve Kaygı Yönetimi:")
                
                st.form_submit_button("💧 Sula (1 AP)", help="Sağlık ve Enerji Verir", use_container_width=True,
                                      on_click=set_action_callback, args=("water",), key="btn_water")
                
                st.form_submit_button("✂️ Kaygı Buda (2 AP)", help="Kaygıyı Zayıflatır/Temizler", use_container_width=True,
                                      on_click=set_action_callback, args=("prune",), key="btn_prune")
                
                st.markdown("---")
                st.form_submit_button("🧘 Meditasyon - Tüm Bahçe (3 AP)", help="Tüm pozitif alanları iyileştirir", use_container_width=True,
                                      on_click=set_action_callback, args=("meditate",), key="btn_meditate")
            
            with tab_special:
                st.write("Gelişmiş Teknikler (Yüksek Etki):")
                
                st.form_submit_button("✨ Sevinç Işığı Oluştur (2 AP)", help="En az 2 güçlü düşünce gerektirir", use_container_width=True,
                                      on_click=set_action_callback, args=("focus_joy",), key="btn_joy")
                
                st.form_submit_button("🌳 Travma Dönüştür (3 AP)", help="Travma Kökünü Bilgeliğe dönüştürür. En az 3 güçlü destek gerektirir.", use_container_width=True,
                                      on_click=set_action_callback, args=("transform",), key="btn_transform")

        # AKSİYON İŞLEME VE TEMİZLEME (Aynı)
        if st.session_state.action_clicked and st.session_state.next_action:
            handle_action(st.session_state.next_action, x, y, st.session_state.thought_type)
            st.session_state.next_action = None
            st.session_state.thought_type = None
            st.session_state.action_clicked = False 
            st.rerun()

        # TUR BİTİR BUTONU (Aynı)
        if st.button("⏭️ TURU BİTİR VE İLERLE", type="primary", use_container_width=True):
            handle_action("end_turn", x, y)
            st.rerun() 
        
        st.markdown("---")
        
        # İstatistikler ve Başarımlar (Aynı)
        engine = MindGardenEngine(state)
        stats = engine.get_stats()
        with st.expander("📊 Bahçe İstatistikleri", expanded=False):
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.metric("🌱 Düşünceler", stats['thoughts'])
                st.metric("🌺 Çiçekler", stats['flowers'])
                st.metric("✨ Sevinç", stats['joy'])
            with col_s2:
                st.metric("🐛 Kaygı", stats['anxiety'])
                st.metric("🌑 Travma", stats['trauma'])
                st.metric("🌳 Bilgelik", stats['wisdom'])
        
        with st.expander("🏆 Başarımlar", expanded=False):
            achievement_list = []
            ACHIEVEMENTS_INFO = {
                'first_flower': {'name': 'İlk Çiçek', 'emoji': '🌺', 'desc': 'İlk bilinç çiçeğini açtı'},
                'day_10': {'name': '10 Gün', 'emoji': '📅', 'desc': '10 gün hayatta kaldı'},
                'gardener': {'name': 'Bahçıvan', 'emoji': '👨‍🌾', 'desc': '15 düşünce ekti'},
                'anxiety_master': {'name': 'Kaygı Ustası', 'emoji': '✂️', 'desc': '10 kaygıyı temizledi'},
                'flower_power': {'name': 'Çiçek Gücü', 'emoji': '💐', 'desc': '5 çiçek açtı'},
                'level_3': {'name': 'Bilinçli', 'emoji': '🧠', 'desc': 'Bilinç seviyesi 3e ulaştı'},
                'zen_master': {'name': 'Zen Ustası', 'emoji': '🧘', 'desc': '20 kez meditasyon yaptı'}
            }
            for key in ACHIEVEMENTS_INFO:
                info = ACHIEVEMENTS_INFO[key]
                is_unlocked = key in state.achievements
                status_emoji = "✅" if is_unlocked else "🔒"
                status_text = "Açıldı" if is_unlocked else "Kilitli"
                color = "#00B894" if is_unlocked else "#999999"
                
                achievement_list.append(f"""
                <div style='display: flex; align-items: center; margin-bottom: 5px; background: #FFFFFF; padding: 5px; border-radius: 5px; border-left: 3px solid {color};'>
                    <span style='font-size: 20px; margin-right: 10px;'>{info['emoji']}</span>
                    <div style='flex-grow: 1;'>
                        <b>{info['name']}</b>
                        <p style='font-size: 12px; margin: 0;'>{info['desc']}</p>
                    </div>
                    <span style='font-size: 12px; font-weight: bold; color: {color};'>{status_emoji} {status_text}</span>
                </div>
                """)
            
            st.markdown("".join(achievement_list), unsafe_allow_html=True)


if __name__ == "__main__":
    main()

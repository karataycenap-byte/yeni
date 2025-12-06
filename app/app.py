import streamlit as st
import random
import json
from enum import Enum
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import plotly.graph_objects as go
import copy

# ============================================================================
# GAME CONSTANTS & ENUMS
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

class TimeOfDay(Enum):
    MORNING = "Sabah"
    NOON = "Ogle"
    EVENING = "Aksam"
    NIGHT = "Gece"

# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Cell:
    type: CellType
    health: int = 50
    energy: int = 0
    age: int = 0
    x: int = 0
    y: int = 0
    
    def to_dict(self):
        return {
            'type': self.type.value,
            'health': self.health,
            'energy': self.energy,
            'age': self.age,
            'x': self.x,
            'y': self.y
        }
    
    @staticmethod
    def from_dict(data):
        cell = Cell(
            type=CellType(data['type']),
            health=data['health'],
            energy=data['energy'],
            age=data['age'],
            x=data['x'],
            y=data['y']
        )
        return cell

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
    
    def __post_init__(self):
        if self.grid is None:
            self.grid = [[Cell(CellType.EMPTY, x=x, y=y) for x in range(self.grid_size)] 
                        for y in range(self.grid_size)]
        if self.event_log is None:
            self.event_log = []
        if self.achievements is None:
            self.achievements = []

# ============================================================================
# GAME CONFIGURATION
# ============================================================================

CELL_CONFIGS = {
    CellType.EMPTY: {
        'emoji': '⬜', 'color': '#F8F9FA', 'name': 'Bos'
    },
    CellType.THOUGHT_CREATIVE: {
        'emoji': '🌸', 'color': '#FF6B9D', 'name': 'Yaratici Dusunce',
        'growth_rate': 15, 'energy_gen': 2, 'cost': 1
    },
    CellType.THOUGHT_ANALYTIC: {
        'emoji': '🌿', 'color': '#4ECDC4', 'name': 'Analitik Dusunce',
        'growth_rate': 8, 'energy_gen': 1, 'cost': 1
    },
    CellType.THOUGHT_EMOTIONAL: {
        'emoji': '🌻', 'color': '#FFE66D', 'name': 'Duygusal Dusunce',
        'growth_rate': 12, 'energy_gen': 3, 'cost': 1
    },
    CellType.THOUGHT_INTUITIVE: {
        'emoji': '🌙', 'color': '#A29BFE', 'name': 'Sezgisel Dusunce',
        'growth_rate': 10, 'energy_gen': 2, 'cost': 2
    },
    CellType.ANXIETY: {
        'emoji': '🐛', 'color': '#C44569', 'name': 'Kaygi'
    },
    CellType.JOY: {
        'emoji': '✨', 'color': '#FFA502', 'name': 'Sevinc'
    },
    CellType.TRAUMA: {
        'emoji': '🌑', 'color': '#2C3A47', 'name': 'Travma Koku'
    },
    CellType.FLOWER: {
        'emoji': '🌺', 'color': '#FD79A8', 'name': 'Bilinc Cicegi'
    }
}

# ============================================================================
# GAME ENGINE
# ============================================================================

class MindGardenEngine:
    def __init__(self, state: GameState):
        self.state = state
    
    def get_neighbors(self, x: int, y: int) -> List[Cell]:
        """Komsu hucreleri dondur"""
        neighbors = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.state.grid_size and 0 <= ny < self.state.grid_size:
                neighbors.append(self.state.grid[ny][nx])
        return neighbors
    
    def plant_thought(self, x: int, y: int, thought_type: CellType) -> bool:
        """Dusunce ek"""
        cell = self.state.grid[y][x]
        if cell.type != CellType.EMPTY:
            return False
        
        cost = CELL_CONFIGS[thought_type].get('cost', 1)
        if self.state.action_points < cost:
            return False
        
        cell.type = thought_type
        cell.health = 50
        cell.energy = 10
        cell.age = 0
        
        self.state.action_points -= cost
        self.add_event(f"Ekildi: {CELL_CONFIGS[thought_type]['name']} ({x},{y})")
        return True
    
    def water_cell(self, x: int, y: int) -> bool:
        """Hucreyi sula"""
        if self.state.action_points < 1:
            return False
        
        cell = self.state.grid[y][x]
        if cell.type == CellType.EMPTY or cell.type == CellType.ANXIETY:
            return False
        
        cell.health = min(100, cell.health + 25)
        cell.energy = min(100, cell.energy + 15)
        
        self.state.action_points -= 1
        self.add_event(f"Sulandi: ({x},{y})")
        return True
    
    def prune_anxiety(self, x: int, y: int) -> bool:
        """Kaygiyi buda"""
        if self.state.action_points < 2:
            return False
        
        cell = self.state.grid[y][x]
        if cell.type != CellType.ANXIETY:
            return False
        
        if random.random() < 0.7:
            cell.type = CellType.EMPTY
            cell.health = 0
            cell.energy = 0
            self.add_event(f"Kaygi budandi ({x},{y})")
        else:
            cell.health -= 30
            self.add_event(f"Kaygi zayiflatildi ({x},{y})")
        
        self.state.action_points -= 2
        return True
    
    def meditate(self) -> bool:
        """Meditasyon yap"""
        if self.state.action_points < 3:
            return False
        
        for row in self.state.grid:
            for cell in row:
                if cell.type != CellType.EMPTY:
                    cell.energy = min(100, cell.energy + 10)
                    cell.health = min(100, cell.health + 5)
        
        self.state.action_points -= 3
        self.add_event("Meditasyon yapildi - Tum bahce sakinlesti")
        return True
    
    def end_turn(self):
        """Turu bitir ve oyun dongusunu calistir"""
        self._grow_thoughts()
        self._spread_anxiety()
        self._apply_neighbor_effects()
        self._check_flower_bloom()
        self._age_cells()
        self._advance_time()
        self.state.action_points = 3
        self._calculate_total_energy()
        self._update_consciousness()
        
        if random.random() < 0.2:
            self._trigger_random_event()
        
        self._check_achievements()
    
    def _grow_thoughts(self):
        """Dusunceleri buyut"""
        time_multiplier = {
            TimeOfDay.MORNING: 1.5,
            TimeOfDay.NOON: 1.0,
            TimeOfDay.EVENING: 0.8,
            TimeOfDay.NIGHT: 0.5
        }[self.state.time_of_day]
        
        for row in self.state.grid:
            for cell in row:
                if cell.type in [CellType.THOUGHT_CREATIVE, CellType.THOUGHT_ANALYTIC, 
                                CellType.THOUGHT_EMOTIONAL, CellType.THOUGHT_INTUITIVE]:
                    growth = CELL_CONFIGS[cell.type]['growth_rate'] * time_multiplier
                    cell.health = min(100, cell.health + growth)
                    
                    if cell.health > 60:
                        energy_gen = CELL_CONFIGS[cell.type]['energy_gen']
                        cell.energy = min(100, cell.energy + energy_gen)
    
    def _spread_anxiety(self):
        """Kaygilari yayil"""
        new_anxieties = []
        
        for row in self.state.grid:
            for cell in row:
                if cell.type == CellType.ANXIETY and cell.health > 30:
                    neighbors = self.get_neighbors(cell.x, cell.y)
                    empty_neighbors = [n for n in neighbors if n.type == CellType.EMPTY]
                    
                    if empty_neighbors and random.random() < 0.3:
                        target = random.choice(empty_neighbors)
                        new_anxieties.append((target.x, target.y))
        
        for x, y in new_anxieties:
            self.state.grid[y][x].type = CellType.ANXIETY
            self.state.grid[y][x].health = 40
            self.add_event(f"Kaygi yayildi ({x},{y})")
    
    def _apply_neighbor_effects(self):
        """Komsu etkilerini uygula"""
        for row in self.state.grid:
            for cell in row:
                if cell.type == CellType.EMPTY:
                    continue
                
                neighbors = self.get_neighbors(cell.x, cell.y)
                
                if cell.type == CellType.ANXIETY:
                    strong_thoughts = [n for n in neighbors 
                                      if n.type in [CellType.THOUGHT_ANALYTIC, CellType.THOUGHT_CREATIVE]
                                      and n.health > 70]
                    if strong_thoughts:
                        cell.health -= len(strong_thoughts) * 5
                        if cell.health <= 0:
                            cell.type = CellType.EMPTY
                            self.add_event(f"Kaygi guclu dusuncelerle eridi ({cell.x},{cell.y})")
                
                if cell.type == CellType.THOUGHT_EMOTIONAL and cell.health > 70:
                    for neighbor in neighbors:
                        if neighbor.type in [CellType.THOUGHT_CREATIVE, CellType.THOUGHT_ANALYTIC]:
                            neighbor.energy = min(100, neighbor.energy + 2)
    
    def _check_flower_bloom(self):
        """Cicek acma kontrolu"""
        for row in self.state.grid:
            for cell in row:
                if cell.type == CellType.THOUGHT_CREATIVE and cell.health >= 90 and cell.age >= 5:
                    if random.random() < 0.15:
                        cell.type = CellType.FLOWER
                        cell.health = 100
                        cell.energy = 50
                        self.add_event(f"BILINC CICEGI ACTI! ({cell.x},{cell.y})")
                        self.state.consciousness_xp += 50
    
    def _age_cells(self):
        """Hucreleri yaslandir"""
        for row in self.state.grid:
            for cell in row:
                if cell.type != CellType.EMPTY:
                    cell.age += 1
    
    def _advance_time(self):
        """Zamani ilerlet"""
        times = list(TimeOfDay)
        current_idx = times.index(self.state.time_of_day)
        next_idx = (current_idx + 1) % len(times)
        self.state.time_of_day = times[next_idx]
        
        if self.state.time_of_day == TimeOfDay.MORNING:
            self.state.day += 1
            self.add_event(f"Gun {self.state.day} basladi")
    
    def _calculate_total_energy(self):
        """Toplam enerji hesapla"""
        total = 0
        for row in self.state.grid:
            for cell in row:
                total += cell.energy
        self.state.total_energy = total
    
    def _update_consciousness(self):
        """Bilinc seviyesi guncelle"""
        xp_needed = self.state.consciousness_level * 100
        if self.state.consciousness_xp >= xp_needed:
            self.state.consciousness_level += 1
            self.state.consciousness_xp = 0
            self.add_event(f"BILINC SEVIYESI {self.state.consciousness_level}!")
    
    def _trigger_random_event(self):
        """Rastgele olay tetikle"""
        events = [
            ("Yagmur", "Tum dusunceler +10 saglik aldi"),
            ("Kelebek Surusu", "Rastgele bos alana tohum birakildi"),
            ("Gunes", "Enerji +20")
        ]
        
        event_name, description = random.choice(events)
        
        if "Yagmur" in event_name:
            for row in self.state.grid:
                for cell in row:
                    if cell.type in [CellType.THOUGHT_CREATIVE, CellType.THOUGHT_ANALYTIC,
                                    CellType.THOUGHT_EMOTIONAL, CellType.THOUGHT_INTUITIVE]:
                        cell.health = min(100, cell.health + 10)
        
        elif "Kelebek" in event_name:
            empty_cells = [(x, y) for y, row in enumerate(self.state.grid) 
                          for x, cell in enumerate(row) if cell.type == CellType.EMPTY]
            if empty_cells:
                x, y = random.choice(empty_cells)
                thought_types = [CellType.THOUGHT_CREATIVE, CellType.THOUGHT_ANALYTIC,
                               CellType.THOUGHT_EMOTIONAL]
                self.state.grid[y][x].type = random.choice(thought_types)
                self.state.grid[y][x].health = 30
        
        self.add_event(f"{event_name}: {description}")
    
    def _check_achievements(self):
        """Basarilari kontrol et"""
        if "first_flower" not in self.state.achievements:
            for row in self.state.grid:
                if any(cell.type == CellType.FLOWER for cell in row):
                    self.state.achievements.append("first_flower")
                    self.add_event("BASARI: Ilk Cicek!")
                    break
        
        if self.state.day >= 10 and "day_10" not in self.state.achievements:
            self.state.achievements.append("day_10")
            self.add_event("BASARI: 10 Gun Hayatta!")
        
        thought_count = sum(1 for row in self.state.grid for cell in row 
                          if cell.type in [CellType.THOUGHT_CREATIVE, CellType.THOUGHT_ANALYTIC,
                                          CellType.THOUGHT_EMOTIONAL, CellType.THOUGHT_INTUITIVE])
        if thought_count >= 15 and "gardener" not in self.state.achievements:
            self.state.achievements.append("gardener")
            self.add_event("BASARI: Bahcivan Ustasi!")
    
    def add_event(self, message: str):
        """Olay logu ekle"""
        self.state.event_log.append(message)
        if len(self.state.event_log) > 10:
            self.state.event_log.pop(0)
    
    def get_stats(self) -> Dict:
        """Istatistikleri getir"""
        stats = {
            'thoughts': 0,
            'anxiety': 0,
            'joy': 0,
            'flowers': 0,
            'trauma': 0
        }
        
        for row in self.state.grid:
            for cell in row:
                if cell.type in [CellType.THOUGHT_CREATIVE, CellType.THOUGHT_ANALYTIC,
                               CellType.THOUGHT_EMOTIONAL, CellType.THOUGHT_INTUITIVE]:
                    stats['thoughts'] += 1
                elif cell.type == CellType.ANXIETY:
                    stats['anxiety'] += 1
                elif cell.type == CellType.JOY:
                    stats['joy'] += 1
                elif cell.type == CellType.FLOWER:
                    stats['flowers'] += 1
                elif cell.type == CellType.TRAUMA:
                    stats['trauma'] += 1
        
        return stats

# ============================================================================
# VISUALIZATION
# ============================================================================

def get_cell_config(cell_type: CellType) -> Dict:
    """Hucre config'ini guvenli sekilde getir"""
    if cell_type in CELL_CONFIGS:
        return CELL_CONFIGS[cell_type]
    else:
        return CELL_CONFIGS[CellType.EMPTY]

def create_garden_visualization(state: GameState):
    """Bahce gorsellestirmesi olustur"""
    z_data = []
    hover_text = []
    
    for y, row in enumerate(state.grid):
        z_row = []
        hover_row = []
        
        for x, cell in enumerate(row):
            config = get_cell_config(cell.type)
            z_row.append(cell.health)
            hover_row.append(
                f"{config['emoji']} {config['name']}<br>"
                f"Saglik: {cell.health}<br>"
                f"Enerji: {cell.energy}<br>"
                f"Yas: {cell.age}"
            )
        
        z_data.append(z_row)
        hover_text.append(hover_row)
    
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        text=[[get_cell_config(cell.type)['emoji'] for cell in row] for row in state.grid],
        hovertext=hover_text,
        hoverinfo='text',
        colorscale=[[0, '#F8F9FA'], [1, '#4ECDC4']],
        showscale=False,
        texttemplate='%{text}',
        textfont={"size": 24}
    ))
    
    fig.update_layout(
        width=500,
        height=500,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='#F0F0F0'
    )
    
    return fig

# ============================================================================
# STREAMLIT APP
# ============================================================================

def initialize_game():
    """Yeni oyun baslat"""
    state = GameState()
    engine = MindGardenEngine(state)
    
    for _ in range(3):
        x, y = random.randint(0, 6), random.randint(0, 6)
        thought_type = random.choice([CellType.THOUGHT_CREATIVE, CellType.THOUGHT_ANALYTIC])
        state.grid[y][x].type = thought_type
        state.grid[y][x].health = 50
    
    x, y = random.randint(0, 6), random.randint(0, 6)
    state.grid[y][x].type = CellType.ANXIETY
    state.grid[y][x].health = 40
    
    engine.add_event("Bahce olusturuldu. Yolculugun basladi...")
    
    return state

def main():
    st.set_page_config(page_title="Zihin Bahcesi", page_icon="🌱", layout="wide")
    
    st.markdown("""
        <style>
        .main {background-color: #F5F7FA;}
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            height: 3em;
            font-size: 16px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if 'game_state' not in st.session_state:
        st.session_state.game_state = initialize_game()
    
    if 'selected_cell' not in st.session_state:
        st.session_state.selected_cell = None
    
    state = st.session_state.game_state
    engine = MindGardenEngine(state)
    
    st.title("🌱 ZIHIN BAHCESI")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Gun", state.day)
    with col2:
        st.metric("Bilinc Seviyesi", f"Lvl {state.consciousness_level}")
    with col3:
        st.metric("Enerji", f"{state.total_energy}")
    with col4:
        st.metric("Zaman", state.time_of_day.value)
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("🗺️ Bahcen")
        
        fig = create_garden_visualization(state)
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("**Hucre Sec:**")
        col_x, col_y = st.columns(2)
        with col_x:
            sel_x = st.number_input("X", 0, state.grid_size-1, 0, key="sel_x")
        with col_y:
            sel_y = st.number_input("Y", 0, state.grid_size-1, 0, key="sel_y")
        
        if st.button("Hucreyi Sec"):
            st.session_state.selected_cell = (sel_x, sel_y)
        
        if st.session_state.selected_cell:
            x, y = st.session_state.selected_cell
            cell = state.grid[y][x]
            config = get_cell_config(cell.type)
            
            st.info(f"**Secili:** {config['emoji']} {config['name']} ({x},{y})\n\n"
                   f"Saglik: {cell.health} | Enerji: {cell.energy} | Yas: {cell.age}")
    
    with col_right:
        st.subheader(f"⚡ Aksiyonlar (AP: {state.action_points}/3)")
        
        st.write("**Ekme (1 AP)**")
        plant_col1, plant_col2 = st.columns(2)
        with plant_col1:
            if st.button("🌸 Yaratici"):
                if st.session_state.selected_cell:
                    x, y = st.session_state.selected_cell
                    engine.plant_thought(x, y, CellType.THOUGHT_CREATIVE)
                    st.rerun()
            if st.button("🌿 Analitik"):
                if st.session_state.selected_cell:
                    x, y = st.session_state.selected_cell
                    engine.plant_thought(x, y, CellType.THOUGHT_ANALYTIC)
                    st.rerun()
        with plant_col2:
            if st.button("🌻 Duygusal"):
                if st.session_state.selected_cell:
                    x, y = st.session_state.selected_cell
                    engine.plant_thought(x, y, CellType.THOUGHT_EMOTIONAL)
                    st.rerun()
            if st.button("🌙 Sezgisel (2AP)"):
                if st.session_state.selected_cell:
                    x, y = st.session_state.selected_cell
                    engine.plant_thought(x, y, CellType.THOUGHT_INTUITIVE)
                    st.rerun()
        
        st.divider()
        
        if st.button("💧 Sula (1 AP)"):
            if st.session_state.selected_cell:
                x, y = st.session_state.selected_cell
                engine.water_cell(x, y)
                st.rerun()
        
        if st.button("✂️ Kaygi Buda (2 AP)"):
            if st.session_state.selected_cell:
                x, y = st.session_state.selected_cell
                engine.prune_anxiety(x, y)
                st.rerun()
        
        if st.button("🧘 Meditasyon (3 AP)"):
            engine.meditate()
            st.rerun()
        
        st.divider()
        
        if st.button("⏭️ TURU BITIR", type="primary"):
            engine.end_turn()
            st.session_state.selected_cell = None
            st.rerun()
        
        st.divider()
        
        st.subheader("📊 Istatistikler")
        stats = engine.get_stats()
        st.write(f"🌱 Dusunceler: {stats['thoughts']}")
        st.write(f"🐛 Kaygilar: {stats['anxiety']}")
        st.write(f"🌺 Cicekler: {stats['flowers']}")
        st.write(f"✨ Sevinçler: {stats['joy']}")
        
        if state.achievements:
            st.subheader("🏆 Basarilar")
            for ach in state.achievements:
                st.write(f"✓ {ach}")
        
        st.subheader("📜 Son Olaylar")
        for event in reversed(state.event_log[-5:]):
            st.caption(event)
        
        st.divider()
        if st.button("🔄 Yeni Oyun"):
            st.session_state.game_state = initialize_game()
            st.session_state.selected_cell = None
            st.rerun()

if __name__ == "__main__":
    main()

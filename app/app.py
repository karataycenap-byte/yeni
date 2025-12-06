import streamlit as st
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict
import plotly.graph_objects as go

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
    WISDOM = "wisdom"

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
# GAME CONFIGURATION
# ============================================================================

CELL_CONFIGS = {
    CellType.EMPTY: {
        'emoji': '⬜', 'color': '#F8F9FA', 'name': 'Bos Alan'
    },
    CellType.THOUGHT_CREATIVE: {
        'emoji': '🌸', 'color': '#FF6B9D', 'name': 'Yaratici Dusunce',
        'growth_rate': 15, 'energy_gen': 2, 'cost': 1,
        'desc': 'Hizli buyur, cicek acabilir'
    },
    CellType.THOUGHT_ANALYTIC: {
        'emoji': '🌿', 'color': '#4ECDC4', 'name': 'Analitik Dusunce',
        'growth_rate': 8, 'energy_gen': 1, 'cost': 1,
        'desc': 'Kaygilara direncli'
    },
    CellType.THOUGHT_EMOTIONAL: {
        'emoji': '🌻', 'color': '#FFE66D', 'name': 'Duygusal Dusunce',
        'growth_rate': 12, 'energy_gen': 3, 'cost': 1,
        'desc': 'Komsulari guclendiri'
    },
    CellType.THOUGHT_INTUITIVE: {
        'emoji': '🌙', 'color': '#A29BFE', 'name': 'Sezgisel Dusunce',
        'growth_rate': 10, 'energy_gen': 2, 'cost': 2,
        'desc': 'Gizli baglantilari acar'
    },
    CellType.ANXIETY: {
        'emoji': '🐛', 'color': '#C44569', 'name': 'Kaygi',
        'desc': 'Yayilir ve zayiflatir'
    },
    CellType.JOY: {
        'emoji': '✨', 'color': '#FFA502', 'name': 'Sevinc',
        'desc': 'Enerji verir'
    },
    CellType.TRAUMA: {
        'emoji': '🌑', 'color': '#2C3A47', 'name': 'Travma Koku',
        'desc': 'Donusturulmeyi bekliyor'
    },
    CellType.FLOWER: {
        'emoji': '🌺', 'color': '#FD79A8', 'name': 'Bilinc Cicegi',
        'desc': 'Guclü enerji kaynagi'
    },
    CellType.WISDOM: {
        'emoji': '🌳', 'color': '#00B894', 'name': 'Bilgelik Agaci',
        'desc': 'Donusmus travma - Tum bahceyi guclendiri'
    }
}

ACHIEVEMENTS_INFO = {
    'first_flower': {'name': 'Ilk Cicek', 'emoji': '🌺', 'desc': 'Ilk bilinc cicegini act'},
    'day_10': {'name': '10 Gun', 'emoji': '📅', 'desc': '10 gun hayatta kald'},
    'gardener': {'name': 'Bahcivan', 'emoji': '👨‍🌾', 'desc': '15 dusunce ekti'},
    'anxiety_master': {'name': 'Kaygi Ustasi', 'emoji': '✂️', 'desc': '10 kaygiyi temizledi'},
    'flower_power': {'name': 'Cicek Gucu', 'emoji': '💐', 'desc': '5 cicek act'},
    'level_3': {'name': 'Bilincli', 'emoji': '🧠', 'desc': 'Bilinc seviyesi 3e ulast'},
    'zen_master': {'name': 'Zen Ustasi', 'emoji': '🧘', 'desc': '20 kez meditasyon yapti'}
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_cell_config(cell_type: CellType) -> Dict:
    """Hucre config'ini guvenli sekilde getir"""
    return CELL_CONFIGS.get(cell_type, CELL_CONFIGS[CellType.EMPTY])

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
    
    def plant_thought(self, x: int, y: int, thought_type: CellType) -> tuple[bool, str]:
        """Dusunce ek"""
        cell = self.state.grid[y][x]
        
        if cell.type != CellType.EMPTY:
            return False, "Bu alan dolu!"
        
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
        return True, "Basarili!"
    
    def water_cell(self, x: int, y: int) -> tuple[bool, str]:
        """Hucreyi sula"""
        if self.state.action_points < 1:
            return False, "Yeterli AP yok!"
        
        cell = self.state.grid[y][x]
        if cell.type == CellType.EMPTY:
            return False, "Bos alan sulanamaz!"
        if cell.type == CellType.ANXIETY:
            return False, "Kaygi sulanamaz!"
        
        cell.health = min(100, cell.health + 30)
        cell.energy = min(100, cell.energy + 20)
        
        self.state.action_points -= 1
        self.add_event(f"💧 ({x},{y}) sulandi (+30 saglik, +20 enerji)")
        return True, "Sulandı!"
    
    def prune_anxiety(self, x: int, y: int) -> tuple[bool, str]:
        """Kaygiyi buda"""
        if self.state.action_points < 2:
            return False, "Yeterli AP yok! (2 AP gerekli)"
        
        cell = self.state.grid[y][x]
        if cell.type != CellType.ANXIETY:
            return False, "Burasi kaygi degil!"
        
        if random.random() < 0.75:
            cell.type = CellType.EMPTY
            cell.health = 0
            cell.energy = 0
            self.state.anxieties_cleared += 1
            self.add_event(f"✂️ Kaygi tamamen temizlendi ({x},{y})")
            message = "Kaygi yok edildi!"
        else:
            cell.health -= 40
            self.add_event(f"✂️ Kaygi zayiflatildi ({x},{y})")
            message = "Kaygi zayifladi!"
        
        self.state.action_points -= 2
        return True, message
    
    def meditate(self) -> tuple[bool, str]:
        """Meditasyon yap"""
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
        self.add_event(f"🧘 Meditasyon - {healed} hucre iyilesti")
        return True, f"{healed} hucre iyilesti!"
    
    def focus_joy(self, x: int, y: int) -> tuple[bool, str]:
        """Sevinc isigi olustur"""
        if self.state.action_points < 2:
            return False, "Yeterli AP yok! (2 AP gerekli)"
        
        cell = self.state.grid[y][x]
        if cell.type != CellType.EMPTY:
            return False, "Bu alan dolu!"
        
        neighbors = self.get_neighbors(x, y)
        strong_thoughts = [n for n in neighbors 
                          if n.type in [CellType.THOUGHT_CREATIVE, CellType.THOUGHT_EMOTIONAL]
                          and n.health > 60]
        
        if len(strong_thoughts) < 2:
            return False, "En az 2 guclu dusunce gerekli!"
        
        cell.type = CellType.JOY
        cell.health = 80
        cell.energy = 50
        
        self.state.action_points -= 2
        self.add_event(f"✨ Sevinc isigi olusturuldu ({x},{y})")
        return True, "Sevinc yaratin!"
    
    def transform_trauma(self, x: int, y: int) -> tuple[bool, str]:
        """Travmayi donustur"""
        if self.state.action_points < 3:
            return False, "Yeterli AP yok! (3 AP gerekli)"
        
        cell = self.state.grid[y][x]
        if cell.type != CellType.TRAUMA:
            return False, "Burasi travma degil!"
        
        neighbors = self.get_neighbors(x, y)
        strong_support = [n for n in neighbors 
                         if n.type in [CellType.THOUGHT_ANALYTIC, CellType.THOUGHT_EMOTIONAL]
                         and n.health > 70]
        
        if len(strong_support) < 3:
            return False, "En az 3 guclu destek dusunce gerekli!"
        
        cell.type = CellType.WISDOM
        cell.health = 100
        cell.energy = 100
        cell.age = 0
        
        self.state.action_points -= 3
        self.state.consciousness_xp += 100
        self.add_event(f"🌳 TRAVMA DONUSTURULDU! Bilgelik Agaci oldu ({x},{y})")
        return True, "Travma iyilesti!"
    
    def end_turn(self):
        """Turu bitir"""
        self._grow_thoughts()
        self._spread_anxiety()
        self._apply_neighbor_effects()
        self._apply_joy_effects()
        self._apply_wisdom_effects()
        self._check_flower_bloom()
        self._age_cells()
        self._advance_time()
        self.state.action_points = 3
        self._calculate_total_energy()
        self._update_consciousness()
        
        if random.random() < 0.25:
            self._trigger_random_event()
        
        self._check_achievements()
    
    def _grow_thoughts(self):
        """Dusunceleri buyut"""
        time_multiplier = {
            TimeOfDay.MORNING: 1.5,
            TimeOfDay.NOON: 1.0,
            TimeOfDay.EVENING: 0.8,
            TimeOfDay.NIGHT: 0.6
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
                    
                    protected = any(n.type == CellType.THOUGHT_ANALYTIC and n.health > 70 
                                   for n in neighbors)
                    if protected:
                        continue
                    
                    empty_neighbors = [n for n in neighbors if n.type == CellType.EMPTY]
                    
                    if empty_neighbors and random.random() < 0.25:
                        target = random.choice(empty_neighbors)
                        new_anxieties.append((target.x, target.y))
        
        for x, y in new_anxieties:
            self.state.grid[y][x].type = CellType.ANXIETY
            self.state.grid[y][x].health = 40
            self.add_event(f"⚠️ Kaygi yayildi ({x},{y})")
    
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
                        cell.health -= len(strong_thoughts) * 8
                        if cell.health <= 0:
                            cell.type = CellType.EMPTY
                            self.add_event(f"💪 Kaygi guclu dusuncelerle eridi ({cell.x},{cell.y})")
                
                if cell.type == CellType.THOUGHT_EMOTIONAL and cell.health > 70:
                    for neighbor in neighbors:
                        if neighbor.type in [CellType.THOUGHT_CREATIVE, CellType.THOUGHT_ANALYTIC]:
                            neighbor.energy = min(100, neighbor.energy + 3)
    
    def _apply_joy_effects(self):
        """Sevinc etkilerini uygula"""
        for row in self.state.grid:
            for cell in row:
                if cell.type == CellType.JOY and cell.health > 50:
                    neighbors = self.get_neighbors(cell.x, cell.y)
                    for neighbor in neighbors:
                        if neighbor.type == CellType.ANXIETY:
                            neighbor.health -= 10
                        elif neighbor.type != CellType.EMPTY:
                            neighbor.energy = min(100, neighbor.energy + 5)
    
    def _apply_wisdom_effects(self):
        """Bilgelik agaci etkilerini uygula"""
        wisdom_cells = []
        for row in self.state.grid:
            for cell in row:
                if cell.type == CellType.WISDOM:
                    wisdom_cells.append(cell)
        
        if wisdom_cells:
            for row in self.state.grid:
                for cell in row:
                    if cell.type not in [CellType.EMPTY, CellType.ANXIETY]:
                        cell.health = min(100, cell.health + len(wisdom_cells) * 2)
    
    def _check_flower_bloom(self):
        """Cicek acma kontrolu"""
        for row in self.state.grid:
            for cell in row:
                if cell.type == CellType.THOUGHT_CREATIVE and cell.health >= 85 and cell.age >= 4:
                    neighbors = self.get_neighbors(cell.x, cell.y)
                    creative_neighbors = [n for n in neighbors if n.type == CellType.THOUGHT_CREATIVE]
                    
                    chance = 0.2 + (len(creative_neighbors) * 0.1)
                    
                    if random.random() < chance:
                        cell.type = CellType.FLOWER
                        cell.health = 100
                        cell.energy = 60
                        self.state.flowers_bloomed += 1
                        self.add_event(f"🌺 BILINC CICEGI ACTI! ({cell.x},{cell.y})")
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
            self.add_event(f"🌅 Gun {self.state.day} basladi")
    
    def _calculate_total_energy(self):
        """Toplam enerji hesapla"""
        total = 0
        for row in self.state.grid:
            for cell in row:
                total += max(0, cell.energy)
        self.state.total_energy = total
    
    def _update_consciousness(self):
        """Bilinc seviyesi guncelle"""
        xp_needed = self.state.consciousness_level * 100
        if self.state.consciousness_xp >= xp_needed:
            self.state.consciousness_level += 1
            self.state.consciousness_xp = 0
            self.add_event(f"⬆️ BILINC SEVIYESI {self.state.consciousness_level}!")
    
    def _trigger_random_event(self):
        """Rastgele olay tetikle"""
        events = [
            ("Yagmur", "rain"),
            ("Kelebek Surusu", "butterfly"),
            ("Gunes Isigi", "sun"),
            ("Ruzgar", "wind")
        ]
        
        event_name, event_type = random.choice(events)
        
        if event_type == "rain":
            for row in self.state.grid:
                for cell in row:
                    if cell.type in [CellType.THOUGHT_CREATIVE, CellType.THOUGHT_ANALYTIC,
                                    CellType.THOUGHT_EMOTIONAL, CellType.THOUGHT_INTUITIVE]:
                        cell.health = min(100, cell.health + 15)
            self.add_event(f"🌧️ {event_name}: Tum dusunceler +15 saglik!")
        
        elif event_type == "butterfly":
            empty_cells = [(x, y) for y, row in enumerate(self.state.grid) 
                          for x, cell in enumerate(row) if cell.type == CellType.EMPTY]
            if empty_cells:
                x, y = random.choice(empty_cells)
                thought_types = [CellType.THOUGHT_CREATIVE, CellType.THOUGHT_ANALYTIC,
                               CellType.THOUGHT_EMOTIONAL]
                self.state.grid[y][x].type = random.choice(thought_types)
                self.state.grid[y][x].health = 40
                self.add_event(f"🦋 {event_name}: Yeni tohum birakti ({x},{y})!")
        
        elif event_type == "sun":
            for row in self.state.grid:
                for cell in row:
                    if cell.type != CellType.EMPTY:
                        cell.energy = min(100, cell.energy + 10)
            self.add_event(f"☀️ {event_name}: Tum enerji +10!")
        
        elif event_type == "wind":
            weak_anxieties = []
            for row in self.state.grid:
                for cell in row:
                    if cell.type == CellType.ANXIETY and cell.health < 30:
                        weak_anxieties.append(cell)
            
            for cell in weak_anxieties:
                cell.type = CellType.EMPTY
                cell.health = 0
            
            if weak_anxieties:
                self.add_event(f"💨 {event_name}: {len(weak_anxieties)} zayif kaygi uctu!")
    
    def _check_achievements(self):
        """Basarilari kontrol et"""
        if "first_flower" not in self.state.achievements and self.state.flowers_bloomed >= 1:
            self.state.achievements.append("first_flower")
            self.add_event("🏆 BASARI: Ilk Cicek!")
        
        if "day_10" not in self.state.achievements and self.state.day >= 10:
            self.state.achievements.append("day_10")
            self.add_event("🏆 BASARI: 10 Gun Hayatta!")
        
        if "gardener" not in self.state.achievements and self.state.total_thoughts >= 15:
            self.state.achievements.append("gardener")
            self.add_event("🏆 BASARI: Bahcivan!")
        
        if "anxiety_master" not in self.state.achievements and self.state.anxieties_cleared >= 10:
            self.state.achievements.append("anxiety_master")
            self.add_event("🏆 BASARI: Kaygi Ustasi!")
        
        if "flower_power" not in self.state.achievements and self.state.flowers_bloomed >= 5:
            self.state.achievements.append("flower_power")
            self.add_event("🏆 BASARI: Cicek Gucu!")
        
        if "level_3" not in self.state.achievements and self.state.consciousness_level >= 3:
            self.state.achievements.append("level_3")
            self.add_event("🏆 BASARI: Bilincli!")
    
    def add_event(self, message: str):
        """Olay logu ekle"""
        self.state.event_log.append(message)
        if len(self.state.event_log) > 15:
            self.state.event_log.pop(0)
    
    def get_stats(self) -> Dict:
        """Istatistikleri getir"""
        stats = {
            'thoughts': 0,
            'anxiety': 0,
            'joy': 0,
            'flowers': 0,
            'trauma': 0,
            'wisdom': 0
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
                elif cell.type == CellType.WISDOM:
                    stats['wisdom'] += 1
        
        return stats

# ============================================================================
# VISUALIZATION
# ============================================================================

def create_garden_visualization(state: GameState):
    """Bahce gorsellestirmesi olustur"""
    z_data = []
    hover_text = []
    colors = []
    
    for y, row in enumerate(state.grid):
        z_row = []
        hover_row = []
        
        for x, cell in enumerate(row):
            config = get_cell_config(cell.type)
            z_row.append(cell.health if cell.type != CellType.EMPTY else 0)
            hover_row.append(
                f"{config['emoji']} {config['name']}<br>"
                f"Konum: ({x},{y})<br>"
                f"Saglik: {cell.health}<br>"
                f"Enerji: {cell.energy}<br>"
                f"Yas: {cell.age} tur"
            )
        
        z_data.append(z_row)
        hover_text.append(hover_row)
    
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        text=[[get_cell_config(cell.type)['emoji'] for cell in row] for row in state.grid],
        hovertext=hover_text,
        hoverinfo='text',
        colorscale=[[0, '#F8F9FA'], [0.5, '#A8E6CF'], [1, '#4ECDC4']],
        showscale=False,
        texttemplate='%{text}',
        textfont={"size": 28}
    ))
    
    fig.update_layout(
        width=600,
        height=600,
        xaxis=dict(showgrid=True, zeroline=False, showticklabels=True, 
                  tickmode='linear', tick0=0, dtick=1),
        yaxis=dict(showgrid=True, zeroline=False, showticklabels=True,
                  tickmode='linear', tick0=0, dtick=1),
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='#E8F4F8'
    )
    
    return fig

# ============================================================================
# STREAMLIT APP
# ============================================================================

def initialize_game():
    """Yeni oyun baslat"""
    state = GameState()
    engine = MindGardenEngine(state)
    
    for _ in range(2):
        x, y = random.randint(1, 5), random.randint(1, 5)
        while state.grid[y][x].type != CellType.EMPTY:
            x, y = random.randint(1, 5), random.randint(1, 5)
        thought_type = random.choice([CellType.THOUGHT_CREATIVE, CellType.THOUGHT_ANALYTIC])
        state.grid[y][x].type = thought_type
        state.grid[y][x].health = 60
        state.grid[y][x].energy = 20
    
    x, y = random.randint(0, 6), random.randint(0, 6)
    while state.grid[y][x].type != CellType.EMPTY:
        x, y = random.randint(0, 6), random.randint(0, 6)
    state.grid[y][x].type = CellType.ANXIETY
    state.grid[y][x].health = 45
    
    x, y = random.randint(0, 6), random.randint(0, 6)
    while state.grid[y][x].type != CellType.EMPTY:
        x, y = random.randint(0, 6), random.randint(0, 6)
    state.grid[y][x].type = CellType.TRAUMA
    state.grid[y][x].health = 100
    
    engine.add_event("🌱 Zihin bahcesi olusturuldu")
    engine.add_event("💡 Ilk dusunceler ekildi")
    engine.add_event("⚠️ Bir kaygi ve bir travma var")
    
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
            font-size: 15px;
            font-weight: 500;
        }
        .metric-card {
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    if 'game_state' not in st.session_state:
        st.session_state.game_state = initialize_game()
    
    if 'selected_cell' not in st.session_state:
        st.session_state.selected_cell = (3, 3)
    
    if 'message' not in st.session_state:
        st.session_state.message = None
    
    state = st.session_state.game_state
    engine = MindGardenEngine(state)
    
    st.title("🌱 ZIHIN BAHCESI")
    st.caption("Zihninizi buyutun, kaygilari yonetin, bilincinizi yukselt")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Gun", state.day)
    with col2:
        st.metric("Bilinc", f"Lvl {state.consciousness_level}")
    with col3:
        st.metric("Enerji", f"{state.total_energy}")
    with col4:
        st.metric("AP", f"{state.action_points}/3")
    with col5:
        st.metric("Zaman", state.time_of_day.value)
    
    if st.session_state.message:
        if "Basarili" in st.session_state.message or "!" in st.session_state.message:
            st.success(st.session_state.message)
        else:
            st.warning(st.session_state.message)
        st.session_state.message = None
    
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.subheader("🗺️ Bahceniz")
        
        fig = create_garden_visualization(state)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 Grid uzerinde koordinatlari gorebilirsiniz. Saga secili hucreyi yonetin.")
    
    with col_right:
        st.subheader("🎯 Kontrol Paneli")
        
        col_x, col_y = st.columns(2)
        with col_x:
            sel_x = st.number_input("X Koordinat", 0, state.grid_size-1, 
                                   st.session_state.selected_cell[0], key="sel_x")
        with col_y:
            sel_y = st.number_input("Y Koordinat", 0, state.grid_size-1, 
                                   st.session_state.selected_cell[1], key="sel_y")
        
        st.session_state.selected_cell = (sel_x, sel_y)
        x, y = st.session_state.selected_cell
        cell = state.grid[y][x]
        config = get_cell_config(cell.type)
        
        st.markdown(f"""
        <div style='background: white; padding: 15px; border-radius: 10px; border-left: 4px solid {config['color']}'>
            <h3>{config['emoji']} {config['name']}</h3>
            <p><b>Konum:</b> ({x}, {y})</p>
            <p><b>Saglik:</b> {cell.health}/100</p>
            <p><b>Enerji:</b> {cell.energy}</p>
            <p><b>Yas:</b> {cell.age} tur</p>
            <p><i>{config.get('desc', '')}</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        tab1, tab2, tab3 = st.tabs(["🌱 Ekme", "⚡ Aksiyonlar", "🎯 Ozel"])
        
        with tab1:
            st.write("**Dusunce Tur Sec:**")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🌸 Yaratici (1 AP)", key="plant_creative", use_container_width=True):
                    success, msg = engine.plant_thought(x, y, CellType.THOUGHT_CREATIVE)
                    st.session_state.message = msg
                    if success:
                        st.rerun()
                
                if st.button("🌻 Duygusal (1 AP)", key="plant_emotional", use_container_width=True):
                    success, msg = engine.plant_thought(x, y, CellType.THOUGHT_EMOTIONAL)
                    st.session_state.message = msg
                    if success:
                        st.rerun()
            
            with col_b:
                if st.button("🌿 Analitik (1 AP)", key="plant_analytic", use_container_width=True):
                    success, msg = engine.plant_thought(x, y, CellType.THOUGHT_ANALYTIC)
                    st.session_state.message = msg
                    if success:
                        st.rerun()
                
                if st.button("🌙 Sezgisel (2 AP)", key="plant_intuitive", use_container_width=True):
                    success, msg = engine.plant_thought(x, y, CellType.THOUGHT_INTUITIVE)
                    st.session_state.message = msg
                    if success:
                        st.rerun()
        
        with tab2:
            st.write("**Temel Islemler:**")
            
            if st.button("💧 Sula (1 AP)", key="water", use_container_width=True):
                success, msg = engine.water_cell(x, y)
                st.session_state.message = msg
                if success:
                    st.rerun()
            
            if st.button("✂️ Kaygi Buda (2 AP)", key="prune", use_container_width=True):
                success, msg = engine.prune_anxiety(x, y)
                st.session_state.message = msg
                if success:
                    st.rerun()
            
            if st.button("🧘 Meditasyon - Tum Bahce (3 AP)", key="meditate", use_container_width=True):
                success, msg = engine.meditate()
                st.session_state.message = msg
                if success:
                    st.rerun()
        
        with tab3:
            st.write("**Gelismis Teknikler:**")
            
            if st.button("✨ Sevinc Isigi Olustur (2 AP)", key="joy", use_container_width=True):
                success, msg = engine.focus_joy(x, y)
                st.session_state.message = msg
                if success:
                    st.rerun()
            st.caption("En az 2 guclu dusunce gerekli")
            
            if st.button("🌳 Travma Donustur (3 AP)", key="transform", use_container_width=True):
                success, msg = engine.transform_trauma(x, y)
                st.session_state.message = msg
                if success:
                    st.rerun()
            st.caption("En az 3 guclu destek dusunce gerekli")
        
        st.divider()
        
        if st.button("⏭️ TURU BITIR", type="primary", use_container_width=True):
            engine.end_turn()
            st.session_state.message = "Tur bitti! Bahce gelisti."
            st.rerun()
        
        st.divider()
        
        stats = engine.get_stats()
        st.subheader("📊 Bahce Durumu")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.metric("🌱 Dusunceler", stats['thoughts'])
            st.metric("🌺 Cicekler", stats['flowers'])
            st.metric("✨ Sevinc", stats['joy'])
        with col_s2:
            st.metric("🐛 Kaygilar", stats['anxiety'])
            st.metric("🌑 Travma", stats['trauma'])
            st.metric("🌳 Bilgelik", stats['wisdom'])
        
        if state.achievements:
            st.subheader("🏆 Basarilar")
            for ach_id in state.achievements:
                ach = ACHIEVEMENTS_INFO.get(ach_id, {'emoji': '✓', 'name': ach_id})
                st.write(f"{ach['emoji']} {ach['name']}")
        
        st.subheader("📜 Olaylar")
        for event in reversed(state.event_log[-8:]):
            st.caption(event)
        
        st.divider()
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 Yeni Oyun", use_container_width=True):
                st.session_state.game_state = initialize_game()
                st.session_state.selected_cell = (3, 3)
                st.session_state.message = "Yeni oyun basladi!"
                st.rerun()
        with col_btn2:
            if st.button("💾 Kaydet", use_container_width=True):
                st.session_state.message = "Oyun otomatik kaydedildi!"

if __name__ == "__main__":
    main()

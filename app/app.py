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
    NOON = "Öğle"
    EVENING = "Akşam"
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

ACHIEVEMENTS_INFO = {
    'first_flower': {'name': 'İlk Çiçek', 'emoji': '🌺', 'desc': 'İlk bilinç çiçeğini açtı'},
    'day_10': {'name': '10 Gün', 'emoji': '📅', 'desc': '10 gün hayatta kaldı'},
    'gardener': {'name': 'Bahçıvan', 'emoji': '👨‍🌾', 'desc': '15 düşünce ekti'},
    'anxiety_master': {'name': 'Kaygı Ustası', 'emoji': '✂️', 'desc': '10 kaygıyı temizledi'},
    'flower_power': {'name': 'Çiçek Gücü', 'emoji': '💐', 'desc': '5 çiçek açtı'},
    'level_3': {'name': 'Bilinçli', 'emoji': '🧠', 'desc': 'Bilinç seviyesi 3e ulaştı'},
    'zen_master': {'name': 'Zen Ustası', 'emoji': '🧘', 'desc': '20 kez meditasyon yaptı'}
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_cell_config(cell_type: CellType) -> Dict:
    """Hücre config'ini güvenli şekilde getirir"""
    return CELL_CONFIGS.get(cell_type, CELL_CONFIGS[CellType.EMPTY])

# ============================================================================
# GAME ENGINE
# ============================================================================

class MindGardenEngine:
    def __init__(self, state: GameState):
        self.state = state
    
    def get_neighbors(self, x: int, y: int) -> List[Cell]:
        """Komşu hücreleri döndürür"""
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
        return True, "Başarılı! Düşünce ekildi."
    
    def water_cell(self, x: int, y: int) -> tuple[bool, str]:
        """Hücreyi sula"""
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
        """Kaygıyı buda"""
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
        self.add_event(f"🧘 Meditasyon - {healed} hücre iyileşti")
        return True, f"Başarılı! {healed} hücre iyileşti."
    
    def focus_joy(self, x: int, y: int) -> tuple[bool, str]:
        """Sevinç ışığı oluşturur"""
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
        """Travmayı dönüştürür"""
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
        """Turu bitir"""
        self._grow_thoughts()
        self._spread_anxiety()
        self._apply_neighbor_effects()
        self._apply_joy_effects()
        self._apply_wisdom_effects()
        self._check_flower_bloom()
        self._age_cells()
        self._advance_time()
        self.state.action_points = 3 # Tur sonunda AP yenilenir
        self._calculate_total_energy()
        self._update_consciousness()
        
        if random.random() < 0.25:
            self._trigger_random_event()
        
        self._check_achievements()
        self.add_event(f"--- Tur Bitti. Gün {self.state.day}, {self.state.time_of_day.value} ---")
    
    def _grow_thoughts(self):
        """Düşünceleri büyüt"""
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
                    
                    # Sağlık ve Yaşa Bağlı Kayıp
                    cell.health = max(0, cell.health - 5)
                    
                    growth = CELL_CONFIGS[cell.type]['growth_rate'] * time_multiplier
                    cell.health = min(100, cell.health + int(growth))
                    
                    if cell.health > 60:
                        energy_gen = CELL_CONFIGS[cell.type]['energy_gen']
                        cell.energy = min(100, cell.energy + energy_gen)
    
    def _spread_anxiety(self):
        """Kaygıları yayar ve hasar verir"""
        new_anxieties = []
        
        for row in self.state.grid:
            for cell in row:
                if cell.type == CellType.ANXIETY:
                    # Kaygı komşulara zarar verir
                    for neighbor in self.get_neighbors(cell.x, cell.y):
                        if neighbor.type not in [CellType.EMPTY, CellType.ANXIETY]:
                            damage = 15
                            if neighbor.type == CellType.THOUGHT_ANALYTIC:
                                damage = 5
                            neighbor.health = max(0, neighbor.health - damage)
                            
                            if neighbor.health == 0:
                                self.add_event(f"💀 ({neighbor.x},{neighbor.y}) Kaygıdan kurudu!")
                                neighbor.type = CellType.EMPTY
                    
                    # Yayılma
                    if cell.health > 30:
                        neighbors = self.get_neighbors(cell.x, cell.y)
                        
                        empty_neighbors = [n for n in neighbors if n.type == CellType.EMPTY]
                        
                        if empty_neighbors and random.random() < 0.25:
                            target = random.choice(empty_neighbors)
                            new_anxieties.append((target.x, target.y))
        
        for x, y in new_anxieties:
            if self.state.grid[y][x].type == CellType.EMPTY: 
                self.state.grid[y][x].type = CellType.ANXIETY
                self.state.grid[y][x].health = 40
                self.add_event(f"⚠️ Kaygı yayıldı ({x},{y})")
    
    def _apply_neighbor_effects(self):
        """Komşu etkilerini uygula"""
        for row in self.state.grid:
            for cell in row:
                if cell.type == CellType.EMPTY:
                    continue
                
                neighbors = self.get_neighbors(cell.x, cell.y)
                
                # Kaygı, güçlü düşüncelerle savaşır
                if cell.type == CellType.ANXIETY:
                    strong_thoughts = [n for n in neighbors 
                                       if n.type in [CellType.THOUGHT_ANALYTIC, CellType.THOUGHT_CREATIVE, CellType.JOY, CellType.WISDOM]
                                       and n.health > 70]
                    if strong_thoughts:
                        cell.health = max(0, cell.health - len(strong_thoughts) * 8)
                        if cell.health <= 0:
                            cell.type = CellType.EMPTY
                            self.add_event(f"💪 Kaygı güçlü düşüncelerle eridi ({cell.x},{cell.y})")
                            self.state.anxieties_cleared += 1
                
                # Duygusal düşünce komşularını destekler
                if cell.type == CellType.THOUGHT_EMOTIONAL and cell.health > 70:
                    for neighbor in neighbors:
                        if neighbor.type in [CellType.THOUGHT_CREATIVE, CellType.THOUGHT_ANALYTIC, CellType.THOUGHT_INTUITIVE]:
                            neighbor.energy = min(100, neighbor.energy + 3)
    
    def _apply_joy_effects(self):
        """Sevinç etkilerini uygula"""
        for row in self.state.grid:
            for cell in row:
                if cell.type == CellType.JOY and cell.health > 50:
                    neighbors = self.get_neighbors(cell.x, cell.y)
                    for neighbor in neighbors:
                        if neighbor.type == CellType.ANXIETY:
                            neighbor.health = max(0, neighbor.health - 10)
                        elif neighbor.type != CellType.EMPTY:
                            neighbor.energy = min(100, neighbor.energy + 5)
                            neighbor.health = min(100, neighbor.health + 2)
    
    def _apply_wisdom_effects(self):
        """Bilgelik ağacı etkilerini uygula"""
        wisdom_cells = [cell for row in self.state.grid for cell in row if cell.type == CellType.WISDOM]
        
        if wisdom_cells:
            heal_amount = len(wisdom_cells) * 2
            for row in self.state.grid:
                for cell in row:
                    if cell.type not in [CellType.EMPTY, CellType.ANXIETY]:
                        cell.health = min(100, cell.health + heal_amount)
                    elif cell.type == CellType.ANXIETY:
                        cell.health = max(0, cell.health - len(wisdom_cells) * 1) 
    
    def _check_flower_bloom(self):
        """Çiçek açma kontrolü"""
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
                        cell.age = 0
                        self.state.flowers_bloomed += 1
                        self.add_event(f"🌺 BİLİNÇ ÇİÇEĞİ AÇTI! ({cell.x},{cell.y})")
                        self.state.consciousness_xp += 50
    
    def _age_cells(self):
        """Hücreleri yaşlandır"""
        for row in self.state.grid:
            for cell in row:
                if cell.type != CellType.EMPTY:
                    cell.age += 1
    
    def _advance_time(self):
        """Zamanı ilerlet"""
        times = list(TimeOfDay)
        current_idx = times.index(self.state.time_of_day)
        next_idx = (current_idx + 1) % len(times)
        self.state.time_of_day = times[next_idx]
        
        if self.state.time_of_day == TimeOfDay.MORNING:
            self.state.day += 1
            # Gün başlangıcı olayı burada eklenir
    
    def _calculate_total_energy(self):
        """Toplam enerji hesapla"""
        total = 0
        for row in self.state.grid:
            for cell in row:
                if cell.type != CellType.EMPTY:
                    total += max(0, cell.energy)
        self.state.total_energy = total
    
    def _update_consciousness(self):
        """Bilinç seviyesi güncelle"""
        xp_needed = self.state.consciousness_level * 100
        if self.state.consciousness_xp >= xp_needed:
            self.state.consciousness_level += 1
            self.state.consciousness_xp = 0
            self.add_event(f"⬆️ BİLİNÇ SEVİYESİ {self.state.consciousness_level}!")
    
    def _trigger_random_event(self):
        """Rastgele olay tetikle"""
        events = [
            ("Yağmur", "rain"),
            ("Kelebek Sürüsü", "butterfly"),
            ("Güneş Işığı", "sun"),
            ("Rüzgar", "wind"),
            ("Yeni Kaygı Dalgalanması", "new_anxiety")
        ]
        
        event_name, event_type = random.choice(events)
        
        if event_type == "rain":
            for row in self.state.grid:
                for cell in row:
                    if cell.type in [CellType.THOUGHT_CREATIVE, CellType.THOUGHT_ANALYTIC,
                                     CellType.THOUGHT_EMOTIONAL, CellType.THOUGHT_INTUITIVE]:
                        cell.health = min(100, cell.health + 15)
            self.add_event(f"🌧️ {event_name}: Tüm düşünceler +15 sağlık!")
        
        elif event_type == "butterfly":
            empty_cells = [(x, y) for y, row in enumerate(self.state.grid) 
                           for x, cell in enumerate(row) if cell.type == CellType.EMPTY]
            if empty_cells:
                x, y = random.choice(empty_cells)
                thought_types = [CellType.THOUGHT_CREATIVE, CellType.THOUGHT_ANALYTIC,
                                 CellType.THOUGHT_EMOTIONAL]
                self.state.grid[y][x].type = random.choice(thought_types)
                self.state.grid[y][x].health = 40
                self.add_event(f"🦋 {event_name}: Yeni tohum bıraktı ({x},{y})!")
        
        elif event_type == "sun":
            for row in self.state.grid:
                for cell in row:
                    if cell.type != CellType.EMPTY:
                        cell.energy = min(100, cell.energy + 10)
            self.add_event(f"☀️ {event_name}: Tüm enerji +10!")
        
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
                self.add_event(f"💨 {event_name}: {len(weak_anxieties)} zayıf kaygı uçtu!")
        
        elif event_type == "new_anxiety":
            empty_cells = [(x, y) for y, row in enumerate(self.state.grid) 
                           for x, cell in enumerate(row) if cell.type == CellType.EMPTY]
            if empty_cells:
                x, y = random.choice(empty_cells)
                self.state.grid[y][x].type = CellType.ANXIETY
                self.state.grid[y][x].health = 50
                self.add_event(f"🚨 {event_name}: Yeni bir kaygı ({x},{y}) belirdi!")

    
    def _check_achievements(self):
        """Başarıları kontrol et"""
        if "first_flower" not in self.state.achievements and self.state.flowers_bloomed >= 1:
            self.state.achievements.append("first_flower")
            self.add_event("🏆 BAŞARI: İlk Çiçek!")
        
        if "day_10" not in self.state.achievements and self.state.day >= 10:
            self.state.achievements.append("day_10")
            self.add_event("🏆 BAŞARI: 10 Gün Hayatta!")
        
        if "gardener" not in self.state.achievements and self.state.total_thoughts >= 15:
            self.state.achievements.append("gardener")
            self.add_event("🏆 BAŞARI: Bahçıvan!")
        
        if "anxiety_master" not in self.state.achievements and self.state.anxieties_cleared >= 10:
            self.state.achievements.append("anxiety_master")
            self.add_event("🏆 BAŞARI: Kaygı Ustası!")
        
        if "flower_power" not in self.state.achievements and self.state.flowers_bloomed >= 5:
            self.state.achievements.append("flower_power")
            self.add_event("🏆 BAŞARI: Çiçek Gücü!")
        
        if "level_3" not in self.state.achievements and self.state.consciousness_level >= 3:
            self.state.achievements.append("level_3")
            self.add_event("🏆 BAŞARI: Bilinçli!")
    
    def add_event(self, message: str):
        """Olay logu ekle"""
        self.state.event_log.append(message)
        if len(self.state.event_log) > 15:
            self.state.event_log.pop(0)
    
    def get_stats(self) -> Dict:
        """İstatistikleri getir"""
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
    """Bahçe görselleştirmesi oluşturur"""
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

    # Hata düzeltmesi: color_map.get() ile güvenli erişim
    z_colors = [[color_map.get(cell.type, 0) for cell in row] for row in state.grid]

    for y, row in enumerate(state.grid):
        z_row = []
        hover_row = []
        
        for x, cell in enumerate(row):
            config = get_cell_config(cell.type)
            # Z değerini hücre tipine göre haritala (Görselleştirmede renk için)
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
    
    # Z-data'yı 0-1 arasına normalize et (Plotly colorscale için)
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
# ACTION HANDLER
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
        success = True # Tur bitirmek her zaman başarılı kabul edilir.

    st.session_state.message = msg
    
    # Hata oluşsa bile (yetersiz AP gibi), state değişmiş olabilir (AP azalmamıştır), 
    # bu yüzden Streamlit'in durumu güncellemesi için rerun/rerender gerekir.
    # Ancak manuel st.rerun() yerine, form dışına çıktığı için otomatik güncellenir.


# ============================================================================
# MAIN APPLICATION LOGIC
# ============================================================================

def main():
    st.set_page_config(page_title="Zihin Bahçesi", page_icon="🌱", layout="wide")
    
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
    
    if 'selected_cell' not in st.session_state:
        st.session_state.selected_cell = (3, 3)

    st.sidebar.title("Kontrol")
    if st.sidebar.button("🔄 Yeni Oyun Başlat", help="Mevcut oyunu sıfırlar.", type="secondary"):
        st.session_state.game_started = False
        st.session_state.game_state = None
        st.session_state.message = "Yeni bir zihin bahçesi kurmaya hazır mısınız?"
        st.rerun()

    # Oyun Başlangıç Ekranı
    if not st.session_state.game_started:
        display_how_to_play()
        return

    # Oyun Başladı
    state = st.session_state.game_state
    engine = MindGardenEngine(state)
    
    st.title("🌱 ZİHİN BAHÇESİ")
    st.caption("Zihninizi büyütün, kaygıları yönetin, bilincinizi yükseltin")
    
    # Üst Bilgi Metrikleri
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
    
    # Aksiyon Mesajları (Önceki hatanın oluştuğu blok düzeltildi)
    if st.session_state.message:
        message_box = st.empty()
        
        # Mesajın türüne göre renkli kutu göster
        if "Başarılı" in st.session_state.message or "iyileşti" in st.session_state.message or "yok edildi" in st.session_state.message or "yarattın" in st.session_state.message or "dönüştürüldü" in st.session_state.message:
            message_box.success(st.session_state.message)
        elif "Yeterli AP" in st.session_state.message or "dolu" in st.session_state.message or "gerekli" in st.session_state.message or "değil" in st.session_state.message:
            message_box.warning(st.session_state.message)
        else:
            message_box.info(st.session_state.message)

        # Mesajı temizleme mantığı: Aksiyon bittiyse (AP kullanıldıysa) mesajı koru.
        # Yeni tur başladıysa veya Turu Bitir mesajı değilse AP 3 iken temizle.
        if "Tur bitti" in st.session_state.message:
             # Tur bitiş mesajını hemen silmeyelim, kullanıcı görsün. Bir sonraki aksiyonda silinecek.
             pass
        elif state.action_points == 3 and not st.session_state.message.startswith("Zihin bahçenize"):
             # Eğer AP 3 ise (yeni tur başı demektir) ve ilk karşılama mesajı değilse, temizle
             st.session_state.message = None
        else:
             # Aksiyon sonrası mesajı tut
             pass
            
    
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.subheader("🗺️ Zihin Haritası")
        
        fig = create_garden_visualization(state)
        st.plotly_chart(fig, use_container_width=True)
        
        # Olay Günlüğü alt bölüme taşındı
        st.markdown("---")
        st.subheader("📜 Olay Günlüğü")
        log_html = ""
        for entry in reversed(state.event_log):
            log_html += f"<li>{entry}</li>"
        st.markdown(f"<ul style='font-size: 14px; list-style-type: none; padding-left: 0;'>{log_html}</ul>",
                    unsafe_allow_html=True)
    
    with col_right:
        st.subheader("🎯 Seçili Alan Kontrolü")
        
        # Koordinat Seçimi
        # Koordinatları st.session_state.selected_cell'den al
        x, y = st.session_state.selected_cell
        
        with st.expander("Koordinat Seç", expanded=True):
            col_x, col_y = st.columns(2)
            with col_x:
                # Koordinatları güncellediğimizde st.session_state'e kaydet
                new_x = st.number_input("X Koordinat", 0, state.grid_size-1, x, key="inp_x", on_change=lambda: st.session_state.update(selected_cell=(st.session_state.inp_x, st.session_state.inp_y)))
            with col_y:
                new_y = st.number_input("Y Koordinat", 0, state.grid_size-1, y, key="inp_y", on_change=lambda: st.session_state.update(selected_cell=(st.session_state.inp_x, st.session_state.inp_y)))
            
            # Güncel koordinatları tekrar çek
            x, y = st.session_state.selected_cell

        cell = state.grid[y][x]
        config = get_cell_config(cell.type)
        
        # Hücre Bilgisi
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

        # **KRİTİK DÜZELTME: MERKEZİ AKSİYON FORMU**
        # Tüm aksiyonları tek bir form içinde tutmak Streamlit'in durum yönetimini kolaylaştırır.
        
        with st.form(key="action_form"):
            tab_plant, tab_action, tab_special = st.tabs(["🌱 EKME", "💧 TEMEL AKSİYON", "✨ İLERİ TEKNİKLER"])
            
            action_to_perform = None
            thought_type_to_plant = None
            
            with tab_plant:
                st.write("Düşünce Türü Seç (Boş Alan Gerekir):")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.form_submit_button("🌸 Yaratıcı (1 AP)", help="Yaratıcı Düşünce Eker", use_container_width=True):
                        action_to_perform = "plant"
                        thought_type_to_plant = CellType.THOUGHT_CREATIVE
                    
                    if st.form_submit_button("🌻 Duygusal (1 AP)", help="Duygusal Düşünce Eker", use_container_width=True):
                        action_to_perform = "plant"
                        thought_type_to_plant = CellType.THOUGHT_EMOTIONAL
                
                with col_b:
                    if st.form_submit_button("🌿 Analitik (1 AP)", help="Analitik Düşünce Eker", use_container_width=True):
                        action_to_perform = "plant"
                        thought_type_to_plant = CellType.THOUGHT_ANALYTIC
                    
                    if st.form_submit_button("🌙 Sezgisel (2 AP)", help="Sezgisel Düşünce Eker (Yüksek AP)", use_container_width=True):
                        action_to_perform = "plant"
                        thought_type_to_plant = CellType.THOUGHT_INTUITIVE
            
            with tab_action:
                st.write("Temel Bakım ve Kaygı Yönetimi:")
                
                if st.form_submit_button("💧 Sula (1 AP)", help="Sağlık ve Enerji Verir", use_container_width=True):
                    action_to_perform = "water"
                
                if st.form_submit_button("✂️ Kaygı Buda (2 AP)", help="Kaygıyı Zayıflatır/Temizler", use_container_width=True):
                    action_to_perform = "prune"
                
                st.markdown("---")
                if st.form_submit_button("🧘 Meditasyon - Tüm Bahçe (3 AP)", help="Tüm pozitif alanları iyileştirir", use_container_width=True):
                    action_to_perform = "meditate"
            
            with tab_special:
                st.write("Gelişmiş Teknikler (Yüksek Etki):")
                
                if st.form_submit_button("✨ Sevinç Işığı Oluştur (2 AP)", help="En az 2 güçlü düşünce gerektirir", use_container_width=True):
                    action_to_perform = "focus_joy"
                
                if st.form_submit_button("🌳 Travma Dönüştür (3 AP)", help="Travma Kökünü Bilgeliğe dönüştürür. En az 3 güçlü destek gerektirir.", use_container_width=True):
                    action_to_perform = "transform"

            # Formun dışında tetiklenen Tur Bitirme Aksiyonu
            # Bu, formun dışında kalmalıdır ki, kullanıcı formu doldurmadan da turu bitirebilsin.
            
            # Hangi aksiyonun seçildiğini kontrol et ve tetikle
            if action_to_perform:
                handle_action(action_to_perform, x, y, thought_type_to_plant)
                st.rerun() # Aksiyon sonrası durumu güncellemek için yeniden çalıştır

        # TUR BİTİR BUTONU (FORM DIŞINDA)
        if st.button("⏭️ TURU BİTİR VE İLERLE", type="primary", use_container_width=True):
            handle_action("end_turn", x, y) # x, y burada kullanılmıyor, ancak çağrım tutarlılığı için tutuldu
            st.rerun()
        
        st.markdown("---")
        
        # İstatistikler ve Başarımlar (Aşağıda kalması uygun)
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

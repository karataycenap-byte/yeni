# ============================================================================
# HOW TO PLAY (DISPLAY) FUNCTION (Bu kısım dosyanızda olmalı!)
# ============================================================================

def display_how_to_play():
    # ... (Burada fonksiyonun tüm içeriği yer almalı)
    st.markdown("## 🧠 Zihin Bahçesi: Nasıl Oynanır?")
    # ...

# ============================================================================
# MAIN APPLICATION LOGIC 
# ============================================================================

def main():
    # ... (Kod başlangıcı)
    
    if not st.session_state.game_started:
        display_how_to_play() # Hatanın oluştuğu satır
        return
        
    # ... (Kalan kod)

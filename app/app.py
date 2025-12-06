# ============================================================================
# HOW TO PLAY (DISPLAY) FUNCTION (Bu kısım dosyanızda olmalı!)
# ============================================================================

def display_how_to_play():
    st.markdown("## 🧠 Zihin Bahçesi: Nasıl Oynanır?")
    st.caption("Bu oyun, zihninizi bir bahçe metaforu üzerinden yönetmeyi ve geliştirmeyi simüle eder.")
    
    st.divider()

    tab_start, tab_cells, tab_strategy = st.tabs(["▶️ Başlangıç", "📊 Hücre Tipleri", "📜 Strateji"])
    
    with tab_start:
        st.markdown("### 1. Temel Mekanik")
        st.markdown("""
        * **Amaç:** Bilinç seviyenizi (XP) yükseltmek, düşüncelerinizi sağlıklı tutmak ve Kaygı/Travma hücrelerini yönetmektir.
        * **AP (Aksiyon Puanı):** Her tur 3 AP ile başlarsınız. Düşünce ekmek, sulamak, budamak gibi her eylem AP harcar.
        * **Tur Sistemi:** Tüm AP'nizi harcadığınızda **'TURU BİTİR'** düğmesine basarsınız. Bu, bitkilerin büyümesine, kaygıların yayılmasına ve yeni gün/zaman dilimine geçilmesine neden olur.
        """)
        
        st.markdown("### 2. İstatistikler")
        st.markdown("""
        * **Sağlık (Health):** Hücrenin canlılığı. Düşük sağlık, hücrenin kuruyarak ölmesine neden olur. Sulayarak artırılır.
        * **Enerji (Energy):** Hücrenin ürettiği ve komşularına aktarabileceği güç. Yüksek enerji, daha hızlı büyümeye ve çiçek açmaya yardımcı olur.
        * **Bilinç Seviyesi:** Deneyim puanı (XP) kazandıkça artar. Travma dönüştürme ve Kaygı temizleme yüksek XP verir.
        """)

    with tab_cells:
        st.markdown("### 3. Hücre Tipleri ve İşlevleri")
        
        # NOTE: Bu kısımda kullanılan CellType ve CELL_CONFIGS değişkenlerinin 
        # kodun üst kısımlarında tanımlı olması GEREKİR.
        
        # Eğer bu kısım NameError verirse, CellType ve CELL_CONFIGS'i kontrol edin.
        
        col_type1, col_type2 = st.columns(2)
        
        # Bu kısımdaki emoji ve isimler, önceki koddaki CELL_CONFIGS sözlüğüne bağlıdır.
        # Eğer CELL_CONFIGS tanımınız hatalıysa, burası da hata verebilir.
        
        # Varsayılan emojiler ve isimlerle devam ediyoruz (Önceki kodunuzdaki gibi):
        
        # Bu CELL_CONFIGS'in kodun üst kısmında tanımlı olduğunu varsayarız.

        with col_type1:
            st.markdown("#### **Pozitif / Gelişen Tipler**")
            st.markdown(f"* **🌸 Yaratıcı Düşünce (1 AP):** Hızlı büyür, Bilinç Çiçeğine dönüşebilir. Dengeli büyütülmelidir.")
            st.markdown(f"* **🌿 Analitik Düşünce (1 AP):** Kaygıların zararına karşı daha dirençlidir. Kaygıların yanına yerleştirmek iyidir.")
            st.markdown(f"* **🌻 Duygusal Düşünce (1 AP):** Komşularının enerjisini artırır, destekleyici bir rol oynar.")
            st.markdown(f"* **🌺 Bilinç Çiçeği:** Yaratıcı düşüncenin olgunlaşmış hali. Güçlü enerji kaynağıdır.")
            st.markdown(f"* **🌳 Bilgelik Ağacı:** Dönüşmüş Travma. Tüm bahçeyi yavaşça iyileştirir (Pasif buff).")
        
        with col_type2:
            st.markdown("#### **Negatif / Yönetilmesi Gereken Tipler**")
            st.markdown(f"* **🐛 Kaygı:** Yayılır, komşu düşüncelerin sağlığını düşürür. **Buda (Prune)** aksiyonu ile temizlenir.")
            st.markdown(f"* **🌑 Travma Kökü:** Sabit bir engeldir. Yüksek seviyede destekleyici düşünce ve **Dönüştür (Transform)** aksiyonu gerektirir.")
            st.markdown(f"* **✨ Sevinç Işığı:** **Oluştur (Focus Joy)** aksiyonu ile üretilir. Komşu kaygıları eritir ve düşüncelere enerji verir.")

    st.divider()
    if st.button("🚀 OYUNU BAŞLAT", type="primary", use_container_width=True):
        st.session_state.game_state = initialize_game()
        st.session_state.message = "Zihin bahçenize hoş geldiniz. İlk AP'lerinizi kullanın!"
        st.session_state.game_started = True
        # Temizlik
        st.session_state.next_action = None
        st.session_state.thought_type = None
        st.session_state.action_clicked = False
        st.rerun()

# ============================================================================

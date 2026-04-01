import streamlit as st
import pandas as pd
from datetime import datetime

# --- 🛰️ SİSTEM AYARLARI VE DASHBOARD TASARIMI ---
st.set_page_config(page_title="AI Atlas Strategic OS", layout="wide")

# CSS ile Görsel İyileştirme
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🧬 AI Atlas: Kurumsal Stratejik İşletim Sistemi")
st.caption("Kişi → Departman → Kurum Konsolide Raporlama ve Karar Destek Paneli")

# --- 📊 ÜST PANEL: KONSOLİDE KURUMSAL ÖZET ---
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Kurum Sağlık Skoru", "%84", "↑ %2")
with c2: st.metric("İK Departman Uyumu", "%91", "Kritik", delta_color="inverse")
with c3: st.metric("AI Güven Endeksi", "78/100", "Stabil")
with c4: st.metric("Dönüşüm Soruları", "12 Adet", "Aksiyon Bekliyor")

st.divider()

# --- 🛠️ ANA PROGRAM AKIŞI (SEKMELER) ---
tabs = st.tabs([
    "👤 KİŞİ: Veri Girişi", 
    "🏢 DEPT: Onay & Ara Değerlendirme", 
    "📈 KURUM: Konsolide Dashboard", 
    "⚖️ AI ATLAS: Karar Odası"
])

# --- 1. KİŞİSEL VERİ GİRİŞİ (Atlas_Operasyon_01/02) ---
with tabs[0]:
    st.subheader("Bireysel Görev ve Operasyonel İlerleme")
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        st.write("**Sorumlu:** Atlas_Operasyon_01 (Ezgi K.)")
        st.info("📌 Görev: Lise Stajyer Görüşmeleri (149 Gün)")
        ilerleme = st.slider("Mevcut İlerleme Yüzdesi (%)", 0, 100, 40)
        kpi_beyan = st.number_input("Bağlı KPI Başarı Beyanı (%)", 0, 100, 90)
    
    with col_b:
        st.write("### Notlar / Engelleyiciler")
        st.text_area("Yöneticiye Not:", "Süreç planlandığı gibi gidiyor ancak aday kalitesi düşük.")
        if st.button("Veriyi Onaya Gönder"):
            st.success("Veri Departman Onayına iletildi.")

# --- 2. DEPARTMAN ONAY VE ARA DEĞERLENDİRME ---
with tabs[1]:
    st.subheader("Departman Süzgeci ve AI Denetimi")
    st.write("**Onay Bekleyen Birim:** İK Departmanı")
    
    # AI AJANI BURADA DEVREYE GİRER
    st.warning(f"⚠️ **DİKKAT:** Atlas_Operasyon_01 ilerlemeyi %{ilerleme} beyan ederken, KPI başarısını %{kpi_beyan} olarak girdi.")
    
    c_onay1, c_onay2 = st.columns(2)
    with c_onay1:
        st.error(f"AI Atlas Analizi: İlerleme (%{ilerleme}) ile KPI Beyanı (%{kpi_beyan}) arasında TUTARSIZLIK tespit edildi.")
        st.metric("Veri Güven Skoru", "35/100")
    
    with c_onay2:
        st.write("### Yönetici Aksiyonu")
        st.button("Veriyi Revizyon İçin Geri Gönder")
        st.button("Tutarsızlığa Rağmen Onayla (Riskli)")

# --- 3. KURUMSAL KONSOLİDE DASHBOARD ---
with tabs[2]:
    st.subheader("Kurum Geneli Performans Konsolidasyonu")
    
    # Konsolide Veri Tablosu
    kons_data = pd.DataFrame({
        "Departman": ["İK", "Operasyon", "Satış", "Finans"],
        "İş Planı %": [85, 62, 91, 88],
        "KPI Skoru %": [70, 58, 94, 90],
        "Kapasite Kullanımı %": [95, 80, 75, 60]
    })
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.write("**Departman Bazlı Performans Karşılaştırması**")
        st.bar_chart(kons_data.set_index("Departman")[["İş Planı %", "KPI Skoru %"]])
    
    with col_chart2:
        st.write("**Stratejik Risk Haritası**")
        st.line_chart(kons_data.set_index("Departman")["Kapasite Kullanımı %"])
    
    st.table(kons_data)

# --- 4. AI ATLAS: KARAR ODASI VE DÖNÜŞÜM ---
with tabs[3]:
    st.subheader("Stratejik Karar Destek Odası")
    st.markdown("### ❓ Neyi farklı yapmalıyız?")
    
    st.write("**Kritik Çıktı:** İK Departmanı Eğitim Verimliliği KPI'ı 3 aydır düşük seyrediyor.")
    
    with st.expander("AI Atlas Önerilerini Gör"):
        st.write("1. Mentorluk sistemini 'Liderlik' etiketiyle iş planına ekleyin.")
        st.write("2. Atlas_Operasyon_02'nin üzerindeki iş yükünü (Stajyer görüşmeleri) %20 azaltın.")
    
    karar = st.text_area("Alınan Stratejik Karar:", placeholder="Buraya alınan kararı yazın...")
    if st.button("Kararı Mühürle ve İş Planına Görev Olarak Ata"):
        st.success("Karar mühürlendi. Bu karar artık yeni bir operasyonel görevdir.")

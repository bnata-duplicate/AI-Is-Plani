import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date

# --- 1. VERİTABANI MİMARİSİ (DİNAMİK YAPI) ---
def vt_kur():
    conn = sqlite3.connect('ai_atlas_v7.db', check_same_thread=False)
    c = conn.cursor()
    # MODÜL 1: İş Planı (PDF Verileriyle Uyumlu Katman)
    c.execute('''CREATE TABLE IF NOT EXISTS is_plani 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, departman TEXT, ana_gorev TEXT, 
                  gorev_adi TEXT, sorumlu TEXT, baslangic TEXT, bitis TEXT, durum TEXT, ilerleme INTEGER)''')
    
    # MODÜL 2: KPI & Veri Dönüşümü (Dönüşüm Noktası Odaklı)
    c.execute('''CREATE TABLE IF NOT EXISTS kpi_sistemi 
                 (id INTEGER PRIMARY KEY, kpi_adi TEXT, kaynak_turu TEXT, hedef REAL, gercek REAL, 
                  onay_durumu TEXT, guven_skoru INTEGER, bagli_is_id INTEGER)''')
    conn.commit()
    conn.close()

vt_kur()

# --- 🤖 AI ATLAS DÖNÜŞÜM VE DOĞRULAMA AJANI ---
def ai_atlas_analizör(kpi_degeri, kaynak, plan_ilerleme):
    # Veri Kaynağı Güven Analizi 
    skor = 100 if kaynak == "Sistem (ERP/Log)" else 65
    
    # İş Planı Çapraz Kontrolü (Shift Question Hazırlığı)
    if kpi_degeri > (plan_ilerleme + 20):
        skor -= 45
        return skor, "🛑 TUTARSIZLIK: Operasyonel ilerleme bu başarıyı doğrulamıyor! 'Neyi farklı yapmalıyız?'"
    return skor, "✅ Veri Kaynağı ve İş Akışı Uyumlu."

# --- 🖥️ AI ATLAS ANA PANEL ---
st.set_page_config(page_title="AI Atlas Strategic OS", layout="wide")
st.title("🧬 AI Atlas: Kurumsal Dönüşüm ve Strateji Paneli")

tab1, tab2, tab3 = st.tabs(["📋 İş Planlama", "🎯 KPI & Veri Dönüşümü", "📈 Stratejik Analiz"])

# --- MODÜL 1: DİNAMİK İŞ PLANLAMA ---
with tab1:
    st.subheader("Operasyonel İş Planı (Sezon ve Faaliyet Yönetimi)")
    
    # Örnek Veri Girişi (PDF Belgelerinden Gelen Gerçek Veriler) 
    with st.expander("➕ Yeni Faaliyet / Irregüler İş Tanımla"):
        col1, col2 = st.columns(2)
        f_ana = col1.selectbox("Ana Görev Grubu", ["Sezon Açılış İşlemleri", "Sezon Faaliyetleri"])
        f_gorev = col2.text_input("Görev Adı (Örn: Lise Stajyer Görüşmeleri)")
        f_sorumlu = st.multiselect("Sorumlu (AI ID)", ["Atlas_Operasyon_01", "Atlas_Operasyon_02"])
        f_baslangic = st.date_input("Başlangıç Tarihi", value=date(2022, 11, 21))
        f_bitis = st.date_input("Bitiş Tarihi (Termin)")
        
    # Mevcut İş Planı Tablosu (Simüle Edilen Veri Seti)
    is_listesi = [
        ["İK", "Sezon Açılış İşlemleri", "Sezon Açılış İşlemleri", "Atlas_Operasyon_01", "2022-11-21", "2023-02-21", 100],
        ["İK", "Sezon Faaliyetleri", "Lise Stajyer Görüşmeleri", "Atlas_Operasyon_01; 02", "2023-02-01", "2023-06-30", 40],
        ["İK", "Sezon Faaliyetleri", "Terfi Kurulunun Toplanması", "Atlas_Operasyon_01; 02", "2023-02-21", "2023-02-28", 100]
    ]
    df_is = pd.DataFrame(is_listesi, columns=["Birim", "Ana Görev", "Görev Adı", "Sorumlu", "Başlangıç", "Bitiş", "İlerleme %"])
    st.dataframe(df_is, use_container_width=True)

# --- MODÜL 2: KPI & VERİ DÖNÜŞÜMÜ (RACI ONAY ZİNCİRİ) ---
with tab2:
    st.subheader("Veri Kaynağı Tanımlama ve Onay Mekanizması")
    c1, c2 = st.columns([2, 1])
    
    with c1:
        k_metrik = st.selectbox("KPI Seçin", ["Personel Devir Oranı", "Eğitim Verimliliği", "Stajyer Verimlilik Skoru"])
        k_kaynak = st.radio("Veri Kaynağı", ["Sistem (ERP/Log)", "İş Planı (Otomatik)", "Manuel Beyan"])
        k_val = st.slider("Gerçekleşen Başarı (%)", 0, 100, 75)
        bagli_is = st.selectbox("Bağlı Oldu İş Planı Maddesi", df_is["Görev Adı"].tolist())
    
    with c2:
        st.write("### ⛓️ RACI Hiyerarşisi")
        st.write("**Sorumlu (R):** Atlas_Operasyon_01")
        st.write("**Onaycı (A):** Birim Amiri")
        st.write("**Danışman (C):** AI Atlas Ajanı")
        
        # AI Analizi Çalıştır
        st_ilerleme = df_is[df_is["Görev Adı"] == bagli_is]["İlerleme %"].values[0]
        skor, mesaj = ai_atlas_analizör(k_val, k_kaynak, st_ilerleme)
        
        if st.button("Veriyi Sisteme Kilitle"):
            st.metric("AI Güven Skoru", f"{skor}/100")
            if skor < 60: st.error(mesaj)
            else: st.success(mesaj)

# --- MODÜL 3: STRATEJİK ANALİZ (DÖNÜŞÜM NOKTASI) ---
with tab3:
    st.subheader("Dönüşüm Noktası (Shift Question) Analizi")
    st.markdown("### ❓ KPI'yı iyileştirmek için NEYİ farklı yapmalıyız?")
    st.info("Bu bölümdeki analizler, 2. Fazda kurulacak OKR sisteminin temelidir.")
    # Stratejik Grafik
    chart_data = pd.DataFrame({"Kriter": ["Liderlik", "Kültür", "Yetkinlik"], "Gelişim": [65, 80, 45]})
    st.bar_chart(chart_data.set_index("Kriter"))

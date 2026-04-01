import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date

# --- 1. VERİTABANI MİMARİSİ: AI ATLAS MASTER ---
def vt_kur():
    conn = sqlite3.connect('ai_atlas_v6.db', check_same_thread=False)
    c = conn.cursor()
    # MODÜL 1: Operasyonel İş Planı (PDF Verileriyle Uyumlu) 
    c.execute('''CREATE TABLE IF NOT EXISTS is_plani 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, departman TEXT, ana_gorev TEXT, 
                  gorev_adi TEXT, sorumlu TEXT, baslangic TEXT, bitis TEXT, durum TEXT)''')
    
    # MODÜL 2: KPI & Veri Dönüşümü (Onay Hiyerarşili) 
    c.execute('''CREATE TABLE IF NOT EXISTS kpi_sistemi 
                 (id INTEGER PRIMARY KEY, kpi_adi TEXT, kaynak_turu TEXT, hedef REAL, gercek REAL, 
                  onay_kademesi TEXT, guven_skoru INTEGER)''')
    conn.commit()
    conn.close()

vt_kur()

# --- 🤖 AI ATLAS DÖNÜŞÜM VE DOĞRULAMA AJANI ---
def ai_atlas_dogrulayici(kpi_degeri, kaynak, ilgili_is_durumu):
    # Veri Kaynağı Güven Analizi: Sistem verisi manuel girişi denetler.
    skor = 100 if kaynak == "Sistem (ERP/Bordro)" else 65
    
    # İş Planı Çapraz Kontrolü: Operasyonel gerçeklik testi.
    # İş planındaki görev (Örn: Stajyer Görüşmeleri) bitmeden başarı skoru yüksekse güven düşer. 
    if kpi_degeri > 80 and ilgili_is_durumu != "Tamamlandı":
        skor -= 40
        return skor, "🛑 TUTARSIZLIK: İş planındaki operasyonel süreçler bu başarı skorunu doğrulamıyor!"
    return skor, "✅ Veri Kaynağı ve Operasyonel Akış Uyumlu."

# --- 🖥️ AI ATLAS KONTROL PANELİ ---
st.set_page_config(page_title="AI Atlas Strategic OS", layout="wide")
st.title("🧬 AI Atlas: Kurumsal Dönüşüm ve Strateji Paneli")

tab1, tab2, tab3 = st.tabs(["📋 İş Planlama", "🎯 KPI & Veri Dönüşümü", "📈 Stratejik OKR Analizi"])

# --- MODÜL 1: İŞ PLANLAMA (KOD İSİMLERLE ANONİMİZE EDİLMİŞ) ---
with tab1:
    st.subheader("Operasyonel İş Planı (Sezon ve Faaliyet Yönetimi)")
    # PDF belgelerinden gelen gerçek veriler kod isimlerle eşleşti 
    is_verisi = {
        "Departman": ["İK", "İK", "İK", "İK"],
        "Ana Görev": ["Sezon Açılış İşlemleri", "Sezon Faaliyetleri", "Sezon Faaliyetleri", "Sezon Faaliyetleri"],
        "Görev Adı": [
            "Sezon Açılış İşlemleri", 
            "Stajyer Seçimi Yazışmaları", 
            "Lise Stajyer Görüşmeleri", 
            "Terfi Kurulunun Toplanması"
        ],
        "Sorumlu (AI ID)": [
            "Atlas_Operasyon_01", 
            "Atlas_Operasyon_01; Atlas_Operasyon_02", 
            "Atlas_Operasyon_01; Atlas_Operasyon_02", 
            "Atlas_Operasyon_01; Atlas_Operasyon_02"
        ],
        "Süre (Gün)": [92, 72, 149, 7], # 
        "Bitiş": ["2023-02-21", "2023-02-01", "2023-06-30", "2023-02-28"] # 
    }
    df_is = pd.DataFrame(is_verisi)
    st.dataframe(df_is, use_container_width=True)
    
    st.info("💡 Atlas_Operasyon_01 ve Atlas_Operasyon_02 sorumluluk alanındaki görevler AI Atlas tarafından takip edilmektedir.")

# --- MODÜL 2: KPI & VERİ DÖNÜŞÜMÜ (RACI ONAY ZİNCİRİ) ---
with tab2:
    st.subheader("Veri Kaynağı Tanımlama ve Hesap Verebilirlik (RACI)")
    c1, c2 = st.columns([2, 1])
    
    with c1:
        # KPI belgesinden gelen gerçek metrikler 
        k_metrik = st.selectbox("KPI Seçin", [
            "Personel Devir Oranı", 
            "Eğitim Verimliliği", 
            "Çalışan Bağlılığı Anket Skoru",
            "İç Kaynakla Pozisyon Doldurma Oranı"
        ])
        k_kaynak = st.radio("Veri Kaynağı Tipi", ["Sistem (ERP/Bordro)", "İş Planı (Otomatik)", "Manuel Beyan"])
        k_gercek = st.slider("Gerçekleşen Başarı (%)", 0, 100, 60)
        
    with c2:
        st.write("### ⛓️ RACI Hiyerarşisi")
        st.write("**Sorumlu (R):** Atlas_Operasyon_01")
        st.write("**Onaycı (A):** Birim / Departman Yöneticisi")
        st.write("**Danışman (C):** Atlas_Denetim_01")
        
        # AI AJANI ÇALIŞTIRMA (Örnek Durum: Devam Ediyor)
        skor, mesaj = ai_atlas_dogrulayici(k_gercek, k_kaynak, "Devam Ediyor")
        
        if st.button("Veriyi Sisteme Mühürle"):
            st.metric("AI Güven Skoru", f"{skor}/100")
            if skor < 65: st.error(mesaj)
            else: st.success(mesaj)

# --- MODÜL 3: OKR DÖNÜŞÜMÜ (STRATEJİK ANALİZ) ---
with tab3:
    st.subheader("Değer, Yetkinlik ve Kültür Odaklı OKR Dönüşümü")
    st.write("İş planı ve KPI katmanından süzülen verilerin stratejik hedeflere etkisi:")
    
    # Stratejik Gelişim Grafiği (Liderlik, Kültür, Yetkinlik)
    chart_data = pd.DataFrame({
        "Boyut": ["Liderlik", "Kurumsal Kültür", "Yetkinlik"], 
        "Gelişim %": [70, 85, 50]
    })
    st.bar_chart(chart_data.set_index("Boyut"))
    
    st.markdown("""
    > **AI Atlas Strateji Notu:** Atlas_Operasyon_01'in 'Sezon Açılış' görevlerindeki hızı, 
    > 'Operasyonel Çeviklik' OKR'sine doğrudan pozitif katkı sağlamaktadır. 
    > Ancak manuel veri girişlerindeki güven skoru, 'Şeffaflık' değerimizi riske atmaktadır.
    """)

import streamlit as st
import pandas as pd
from datetime import date

# --- 🛰️ SİSTEM AYARLARI ---
st.set_page_config(page_title="AI Atlas Strategic OS", layout="wide")

st.title("🧬 AI Atlas: Kurumsal Stratejik İşletim Sistemi")
st.caption("Operasyonel Veri Giriş Merkezi (PDF Kaynaklı Veri Setleri)")

# --- 📊 ÜST PANEL (Dinamik Özet) ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Toplam Aktif Görev", "12 Adet", "Sezon Açılış")
c2.metric("Bekleyen Onay", "4 Adet", "Kritik")
c3.metric("AI Güven Skoru", "88/100", "Stabil")
c4.metric("Dönüşüm Bekleyen KPI", "3 Adet", "Aksiyon Gerekli")

st.divider()

# --- 🛠️ ANA PROGRAM AKIŞI (SEKMELER) ---
tabs = st.tabs([
    "👤 KİŞİ: VERİ GİRİŞ EKRANLARI", 
    "🏢 DEPT: ONAY & ARA DEĞERLENDİRME", 
    "📈 KURUM: KONSOLİDE DASHBOARD", 
    "⚖️ AI ATLAS: KARAR ODASI"
])

# --- 1. KİŞİ: VERİ GİRİŞ EKRANLARI (PDF'DEKİ TÜM BAŞLIKLAR) ---
with tabs[0]:
    st.subheader("📋 Günlük ve Dönemsel Faaliyet Girişi")
    st.info("Lütfen sorumlu olduğunuz faaliyet alanına ait verileri giriniz.")

    # PDF VERİ GİRİŞ NOKTASI 1: SEZON AÇILIŞ VE FAALİYETLER
    with st.expander("🚀 SEZON AÇILIŞ VE REVİZYON İŞLEMLERİ", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("**Operasyonel Durum**")
            sezon_durum = st.selectbox("Sezon Hazırlık Durumu", ["Hazırlık", "Revizyon", "Tamamlandı", "Ertelendi"], key="s1")
            ilerleme_s = st.slider("Genel Hazırlık İlerlemesi (%)", 0, 100, 40, key="s2")
        with col2:
            st.write("**Dokümantasyon**")
            talimat_sayisi = st.number_input("Güncellenen Talimat/Prosedür Sayısı", 0, 50, 0)
            onay_durum = st.checkbox("Yönetim Onayı Alındı mı?")
        with col3:
            st.write("**Zamanlama**")
            st.date_input("Tahmini Bitiş Tarihi", value=date(2023, 6, 30))
            st.button("Sezon Verilerini Kaydet")

    # PDF VERİ GİRİŞ NOKTASI 2: STAJYER VE İŞE ALIM SÜREÇLERİ
    with st.expander("🎓 STAJYER SEÇİM VE MÜLAKAT YÖNETİMİ"):
        col4, col5, col6 = st.columns(3)
        with col4:
            st.write("**Mülakat Havuzu**")
            aday_sayisi = st.number_input("Görüşülen Toplam Aday Sayısı", 0, 500, 0)
            mulakat_puani = st.slider("Aday Kalite Ortalaması (1-10)", 1, 10, 5)
        with col5:
            st.write("**Yerleştirme**")
            secilen_stajyer = st.number_input("Seçilen/Onaylanan Stajyer", 0, 100, 0)
            stajyer_kpi = st.progress(secilen_stajyer/100 if secilen_stajyer <= 100 else 1.0)
        with col6:
            st.write("**AI Analiz Notu**")
            st.text_area("Mülakat Engelleyicileri:", "Örn: Teknik yetkinlik yetersizliği...", height=100)
            st.button("Stajyer Verilerini Gönder")

    # PDF VERİ GİRİŞ NOKTASI 3: TERFİ VE EĞİTİM YÖNETİMİ
    with st.expander("📈 TERFİ KURULU VE EĞİTİM VERİMLİLİĞİ"):
        col7, col8 = st.columns(2)
        with col7:
            st.write("**Terfi Kurulu**")
            aday_personel = st.number_input("Kurula Giren Personel Sayısı", 0, 50, 0)
            terfi_onay = st.number_input("Onaylanan Terfi Sayısı", 0, 50, 0)
        with col8:
            st.write("**Eğitim**")
            egitim_saat = st.number_input("Toplam Verilen Eğitim (Saat)", 0, 1000, 0)
            basari_skoru = st.slider("Eğitim Başarı Puanı (%)", 0, 100, 75)
        st.button("Eğitim/Terfi Verilerini Mühürle")

# --- DİĞER SEKMELER (Geliştirilmeye Hazır Boş Yapı) ---
with tabs[1]:
    st.subheader("🏢 Departman Onay Süzgeci")
    st.write("Kişi sekmesinden girilen veriler burada AI tarafından denetlenir.")

with tabs[2]:
    st.subheader("📈 Kurumsal Konsolide Dashboard")
    st.write("Tüm operasyonel verilerin stratejik özeti.")

with tabs[3]:
    st.subheader("⚖️ AI ATLAS: Karar Odası")
    st.write("Neyi farklı yapmalıyız? sorusunun sorulduğu yer.")

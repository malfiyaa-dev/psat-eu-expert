import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- 1. KONFIGURASI API GEMINI ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except FileNotFoundError:
    st.error("⚠️ File .streamlit/secrets.toml tidak ditemukan. Harap masukkan API Key.")
    st.stop()
except Exception as e:
    st.error(f"⚠️ Terjadi masalah konfigurasi API: {e}")
    st.stop()

# --- 2. FUNGSI BACA PDF ---
@st.cache_resource
def load_pdf_content(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except FileNotFoundError:
        return None
    except Exception as e:
        return None

# Load File PDF (Pastikan nama file 'regulasi.pdf' ada di folder proyek)
PDF_FILENAME = "Regulasi.pdf" 
pdf_text = load_pdf_content(PDF_FILENAME)

# --- 3. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="PSAT EU Expert", page_icon="🌱", layout="wide")

st.title("🌱 Asisten Sampling PSAT (Ekspor EU)")
st.markdown("Kalkulator Sampling Khusus **Pangan Segar Asal Tumbuhan (PSAT) by Muhamad Alfiya** - Regulasi EU 2023/2782.")

if pdf_text:
    st.success(f"✅ Database Regulasi Terhubung: {PDF_FILENAME}")
else:
    st.error(f"❌ File PDF '{PDF_FILENAME}' tidak ditemukan. Mohon RENAME file PDF Anda menjadi 'regulasi.pdf'.")

# Tab Navigasi
tab1, tab2 = st.tabs(["🧮 Kalkulator Sampling PSAT", "🤖 Konsultasi AI"])

# ==========================================
# TAB 1: KALKULATOR SAMPLING (KHUSUS PSAT)
# ==========================================
with tab1:
    st.header("Rencana Sampling Komoditas Tumbuhan")
    st.write("Pilih jenis komoditas tumbuhan (PSAT) di bawah ini:")

    # --- LOGIKA PERHITUNGAN SAMPLING (HANYA PSAT) ---
    def get_sampling_plan(category_code, weight):
        
        # --- A. CEREALS & OILSEEDS (Serealia & Biji-bijian) ---
        if category_code.startswith("A."):
            # Sumber: Table 2 Part A [cite: 187]
            if weight >= 50: return {"n": 100, "agg": "10 kg", "note": "Lot Besar (≥ 50 ton). Part A.3."}
            if weight <= 0.05: return {"n": 3, "agg": "1 kg", "note": "Lot ≤ 0.05 ton"}
            elif weight <= 0.5: return {"n": 5, "agg": "1 kg", "note": "Lot 0.05-0.5 ton"}
            elif weight <= 1.0: return {"n": 10, "agg": "1 kg", "note": "Lot 0.5-1 ton"}
            elif weight <= 3.0: return {"n": 20, "agg": "2 kg", "note": "Lot 1-3 ton"}
            elif weight <= 10.0: return {"n": 40, "agg": "4 kg", "note": "Lot 3-10 ton"}
            elif weight <= 20.0: return {"n": 60, "agg": "6 kg", "note": "Lot 10-20 ton"}
            else: return {"n": 100, "agg": "10 kg", "note": "Lot 20-50 ton"}

        # --- B. DRIED FRUIT (Buah Kering non-Ara) ---
        elif category_code.startswith("B."):
            # Sumber: Table 2 Part B [cite: 232]
            if weight >= 15: return {"n": 100, "agg": "10 kg", "note": "Lot Besar (≥ 15 ton). Part B.3."}
            if weight <= 0.1: return {"n": 10, "agg": "1 kg", "note": "Lot ≤ 0.1 ton"}
            elif weight <= 0.2: return {"n": 15, "agg": "1.5 kg", "note": "Lot 0.1-0.2 ton"}
            elif weight <= 0.5: return {"n": 20, "agg": "2 kg", "note": "Lot 0.2-0.5 ton"}
            elif weight <= 1.0: return {"n": 30, "agg": "3 kg", "note": "Lot 0.5-1.0 ton"}
            elif weight <= 2.0: return {"n": 40, "agg": "4 kg", "note": "Lot 1.0-2.0 ton"}
            elif weight <= 5.0: return {"n": 60, "agg": "6 kg", "note": "Lot 2.0-5.0 ton"}
            elif weight <= 10.0: return {"n": 80, "agg": "8 kg", "note": "Lot 5.0-10.0 ton"}
            else: return {"n": 100, "agg": "10 kg", "note": "Lot 10-15 ton"}

        # --- C. DRIED FIGS (Buah Ara) ---
        elif category_code.startswith("C."):
            # Sumber: Table 2 Part C [cite: 275]
            if weight >= 15: return {"n": 100, "agg": "30 kg", "note": "Lot Besar (≥ 15 ton). Part C.3."}
            if weight <= 0.1: return {"n": 10, "agg": "3 kg", "note": "Lot ≤ 0.1 ton"}
            elif weight <= 0.2: return {"n": 15, "agg": "4.5 kg", "note": "Lot 0.1-0.2 ton"}
            elif weight <= 0.5: return {"n": 20, "agg": "6 kg", "note": "Lot 0.2-0.5 ton"}
            elif weight <= 1.0: return {"n": 30, "agg": "9 kg", "note": "Lot 0.5-1.0 ton"}
            elif weight <= 2.0: return {"n": 40, "agg": "12 kg", "note": "Lot 1.0-2.0 ton"}
            elif weight <= 5.0: return {"n": 60, "agg": "18 kg", "note": "Lot 2.0-5.0 ton"}
            elif weight <= 10.0: return {"n": 80, "agg": "24 kg", "note": "Lot 5.0-10.0 ton"}
            else: return {"n": 100, "agg": "30 kg", "note": "Lot 10-15 ton"}

        # --- D. NUTS (Kacang-kacangan) ---
        elif category_code.startswith("D."):
            # Sumber: Table 2 Part D [cite: 342]
            if weight >= 15: return {"n": 100, "agg": "20 kg", "note": "Lot Besar (≥ 15 ton). Part D.3."}
            if weight <= 0.1: return {"n": 10, "agg": "2 kg", "note": "Lot ≤ 0.1 ton"}
            elif weight <= 0.2: return {"n": 15, "agg": "3 kg", "note": "Lot 0.1-0.2 ton"}
            elif weight <= 0.5: return {"n": 20, "agg": "4 kg", "note": "Lot 0.2-0.5 ton"}
            elif weight <= 1.0: return {"n": 30, "agg": "6 kg", "note": "Lot 0.5-1.0 ton"}
            elif weight <= 2.0: return {"n": 40, "agg": "8 kg", "note": "Lot 1.0-2.0 ton"}
            elif weight <= 5.0: return {"n": 60, "agg": "12 kg", "note": "Lot 2.0-5.0 ton"}
            elif weight <= 10.0: return {"n": 80, "agg": "16 kg", "note": "Lot 5.0-10.0 ton"}
            else: return {"n": 100, "agg": "20 kg", "note": "Lot 10-15 ton"}

        # --- E. SPICES (Rempah Kering Utuh) ---
        elif category_code.startswith("E."):
            # Sumber: Table 2 Part E [cite: 414]
            if weight >= 15: return {"n": 100, "agg": "10 kg", "note": "Lot Besar (≥ 15 ton). Part E.3."}
            if weight <= 0.01: return {"n": 5, "agg": "0.5 kg", "note": "Lot ≤ 0.01 ton"}
            elif weight <= 0.1: return {"n": 10, "agg": "1 kg", "note": "Lot 0.01-0.1 ton"}
            elif weight <= 0.2: return {"n": 15, "agg": "1.5 kg", "note": "Lot 0.1-0.2 ton"}
            elif weight <= 0.5: return {"n": 20, "agg": "2 kg", "note": "Lot 0.2-0.5 ton"}
            elif weight <= 1.0: return {"n": 30, "agg": "3 kg", "note": "Lot 0.5-1.0 ton"}
            elif weight <= 2.0: return {"n": 40, "agg": "4 kg", "note": "Lot 1.0-2.0 ton"}
            elif weight <= 5.0: return {"n": 60, "agg": "6 kg", "note": "Lot 2.0-5.0 ton"}
            elif weight <= 10.0: return {"n": 80, "agg": "8 kg", "note": "Lot 5.0-10.0 ton"}
            else: return {"n": 100, "agg": "10 kg", "note": "Lot 10-15 ton"}

        # --- G. COFFEE & COCOA (Kopi & Kakao) ---
        elif category_code.startswith("G."):
            # Sumber: Table 2 Part G [cite: 478]
            if weight >= 15: return {"n": 100, "agg": "10 kg", "note": "Lot Besar (Part G.3)"}
            if weight <= 0.1: return {"n": 10, "agg": "1 kg", "note": "Lot ≤ 0.1 ton"}
            elif weight <= 0.2: return {"n": 15, "agg": "1.5 kg", "note": "Lot 0.1-0.2 ton"}
            elif weight <= 0.5: return {"n": 20, "agg": "2 kg", "note": "Lot 0.2-0.5 ton"}
            elif weight <= 1.0: return {"n": 30, "agg": "3 kg", "note": "Lot 0.5-1.0 ton"}
            elif weight <= 2.0: return {"n": 40, "agg": "4 kg", "note": "Lot 1.0-2.0 ton"}
            elif weight <= 5.0: return {"n": 60, "agg": "6 kg", "note": "Lot 2.0-5.0 ton"}
            elif weight <= 10.0: return {"n": 80, "agg": "8 kg", "note": "Lot 5.0-10.0 ton"}
            else: return {"n": 100, "agg": "10 kg", "note": "Lot 10-15 ton"}

        # --- H. VEGETABLE OILS (Minyak Nabati) ---
        elif category_code.startswith("K."):
            # Sumber: Table 2 Part K (based on packages logic for cleaner UI) [cite: 566]
            if weight <= 0.05: return {"n": 3, "agg": "1 kg", "note": "Part K (≤ 50kg)"}
            elif weight <= 0.5: return {"n": 5, "agg": "1 kg", "note": "Part K (50-500kg)"}
            else: return {"n": 10, "agg": "1 kg", "note": "Part K (> 500kg). Lihat Part N jika Curah."}

        # --- I. HERBS & TEA (Herbal, Teh, Rempah Bubuk) ---
        elif category_code.startswith("M."):
             # Sumber: Table 2 Part M [cite: 615]
            if weight >= 15: return {"n": 50, "agg": "4.0 kg", "note": "Lot Besar (Part M.3)."}
            if weight <= 0.1: return {"n": 3, "agg": "0.2 kg", "note": "Lot ≤ 0.1 ton"}
            elif weight <= 0.5: return {"n": 10, "agg": "0.8 kg", "note": "Lot 0.1-0.5 ton"}
            elif weight <= 5.0: return {"n": 25, "agg": "2.0 kg", "note": "Lot 0.5-5.0 ton"}
            elif weight <= 10.0: return {"n": 35, "agg": "2.8 kg", "note": "Lot 5.0-10.0 ton"}
            else: return {"n": 50, "agg": "4.0 kg", "note": "Lot 10-15 ton"}

        return {"n": "Manual", "agg": "1 kg", "note": "Cek Dokumen"}

    # --- UI INPUT KHUSUS PSAT ---
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Pilihan DISESUAIKAN (Hanya PSAT)
        psat_options = [
            "A. Cereals & Oilseeds (Serealia/Bijian)",
            "B. Dried Fruit except Figs (Buah Kering)",
            "C. Dried Figs (Buah Ara Kering)",
            "D. Groundnuts/Nuts (Kacang-kacangan)",
            "E. Dried Spices (Rempah Kering Utuh)",
            "G. Coffee & Cocoa (Kopi/Kakao)",
            "K. Vegetable Oils (Minyak Nabati)",
            "M. Herbs, Tea, Powdered Spices (Teh/Bubuk)"
        ]
        pil_kategori = st.selectbox("Pilih Komoditas PSAT:", psat_options)
        pil_berat = st.number_input("Berat Lot (Ton):", min_value=0.0, step=0.01, format="%.2f")
        tombol_hitung = st.button("Hitung Sampel", type="primary")

    with col2:
        if tombol_hitung and pil_berat > 0:
            hasil = get_sampling_plan(pil_kategori, pil_berat)
            
            st.divider()
            st.subheader("📋 Hasil Sampling Plan")
            
            c1, c2 = st.columns(2)
            with c1: st.success(f"**Jumlah Titik Sampel (n):**\n# {hasil['n']} titik")
            with c2: st.warning(f"**Berat Minimum Sampel Agregat (Kg):**\n# {hasil['agg']}")
            st.caption(f"Dasar Regulasi: {hasil['note']}")

            # FITUR INSTRUKSI DETAIL (KEMBALI ADA)
            with st.expander("📝 Instruksi Detail Pengambilan Sampel", expanded=True):
                st.markdown(f"""
                1. **Persiapan:** Siapkan wadah bersih dan alat sampling yang sesuai (tombak/sekop).
                2. **Incremental Sampling:** Ambil sampel kecil secara acak dari **{hasil['n']} titik berbeda** di seluruh lot.
                3. **Berat per Titik:** Pastikan setiap pengambilan sampel kecil (incremental) beratnya cukup (biasanya ±100g) agar totalnya mencapai target.
                4. **Agregasi:** Gabungkan semua sampel kecil tersebut menjadi satu wadah besar.
                5. **Homogenisasi:** Aduk rata sampel gabungan.
                6. **Target Akhir:** Pastikan berat total sampel gabungan minimal **{hasil['agg']}**.
                """)
                
        elif tombol_hitung and pil_berat == 0:
            st.warning("⚠️ Masukkan berat lot lebih dari 0.")

# ==========================================
# TAB 2: CHATBOT AI
# ==========================================
with tab2:
    st.header("Konsultasi Regulasi PSAT")
    
    if not pdf_text:
        st.warning("⚠️ Harap masukkan file 'regulasi.pdf' ke folder proyek.")
    else:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for chat in st.session_state.chat_history:
            with st.chat_message(chat["role"]):
                st.markdown(chat["content"])

        user_query = st.chat_input("Contoh: Berapa batas mikotoksin untuk jagung?")
        
        if user_query:
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)

            with st.spinner("Sedang menganalisis regulasi..."):
                try:
                    # MENGGUNAKAN GEMINI-1.5-FLASH
                    model = genai.GenerativeModel("gemini-2.5-flash") 
                    
                    final_prompt = f"""
                    Kamu adalah ahli Pengawas Mutu Hasil Pertanian (PMHP) spesialis Pangan Segar Asal Tumbuhan (PSAT).
                    Jawab pertanyaan user berdasarkan konteks dokumen EU 2023/2782 berikut.
                    
                    KONTEKS DOKUMEN:
                    {pdf_text[:40000]}
                    
                    PERTANYAAN USER:
                    {user_query}
                    
                    JAWABAN (Bahasa Indonesia Formal):
                    """
                    
                    response = model.generate_content(final_prompt)
                    ai_reply = response.text
                    
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
                    with st.chat_message("assistant"):
                        st.markdown(ai_reply)

                except Exception as e:
                    # Fallback ke gemini-pro
                    try:
                        model = genai.GenerativeModel("gemini-pro")
                        response = model.generate_content(final_prompt)
                        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                        with st.chat_message("assistant"):
                            st.markdown(response.text)
                    except:
                        st.error(f"Error AI: {e}")
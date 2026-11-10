import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(
    page_title="Pendataan Penyu",
    page_icon="🐢",
    layout="centered"
)

st.title("🐢 Sistem Pendataan Penyu Bertelur")
st.subheader("Konservasi Penyu Pangumbahan")
st.write("Aplikasi untuk mencatat hasil pengamatan penyu bertelur.")

FILE = "data_penyu.csv"

# Membaca data
if os.path.exists(FILE):
    data = pd.read_csv(FILE)
else:
    data = pd.DataFrame(columns=[
        "Tanggal",
        "Jumlah Penyu",
        "Total Telur",
        "Rata-rata Telur"
    ])

st.divider()

st.header("📝 Form Pendataan")

with st.form("form_penyu"):
    tanggal = st.date_input(
        "Tanggal Pengamatan",
        value=date.today()
    )

    jumlah_penyu = st.number_input(
        "Jumlah Penyu Bertelur",
        min_value=1,
        step=1
    )

    total_telur = st.number_input(
        "Jumlah Total Telur",
        min_value=1,
        step=1
    )

    simpan = st.form_submit_button("💾 Simpan Data")

if simpan:
    if total_telur < jumlah_penyu:
        st.error("Jumlah telur tidak boleh lebih sedikit dari jumlah penyu.")
    else:
        rata_rata = total_telur / jumlah_penyu

        data_baru = pd.DataFrame([{
            "Tanggal": tanggal.strftime("%Y-%m-%d"),
            "Jumlah Penyu": jumlah_penyu,
            "Total Telur": total_telur,
            "Rata-rata Telur": round(rata_rata, 2)
        }])

        data = pd.concat(
            [data, data_baru],
            ignore_index=True
        )

        data.to_csv(FILE, index=False)

        st.success("Data pengamatan berhasil disimpan!")

st.divider()

st.header("📊 Riwayat Pengamatan")

if not data.empty:
    st.dataframe(data, use_container_width=True)

    st.subheader("Ringkasan Data")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Penyu", int(data["Jumlah Penyu"].sum()))
    col2.metric("Total Telur", int(data["Total Telur"].sum()))
    col3.metric("Jumlah Pengamatan", len(data))

    csv = data.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Unduh Laporan CSV",
        data=csv,
        file_name="laporan_pendataan_penyu.csv",
        mime="text/csv"
    )
else:
    st.info("Belum ada data pengamatan.")

st.divider()
st.caption("Sistem Pendataan Penyu | Konservasi Penyu Pangumbahan")

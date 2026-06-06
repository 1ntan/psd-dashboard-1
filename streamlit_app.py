import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Food Delivery Dashboard",
    page_icon="🍔",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* Background utama */
.stApp {
    background-color: #FFF7ED;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #FED7AA;
}

/* Judul */
h1 {
    color: #EA580C !important;
    font-size: 50px !important;
    font-weight: bold !important;
}

/* Subjudul */
h2, h3 {
    color: #C2410C !important;
}

/* Text */
p, li, label {
    color: #334155 !important;
}

/* Metric card */
[data-testid="metric-container"] {
    background-color: white;
    border: 2px solid #F97316;
    padding: 15px;
    border-radius: 15px;
}

/* Tombol */
.stButton button {
    background-color: #F97316;
    color: white;
    border-radius: 10px;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    DATA_FILENAME = Path(__file__).parent / "data/scenario_results.csv"
    df = pd.read_csv(DATA_FILENAME)
    return df
df = load_data()

# =========================================================
# TITLE
# =========================================================

st.title("🍔 Dashboard Simulasi Food Delivery Online")

st.markdown("""
Dashboard ini menampilkan hasil simulasi sistem food delivery online menggunakan pendekatan Agent-Based Modeling (ABM).

Tujuan simulasi adalah menganalisis:
- Waktu tunggu pelanggan
- Jumlah pesanan yang berhasil diselesaikan
- Jumlah pesanan yang dibatalkan
- Performa sistem pada berbagai skenario operasional
""")

# =========================================================
# MANUAL INPUT SIMULATION
# =========================================================

st.sidebar.header("⚙️ Parameter Simulasi")

input_drivers = st.sidebar.slider(
    "Number of Drivers",
    min_value=1,
    max_value=20,
    value=5
)

input_restaurants = st.sidebar.slider(
    "Number of Restaurants",
    min_value=1,
    max_value=10,
    value=3
)

input_customers = st.sidebar.slider(
    "Number of Customers",
    min_value=100,
    max_value=5000,
    value=1000,
    step=100
)

# SIMPLE ESTIMATION MODEL

estimated_waiting_time = round(
    (input_customers / input_drivers) * 0.1
    +
    (10 / input_restaurants),
    2
)

estimated_completed_orders = int(
    input_customers * (
        input_drivers / (
            input_drivers + 2
        )
    )
)

estimated_canceled_orders = int(
    input_customers -
    estimated_completed_orders
)

# =========================================================
# DISPLAY MANUAL SIMULATION
# =========================================================

with st.container(border=True):
    st.subheader("🧪 Simulasi Interaktif")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Estimated Waiting Time",
            estimated_waiting_time
        )

    with col2:
        st.metric(
            "Estimated Completed Orders",
            estimated_completed_orders
        )

    with col3:
        st.metric(
            "Estimated Canceled Orders",
            estimated_canceled_orders
        )

# =========================================================
# MANUAL SIMULATION CHART
# =========================================================

manual_df = pd.DataFrame({
    "Metric": [
        "Waiting Time",
        "Completed Orders",
        "Canceled Orders"
    ],
    "Value": [
        estimated_waiting_time,
        estimated_completed_orders,
        estimated_canceled_orders
    ]
})

with st.container(border=True):
    st.subheader("📊 Visualisasi Simulasi")

    fig_manual = px.bar(
        manual_df,
        x="Metric",
        y="Value",
        text="Value"
    )

    fig_manual.update_layout(
        paper_bgcolor="#FFF7ED",
        plot_bgcolor="#FFF7ED",
        height=400
    )

    st.plotly_chart(
        fig_manual,
        use_container_width=True,
        config=plotly_config
    )

# =========================================================
# SHOW DATA
# =========================================================

st.subheader("📊 Hasil Simulasi")
st.dataframe(df)

# =========================================================
# SCENARIO DESCRIPTION
# =========================================================

st.subheader("📖 Deskripsi Skenario")

with st.expander("Very Busy"):
    st.write(
        "Kondisi beban pesanan sangat tinggi sehingga antrean dan waktu tunggu cenderung meningkat."
    )

with st.expander("Normal"):
    st.write(
        "Kondisi operasional normal dengan keseimbangan antara jumlah pesanan dan sumber daya."
    )

with st.expander("Medium Improvement"):
    st.write(
        "Peningkatan sumber daya untuk mengurangi antrean dan memperbaiki performa layanan."
    )

with st.expander("More Drivers"):
    st.write(
        "Fokus pada penambahan kapasitas pengantaran untuk mempercepat proses delivery."
    )

with st.expander("High Optimization"):
    st.write(
        "Kondisi optimal dengan pengelolaan sumber daya yang lebih efisien."
    )

st.info(
    """
    Setiap skenario digunakan untuk mengevaluasi pengaruh perubahan kondisi operasional
    terhadap waktu tunggu pelanggan, jumlah pesanan yang berhasil diselesaikan,
    dan jumlah pesanan yang dibatalkan.
    """
)

# =========================================================
# SCENARIO FILTER
# =========================================================

scenarios = df["Scenario"].unique()
selected_scenarios = st.multiselect(
    "Pilih Skenario",
    scenarios,
    default=scenarios
)

filtered_df = df[
    df["Scenario"].isin(selected_scenarios)
]

# =========================================================
# CANCELLATION RATE
# =========================================================

filtered_df = filtered_df.copy()
filtered_df["Cancellation Rate (%)"] = (
    filtered_df["Canceled Orders"] /
    (
        filtered_df["Completed Orders"] +
        filtered_df["Canceled Orders"]
    )
) * 100

# =========================================================
# PLOTLY CONFIG
# =========================================================

plotly_config = {
    "scrollZoom": True,
    "displaylogo": False
}

# =========================================================
# WAITING TIME CHART
# =========================================================

with st.container(border=True):
    st.subheader("⏳ Rata-rata Waktu Tunggu")

    fig_wait = px.line(
        filtered_df,
        x="Scenario",
        y="Average Waiting Time",
        markers=True
    )

    fig_wait.update_layout(
        paper_bgcolor="#FFF7ED",
        plot_bgcolor="#FFF7ED",
        height=400
    )

    st.plotly_chart(
        fig_wait,
        use_container_width=True,
        config=plotly_config
    )
    
# =========================================================
# COMPLETED ORDERS
# =========================================================

with st.container(border=True):
    st.subheader("✅ Pesanan Selesai")

    fig_completed = px.bar(
        filtered_df,
        x="Scenario",
        y="Completed Orders"
    )

    fig_completed.update_layout(
        paper_bgcolor="#FFF7ED",
        plot_bgcolor="#FFF7ED",
        height=400
    )

    st.plotly_chart(
        fig_completed,
        use_container_width=True,
        config=plotly_config
    )

# =========================================================
# CANCELED ORDERS
# =========================================================

with st.container(border=True):
    st.subheader("❌ Pesanan Dibatalkan")

    fig_cancel = px.bar(
        filtered_df,
        x="Scenario",
        y="Canceled Orders"
    )

    fig_cancel.update_layout(
        paper_bgcolor="#FFF7ED",
        plot_bgcolor="#FFF7ED",
        height=400
    )

     st.plotly_chart(
        fig_cancel,
        use_container_width=True,
        config=plotly_config
    )

# =========================================================
# CANCELLATION RATE CHART
# =========================================================

with st.container(border=True):
    st.subheader("📉 Tingkat Pembatalan (%)")

    fig_rate = px.bar(
        filtered_df,
        x="Scenario",
        y="Cancellation Rate (%)"
    )

    fig_rate.update_layout(
        paper_bgcolor="#FFF7ED",
        plot_bgcolor="#FFF7ED",
        height=400
    )

       st.plotly_chart(
        fig_rate,
        use_container_width=True,
        config=plotly_config
    )

# =========================================================
# PERBANDINGAN ANTAR SKENARIO
# =========================================================

with st.container(border=True):

    st.subheader("📊 Perbandingan Antar Skenario")

    comparison_df = filtered_df.melt(
        id_vars="Scenario",
        value_vars=[
            "Completed Orders",
            "Canceled Orders"
        ],
        var_name="Metrik",
        value_name="Nilai"
    )

    fig_compare = px.bar(
        comparison_df,
        x="Scenario",
        y="Nilai",
        color="Metrik",
        barmode="group"
    )

    fig_compare.update_layout(
        paper_bgcolor="#FFF7ED",
        plot_bgcolor="#FFF7ED",
        height=450
    )

    st.plotly_chart(
        fig_wait,
        use_container_width=True,
        config=plotly_config
    )

# =========================================================
# METRICS
# =========================================================

st.subheader("📌 Ringkasan Hasil")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "Average Waiting Time",
        round(
            filtered_df["Average Waiting Time"].mean(),
            2
        )
    )

with col2:
    st.metric(
        "Completed Orders",
        int(
            filtered_df["Completed Orders"].sum()
        )
    )

with col3:
    st.metric(
        "Canceled Orders",
        int(
            filtered_df["Canceled Orders"].sum()
        )
    )

# =========================================================
# SKENARIO TERBAIK
# =========================================================

st.subheader("🏆 Skenario Terbaik")

best_scenario = filtered_df.loc[
    filtered_df["Average Waiting Time"].idxmin()
]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Skenario",
        best_scenario["Scenario"]
    )

with col2:
    st.metric(
        "Waktu Tunggu",
        f"{best_scenario['Average Waiting Time']} menit"
    )

with col3:
    st.metric(
        "Pesanan Selesai",
        int(best_scenario["Completed Orders"])
    )

with col4:
    st.metric(
        "Pesanan Dibatalkan",
        int(best_scenario["Canceled Orders"])
    )

# =========================================================
# CONCLUSION
# =========================================================

st.subheader("📝 Kesimpulan")

st.write("""
Berdasarkan hasil simulasi, performa sistem food delivery dipengaruhi oleh jumlah driver, kapasitas restoran, dan tingkat kedatangan pelanggan.
Skenario dengan jumlah driver yang lebih banyak cenderung menghasilkan waktu tunggu yang lebih rendah, tingkat pembatalan yang lebih kecil, serta kepuasan pelanggan yang lebih tinggi dibandingkan skenario lainnya.
""")

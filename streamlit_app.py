import streamlit as st
import pandas as pd
from pathlib import Path

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

st.title("🍔 Food Delivery Online Simulation Dashboard")

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

st.sidebar.header("⚙️ Simulation Input")

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
    st.subheader("🧪 Manual Simulation Test")
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
    st.subheader("📊 Manual Simulation Visualization")
    st.bar_chart(
        manual_df,
        x="Metric",
        y="Value"
    )

# =========================================================
# SHOW DATA
# =========================================================

st.subheader("📊 Simulation Results")
st.dataframe(df)

# =========================================================
# SCENARIO DESCRIPTION
# =========================================================

st.subheader("📖 Scenario Description")
scenario_desc = pd.DataFrame({
    "Scenario": [
        "Normal",
        "Peak Hour",
        "Extra Driver",
        "Low Patience"
    ],
    "Description": [
        "Jumlah driver dan order seimbang",
        "Jumlah order meningkat saat jam sibuk",
        "Penambahan jumlah driver",
        "Pelanggan memiliki tingkat kesabaran rendah"
    ]
})

st.table(scenario_desc)


# =========================================================
# SCENARIO FILTER
# =========================================================

scenarios = df["Scenario"].unique()
selected_scenarios = st.multiselect(
    "Select Scenario",
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
# WAITING TIME CHART
# =========================================================

with st.container(border=True):
    st.subheader("⏳ Average Waiting Time")
    st.line_chart(
        filtered_df,
        x="Scenario",
        y="Average Waiting Time"
    )

# =========================================================
# COMPLETED ORDERS
# =========================================================

with st.container(border=True):
    st.subheader("✅ Completed Orders")
    st.bar_chart(
        filtered_df,
        x="Scenario",
        y="Completed Orders"
    )

# =========================================================
# CANCELED ORDERS
# =========================================================

with st.container(border=True):
    st.subheader("❌ Canceled Orders")
    st.bar_chart(
        filtered_df,
        x="Scenario",
        y="Canceled Orders"
    )

# =========================================================
# CANCELLATION RATE CHART
# =========================================================

with st.container(border=True):
    st.subheader("📉 Cancellation Rate (%)")
    st.bar_chart(
        filtered_df,
        x="Scenario",
        y="Cancellation Rate (%)"
    )

# =========================================================
# METRICS
# =========================================================

st.subheader("📌 Summary Metrics")
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
# BEST SCENARIO
# =========================================================

st.subheader("🏆 Best Scenario")

best_scenario = filtered_df.loc[
    filtered_df["Average Waiting Time"].idxmin()
]

st.success(
    f"""
    Scenario : {best_scenario['Scenario']}
    Average Waiting Time : {best_scenario['Average Waiting Time']} menit
    Completed Orders : {best_scenario['Completed Orders']}
    Canceled Orders : {best_scenario['Canceled Orders']}
    """
)

# =========================================================
# CONCLUSION
# =========================================================

st.subheader("📝 Conclusion")

st.write("""
Berdasarkan hasil simulasi, performa sistem food delivery dipengaruhi oleh jumlah driver, kapasitas restoran, dan tingkat kedatangan pelanggan.
Skenario dengan jumlah driver yang lebih banyak cenderung menghasilkan waktu tunggu yang lebih rendah, tingkat pembatalan yang lebih kecil, serta kepuasan pelanggan yang lebih tinggi dibandingkan skenario lainnya.
""")

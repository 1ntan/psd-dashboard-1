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
    background-color: #0F172A;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1E293B;
}

/* Judul */
h1 {
    color: #F97316 !important;
    font-size: 50px !important;
    font-weight: bold !important;
}

/* Subjudul */
h2, h3 {
    color: #FDBA74 !important;
}

/* Text biasa */
p, li, label {
    color: white !important;
}

/* Metric card */
[data-testid="metric-container"] {
    background-color: #1E293B;
    border: 2px solid #F97316;
    padding: 15px;
    border-radius: 15px;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 10px;
}

/* Tombol */
.stButton button {
    background-color: #F97316;
    color: white;
    border-radius: 10px;
    border: none;
}

/* Selectbox */
.stMultiSelect {
    background-color: #1E293B;
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
Dashboard ini menampilkan hasil simulasi sistem food delivery online menggunakan:
- Agent-Based Modeling (ABM)
- Discrete Event Simulation (DES)
- Monte Carlo Simulation
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
# CONCLUSION
# =========================================================

st.subheader("📝 Conclusion")

st.write("""
Hasil simulasi menunjukkan bahwa penambahan jumlah driver dan kapasitas restaurant dapat mengurangi waiting time pelanggan dan meningkatkan performa sistem food delivery online.
""")
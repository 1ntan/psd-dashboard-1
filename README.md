# 🍔 Food Delivery Online Simulation Dashboard

Project ini merupakan simulasi sistem food delivery online menggunakan:

- Agent-Based Modeling (ABM)
- Discrete Event Simulation (DES)
- Monte Carlo Simulation

Simulasi dibuat menggunakan Python, SimPy, dan Streamlit untuk menganalisis performa sistem food delivery berdasarkan beberapa skenario.

---

# 📌 Tujuan Project

Menganalisis performa sistem food delivery online berdasarkan:
- jumlah driver
- jumlah restaurant
- waiting time customer
- completed order
- canceled order

---

# ⚙️ Metode Simulasi

## 1. Agent-Based Modeling (ABM)
Digunakan untuk memodelkan interaksi antar agent:
- Customer
- Driver
- Restaurant

## 2. Discrete Event Simulation (DES)
Digunakan untuk memodelkan event:
- order masuk
- cooking process
- delivery process

## 3. Monte Carlo Simulation
Digunakan untuk menjalankan simulasi sebanyak 1000 iterasi pada setiap skenario.

---

# 📊 Skenario Simulasi

| Scenario | Drivers | Restaurants |
|---|---|---|
| Very Busy | 3 | 2 |
| Normal | 5 | 3 |
| Medium Improvement | 7 | 3 |
| More Drivers | 10 | 4 |
| High Optimization | 15 | 5 |

---

# 📈 Dashboard Features

- Waiting Time Visualization
- Completed Orders Visualization
- Canceled Orders Visualization
- Monte Carlo Simulation Visualization
- Interactive Manual Simulation Input

---

# 🖥️ Dashboard Preview

Tambahkan screenshot dashboard di sini.

---

# 🚀 Cara Menjalankan Dashboard

```bash
streamlit run streamlit_app.py
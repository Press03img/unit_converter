import streamlit as st

# ==============================

# 幅制限（中央寄せ）

# ==============================

st.markdown(
""" <style>
.main > div {
max-width: 600px;
margin: auto;
} </style>
""",
unsafe_allow_html=True
)

st.title("単位換算ツール")

# ==============================

# 単位定義

# ==============================

units = {
"長さ": {
"m": 1,
"cm": 0.01,
"mm": 0.001,
"μm": 1e-6,
"nm": 1e-9,
"km": 1000
},
"力": {
"N": 1,
"kN": 1000,
"mN": 0.001,
"kgf": 9.80665,
"gf": 0.00980665,
"lbf": 4.44822,
"ozf": 0.2780139,
"klbf": 4448.22
},
"圧力": {
"Pa": 1,
"N/m^2": 1,
"kPa": 1000,
"kN/m^2": 1000,
"MPa": 1e6,
"GPa": 1e9,
"bar": 1e5,
"psi": 6894.76,
"ksi": 6.89476e6,
"N/mm^2": 1e6,
"kN/mm^2": 1e9,
"kgf/mm^2": 9.80665e6,
"gf/mm^2": 9.80665e3,
"kgf/m^2": 9.80665,
"gf/m^2": 0.00980665
},
"速度": {
"m/s": 1,
"cm/s": 0.01,
"mm/s": 0.001,
"m/min": 1/60,
"km/min": 1000/60,
"cm/min": 0.01/60,
"km/h": 1000/3600,
"ft/sec": 0.3048,
"kn": 0.514444
}
}

# ==============================

# 入力値

# ==============================

col_input, _ = st.columns([1, 1])
with col_input:
value = st.number_input(
"値",
value=0.0,
step=1.0
)

# ==============================

# カテゴリ

# ==============================

col_category, _ = st.columns([1, 1])
with col_category:
category = st.selectbox(
"カテゴリ",
list(units.keys())
)

unit_list = list(units[category].keys())

# ==============================

# 初期化

# ==============================

if "from_unit" not in st.session_state:
st.session_state.from_unit = unit_list[0]

if "to_unit" not in st.session_state:
st.session_state.to_unit = unit_list[0]

# ==============================

# 単位選択

# ==============================

col1, col_btn, col2 = st.columns([4, 1, 4])

with col1:
from_unit = st.selectbox(
"変換元",
unit_list,
index=unit_list.index(st.session_state.from_unit)
)

with col_btn:
st.write("")
if st.button("🔁"):
st.session_state.from_unit, st.session_state.to_unit = (
st.session_state.to_unit,
st.session_state.from_unit
)
st.rerun()

with col2:
to_unit = st.selectbox(
"変換先",
unit_list,
index=unit_list.index(st.session_state.to_unit)
)

st.session_state.from_unit = from_unit
st.session_state.to_unit = to_unit

# ==============================

# 計算

# ==============================

base_value = value * units[category][from_unit]
result = base_value / units[category][to_unit]

# ==============================

# 表示

# ==============================

st.markdown(
f"<div style='font-size:24px; font-family: Arial;'>結果: {result}</div>",
unsafe_allow_html=True
)

st.text_input("コピー用（値のみ）", value=str(result))

import streamlit as st

st.set_page_config(layout="wide")

# ==============================
# 単位定義（削除なし＋追加反映済）
# ==============================
units = {
    "長さ": {
        "m": 1,
        "mm": 0.001,
        "cm": 0.01,
        "km": 1000,
        "inch": 0.0254,
        "ft": 0.3048
    },
    "質量": {
        "kg": 1,
        "g": 0.001,
        "mg": 0.000001,
        "lb": 0.453592
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
        "kPa": 1000,
        "MPa": 1000000,
        "GPa": 1000000000,
        "bar": 100000,
        "atm": 101325,
        "psi": 6894.76,
        "N/m^2": 1,
        "kN/m^2": 1000,
        "N/mm^2": 1000000,
        "kN/mm^2": 1000000000,
        "kgf/mm^2": 9806650,
        "gf/mm^2": 9806.65,
        "kgf/m^2": 9.80665,
        "gf/m^2": 0.00980665
    },
    "速度": {
        "m/s": 1,
        "km/h": 0.277778,
        "mph": 0.44704
    },
    "温度": {
        "C": "C",
        "F": "F",
        "K": "K"
    }
}

# ==============================
# 変換関数
# ==============================
def convert(value, from_unit, to_unit, category):
    if category == "温度":
        if from_unit == "C":
            if to_unit == "F":
                return value * 9/5 + 32
            elif to_unit == "K":
                return value + 273.15
        elif from_unit == "F":
            if to_unit == "C":
                return (value - 32) * 5/9
            elif to_unit == "K":
                return (value - 32) * 5/9 + 273.15
        elif from_unit == "K":
            if to_unit == "C":
                return value - 273.15
            elif to_unit == "F":
                return (value - 273.15) * 9/5 + 32
        return value
    else:
        base = value * units[category][from_unit]
        return base / units[category][to_unit]

# ==============================
# UI
# ==============================
st.title("単位換算ツール")

# ---- カテゴリ選択（幅統一）----
col_cat = st.columns([1])[0]
with col_cat:
    category = st.selectbox("カテゴリ", list(units.keys()))

unit_list = list(units[category].keys())

# ---- 横並び（幅調整）----
col1, col2, col3, col4 = st.columns([3, 2, 1, 2])

with col1:
    value = st.number_input("値", value=0.0)

with col2:
    from_unit = st.selectbox("変換元", unit_list)

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    convert_btn = st.button("→")

with col4:
    to_unit = st.selectbox("変換先", unit_list)

# ---- 出力 ----
if convert_btn:
    result = convert(value, from_unit, to_unit, category)
    st.success(f"{result:.6g} {to_unit}")

import streamlit as st

st.set_page_config(page_title="単位換算ツール", layout="centered")

st.title("単位換算ツール")

# ==============================
# 単位定義
# ==============================

unit_categories = {

    "長さ": {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1,
        "km": 1000,
        "inch": 0.0254,
        "ft": 0.3048
    },

    "質量": {
        "g": 0.001,
        "kg": 1,
        "t": 1000,
        "lb": 0.453592
    },

    "力・重量": {
        "N": 1,
        "kN": 1000,
        "kgf": 9.80665
    },

    "速度": {
        "m/s": 1,
        "km/h": 0.277778,
        "ft/s": 0.3048
    },

    "圧力・応力": {
        "Pa": 1,
        "kPa": 1000,
        "MPa": 1e6,
        "bar": 1e5,
        "kgf/cm2": 98066.5,
        "psi": 6894.76
    },

    "モーメント・トルク": {
        "N·m": 1,
        "kN·m": 1000,
        "kgf·m": 9.80665
    },

    "温度": {
        "C": "C",
        "K": "K",
        "F": "F"
    },

    "密度": {
        "kg/m3": 1,
        "g/cm3": 1000
    }
}

# ==============================
# カテゴリ選択
# ==============================

category = st.selectbox(
    "カテゴリを選択",
    list(unit_categories.keys())
)

unit_dict = unit_categories[category]
unit_list = list(unit_dict.keys())

# ==============================
# session_state 保護
# ==============================

if "from_unit" not in st.session_state or st.session_state.from_unit not in unit_list:
    st.session_state.from_unit = unit_list[0]

if "to_unit" not in st.session_state or st.session_state.to_unit not in unit_list:
    st.session_state.to_unit = unit_list[1] if len(unit_list) > 1 else unit_list[0]

# ==============================
# UI
# ==============================

value = st.number_input("値を入力", value=1.0)

col1, col2 = st.columns(2)

with col1:
    from_unit = st.selectbox(
        "変換元",
        unit_list,
        index=unit_list.index(st.session_state.from_unit)
    )

with col2:
    to_unit = st.selectbox(
        "変換先",
        unit_list,
        index=unit_list.index(st.session_state.to_unit)
    )

st.session_state.from_unit = from_unit
st.session_state.to_unit = to_unit

# ==============================
# 変換処理
# ==============================

if st.button("変換"):

    if category == "温度":

        if from_unit == "C":
            base = value + 273.15
        elif from_unit == "F":
            base = (value - 32) * 5/9 + 273.15
        else:
            base = value

        if to_unit == "C":
            result = base - 273.15
        elif to_unit == "F":
            result = (base - 273.15) * 9/5 + 32
        else:
            result = base

    else:

        base = value * unit_dict[from_unit]
        result = base / unit_dict[to_unit]

    # 指数表示禁止 + 小数4桁
    formatted = f"{result:.4f}"

    st.subheader("変換結果")
    st.success(f"{formatted} {to_unit}")

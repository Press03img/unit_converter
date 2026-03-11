import streamlit as st

st.title("単位換算ツール")

# 単位データ（SI基準）
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
    "力・重量": {
        "N": 1,
        "kN": 1000,
        "kgf": 9.80665
    },
    "速度": {
        "m/s": 1,
        "km/h": 0.277778
    },
    "圧力・応力": {
        "Pa": 1,
        "kPa": 1000,
        "MPa": 1000000,
        "bar": 100000,
        "kgf/cm²": 98066.5
    },
    "モーメント・トルク": {
        "N·m": 1,
        "kN·m": 1000
    },
    "密度": {
        "kg/m³": 1,
        "g/cm³": 1000
    }
}

# カテゴリ選択
category = st.selectbox("カテゴリ", list(units.keys()))

unit_list = list(units[category].keys())

# 入力
value = st.number_input("値を入力", value=0.0)

col1, col2 = st.columns(2)

with col1:
    from_unit = st.selectbox("変換前単位", unit_list)

with col2:
    to_unit = st.selectbox("変換後単位", unit_list)

# 変換
if st.button("変換"):

    base_value = value * units[category][from_unit]

    result = base_value / units[category][to_unit]

    st.subheader("変換結果")

    st.write(f"{result:.4g} {to_unit}")

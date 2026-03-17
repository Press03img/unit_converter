import streamlit as st

# ==============================
# ページ設定
# ==============================
st.set_page_config(layout="centered")

# ==============================
# 単位定義
# ==============================
units = {
    "長さ": {
        "m": 1, "mm": 0.001, "cm": 0.01, "km": 1000,
        "inch": 0.0254, "ft": 0.3048
    },
    "質量": {
        "kg": 1, "g": 0.001, "mg": 0.000001, "lb": 0.453592
    },
    "力": {
        "N": 1, "kN": 1000, "mN": 0.001,
        "kgf": 9.80665, "gf": 0.00980665,
        "lbf": 4.44822, "ozf": 0.2780139, "klbf": 4448.22
    },
    "圧力": {
        "Pa": 1, "kPa": 1000, "MPa": 1000000, "GPa": 1000000000,
        "bar": 100000, "atm": 101325, "psi": 6894.76,
        "N/m^2": 1, "kN/m^2": 1000,
        "N/mm^2": 1000000, "kN/mm^2": 1000000000,
        "kgf/mm^2": 9806650, "gf/mm^2": 9806.65,
        "kgf/m^2": 9.80665, "gf/m^2": 0.00980665
    },
    "速度": {
        "m/s": 1, "km/h": 0.277778, "mph": 0.44704
    },
    "温度": {
        "C": "C", "F": "F", "K": "K"
    }
}

# ==============================
# 上付き変換
# ==============================
def format_unit(unit):
    return unit.replace("^2", "²").replace("^3", "³")

# ==============================
# 変換処理
# ==============================
def convert(value, from_unit, to_unit, category):
    if category == "温度":
        if from_unit == "C":
            return value * 9/5 + 32 if to_unit == "F" else value + 273.15 if to_unit == "K" else value
        elif from_unit == "F":
            return (value - 32) * 5/9 if to_unit == "C" else (value - 32) * 5/9 + 273.15 if to_unit == "K" else value
        elif from_unit == "K":
            return value - 273.15 if to_unit == "C" else (value - 273.15) * 9/5 + 32 if to_unit == "F" else value
    else:
        base = value * units[category][from_unit]
        return base / units[category][to_unit]

# ==============================
# CSS（最大幅400px）
# ==============================
st.markdown("""
<style>
.block-container {
    max-width: 400px;
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

st.title("単位換算")

# ==============================
# 1行目
# ==============================
col1, col2 = st.columns([1,1])

with col1:
    category = st.selectbox("カテゴリ", list(units.keys()))

with col2:
    value = st.number_input("入力値", value=0.0)

unit_list = list(units[category].keys())

# ==============================
# ★ ここが重要：カテゴリ変更時のリセット
# ==============================
if "prev_category" not in st.session_state:
    st.session_state.prev_category = category

if st.session_state.prev_category != category:
    st.session_state.from_unit = unit_list[0]
    st.session_state.to_unit = unit_list[1] if len(unit_list) > 1 else unit_list[0]
    st.session_state.prev_category = category

# 初期値
if "from_unit" not in st.session_state:
    st.session_state.from_unit = unit_list[0]

if "to_unit" not in st.session_state:
    st.session_state.to_unit = unit_list[1] if len(unit_list) > 1 else unit_list[0]

# 表示用
unit_display = [format_unit(u) for u in unit_list]
unit_map = dict(zip(unit_display, unit_list))

# ==============================
# 2行目
# ==============================
col3, col4, col5 = st.columns([2,1,2])

with col3:
    from_disp = st.selectbox(
        "変換前",
        unit_display,
        index=unit_list.index(st.session_state.from_unit)
    )
    from_unit = unit_map[from_disp]

with col4:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⇄"):
        st.session_state.from_unit, st.session_state.to_unit = \
            st.session_state.to_unit, st.session_state.from_unit
        st.rerun()

with col5:
    to_disp = st.selectbox(
        "変換後",
        unit_display,
        index=unit_list.index(st.session_state.to_unit)
    )
    to_unit = unit_map[to_disp]

# 状態更新
st.session_state.from_unit = from_unit
st.session_state.to_unit = to_unit

# ==============================
# 3行目
# ==============================
col6, col7 = st.columns([1,1])

with col6:
    convert_btn = st.button("変換")

with col7:
    if convert_btn:
        result = convert(value, from_unit, to_unit, category)
        st.success(f"{result:.6g} {format_unit(to_unit)}")

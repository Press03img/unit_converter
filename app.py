import streamlit as st

# ==============================
# ページ設定
# ==============================
st.set_page_config(page_title="単位換算", layout="centered")

# ==============================
# 単位定義（ユーザー指定ベース）
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
# 上付き表示
# ==============================
def format_unit(u):
    return (
        u.replace("^2", "²")
         .replace("^3", "³")
         .replace("2", "²")
         .replace("3", "³")
    )

# ==============================
# 変換処理
# ==============================
def convert(value, from_unit, to_unit, category):
    base = value * units[category][from_unit]
    return base / units[category][to_unit]

# ==============================
# セッション初期化
# ==============================
if "from_unit" not in st.session_state:
    st.session_state.from_unit = list(units["長さ"].keys())[0]
if "to_unit" not in st.session_state:
    st.session_state.to_unit = list(units["長さ"].keys())[1]

# ==============================
# CSS
# ==============================
st.markdown("""
<style>
.block-container {
    max-width: 400px;
    padding-top: 1.5rem;
}
.stButton button {
    height: 48px;
    width: 100%;
}
input {
    height: 48px !important;
}
div[data-baseweb="select"] > div {
    height: 48px;
}
.result-box {
    background-color: #dff0d8;
    padding: 10px;
    border-radius: 8px;
    height: 48px;
    display: flex;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# UI
# ==============================

# 1行目
col1, col2 = st.columns([2,2])

with col1:
    category = st.selectbox("カテゴリ", list(units.keys()))

with col2:
    value = st.number_input("入力値", value=0.0)

# 単位リスト
unit_list = list(units[category].keys())
unit_display = [format_unit(u) for u in unit_list]
unit_map = dict(zip(unit_display, unit_list))

# 安全補正
if st.session_state.from_unit not in unit_list:
    st.session_state.from_unit = unit_list[0]
if st.session_state.to_unit not in unit_list:
    st.session_state.to_unit = unit_list[-1]

# 2行目
col3, col4, col5 = st.columns([2,1,2])

with col3:
    from_disp = st.selectbox(
        "変換前",
        unit_display,
        index=unit_list.index(st.session_state.from_unit)
    )
    st.session_state.from_unit = unit_map[from_disp]

with col4:
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
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
    st.session_state.to_unit = unit_map[to_disp]

# 3行目
col6, col7 = st.columns([2,2])

with col6:
    convert_btn = st.button("変換")

with col7:
    if convert_btn:
        result = convert(
            value,
            st.session_state.from_unit,
            st.session_state.to_unit,
            category
        )
        st.markdown(
            f"<div class='result-box'>{result:.6g} {format_unit(st.session_state.to_unit)}</div>",
            unsafe_allow_html=True
        )

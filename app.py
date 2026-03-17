import streamlit as st
from units import units   # ← ★ここが重要

# ==============================
# ページ設定
# ==============================
st.set_page_config(page_title="単位換算ツール", layout="wide")
st.markdown("<h3>単位換算ツール</h3>", unsafe_allow_html=True)

# ==============================
# 上付き表示
# ==============================
def format_unit(u):
    return (
        u.replace("^2", "²")
         .replace("^3", "³")
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
    first_cat = list(units.keys())[0]
    st.session_state.from_unit = list(units[first_cat].keys())[0]
    st.session_state.to_unit = list(units[first_cat].keys())[1]

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
    if st.button("変換"):
        result = convert(
            value,
            st.session_state.from_unit,
            st.session_state.to_unit,
            category
        )
        st.session_state.result = result

with col7:
    if "result" in st.session_state:
        st.markdown(
            f"<div class='result-box'>{st.session_state.result:.6g} {format_unit(st.session_state.to_unit)}</div>",
            unsafe_allow_html=True
        )

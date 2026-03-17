import streamlit as st
from units import units

# ==============================
# ページ設定
# ==============================
st.set_page_config(page_title="単位換算ツール", layout="wide")

st.write("")
st.write("")

st.markdown(
    "<div class='title'>単位換算ツール</div>",
    unsafe_allow_html=True
)

# ==============================
# 上付き表示
# ==============================
def format_unit(u):
    return (
        u.replace("^2", "²")
         .replace("^3", "³")
    )

# ==============================
# 変換処理（温度の特殊計算に対応）
# ==============================
def convert(value, from_unit, to_unit, category):
    # 温度カテゴリの場合（足し算・引き算が必要なため特殊処理）
    if category == "温度":
        # 1. まず全て摂氏(C)に正規化
        if from_unit == "℃":
            celsius = value
        elif from_unit == "℉":
            celsius = (value - 32) * 5/9
        elif from_unit == "K":
            celsius = value - 273.15
        else:
            celsius = value
            
        # 2. 摂氏から目的の単位へ変換
        if to_unit == "℃":
            return celsius
        elif to_unit == "℉":
            return (celsius * 9/5) + 32
        elif to_unit == "K":
            return celsius + 273.15
        else:
            return celsius
            
    # 通常の単位カテゴリの場合（比率計算）
    else:
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
.title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 10px;
}
.block-container {
    max-width: 400px;
    padding-top: 1.5rem;
    padding-bottom: 0.5rem;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    margin: 0 auto;
}
[data-testid="column"] {
    flex: 1 1 0% !important;
}
section.main > div {
    padding-bottom: 0rem;
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
    font-weight: bold;
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

# 単位リストの取得
unit_list = list(units[category].keys())
unit_display = [format_unit(u) for u in unit_list]
unit_map = dict(zip(unit_display, unit_list))

# 安全補正（カテゴリ切り替え時に存在しない単位を参照しないようにする）
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
        # 変換結果の表示（温度の場合は桁数を少し調整しても良いかもしれません）
        st.markdown(
            f"<div class='result-box'>{st.session_state.result:.6g} {format_unit(st.session_state.to_unit)}</div>",
            unsafe_allow_html=True
        )

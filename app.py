import streamlit as st
# ==============================
# CSS（高さ・余白調整）
# ==============================
st.markdown("""
<style>
.block-container {
    max-width: 400px;
    padding-top: 1.5rem;
}

/* ボタン高さ統一 */
.stButton button {
    height: 48px;
    width: 100%;
}

/* selectboxとinput高さ揃え */
div[data-baseweb="select"] > div {
    height: 48px;
}
input {
    height: 48px !important;
}

/* 結果表示ボックス */
.result-box {
    background-color: #dff0d8;
    padding: 10px;
    border-radius: 8px;
    height: 48px;
    display: flex;
    align-items: center;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 1行目
# ==============================
col1, col2 = st.columns([2,2])

with col1:
    category = st.selectbox("カテゴリ", list(units.keys()))

with col2:
    value = st.number_input("入力値", value=0.0)

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
    to_unit = unit_map[to_disp]

# ==============================
# 3行目
# ==============================
col6, col7 = st.columns([2,2])

with col6:
    convert_btn = st.button("変換")

with col7:
    if convert_btn:
        result = convert(value, from_unit, to_unit, category)
        st.markdown(
            f"<div class='result-box'>{result:.6g} {format_unit(to_unit)}</div>",
            unsafe_allow_html=True
        )

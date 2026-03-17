```python
import streamlit as st

# ==============================
# 幅制限（中央寄せ）
# ==============================
st.markdown("""
<style>
.main > div {
    max-width: 600px;
    margin: auto;
}
</style>
""", unsafe_allow_html=True)

st.title("単位換算ツール")

# ==============================
# 入力値（基準幅）
# ==============================
col_input, _ = st.columns([1, 1])

with col_input:
    value = st.number_input(
        "値",
        value=0.0,
        step=1.0,
        key="input_value"
    )

# ==============================
# カテゴリ（値と同幅）
# ==============================
col_category, _ = st.columns([1, 1])

with col_category:
    category = st.selectbox(
        "カテゴリ",
        ["長さ", "力", "圧力", "速度"],
        key="category"
    )

# ==============================
# 単位選択（合計幅＝値と同じ）
# ==============================
col1, col_btn, col2 = st.columns([4, 1, 4])

with col1:
    from_unit = st.selectbox(
        "変換元",
        ["m", "cm", "mm"],
        key="from_unit"
    )

with col_btn:
    st.write("")  # 高さ調整
    if st.button("🔁"):
        st.session_state.from_unit, st.session_state.to_unit = (
            st.session_state.to_unit,
            st.session_state.from_unit
        )
        st.rerun()

with col2:
    to_unit = st.selectbox(
        "変換先",
        ["m", "cm", "mm"],
        key="to_unit"
    )

# ==============================
# セッション反映
# ==============================
st.session_state.from_unit = from_unit
st.session_state.to_unit = to_unit
```

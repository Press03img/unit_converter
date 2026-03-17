import streamlit as st

st.set_page_config(page_title="Unit Converter", layout="centered")

# ==============================
# 幅制限（50%）
# ==============================
st.markdown("""
<style>
.main > div {
    max-width: 600px;
    margin: auto;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 数値表示フォーマット
# ==============================
def format_number(x):
    s = f"{x:.4f}"
    s = s.rstrip("0").rstrip(".")
    if s == "-0":
        s = "0"
    return s


# ==============================
# 単位データ
# ==============================
units = {
    "長さ": {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1,
        "km": 1000,
        "in": 0.0254,
        "ft": 0.3048
    },
    "質量": {
        "g": 0.001,
        "kg": 1,
        "t": 1000,
        "lb": 0.45359237
    },
    "力": {
        "N": 1,
        "kN": 1000,
        "kgf": 9.80665
    },
    "圧力・応力": {
        "Pa": 1,
        "kPa": 1000,
        "MPa": 1000000,
        "N/mm²": 1000000,
        "bar": 100000,
        "kgf/cm²": 98066.5
    },
    "速度": {
        "m/s": 1,
        "km/h": 0.277777778
    },
    "密度": {
        "kg/m³": 1,
        "g/cm³": 1000
    },
    "トルク": {
        "N·m": 1,
        "N·cm": 0.01,
        "N·mm": 0.001
    }
}

# ==============================
# 初期状態
# ==============================
if "from_unit" not in st.session_state:
    st.session_state.from_unit = "mm"

if "to_unit" not in st.session_state:
    st.session_state.to_unit = "cm"

if "result" not in st.session_state:
    st.session_state.result = None


# ==============================
# タイトル
# ==============================
st.title("単位変換ツール")


# ==============================
# カテゴリ
# ==============================
category = st.selectbox(
    "カテゴリ",
    list(units.keys()),
    key="category_box"
)

unit_list = list(units[category].keys())

if st.session_state.from_unit not in unit_list:
    st.session_state.from_unit = unit_list[0]

if st.session_state.to_unit not in unit_list:
    st.session_state.to_unit = unit_list[1]


# ==============================
# 入力（幅制限）
# ==============================
col_input, _ = st.columns([1,1])

with col_input:
    value = st.number_input(
        "値",
        value=0.0,
        step=1.0,
        key="input_value"
    )


# ==============================
# 単位選択
# ==============================
col1, col2, col3 = st.columns([4,1,4])

with col1:
    from_unit = st.selectbox(
        "変換元",
        unit_list,
        index=unit_list.index(st.session_state.from_unit),
        key="from_unit_box"
    )

with col2:
    st.write("")
    st.write("")
    if st.button("🔁", key="swap_button"):
        st.session_state.from_unit, st.session_state.to_unit = (
            st.session_state.to_unit,
            st.session_state.from_unit
        )
        st.rerun()

with col3:
    to_unit = st.selectbox(
        "変換先",
        unit_list,
        index=unit_list.index(st.session_state.to_unit),
        key="to_unit_box"
    )

st.session_state.from_unit = from_unit
st.session_state.to_unit = to_unit


# ==============================
# 変換ボタン
# ==============================
if st.button("変換", key="convert_button"):

    base_value = value * units[category][from_unit]
    result = base_value / units[category][to_unit]

    st.session_state.result = result


# ==============================
# 結果表示
# ==============================
if st.session_state.result is not None:

    formatted = format_number(st.session_state.result)

    st.subheader("変換結果")

    st.code(f"{formatted} {to_unit}")

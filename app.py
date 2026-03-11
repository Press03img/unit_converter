import streamlit as st

from units_data import units
from converter import convert
from history import add, get

st.title("単位変換ツール")

category = st.selectbox("カテゴリ", list(units.keys()))

value = st.number_input("数値", value=1.0)

from_unit = st.selectbox("変換元", list(units[category].keys()))

to_unit = st.selectbox("変換先", list(units[category].keys()))

if st.button("変換"):

    result = convert(value, from_unit, to_unit, category)

    st.success(result)

    add(f"{value} {from_unit} → {result} {to_unit}")


st.subheader("履歴")

for h in get():

    st.write(h)
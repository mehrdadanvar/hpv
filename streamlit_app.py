import streamlit as st
import pandas as pd
import numpy as np
df = pd.read_csv("./hpv/final.csv")
print(df.shape)
for x in df.columns:
    if pd.isna(df[x][0]):
        df = df.drop(x, axis=1)
without_names = df.columns[df.columns.str.contains("Unnamed")]
df.drop(list(without_names),axis=1,inplace=True)
df = df.drop(1,axis=0)
# new_names = [df[x][0] for x in df.columns]
# df.columns = new_names

st.text("HPV campaign test results!")
st.text("Mehrdad is great!")
st.write(df.head())
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)
st.text_input("Your name", key="name")

# You can access the value at any point with:
st.session_state.name
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data


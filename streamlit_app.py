import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
know = pd.read_csv("./knowscore.csv")
bel = pd.read_csv("./belscores.csv")
main = pd.read_csv("./hpv/final2.csv")
df = pd.merge(know,bel,how="left",on="d_time")
print(df.shape)
df = df.drop(index=range(4))
print(df.shape)

# new_names = [df[x][0] for x in df.columns]
# df.columns = new_names
#############################################
st.title("Save the FDU Knights Campaign")
st.divider()
st.header(":orange[Descriptive Statistics on Demographics]")
st.subheader("Gender")
source = pd.DataFrame(
    {"category": ["Male","Female"], "value": [15,26]}
)

c = alt.Chart(source).mark_arc(innerRadius=60).encode(theta="value",color="category:N")
st.altair_chart(c)

st.write(df["d_gender"].value_counts())

st.divider()
####################################################
st.subheader("Age")
age = list(df["d_age"])
fig,ax = plt.subplots()
ax.hist(age,bins=10,color="orange",edgecolor="white",alpha=0.8)
plt.xlim(15,55)
plt.xlabel("age")
plt.ylabel("frequency")
st.pyplot(fig)
st.write(df["d_age"].describe())
st.divider()
##################################################
st.subheader("Marital Status")
marry = df["d_marital"].value_counts()
marry_per = round((marry/41*100),1)
marriage = pd.DataFrame({"Counts":marry,"Percentages":marry_per})
st.table(marriage)
st.divider()
#########################################3########
st.subheader("Number of Children")
df["d_children"].value_counts()

def clean_child(row):
    ans = row["d_children"]
    category = ""
    if ans == "0":
        category = "No Child"
    else:
        category = ">=1 Child"
    return category
df["d_child"] = df.apply(lambda x:clean_child(x),axis=1)
df["d_child"].value_counts()
child = df["d_child"].value_counts()
child_per = round((child/41*100),1)
child_table = pd.DataFrame({"Counts":child,"Percentages":child_per})
st.table(child_table)
child_source = pd.DataFrame(
    {"category": ["No Child",">= 1 Child"], "value": [26,15]}
)

child_fig = alt.Chart(child_source).mark_arc(innerRadius=60).encode(theta="value",color="category:N")
st.altair_chart(child_fig)
st.divider()
####################################
st.subheader("Students' Income")
def clean_income(row):
    ans = row["d_income"]
    category = ""
    if ans =="$ 1000-1999 CAD" or ans=="< $ 1000 CAD":
        category ="< $2000 CAD"
    else:
        category = ">= $2000 CAD"
    return category
df["clean_income"]= df.apply(lambda x:clean_income(x),axis=1)
income = df["clean_income"].value_counts()
income_per = round((income/41*100),1)
income_table = pd.DataFrame({"Counts":income,"Percentages":income_per})
st.table(income_table)
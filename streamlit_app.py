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
import time

progress_text = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.005)
    my_bar.progress(percent_complete + 1, text=progress_text)
st.header("Section 1 :orange[Descriptive Statistics] on Demographics")
st.subheader("Gender")
source = pd.DataFrame(
    {"category": ["Male","Female"], "value": [15,26]}
)

c = alt.Chart(source).mark_arc(innerRadius=60).encode(theta="value",color="category:N")
st.altair_chart(c)

st.write(df["d_gender"].value_counts())

st.divider()
####################################################
st.subheader("Age Distribution Histogram")
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
income_source = pd.DataFrame(
    {"category": ["<$2000",">=2000"], "value": [23,18]}
)

income_fig = alt.Chart(income_source).mark_arc(innerRadius=60).encode(theta="value",color="category")
st.altair_chart(income_fig)
st.divider()
######################################
st.subheader("Religon")
def clean_religion(row):
    ans = row["d_religion"]
    cat = ""
    if ans =="Yes":
        cat="Yes"
    else:
        cat="No"
    return cat

df["clean_religion"] = df.apply(lambda x : clean_religion(x),axis=1)
religion = df["clean_religion"].value_counts()
religion_per = round((religion/41*100),1)
religion_table = pd.DataFrame({"Counts":religion,"Percentages":religion_per})
st.table(religion_table)
rel_source = pd.DataFrame(
    {"category": ["Yes","No"], "value": [29,12]}
)

rel_fig = alt.Chart(rel_source).mark_arc(innerRadius=60).encode(theta="value",color="category:N")
st.altair_chart(rel_fig)
st.divider()
#######################################3
st.subheader("Vaccination Status")
def clean_vaccination(row):
    ans = row["d_vaccinated"]
    category = ""
    if ans == "Yes, fully vaccinated.":
        category = "Positive"
    else:
        category = "Unsure | Negetaive"
    return category

df["clean_vaccinated"]= df.apply(lambda x:clean_vaccination(x),axis=1)
vaccination = df["clean_vaccinated"].value_counts()
vaccination_per = round((vaccination/41*100),1)
vaccination_table = pd.DataFrame({"Counts":vaccination,"Percentages":vaccination_per})
st.table(vaccination_table)
st.divider()
##########################################
st.header("Section 2 :orange[Hypothesis Testing] on Knowledge & Belief Scores")
st.subheader("Distribution of the :blue[Knowledge Score]")
st.write("Knowledge Score was calculated based on answers to :red[19] qustions.")
knowledge = list(df["k_finalscore"])
fig,ax = plt.subplots()
ax.hist(knowledge,bins=10,color="purple",edgecolor="white",alpha=0.8)
plt.xlim(1,24)
plt.xlabel("Knowledge Score")
plt.ylabel("Number of Students")
st.pyplot(fig)
st.write(df["k_finalscore"].describe())


st.divider()
################
st.subheader("Distribution of the :blue[Belief Score]")
st.write("Knowledge Score was calculated based on answers to :blue[18] qustions.")
belief = list(df["b_finalscore"])
fig,ax = plt.subplots()
ax.hist(belief,bins=10,color="cyan",edgecolor="white",alpha=0.8)
plt.xlim(4,16)
plt.xlabel("Belief Score")
plt.ylabel("Number of Students")
st.pyplot(fig)
st.write(df["b_finalscore"].describe())
st.divider()
#####################
st.subheader(":green[Hypothesis] : There Is No Association Between Students' Knowledge and Thier Beliefs on HPV")
st.subheader(":red[lets test that!]")
kb_fig,ax =plt.subplots()
ax.scatter(df.k_finalscore,df.b_finalscore,color="red")
ax.set(xlim=(2,26))
plt.xlabel("x : Knowledge Score")
plt.ylabel("y : Belief Score ")
st.pyplot(kb_fig)
#########################
a = 2
col1,col2,col3 =st.columns(3)
col1.metric(label="some text",value="5")
col2.metric("col2","7")


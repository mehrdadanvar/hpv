import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from scipy.stats import chi2_contingency

know = pd.read_csv("./knowscore.csv")
bel = pd.read_csv("./belscores.csv")
main = pd.read_csv("./hpv/final2.csv")
df = pd.merge(know,bel,how="left",on="d_time")
print(df.shape)
df = df.drop(index=range(4))
print(df.shape)
names = list(df.columns)
df = df.drop(columns=df.loc[:, df.columns.str.endswith('_1')])
print(df.columns)
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
st.write("Belief Score was calculated based on answers to :blue[18] qustions.")
belief = list(df["b_finalscore"])
fig,ax = plt.subplots()
ax.hist(belief,bins=10,color="cyan",edgecolor="white",alpha=0.8)
plt.xlim(4,16)
plt.xlabel("Belief Score")
plt.ylabel("Number of Students")
st.pyplot(fig)
st.write(df["b_finalscore"].describe())
st.divider()

###########################
st.header(":green[Hypothesis 1]")
st.subheader("There Is No Difference between Male and Female Students With Regards to Knowledge on HPV")
def categorize_knowledge(row):
    ans = row["k_finalscore"]
    category = "0"
    if ans > 13:
        category = "score>13"
    else:
        category="score<=13"
    return category

df["knowledge_score"] = df.apply(lambda x:categorize_knowledge(x), axis=1)
gender_know = pd.crosstab(df['d_gender'], df['knowledge_score'])
gk_chi2, gk_p_value, gk_dof, gk_expected = chi2_contingency(gender_know)
gk_sample = pd.DataFrame(gk_expected)
gender_know["Total"] = gender_know["score<=13"] + gender_know["score>13"]
sums = gender_know.sum()
gender_know.loc[len(gender_know)]= sums
gender_know.index = ["Female","Male","Total"]
st.subheader(":blue[Corsstab Gender & Knowledge Score (Observed)]")
st.table(gender_know)
gk_sample.index = ["Female","Male"]
gk_sample.columns = ["score<=13","score>13"]
gk_sample = gk_sample.reindex(columns= ["score<=13","score>13"])
st.subheader(":blue[Corsstab Gender & Knowledge Score (Expected)]")
st.table(gk_sample)
col1,col2,col3 = st.columns(3)
col1.metric(label="Chi-Squre",value=str(round(gk_chi2,3)))
col2.metric("P_value",str(round(gk_p_value,3)))
col3.metric("degrees of freedom",str(gk_dof))
st.write(":red[There is not enough evidence to reject the hypothesis!]")
st.divider()
#####################################3
st.header(":green[Hypothesis 2]")
st.subheader("There Is No Difference between Low and High Income Students With Regards to Knowledge on HPV")
def clean_income(row):
    ans = row["d_income"]
    category = ""
    if ans =="$ 1000-1999 CAD" or ans=="< $ 1000 CAD":
        category ="<$2000CAD"
    else:
        category = ">=$2000CAD"
    return category
df["clean_income"]= df.apply(lambda x:clean_income(x),axis=1)
income_know = pd.crosstab(df["clean_income"],df["knowledge_score"])
ki_chi2, ki_p_value, ki_dof, ki_expected = chi2_contingency(income_know)
ki_sample = pd.DataFrame(ki_expected)
income_know["Total"] = income_know["score<=13"] + income_know["score>13"]
sums = income_know.sum()
income_know.loc[len(income_know)]= sums
income_know.index = ["<$2000CAD",">=$2000CAD","Total"]
st.subheader(":blue[Crosstab Income & Knowledge Score (Observed)]")
st.table(income_know)
ki_sample.index = ["<$2000CAD",">=$2000CAD"]
ki_sample.columns = ["score<=13","score>13"]
ki_sample = ki_sample.reindex(columns= ["score<=13","score>13"])
st.subheader(":blue[Corsstab Income & Knowledge Score (Expected)]")
st.table(ki_sample)
col1,col2,col3 = st.columns(3)
col1.metric(label="Chi-Squre",value=str(round(ki_chi2,3)))
col2.metric("P_value",str(round(ki_p_value,3)))
col3.metric("degrees of freedom",str(ki_dof))
st.write(":red[There is not enough evidence to reject the hypothesis!]")
st.divider()
##########################
st.header(":green[Hypothesis 3]")
st.subheader("Students's Marital Status Is Not Linked to their Knowledge of HPV")
def  clean_marry(row):
    ans = row["d_marital"]
    category = ""
    if "Divorced" in ans or "Single" in ans:
        category = "Single"
    else:
        category = "Involved"
    return category
df["clean_marr"] = df.apply(lambda x:clean_marry(x),axis=1)
marry_know = pd.crosstab(df["clean_marr"],df["knowledge_score"])

mk_chi2, mk_p_value, mk_dof, mk_expected = chi2_contingency(marry_know)
mksample = pd.DataFrame(mk_expected)
marry_know["Total"] = marry_know["score<=13"] + marry_know["score>13"]
sums = marry_know.sum()
marry_know.loc[len(marry_know)]= sums
marry_know.index = ["Involved","Single","Total"]
st.subheader(":blue[Corsstab Marital Status & Knowledge Score(Observed)]")
st.table(marry_know)
mksample.index = ["Involved","Single"]
mksample.columns = ["score<=13","score>13"]
mksample = mksample.reindex(columns=["score<=13","score>13"])
st.subheader(":blue[Corsstab Marital Status & Knowledge Score (Expected)]")
st.table(mksample)
col1,col2,col3 = st.columns(3)
col1.metric(label="Chi-Squre",value=str(round(mk_chi2,3)))
col2.metric("P_value",str(round(mk_p_value,3)))
col3.metric("degrees of freedom",str(round(mk_dof,3)))
st.write(":green[There is enough evidence to reject the null hypothesis and support the alternative]")

st.divider()
#########################################################################
st.header("Section 3")
st.header("Hypothesis Testing on :purple[Belief Scores]")
st.subheader(":green[Hypothesis 4]")
st.subheader("There Is No Difference between Male and Female Students With Regards to Beliefs (Missconceptions) on HPV")
def cat_bel(row):
    ans = row["b_finalscore"]
    category = "0"
    if ans > 9:
        category = "score>9"
    else:
        category="score<=9"
    return category

df["belief_score"] = df.apply(lambda x:cat_bel(x), axis=1)
gender_bel = pd.crosstab(df['d_gender'], df['belief_score'])
gb_chi2, gb_p_value, gb_dof, gb_expected = chi2_contingency(gender_bel)
gb_sample = pd.DataFrame(gb_expected)
gender_bel["Total"] = gender_bel["score>9"] + gender_bel["score<=9"]
gbsums = gender_bel.sum()
gender_bel.loc[len(gender_bel)]= gbsums
gender_bel.index = ["Female","Male","Total"]
st.subheader(":blue[Corsstab Gender & Belief Score (Observed)]")
st.table(gender_bel)
gb_sample.index = ["Female","Male"]
gb_sample.columns = ["score>9","score<=9"]
gb_sample = gb_sample.reindex(columns=["score<=9","score>9"])
st.subheader(":blue[Corsstab Gender & Belief Score (Expected)]")
st.table(gb_sample)
col1,col2,col3 = st.columns(3)
col1.metric(label="Chi-Squre",value=str(round(gb_chi2,3)))
col2.metric("P_value",str(round(gb_p_value,3)))
col3.metric("degrees of freedom",str(round(gb_dof,3)))
st.write(":red[There is not enough evidence to reject the hypothesis!]")
st.divider()
##########################################33
st.subheader(":green[Hypothesis 5]")
st.subheader("Having Children Is Not Related to Missconceptions on HPV")
def clean_child(row):
    ans = row["d_children"]
    category = ""
    if ans == "0":
        category = "NoChild"
    else:
        category = ">=1Child"
    return category
df["cleaned_child"] = df.apply(lambda x:clean_child(x),axis=1)
chilbel = pd.crosstab(df['cleaned_child'], df['belief_score'])
rb_chi2, rb_p_value, rb_dof, rb_expected = chi2_contingency(chilbel)
rb_sample = pd.DataFrame(rb_expected)
chilbel["Total"] = chilbel["score>9"] + chilbel["score<=9"]
rbsums = chilbel.sum()
chilbel.loc[len(chilbel)]= rbsums
chilbel.index = [">=1Child","NoChild","Total"]
st.subheader(":blue[Corsstab Having Children & Belief Score (Observed)]")
st.table(chilbel)
rb_sample.index = [">=1Child","NoChild"]
rb_sample.columns = ["score>9","score<=9"]
rb_sample = rb_sample.reindex(columns=["score<=9","score>9"])
st.subheader(":blue[Corsstab Having Children & Belief Score (Expected)]")
st.table(rb_sample)
col1,col2,col3 = st.columns(3)
col1.metric(label="Chi-Squre",value=str(round(rb_chi2,3)))
col2.metric("P_value",str(round(rb_p_value,3)))
col3.metric("degrees of freedom",str(round(rb_dof,3)))
st.write(":green[There is enough evidence to reject the null hypothesis and support the alternative]")
st.divider()
#####################
st.subheader(":green[Hypothesis 6]")
st.subheader("There Is No Association Between Students' Knowledge and Thier Beliefs on HPV")
kb_fig,ax =plt.subplots()
ax.scatter(df.k_finalscore,df.b_finalscore,color="purple")
ax.set(xlim=(2,26))
plt.xlabel("x : Knowledge Score")
plt.ylabel("y : Belief Score ")
st.pyplot(kb_fig)
#########################
import scipy.stats as ss
col1,col2=st.columns(2)
col1.metric(label="Pearson Correlation Coefficient",value= round(ss.pearsonr(df.k_finalscore,df.b_finalscore)[0],2))
col2.metric("P_Value",value= round(ss.pearsonr(df.k_finalscore,df.b_finalscore)[1],4))
st.write(":green[There is enough evidence to reject the null hypothesis and support the alternative]")
st.divider()
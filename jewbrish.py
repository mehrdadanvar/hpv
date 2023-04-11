def recode_values(df):
    translation_list = []
    for col in df.columns:
        if df[col].dtype == "object":
            print(True)
            categories = df[col].unique()
            if "TRUE" in categories: 
                print("inclues yes") 
            recode_map = {category:i for i,category in enumerate(categories)}
            df[col] = df[col].replace(recode_map)
            translation_list.append({col:recode_map})
        else:
            print(False)
    return df, translation_list

import matplotlib.pyplot as plt
sample =1
know = 1
know.hist("k_finalscore",bins=20)
plt.show()
grouped = sample.groupby("d_gender")
fig, ax = plt.subplots()
for name, group in grouped:
    ax.hist(group['k_finalscore'], bins=5, alpha=0.5, label=name)

# add labels and legend to the plot
ax.set_xlabel('Final Score')
ax.set_ylabel('Count')
ax.legend()

# show the plot
plt.show()
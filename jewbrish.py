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

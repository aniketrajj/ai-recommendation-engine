#Use the ai-recommendation-engine as project root folder as links are all relative to that
#Cleaning users_raw.csv using pandas and thefuzz(Fuzzy matching)

import pandas as pd
#Used to calculate similarity between two words and fix typos using mathematical Levenshtein Distance to generate scores
from thefuzz import process 

print("Starting user data cleaning...\n")

#Reading the raw file into a DataFrame
raw_users = pd.read_csv("../ai-recommendation-engine/data/raw/users_raw.csv")
clean_users = raw_users.copy()
# print(raw_users) #Before cleaning
# print(raw_users.info())

#Cleaning the file column by column

#Cleaning column: user_id
# print(clean_users.value_counts(subset="user_id",dropna=False))
clean_users = clean_users.drop_duplicates(subset=["user_id"])
clean_users = clean_users.dropna(subset="user_id")
# print(clean_users.value_counts(subset="user_id",dropna=False))

#Cleaning column: city
# print(clean_users.value_counts(subset="city",dropna=False))

valid_cities = [
    'rourkela','bhubaneswar','mumbai','new_delhi','kolkata',
    'pune','bangalore','chennai','hyderabad','ahmedabad',
    'jaipur','lucknow','chandigarh','indore'
]

def fix_city_name(city):
    #If this "if" block is executed then the functions exixts as there is a return block
    if pd.isna(city):
        return "missing"
    
    clean_city = city.strip().lower()

    #match the closest to the clean_city from the valid_cities list and give score of match
    match,score = process.extractOne(clean_city, valid_cities)

    if score >= 70 :
        return match
    
    else:
        return "missing"

#apply function iterates over each value in "city" column, using apply functions we are not calling the function, we are telling pandas to call the function for us.
clean_users["city"] = clean_users["city"].apply(fix_city_name)
# print(clean_users.value_counts(subset="city",dropna=False))

#Cleaning column: employment_status
# print(clean_users.value_counts(subset="employment_status",dropna=False))
clean_users["employment_status"] = clean_users["employment_status"].str.lower().str.strip().str.replace(" ","_").replace("notemployed","not_employed")
clean_users["employment_status"] = clean_users["employment_status"].fillna("missing")
# print(clean_users.value_counts(subset="employment_status",dropna=False))


print(clean_users.info())
print("\nUser data cleaned successfully!")

#Saving this clean_users dataframe into a new users_clean.csv file
clean_users.to_csv("../ai-recommendation-engine/data/processed/users_clean.csv", index=False)

print("File saved as users_clean.csv under ai-recommendation-engine/data/processed/")
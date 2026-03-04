#Use the ai-recommendation-engine as project root folder as links are all relative to that
#This gives us a mathematical score for our recommendation model of how accurate it is
#Rules for modules: 1. Module name should not start with a number or _ 2. Do not use .py extension for module
#Imports also work differently, python doesn't take the current working directory as the project root, use python -m from terminal to run such files

import pandas as pd

#import recommendation function from recommend.py for score calculation
#use package-module logic and give entire path as ai-recommendation-engine is the top level directory
from src.models.recommend import recommendation

#To calculate mean from list
import statistics as st

#Read the test_interactions only no need for user-item or similarity files as its present on models file which is imported
test_df = pd.read_csv("../ai-recommendation-engine/data/processed/test_interactions.csv")

k = 10 #No of recommendations for which scores are calculated

precision_list = []
recall_list = []
f1_list = []

#iterrows() used to iterate row by row(series) from dataframe
for _, row in test_df.iterrows():

    user_id = row["user_id"]
    hidden_pr = row["pr_id"]

    recommendations = recommendation(user_id,k)
    
    #If recommendation logic recommends product that was hidden
    if hidden_pr in recommendations:
        
        precision_score = 1/k
        recall_score = 1
        f1_score = 2*(precision_score*recall_score)/(precision_score+recall_score)

    else:
        precision_score = 0
        recall_score = 0
        f1_score = 0
    
    precision_list.append(precision_score)
    recall_list.append(recall_score)
    f1_list.append(f1_score)

precision = st.mean(precision_list)
recall = st.mean(recall_list)
f1 = st.mean(f1_list)

print(f"Total test interactions evaluated: {len(test_df)}")
print(f"Precision@{k}: {precision:.4f}")
print(f"Recall@{k}: {recall:.4f}")
print(f"F1@{k}: {f1:.4f}")

#use python -m src.evaluation.archive.02_item_metrics to execute script(here module)
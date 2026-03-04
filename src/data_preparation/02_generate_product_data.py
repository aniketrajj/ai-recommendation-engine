#Use the ai-recommendation-engine as project root folder as links are all relative to that
#To generate synthetic product pr_data and converting it into csv file
import random, pandas as pd
products = []

print("Starting product data generation...\n")
#There are only 5 unique product categories: electronics, daily essential, luxury, fashion, groceries
#Knowingly introduced ambiguities to simulate real-world pr_data
product_categories = ["electronics","daily_essential","luxury","groceries","FAshioN", "EleCtroNicS", "Daily Essential","LUXURY", "GROCERY","daily essential","elecTronIcs ","Luxury ","fashion"]

#Created product labels, inside each category exist distinct products along with empty entities(None)
product_label = {
    "electronics": ["headphones", "charger", None, "smartwatch","powerbank"],
    "daily_essential": ["soap", "toothpaste", "detergent", "shampoo"],
    "luxury": ["perfume", "watch", "sunglasses", None],
    "grocery": ["rice", "oil", "sugar", None, "wheat-flour"],
    "fashion": ["tshirt", "jeans", "jacket", "sneakers"]
}

#Created product cost to align cost of each product with it's category
product_cost = {
    "electronics": (400, 8000),
    "daily_essential": (10, 1000),
    "luxury": (1000, 15000),
    "grocery": (50, 1000),
    "fashion": (500, 3000)
}

#Created 600 product pr_data with fields pr_id, pr_category, pr_label, pr_cost, pr_rating
for i in range(600):

    raw_category = random.choice(product_categories)
    #Created formatted_category to remove product_categories inconsistencies and map category to labels and cost
    formatted_category = raw_category.lower().strip().replace("groceries","grocery").replace(" ","_") #It just returns a formatted str
    
    #price_range contains a tuple of min max values of product cost
    price_range = product_cost[formatted_category]

    pr_data = {
        "pr_id" : f"P{random.randint(1,520)}",
        
        "pr_category" : raw_category,
        
        #Mapping category to label and choosing a random label from category
        "pr_label" : random.choice(product_label[formatted_category]),
        
        #Choosing price according to category
        "pr_cost" : random.randint(min(price_range), max(price_range)),
        
        #Using round to round floating point to 1 decimal places
        "pr_rating" : round(random.uniform(3.0,4.9),1)
    
    }
    
    #pr_data acts as the details of a single product entry
    products.append(pr_data)

#Converting the list of dictionaries to rows and columns using DataFrame of pandas
df = pd.DataFrame(products)

print(df.info())

print("\nProduct data generation successful!")
#Convert the dataframe to csv works only if project folder is the root folder
df.to_csv("../ai-recommendation-engine/data/raw/products_raw.csv",index=False)

print("File saved as products_raw.csv under ai-recommendation-engine/data/raw/")
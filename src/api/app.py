

import pandas as pd
from flask import Flask, jsonify, request, render_template
from src.models.recommend import recommendation

app = Flask(__name__)

# Load the products dataset from the correct processed folder
file_path = "data/processed/products_clean.csv"

try:
    products_df = pd.read_csv(file_path)
    # Convert the pandas dataframe to a list of dictionaries for the frontend
    products_list = products_df.to_dict('records')
    print(f"✅ Successfully loaded products from: {file_path}")
except FileNotFoundError:
    print(f"❌ CRITICAL ERROR: Could not find the file at {file_path}")
    products_list = []

@app.route("/")
def home():
    return render_template("index.html")

# New route: Get default catalog (first 20 products for display)
@app.route("/api/products")
def get_products():
    return jsonify({"status": "success", "data": products_list[:20]})

@app.route("/recommend")
def recommend_api():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"status": "error", "message": "User ID is required"})

    try:
        # Get recommended IDs from your model
        rec_ids = recommendation(user_id, n=10)
        
        # Map IDs to full product details from the CSV
        recommended_products = [p for p in products_list if p['pr_id'] in rec_ids]
        
        # Sort them to maintain the exact order returned by your recommendation engine
        if recommended_products and rec_ids:
            order_map = {id: index for index, id in enumerate(rec_ids)}
            recommended_products.sort(key=lambda x: order_map.get(x['pr_id'], 999))

        return jsonify({"status": "success", "data": recommended_products})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
@app.route("/user_recommendations")
def user_recommendations_page():
    # Grab the user_id from the URL (e.g., /user_recommendations?user_id=U102)
    user_id = request.args.get("user_id")
    # Pass it to the new HTML template
    return render_template("recommendations.html", user_id=user_id)

if __name__ == "__main__":
    app.run(debug=True)
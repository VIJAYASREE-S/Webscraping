import requests
import pandas as pd
from datetime import datetime
import json

# API URL and headers
url = 'https://www.swiggy.com/api/instamart/item/P7M9WFVLNR/widgets?storeId=1386719&primaryStoreId=1386719&secondaryStoreId='
headers = {
    'accept': '',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36',
}

# Send the request
response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)
print(response)

# Proceed if status code is 200 (successful)
if response.status_code == 200:
    try:
        data = response.json()

        # Get the product info from the response
        item_data = None
        for widget in data.get("data", {}).get("widgets", []):
            if widget.get("id") == "ITEM_DETAILS":
                item_data = widget.get("data", {})
                break

        if not item_data:
            raise ValueError("ITEM_DETAILS widget not found in response.")

        item = item_data.get("item", {})
        variations = item.get("variations", [])

        if not variations:
            raise ValueError("No variations found for the product.")

        v = variations[0]
        scrape_date = datetime.today().strftime('%Y-%m-%d')
        insert_time = datetime.now().timestamp()

        # Extract required fields
        row = {
            'scrape_date': scrape_date,
            'insert_time': insert_time,
            'product_id': item.get('product_id'),
            'variation_id': v.get('id'),
            'spin_id': v.get('spin'),
            'brand_name': item.get('brand'),
            'brand_id': v.get('brand_id'),
            'product_name': v.get('display_name'),
            'pack_of': v.get('quantity'),
            'formatted_packsize': v.get('sku_quantity_with_combo'),
            'weight': v.get('weight_in_grams'),
            'mrp': v.get('price', {}).get('mrp'),
            'discounted_selling_price': v.get('price', {}).get('offer_price'),
            'discount_percent': v.get('price', {}).get('offer_applied', {}).get('product_description'),
            'in_stock': v.get('inventory', {}).get('in_stock'),
            'available_quantity': v.get('inventory', {}).get('total'),
            'max_allowed_quantity': v.get('max_allowed_quantity'),
            'category_id': v.get('category_id'),
            'category_name': v.get('category'),
            'subcategory_name': v.get('sub_category'),
            'supercategory_name': v.get('super_category'),
            'group_id': v.get('meta', {}).get('group'),
            'Variant_Flag': v.get('displayVariant'),
            'scraped_store_id': v.get('store_id'),
        }
        print("Response Length:", len(response.text))
        print("Raw Response Content (first 500 chars):", response.text[:500])

        # Save to Excel
        df = pd.DataFrame([row])
        df.to_excel('instamart_product_data.xlsx', index=False)

        print("Data saved to instamart_product_data.xlsx")

    except Exception as e:
        print(f"Error parsing JSON: {e}")
else:
    print(f"Failed to fetch data, status code: {response.status_code}")

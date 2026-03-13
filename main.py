from fastapi import FastAPI, Response, status, Query
from pydantic import BaseModel, Field
from typing import Optional, List
app=FastAPI()
products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook',       'price':  99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub',         'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set',          'price':  49, 'category': 'Stationery',  'in_stock': True },
]
# Pydantic Model
class NewProduct(BaseModel):
    name: str
    price: int
    category: str
    in_stock: bool = True
# Helper Function
def find_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p
    return None
# Home endpoint
@app.get("/")
def home():
    return {"message": "Welcome to Product API"}
# Get all products
@app.get("/products")
def get_products():
    return {
        "products": products,
        "total_products": len(products)
    }
# Add product
@app.post("/products")
def add_product(product: dict):
    products.append(product)
    return {
        "message": "Product added successfully",
        "product": product
    }
@app.get("/category/{category_name}")
def get_products_by_category(category_name: str):
    result = []
    for product in products:
        if product["category"].lower() == category_name.lower():
            result.append(product)
    if result:
        return result
    else:
        return {"message": "No products found in this category"}
@app.get("/products/instock") 
def get_instock(): 
    available = [p for p in products if p["in_stock"] == True] 
    return {"in_stock_products": available, "count": len(available)}
@app.get("/store/summary") 
def store_summary(): 
    in_stock_count = len([p for p in products if p["in_stock"]]) 
    out_stock_count = len(products) - in_stock_count 
    categories = list(set([p["category"] for p in products])) 
    return { "store_name": "My E-commerce Store", "total_products": len(products), "in_stock": in_stock_count, "out_of_stock": out_stock_count, "categories": categories, }
@app.get("/products/search/{keyword}") 
def search_products(keyword: str): 
    results = [ p for p in products if keyword.lower() in p["name"].lower() ] 
    if not results: 
       return {"message": "No products matched your search"} 
    return {"keyword": keyword, "results": results, "total_matches": len(results)}
@app.get("/products/deals") 
def get_deals(): 
    cheapest = min(products, key=lambda p: p["price"]) 
    expensive = max(products, key=lambda p: p["price"]) 
    return { "best_deal": cheapest, "premium_pick": expensive, }
# ---- ASSIGNMENT 2 ----
# ---- Filter Products ----
@app.get("/products/filter")
def filter_products(min_price: int = Query(None, description='Minimum price'),
max_price: int= Query(None, description='Minimum price')):
    result = products
    if min_price:
        result = [p for p in result if p['price'] >= min_price]
    if max_price:
        result = [p for p in result if p["price"] <= max_price]
    return result
# ---- Get only product price ----
@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {
                "name": product["name"],
                "price": product["price"]
            }
    return {"error": "Product not found"}
# ---- Customer Feedback ----
feedback = []
class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)
@app.post("/feedback")
def add_feedback(data: CustomerFeedback):
    feedback.append(data)
    return {
        "message": "Feedback submitted successfully",
        "feedback": data,
        "total_feedback": len(feedback)
    }
# ---- Product Summary Dashboard ----
@app.get("/products/summary")
def product_summary():
    total_products = len(products)
    in_stock = [p for p in products if p["in_stock"]]
    out_of_stock = [p for p in products if not p["in_stock"]]
    most_expensive = max(products, key=lambda x: x["price"])
    cheapest = min(products, key=lambda x: x["price"])
    categories = list(set(p["category"] for p in products))
    return {
        "total_products": total_products,
        "in_stock_count": len(in_stock),
        "out_of_stock_count": len(out_of_stock),
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        },
        "cheapest": {
            "name": cheapest["name"],
            "price": cheapest["price"]
        },
        "categories": categories
    }
# ---- Bulk Order System ----
class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=50)
class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem]
@app.post("/orders/bulk")
def bulk_order(order: BulkOrder):
    confirmed = []
    failed = []
    grand_total = 0
    for item in order.items:
        product = next((p for p in products if p["id"] == item.product_id), None)
        if not product:
            failed.append({
                "product_id": item.product_id,
                "reason": "Product not found"
            })
            continue
        if not product["in_stock"]:
            failed.append({
                "product_id": item.product_id,
                "reason": f"{product['name']} is out of stock"
            })
            continue
        subtotal = product["price"] * item.quantity
        grand_total += subtotal
        confirmed.append({
            "product": product["name"],
            "qty": item.quantity,
            "subtotal": subtotal
        })
    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }
# ---- BONUS — Order Tracking ----
orders = []
@app.post("/orders")
def create_order(order: dict):
    order_id = len(orders) + 1
    order["id"] = order_id
    order["status"] = "pending"
    orders.append(order)
    return order
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["id"] == order_id:
            return order
    return {"error": "Order not found"}
@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):
    for order in orders:
        if order["id"] == order_id:
            order["status"] = "confirmed"
            return order
    return {"error": "Order not found"}
# ---- Assignment 3 ----
# ---- Add 2 New Products Using POST----
# ADD PRODUCT
# -------------------------
@app.post("/products", status_code=status.HTTP_201_CREATED)
def add_product(product: NewProduct, response: Response):
    # Check duplicate name
    for p in products:
        if p["name"].lower() == product.name.lower():
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"error": "Product with this name already exists"}

    next_id = max(p["id"] for p in products) + 1
    new_product = {
        "id": next_id,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "in_stock": product.in_stock,
    }
    products.append(new_product)
    return {
        "message": "Product added",
        "product": new_product
    }
# UPDATE PRODUCT
@app.put("/products/{product_id}")
def update_product(
        product_id: int,
        response: Response,
        price: Optional[int] = None,
        in_stock: Optional[bool] = None
):
    product = find_product(product_id)
    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    if price is not None:
        product["price"] = price

    if in_stock is not None:
        product["in_stock"] = in_stock

    return {
        "message": "Product updated",
        "product": product
    }

# DELETE PRODUCT
@app.delete("/products/{product_id}")
def delete_product(product_id: int, response: Response):

    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    products.remove(product)

    return {"message": f"Product '{product['name']}' deleted"}


# =========================================================
# NEW ENDPOINTS (ASSIGNMENT PART)
# =========================================================

# -------------------------
# PRODUCT AUDIT SUMMARY
# (Must be ABOVE /products/{product_id})
# -------------------------
@app.get("/products/audit")
def product_audit():
    in_stock_list = [p for p in products if p["in_stock"]]
    out_stock_list = [p for p in products if not p["in_stock"]]

    stock_value = sum(p["price"] * 10 for p in in_stock_list)

    priciest = max(products, key=lambda p: p["price"])

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock_list),
        "out_of_stock_names": [p["name"] for p in out_stock_list],
        "total_stock_value": stock_value,
        "most_expensive": {
            "name": priciest["name"],
            "price": priciest["price"]
        }
    }
# BULK CATEGORY DISCOUNT
# (Must be ABOVE /products/{product_id})
@app.put("/products/discount")
def bulk_discount(
        category: str = Query(..., description="Category to discount"),
        discount_percent: int = Query(..., ge=1, le=99, description="Discount percentage")
):
    updated = []

    for p in products:
        if p["category"] == category:
            p["price"] = int(p["price"] * (1 - discount_percent / 100))
            updated.append(p)

    if not updated:
        return {"message": f"No products found in category: {category}"}

    return {
        "message": f"{discount_percent}% discount applied to {category}",
        "updated_count": len(updated),
        "updated_products": updated
    }
# GET SINGLE PRODUCT
# (Placed LAST so /audit works correctly)
@app.get("/products/{product_id}")
def get_product(product_id: int, response: Response):

    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}
    return product

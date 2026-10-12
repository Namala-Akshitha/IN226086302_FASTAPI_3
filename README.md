# FastAPI Internship – Day 4
## E-Commerce Product CRUD API

### Overview
This project extends an e-commerce API with product creation, updating, deletion, inventory auditing, and category-wide discounts.

### Features
- Add products using POST.
- Update product prices and stock status using PUT.
- Delete products and handle missing product IDs.
- Complete a product CRUD lifecycle.
- Generate an inventory audit report.
- Apply percentage discounts to products by category.

### Technologies
- Python
- FastAPI
- Uvicorn
- Swagger UI

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/products` | Add a product |
| GET | `/products` | List all products |
| GET | `/products/{product_id}` | Retrieve one product |
| PUT | `/products/{product_id}` | Update product details |
| DELETE | `/products/{product_id}` | Delete a product |
| GET | `/products/audit` | Generate inventory summary |
| PUT | `/products/discount` | Apply a category-wide discount |

### How to Run
1. Install dependencies: `pip install fastapi uvicorn`
2. Run: `uvicorn main:app --reload`
3. Open: `http://127.0.0.1:8000/docs`
4. Test all endpoints and verify changes using GET requests.

### Learning Outcomes
- Implementing CRUD operations.
- Using path and query parameters.
- Handling missing resources.
- Calculating inventory values.
- Updating product collections with business rules.

### Internship
FastAPI Internship Training – Day 4 Assignment.

# E-commerce Backend API

A Python FastAPI application that serves static data for an e-commerce platform with shops, categories, attributes, and products.

## Backend API Features

The API provides exactly 4 endpoints as requested:

1. **List Shops API** - Returns shop details with categories and metadata including shop image URLs
2. **List Categories API** - Returns categories with their attributes and all possible values for each attribute
3. **Get Products API** - Returns filtered products by category with attribute filters, including product images, prices, reviews, and metadata
4. **Get Product by ID API** - Returns complete product information by product ID

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd hackathon3
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the FastAPI server:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Interactive API Documentation (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API Documentation (ReDoc)**: `http://localhost:8000/redoc`
- **OpenAPI JSON Schema**: `http://localhost:8000/openapi.json`

## Backend API Endpoints

### 1. List Shops API
- **GET** `/shops`
- Returns all shops with:
  - Shop details (name, description, image_url)
  - List of categories with metadata for each shop

### 2. List Categories API  
- **GET** `/categories`
- Returns all categories with:
  - Category metadata (name, description, image_url)
  - List of attributes for each category
  - List of possible values for each attribute

### 2b. Get Category by ID API
- **GET** `/categories/{category_id}`
- Returns a specific category by ID with:
  - Category metadata (name, description, image_url)
  - List of attributes for the category
  - List of possible values for each attribute

### 3. Get Products API
- **POST** `/products`
- Request body:
  ```json
  {
    "category": "category_id",
    "filters": [
      {"attribute": "color", "value": "Blue"},
      {"attribute": "size", "value": "M"}
    ]
  }
  ```
- Returns filtered products with:
  - Product IDs with complete data
  - Product image, name, price, reviews
  - All product metadata and attributes

### 4. Get Product by ID API
- **GET** `/products/{product_id}`
- Returns complete product information including:
  - Product details (name, description, price, image)
  - Reviews and ratings
  - All attributes and metadata

## Sample Data Structure

### Shops with Enhanced Metadata
- **Fashion Store**: Trendy fashion with clothing, accessories, footwear categories
- **Electronics Hub**: Latest electronics with smartphones, laptops categories  
- **Home & Garden**: Home essentials with furniture, decor, appliances categories

Each shop includes:
- `id`, `name`, `description`, `image_url`
- List of associated categories with full metadata

### Categories with Complete Attribute Information
- **clothing**: size, color, material, brand (with all possible values)
- **smartphones**: brand, storage, ram, color (with all possible values)
- **furniture**: material, color, style (with all possible values)
- And 6 more categories...

Each category includes:
- `id`, `name`, `description`, `image_url`
- Complete list of attributes with their allowed values

### Enhanced Product Data
Products include comprehensive information:
- Basic details: `id`, `name`, `description`, `price`, `image_url`
- Reviews: `rating`, `count`, `average`
- Product attributes with values
- Additional metadata: `sku`, specifications, care instructions, etc.

Sample products:
- Cotton T-Shirt (4.5★, 128 reviews, H&M brand)
- iPhone 15 (4.8★, 512 reviews, Apple, 256GB)
- Modern Coffee Table (4.4★, 156 reviews, Wood, Modern style)
- And 6 more products across different categories...

## Usage Examples

### 1. List all shops with categories and metadata
```bash
curl http://localhost:8000/shops
```

### 2. List all categories with attributes and their values
```bash
curl http://localhost:8000/categories
```

### 2b. Get specific category by ID
```bash
curl http://localhost:8000/categories/clothing
```

### 3. Get products by category with filters
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "category": "clothing",
    "filters": [
      {"attribute": "color", "value": "Blue"},
      {"attribute": "size", "value": "M"}
    ]
  }'
```

### 4. Get specific product by ID
```bash
curl http://localhost:8000/products/prod_1
```

### Example: Get all smartphones from Samsung
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "category": "smartphones",
    "filters": [
      {"attribute": "brand", "value": "Samsung"}
    ]
  }'
```

### Example: Get all products in clothing category (no filters)
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "category": "clothing",
    "filters": []
  }'
```

## Response Format

All endpoints return responses in this format:

```json
{
  "success": true,
  "data": [...],
  "message": "Optional message"
}
```

## Project Structure

```
hackathon3/
├── main.py              # FastAPI application and routes
├── models.py            # Pydantic data models  
├── data_loader.py       # JSON data loader utilities
├── requirements.txt     # Python dependencies
├── static/             # Static JSON data files
│   ├── shops.json      # Shop data with categories
│   ├── categories.json # Category data with attributes  
│   └── products.json   # Product data with reviews and metadata
└── README.md           # This file
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running the application
- **Pydantic**: Data validation using Python type annotations
- **python-multipart**: For handling form data

## Data Management

The application uses **JSON files** for data storage in the `static/` directory:

### Adding New Data

1. **Add Shops**: Edit `static/shops.json` to add new shops with their categories
2. **Add Categories**: Edit `static/categories.json` to add new categories with attributes
3. **Add Products**: Edit `static/products.json` to add new products with complete metadata

### Data Structure

- **shops.json**: Object with shop IDs as keys, containing shop details and category arrays
- **categories.json**: Object with category IDs as keys, containing category details and attribute arrays  
- **products.json**: Array of product objects with reviews, attributes, and metadata

#### Example JSON Structures

**shops.json structure:**
```json
{
  "shop_1": {
    "id": "shop_1",
    "name": "Fashion Store",
    "description": "Your one-stop destination for trendy fashion",
    "image_url": "https://example.com/images/fashion-store.jpg",
    "categories": [
      {
        "id": "clothing",
        "name": "Clothing",
        "description": "Fashion clothing for all occasions",
        "image_url": "https://example.com/images/clothing.jpg"
      }
    ]
  }
}
```

**categories.json structure:**
```json
{
  "clothing": {
    "id": "clothing",
    "name": "Clothing",
    "description": "Fashion clothing for all occasions",
    "image_url": "https://example.com/images/clothing.jpg",
    "attributes": [
      {
        "id": "size",
        "name": "Size",
        "type": "select",
        "allowed_values": ["XS", "S", "M", "L", "XL"]
      }
    ]
  }
}
```

**products.json structure:**
```json
[
  {
    "id": "prod_1",
    "name": "Cotton T-Shirt",
    "description": "Comfortable cotton t-shirt for everyday wear",
    "price": 29.99,
    "image_url": "https://example.com/images/products/cotton-tshirt.jpg",
    "category_id": "clothing",
    "shop_id": "shop_1",
    "reviews": {
      "rating": 4.5,
      "count": 128,
      "average": 4.5
    },
    "attributes": {
      "size": "M",
      "color": "Blue",
      "material": "Cotton",
      "brand": "H&M"
    },
    "metadata": {
      "sku": "TSH001",
      "weight": "200g",
      "care_instructions": "Machine wash cold"
    }
  }
]
```

### Development

The application is designed to be easily extendable:

1. **Data**: Modify JSON files in `static/` directory (no code changes needed)
2. **Endpoints**: Add new API endpoints in `main.py`
3. **Models**: Extend data models in `models.py`
4. **Data Loading**: Enhance data processing in `data_loader.py`

## License

This project is created for demonstration purposes. 
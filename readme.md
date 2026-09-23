# Product Marketing E-Commerce Application

A complete e-commerce web application built with Flask, MySQL, Bootstrap, and Jinja2.

## Features

- **User Authentication**: Registration, login, logout with password hashing
- **Product Catalog**: Browse products by category, search functionality
- **Shopping Cart**: Add/remove items, update quantities
- **Checkout**: Order placement with address validation
- **Order History**: View past orders with detailed tracking

## Tech Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Template Engine**: Jinja2
- **Security**: Werkzeug password hashing

## Installation Steps

### 1. Prerequisites
- Python 3.8 or higher
- MySQL Server 8.0 or higher
- pip (Python package manager)

### 2. Database Setup

```bash
# Login to MySQL
mysql -u root -p

# Run the database.sql file
source /path/to/database.sql
```

Or import via MySQL Workbench or phpMyAdmin.

### 3. Project Setup

```bash
# Clone or download the project
cd product-marketing

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configuration

Edit `config.py` and update MySQL credentials:

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'  # Set your MySQL password
MYSQL_DB = 'product_marketing'
```

### 5. Run the Application

```bash
python app.py
```

The application will be available at: `http://127.0.0.1:5000`

## Project Structure

```
product-marketing/
├── app.py                      # Main application file
├── config.py                   # Configuration settings
├── database.py                 # Database connection
├── requirements.txt            # Python dependencies
├── database.sql                # Database schema and sample data
├── controllers/
│   ├── auth_controller.py      # Authentication logic
│   ├── product_controller.py   # Product management
│   ├── cart_controller.py      # Shopping cart operations
│   └── order_controller.py     # Order processing
├── utils/
│   └── validators.py           # Input validation utilities
└── templates/
    ├── base.html               # Base template
    ├── register.html           # Registration page
    ├── login.html              # Login page
    ├── index.html              # Home/Products page
    ├── product_detail.html     # Product details
    ├── cart.html               # Shopping cart
    ├── checkout.html           # Checkout page
    └── orders.html             # Order history
```

## API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /logout` - User logout

### Products
- `GET /api/products` - Get all products (with optional filters)
- `GET /api/categories` - Get all categories

### Cart
- `GET /api/cart` - Get cart items
- `POST /api/cart/add` - Add item to cart
- `POST /api/cart/update` - Update cart item quantity
- `POST /api/cart/remove` - Remove item from cart

### Orders
- `POST /api/orders/checkout` - Place order
- `GET /api/orders` - Get order history
- `GET /api/orders/<order_id>` - Get order details

## Default Sample Data

The database includes:
- 5 product categories
- 12 sample products with images
- All products have stock available

## Testing the Application

To test the application with a sample user, execute the following SQL after setting up the database:

```sql
USE product_marketing;

INSERT INTO users (name, email, password, phone, address)
VALUES (
    'Test User',
    'test@example.com',
    'scrypt:32768:8:1$zxOv8P7LKqF3gQHi$c8a2e2d3f4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1',
    '03001234567',
    'Test Address'
);
```

**Then login with:**
- Email: `test@example.com`
- Password: `password123`

---

## **After Login - What You'll See:**

Once logged in, you'll be redirected to the **Product Dashboard** where you can:

✅ **View all products** with images and prices
✅ **Search products** by name
✅ **Filter by category** (Electronics, Clothing, Books, etc.)
✅ **Add products to cart**
✅ **View product details**
✅ **Manage your shopping cart**
✅ **Place orders**
✅ **View order history**

---

## **Quick Navigation Guide:**
```
After Login, you'll see these menu items:

🏠 Home          → Product listing page
🛒 Cart          → Your shopping cart
📦 Orders        → Your order history
👤 [Your Name]   → Dropdown with Logout option

- Password hashing using Werkzeug
- Email format validation
- Password strength validation (8+ characters, must include numbers)
- Phone number validation (11 digits)
- Input sanitization
- SQL injection protection via parameterized queries
- Session management

## Color Scheme

- Primary Blue: `#4A90E2`
- Light Gray: `#F5F5F5`
- White backgrounds
- Black text

## Browser Compatibility

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

### MySQL Connection Error
- Verify MySQL is running
- Check credentials in `config.py`
- Ensure database exists

### Module Import Errors
```bash
pip install -r requirements.txt
```

### Port Already in Use
Edit `app.py`:
```python
app.run(debug=True, port=5001)
```

## Development Notes

- Debug mode is enabled by default
- Change `SECRET_KEY` in production
- Update MySQL password in `config.py`
- Sample product images use Unsplash API

## Future Enhancements

- Payment gateway integration
- Admin panel
- Product reviews and ratings
- Wishlist functionality
- Email notifications
- Advanced search filters

## License

This project is for educational purposes.

## Support

For issues or questions, please check the documentation or create an issue in the project repository.
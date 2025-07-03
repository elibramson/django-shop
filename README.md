# Django Shop - E-commerce Platform

A Django-based e-commerce application built for learning purposes. This project demonstrates basic e-commerce functionality including product management, shopping cart operations, and a responsive user interface.

## Features

### Product Management
- Product catalog with category organization
- Product detail pages with images and descriptions
- Category-based product filtering
- Product availability status tracking
- Basic product recommendations
- Product sorting by name and price
- Pagination for product listings

### Shopping Cart System
- Session-based shopping cart functionality
- Add products to cart with quantity selection
- Update cart quantities and remove items
- Cart validation with quantity limits
- Cart summary with total calculations
- Global cart access across all pages

### User Interface
- Responsive design using Bootstrap 5
- Basic product grid layout
- Product detail pages with image display
- Shopping cart interface
- Navigation with breadcrumbs
- Empty state handling for cart and products

### Technical Implementation
- Class-based views for product display
- Database queries with basic optimization
- Form handling with validation
- Error handling and user feedback
- CSRF protection and input validation
- Session management for cart persistence

## Technology Stack

- **Backend**: Django 5.2.3
- **Database**: SQLite (development)
- **Frontend**: Bootstrap 5.3.0, Bootstrap Icons
- **Image Processing**: Pillow 11.2.1
- **Configuration**: python-decouple 3.8
- **Styling**: Custom CSS with basic responsive design

## Project Structure

```
django-shop/
├── cart/                          # Shopping cart application
│   ├── cart.py                   # Cart session management
│   ├── forms.py                  # Cart form validation
│   ├── views.py                  # Cart operations (add, remove, update)
│   ├── context_processors.py     # Global cart context
│   └── templates/cart/           # Cart templates
├── main/                         # Main product application
│   ├── models.py                 # Product and Category models
│   ├── views.py                  # Product listing and detail views
│   └── templates/main/           # Product templates
├── shop/                         # Project settings
│   ├── settings.py               # Django configuration
│   └── urls.py                   # URL routing
└── requirements.txt              # Python dependencies
```

## Database Models

### Product Model
- Basic fields: name, slug, description, price, image, available status
- Foreign key relationship to Category
- Auto-generated slugs and basic price formatting
- Simple related products functionality

### Category Model
- Basic fields: name, slug
- Product count property for basic statistics
- SEO-friendly URL generation

### Cart System
- Session-based cart storage
- Basic quantity management and price calculations
- Simple validation for quantity limits

## User Interface Features

### Product Listing Page
- Grid layout with product cards
- Sorting options for name and price
- Category filtering functionality
- Basic pagination
- Product cards with image, title, price, and availability

### Product Detail Page
- Product information display
- Image viewing with basic zoom functionality
- Add to cart form with quantity selection
- Related products section
- Breadcrumb navigation

### Shopping Cart
- Cart item listing with product details
- Quantity adjustment controls
- Price calculations and totals
- Basic order summary
- Cart management actions

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd django-shop
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   Create a `.env` file in the project root:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Usage

### Admin Interface
- Access Django admin at `/admin/`
- Manage products, categories, and basic user data
- Upload product images and set availability status

### Shopping Experience
1. Browse products on the homepage
2. Filter products by category using navigation
3. View detailed product information
4. Add products to cart with quantity selection
5. Manage cart contents (update quantities, remove items)
6. Review cart summary (checkout not implemented)

## Implementation Notes

### Django Concepts Used
- Class-based views for product display
- Context processors for global cart data
- Form handling with basic validation
- URL patterns with namespacing
- Template inheritance for consistent layout

### Basic Optimizations
- Database indexes on frequently queried fields
- Select related queries to reduce database calls
- Session-based cart for persistence
- Static file configuration for media handling

### Security Considerations
- CSRF protection on forms
- Basic input validation
- Django ORM for SQL injection prevention
- Template auto-escaping for XSS prevention

## Limitations

This is a learning project with several limitations:
- No user authentication system
- No payment processing
- No order management
- No advanced search functionality
- No inventory tracking
- No email notifications
- No user reviews or ratings
- No discount or coupon system

## Future Improvements

Potential areas for enhancement:
- User registration and authentication
- Complete checkout and order processing
- Payment gateway integration
- Product review system
- Advanced search and filtering
- Email notification system
- Inventory management
- Discount and promotion system
- Multi-language support

## Contributing

This is an educational project for learning Django concepts. Feel free to fork and extend the functionality for your own learning purposes.

## License

This project is for educational purposes. Use responsibly and respect the learning objectives.

---

Built with Django and Bootstrap for educational purposes.
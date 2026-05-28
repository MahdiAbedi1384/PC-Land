# PC-Land - E-Commerce Platform for Computer Components

A comprehensive Django-based e-commerce platform specializing in computer hardware and components. PC-Land provides a full-featured shopping experience with product management, cart management, order processing, payment integration, and customer support.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Database](#database)
- [Apps Overview](#apps-overview)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

PC-Land is a modern e-commerce platform designed for buying and selling computer hardware components. It features a user-friendly interface, robust product catalog with advanced search capabilities powered by Elasticsearch, multiple payment gateway integrations, and comprehensive customer support through a ticketing system.

The platform supports Persian (Farsi) language and Iranian localization, including Iranian cities, local payment methods, and national identification support.

## ✨ Features

### User Management
- **Custom User Model** with support for:
  - National identification code validation
  - Phone number verification
  - Gender selection
  - Email verification
  - Persian language support
- **Social Authentication** via Google OAuth
- **User Addresses** management with Iranian city/province support
- **Account Security** with django-axes for login attempt tracking

### Product Management
- **Extensive Product Catalog** including:
  - Computer monitors
  - Graphics cards (GPUs)
  - Motherboards
  - Processors (CPUs)
  - RAM (Memory)
  - Power supplies
  - Computer cases
  - Cooling systems
  - Storage devices
- **Product Details** with:
  - Images gallery
  - Specifications (brand, model, weight, SKU)
  - Price tracking
  - Stock management
  - Detailed descriptions
- **Search & Filtering** powered by Elasticsearch
- **Product Categories** with hierarchical structure

### Shopping Cart
- **Session-based or Database-backed Cart** management
- **Add/Remove Items** functionality
- **Quantity Management**
- **Price Calculations** with taxes and shipping
- **Context Processor Integration** for site-wide cart access

### Order Management
- **Order Creation & Tracking**
- **Discount System** with:
  - Percentage-based discounts
  - Fixed amount discounts
  - Usage limits and expiration dates
  - Discount code generation
- **Order Status Tracking** (pending, processing, shipped, delivered, cancelled)
- **Tracking Code Generation** for shipment tracking
- **Order Items** with pricing history

### Payment Processing
- **Multiple Payment Gateways**:
  - ZarinPal (Iranian payment gateway)
  - Integration with Kavenegar SMS service for notifications
- **Payment Status Management**
- **Order-Payment Linking**

### Customer Support
- **Ticketing System** for customer inquiries:
  - Create new support tickets
  - Ticket status management (open, in progress, closed)
  - Two-way messaging between users and support staff
  - Staff/Admin dashboard for managing all tickets
- **Message Threading** within tickets
- **User-specific Ticket Views** with admin override capability

### Internationalization
- **Multi-language Support** via django-rosetta
- **Persian (Farsi) Language** translations
- **Jalali Calendar** support for Persian dates
- **Iranian City/Province** localization
- **Phone Number** field with Iranian region support

### Admin Interface
- **Django Admin Customization**
- **Rich Admin Actions**
- **Inline Editing** for related models
- **Autocomplete Fields** via django-autocomplete-light
- **Search Capabilities** across models

## 🛠 Tech Stack

### Backend
- **Framework**: Django 6.0.3
- **Python**: 3.8+
- **Database**: PostgreSQL (via Django ORM)
- **Cache**: Redis
- **Search Engine**: Elasticsearch 8.19.3

### Frontend
- **Bootstrap 5** via django-bootstrap5
- **Crispy Forms** for form rendering
- **Django Widget Tweaks** for template customization
- **JavaScript/jQuery** for interactivity

### Authentication & Authorization
- **django-allauth** - Social authentication
- **django-axes** - Brute force protection

### Additional Libraries
- **django-jalali** - Persian calendar support
- **django-iranian-cities** - Iranian localization
- **phonenumber-field** - Phone number handling
- **Pillow** - Image processing
- **redis** - Caching and sessions
- **elasticsearch-dsl** - Search functionality
- **kavenegar** - SMS notifications
- **zarinpal-py-sdk** - Payment gateway integration
- **pytest** - Testing framework
- **mypy** - Type checking

## 📁 Project Structure

```
PC-Land/
├── config/                 # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL routing configuration
│   ├── wsgi.py            # WSGI application
│   └── asgi.py            # ASGI application
│
├── accounts/              # User authentication & profiles
│   ├── models.py          # CustomUser, Addresses
│   ├── views.py           # User profile views
│   ├── forms.py           # User forms
│   ├── validators.py      # Custom validators
│   └── urls.py            # Account URLs
│
├── shop/                  # Product catalog
│   ├── models.py          # Product models (GPU, CPU, Monitor, etc.)
│   ├── views.py           # Product listing, detail views
│   ├── documents.py       # Elasticsearch documents
│   ├── filters/           # Search filters
│   ├── services/          # Business logic
│   ├── admin.py           # Admin customization
│   └── urls.py            # Shop URLs
│
├── cart/                  # Shopping cart
│   ├── models.py          # Cart model
│   ├── views.py           # Cart management views
│   ├── cart.py            # Cart logic
│   ├── functions.py       # Cart utilities
│   ├── context_processors.py  # Make cart available in templates
│   └── urls.py            # Cart URLs
│
├── orders/                # Order management
│   ├── models.py          # Order, OrderItem, Discount models
│   ├── views.py           # Order views
│   ├── forms.py           # Order forms
│   ├── admin.py           # Admin customization
│   └── urls.py            # Order URLs
│
├── payment/               # Payment processing
│   ├── models.py          # Payment model
│   ├── views.py           # Payment gateway integration
│   ├── forms.py           # Payment forms
│   └── urls.py            # Payment URLs
│
├── support/               # Customer support
│   ├── models.py          # Ticket, Message models
│   ├── views.py           # Ticket management views
│   ├── forms.py           # Ticket forms
│   └── urls.py            # Support URLs
│
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   └── [app-specific]/    # App templates
│
├── static/                # CSS, JavaScript, images
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                 # User-uploaded files (product images)
│
├── manage.py              # Django management script
└── requirement.txt        # Python dependencies
```

## 💻 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- PostgreSQL database
- Redis server
- Elasticsearch 8.x (optional, for search features)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd PC-Land
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirement.txt
```

### Step 4: Configure Environment Variables
Copy `.env.example` to `.env` and fill in the required values:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
# Secret & Debug
SECRET_KEY=your-secret-key-here
DEBUG_MODE=True

# Database
DJANGO_DATABASE_NAME=pcland_db
DJANGO_DATABASE_USERNAME=postgres
DJANGO_DATABASE_PASSWORD=your-password

# Redis
REDIS_LOCATION=redis://localhost:6379/1

# Elasticsearch
ELASTICSEARCH_DSL_HOST=http://localhost:9200

# SMS Gateway (Kavenegar)
KAVENEGAR_API=your-kavenegar-api-key
KAVENEGAR_SENDER=your-sender-id

# Payment Gateway (ZarinPal)
ZARINPAL_MERCHANT_ID=your-merchant-id

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## ⚙️ Configuration

### Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

### Elasticsearch Setup (Optional but Recommended)
```bash
# Index products for search
python manage.py search_index --rebuild
```

### Static Files
```bash
# Collect static files for production
python manage.py collectstatic --noinput
```

### Load Initial Data (Optional)
```bash
# Load fixtures if available
python manage.py loaddata initial_data.json
```

## 🚀 Running the Application

### Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

### With Celery (for async tasks)
```bash
# Terminal 1: Django development server
python manage.py runserver

# Terminal 2: Celery worker (if configured)
celery -A config worker -l info

# Terminal 3: Celery beat (if configured)
celery -A config beat -l info
```

### Production Deployment
For production, use a production-grade WSGI server:

```bash
# Using Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4

# Using uWSGI
uwsgi --http :8000 --wsgi-file config/wsgi.py --master --processes 4
```

## 🗄️ Database

### Database Models Overview

**accounts app:**
- `CustomUser` - Extended user model with national ID, phone, gender
- `Addresses` - User delivery addresses with Iranian city support

**shop app:**
- `GPU` - Graphics cards
- `CPU` - Processors
- `Monitor` - Computer monitors
- `Motherboard` - Motherboards
- `RAM` - Memory modules
- `PowerSupply` - Power supplies
- `ComputerCase` - PC cases
- `CoolingSystem` - CPU/case cooling
- `StorageDevice` - SSDs and HDDs
- `Images` - Product gallery images (generic foreign key)

**orders app:**
- `Order` - Customer orders
- `OrderItem` - Individual items in orders
- `Discount` - Discount codes with validity rules

**payment app:**
- `Payment` - Payment transaction records

**support app:**
- `Tickets` - Customer support tickets
- `Message` - Messages within tickets

### Migrations
Migrations are automatically generated and tracked. To create new migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📚 Apps Overview

### Accounts App
Handles user authentication, profiles, and address management.
- Custom user model with national ID and phone verification
- Multiple addresses support for users
- Integration with django-allauth for social authentication

### Shop App
Main product catalog and browsing functionality.
- Comprehensive product models for computer components
- Elasticsearch integration for advanced search
- Product filtering and categorization
- Image gallery management

### Cart App
Shopping cart management with session and database support.
- Add/remove items
- Quantity adjustments
- Price calculation with taxes
- Session persistence

### Orders App
Order processing and management.
- Order creation from cart
- Discount code application
- Order tracking
- Discount management with usage limits

### Payment App
Payment gateway integration.
- ZarinPal payment processor integration
- Payment status tracking
- Order-payment linking
- SMS notifications via Kavenegar

### Support App
Customer support ticketing system.
- Create and manage support tickets
- Two-way messaging
- Ticket status tracking
- Admin dashboard for support staff

## 🔍 API Documentation

The application uses Django's default routing. Key endpoints:

**Shop:**
- `GET /` - Home page with featured products
- `GET /products/` - Product listing
- `GET /products/<model>/<pk>/<slug>/` - Product detail

**Cart:**
- `GET /cart/` - View cart
- `POST /cart/add/` - Add to cart
- `POST /cart/remove/` - Remove from cart

**Orders:**
- `GET /orders/` - Order history
- `POST /orders/create/` - Create order from cart
- `GET /orders/<id>/` - Order detail

**Accounts:**
- `GET /accounts/login/` - Login page
- `POST /accounts/login/` - Submit login
- `GET /accounts/profile/` - User profile
- `GET /accounts/addresses/` - Manage addresses

**Support:**
- `GET /support/tickets/` - Ticket list
- `POST /support/tickets/create/` - Create ticket
- `GET /support/tickets/<id>/` - Ticket detail

## 🧪 Testing

Run tests using pytest:
```bash
pytest
pytest --cov=.  # With coverage
pytest -v       # Verbose output
```

## 🌍 Internationalization

The platform supports multiple languages with django-rosetta. To add translations:

```bash
# Extract translatable strings
python manage.py makemessages -l fa

# Update existing translations
python manage.py makemessages -a

# Compile translations
python manage.py compilemessages
```

Access translation UI at `/rosetta/` (admin only)

## 🔒 Security

- **CSRF Protection**: Enabled by default
- **XFrame Options**: Prevents clickjacking
- **SQL Injection**: Protected by Django ORM
- **Brute Force Protection**: django-axes prevents login attacks
- **Secret Key**: Stored in environment variables
- **Debug Mode**: Should be `False` in production

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For support, please:
1. Check the documentation in this README
2. Review existing GitHub issues
3. Create a support ticket in the application
4. Contact the development team

## 🗺️ Roadmap

- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Loyalty points system
- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Advanced inventory management
- [ ] Multi-vendor support
- [ ] Automated email notifications
- [ ] API (REST/GraphQL) for third-party integration

---

**Last Updated**: May 28, 2024

For more information, visit the project repository or documentation.

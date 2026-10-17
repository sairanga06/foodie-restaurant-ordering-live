# 🍔 Foodie — Restaurant Discovery & Food Ordering Platform

<p align="center">
  <strong>Discover food. Explore restaurants. Order your favourites.</strong>
</p>

<p align="center">
  🚀 <a href="https://foodie-restaurant-ordering.onrender.com"><strong>Visit Live Website</strong></a> |
  💻 <a href="https://github.com/sairanga06/foodie-restaurant-ordering-live"><strong>View Source Code</strong></a>
</p>

---

## 📌 About the Project

**Foodie** is a responsive restaurant discovery and food-ordering web application inspired by popular food delivery platforms. It allows users to explore restaurants, search for different cuisines, browse food menus, add dishes to their cart, and complete a simulated checkout process.

The project is built using Python, Django, SQLite/PostgreSQL, HTML, CSS, and JavaScript. It demonstrates full-stack web development concepts, including authentication, database management, server-side validation, and order workflows.

This is an independent educational portfolio project and is not affiliated with Zomato.

## ✨ Key Features

### 🏠 Restaurant Discovery
- Modern homepage with a looping food-video hero section.
- Responsive layout for desktop and mobile screens.
- 65 fictional demo restaurants featuring a variety of cuisines.
- Restaurant information, ratings, estimated delivery times, and menu listings.
- Food categories including Biryani, Shawarma, Noodles, Pizza, Burgers, Momos, Dosa, Rolls, Desserts, and more.

### 🔍 Search & Food Filters
- Search restaurants, cuisines, and menu items.
- Filter restaurants by cuisine.
- Explore vegetarian and non-vegetarian food options.
- Browse restaurant menus with dish descriptions and prices.

### 👤 User Authentication
- User registration and login.
- Logout and profile pages.
- Login-protected ordering and checkout.
- Order history associated with the logged-in user.

### 🛒 Shopping Cart & Checkout
- Add food items to the cart.
- Update cart quantities.
- Enter delivery information and select a demo delivery area.
- Apply coupon codes and view order totals.
- Continue through a simulated payment workflow.

### 💳 Demo Payment System
- Simulate successful or failed payments.
- Validate coupon codes:
  - `FOODIE10` — 10% off, up to ₹100.
  - `WELCOME50` — ₹50 off orders of ₹250 or more.
- Calculate order totals using server-side menu prices.
- No real payments or payment-card details are processed.

### 📦 Order Tracking
- View previous orders and order details.
- Follow status stages such as Confirmed, Preparing, Out for Delivery, and Delivered.
- Update demo order statuses through the manager dashboard or Django admin.

### ❤️ Reviews & Favourites
- Save favourite restaurants.
- Submit restaurant reviews and ratings.
- View existing reviews on restaurant pages.

### 🧑‍🍳 Restaurant Management
- Manage restaurant details and menu items through Django admin.
- Update menu prices and availability using the manager dashboard.
- Update the status of demo orders.
- Access JSON API endpoints for restaurant listings and authenticated order-status queries.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application programming |
| Django | Backend framework, routing, authentication, and database operations |
| SQLite | Local development database |
| PostgreSQL | Persistent database for deployment |
| HTML5 | Page structure |
| CSS3 | Responsive layout, styling, and animations |
| JavaScript | Client-side interactions and shopping cart |
| Git & GitHub | Version control and source code hosting |
| Render | Application hosting and deployment |
| Neon | Managed PostgreSQL database hosting |

## 🏗️ Project Structure

```text
Foodie_Complete_Project/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── restaurants/
│   ├── management/
│   │   └── commands/
│   │       └── seed_demo.py
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── templates/
│   ├── base.html
│   └── restaurants/
├── build.sh
├── manage.py
├── render.yaml
├── requirements.txt
├── RUN_FOODIE.bat
└── README.md
```

## ⚙️ Run the Project Locally

### Prerequisites

- Python 3.10 or newer
- Git
- Visual Studio Code (recommended)
- An internet connection for installing dependencies and loading remote images/video

### 1. Clone the repository

Open a terminal and run:

```bash
git clone https://github.com/sairanga06/foodie-restaurant-ordering-live.git
cd foodie-restaurant-ordering-live
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Create database tables

```powershell
python manage.py migrate
```

### 5. Add demo restaurants and menus

```powershell
python manage.py seed_demo
```

### 6. Start the development server

```powershell
python manage.py runserver
```

Open the website:

**http://127.0.0.1:8000/**

Alternatively, on Windows, run `RUN_FOODIE.bat` from the project folder to automate local setup and startup.

## 🔐 Django Admin

Create an administrator account:

```powershell
python manage.py createsuperuser
```

Start the server and visit:

**http://127.0.0.1:8000/admin/**

Use the administrator account to manage restaurants, menu items, orders, coupons, reviews, favourites, and restaurant-manager profiles.

## 🌐 Live Deployment

The project is deployed using Render, with PostgreSQL configured through Neon.

- **Live Website:** https://foodie-restaurant-ordering.onrender.com
- **GitHub Repository:** https://github.com/sairanga06/foodie-restaurant-ordering-live

The repository contains the Render Blueprint configuration (`render.yaml`) and build script (`build.sh`). These automate dependency installation, database migrations, demo-data setup, and static-file collection during deployment.

### Deployment Workflow

1. Push project changes to GitHub.
2. Connect the GitHub repository to Render.
3. Configure `DATABASE_URL` using the Neon PostgreSQL connection string.
4. Allow Render to build and deploy the application.
5. Open the generated public website URL.

Never commit database credentials, secret keys, passwords, or `.env` files to a public repository.

## 🧪 Important Demo Limitations

This application is intended for learning and portfolio demonstration.

- Payments are simulated and do not charge real money.
- Order tracking uses database statuses and does not include live delivery-partner GPS.
- Delivery locations are selected manually; live maps and GPS routing are not implemented.
- Restaurant listings and menus are fictional sample data.
- Restaurant imagery and the hero video are externally hosted assets and may depend on third-party availability.

Real-world commercial use would require additional security and testing, a production payment provider, delivery integrations, monitoring, privacy policies, and other operational safeguards.

## 🎯 Learning Outcomes

Through this project, I practised:

- Building a full-stack application with Django.
- Designing responsive user interfaces using HTML and CSS.
- Implementing user authentication and protected workflows.
- Working with relational databases and Django ORM.
- Creating and validating shopping-cart and checkout flows.
- Implementing search, filters, reviews, favourites, and coupon logic.
- Deploying a web application using GitHub, Render, and PostgreSQL.

## 👨‍💻 Author

**Sai Ranga**

- GitHub: https://github.com/sairanga06
- Project Repository: https://github.com/sairanga06/foodie-restaurant-ordering-live
- Live Demo: https://foodie-restaurant-ordering.onrender.com

---

<p align="center">
  <strong>Built with Python, Django, and a passion for learning full-stack development.</strong>
</p>

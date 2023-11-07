# About 

This is an API for a shopping list application that allows users to record and share things they want to spend money on and keep track of their shopping lists. This API is developed using the Django REST Framework.


## How to install it?

- First Clone this repo

```bash
    git clone https://github.com/master-projects-theses/laksmiprasanna-malempati.git
```

- Change into the project directory

```bash
    cd Master's-Project
```

- Create a Virtualenv and the project directory

```bash
    python -m venv venv
```

- Activate the virtualenv

```bash
    venv/Scripts/activate
```

- Install the project Dependencies

```bash
    pip install -r requirements.txt
```

- Make The Migrations To the database

```bash
    python manage.py migrate
```

- Spin Up The Django Developement Server

```bash
    python manage.py runserver
```

Now You Are all set and the server Is Running on the url http://localhost:8000 and you can create the products by visiting API endpoints http://127.0.0.1:8000/products, for cart details visit the endpoint http://127.0.0.1:8000/cart.

## Features
With this API;

You can create a user account - Registration
You can login and log out - Authorization and Authentication
You can create, view, update, and delete a shopping list in your user account
You can create, view, update, and delete an item in your shopping list under your account

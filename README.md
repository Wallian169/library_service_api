# Library Management System

A Django REST Framework application for managing a library, including features for books, users, and borrowings.

## DB Sheme
![Alt text](https://raw.githubusercontent.com/Wallian169/images/refs/heads/main/library_DB.jpg)

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Running Tests](#running-tests)

## Features

- Manage books and authors
- User registration and authentication
- Borrowing and returning books
- Track borrowings history
- RESTful API for all functionalities

## Technologies

- Django
- Django REST Framework
- SQLite
- Django REST Framework Spectacular for API documentation
- Simple JWT for authentication

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/library-management-system.git
2. Create venv
    ```bash
    python -m venv venv
3. Activate the virtual environment:
   - For **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - For **macOS and Linux**:
     ```bash
     source venv/bin/activate
     ```
4. Install dependencies:

     ```bash
     pip install -r requirements.txt
     ```
   
## Running tests
```bash
    python manage.py test
```
        
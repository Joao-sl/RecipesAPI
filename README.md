# Recipes API

A comprehensive API for managing recipes, allowing users to create, read, update, and delete their recipes. This project is built with **Django REST Framework** and follows best practices for a RESTful API.

## 🚀 Features

- **User Authentication**: User management via authentication tokens (JWT).
- **Recipes (CRUD)**:
    - Create, view, edit, and delete your own recipes.
    - Support for multiple ingredients and preparation steps per recipe.
    - Search and filter by title, ingredients, or categories.
    - Public/private flag for recipes.
- **Categories and Ingredients**: Management of categories and ingredients associated with each recipe.
- **API Statistics**: A public endpoint to view total recipe, user, and category counts.

## 🛠️ Tech Stack

- **Backend**:
    - **Django**: Python web framework.
    - **Django REST Framework (DRF)**: For building the API.
    - **drf-spectacular**: For interactive documentation (OpenAPI 3.0).
    - **Pillow**: For handling recipe cover images.
- **Database**:
    - **SQLite** (default, for development)
    - Support for other databases like PostgreSQL and MySQL (just configure in `settings.py`).

## 💻 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

Make sure you have Python 3.8+ and `pip` installed.

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Joao-sl/RecipesAPI.git
    cd RecipesAPI
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # or `./venv/Scripts/activate` on Windows
    ```
3.  Install project dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run database migrations:
    ```bash
    python manage.py migrate
    ```
5.  Start the development server:
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/`.

---

### 🗄️API Documentation

The interactive API documentation can be accessed at:

- **Swagger UI**: `http://127.0.0.1:8000/api/schema/swagger-ui/`
- **ReDoc**: `http://127.0.0.1:8000/api/schema/redoc/`

---

## 🤝 Contact

Made with ❤️ by [João](https://github.com/Joao-sl). Feel free to get in touch!

## 📄 License

This project is licensed under the [MIT License](LICENSE).

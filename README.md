
# FastAPI Sample Project

This project is a web application built using Python and FastAPI, following the MVC design pattern. It interfaces with a MySQL database using SQLAlchemy for ORM and implements field validation and dependency injection. The application includes endpoints for user authentication and post management, with token-based authentication and response caching.

## Table of Contents

- [Installation](#installation)
- [Project Structure](#project-structure)
- [Endpoints](#endpoints)
- [Additional Features](#additional-features)
- [Usage](#usage)


## Installation

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd fastapi-sample-project-main
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    - Ensure you have MySQL installed and running.
    - Update the database connection settings in `db/config.py`.
    - Run database migrations using Alembic:

    ```bash
    alembic upgrade head
    ```

5. **Start the FastAPI server:**

    ```bash
    fastapi dev main.py 
    ```

## Project Structure

```
fastapi-sample-project-main/
├── alembic/                 # Database migrations
├── api/                     # API endpoints
│   ├── routes/
│   └── dependencies/
├── core/                    # Core application logic
├── db/                      # Database models and configurations
├── main.py                  # Application entry point
├── requirements.txt         # Project dependencies
├── utils.py                 # Utility functions
└── .gitignore
```

## Endpoints

### Signup

- **URL:** `/signup`
- **Method:** `POST`
- **Payload:**
    ```json
    {
        "email": "user@example.com",
        "password": "password123"
    }
    ```
- **Response:**
    ```json
    {
        "token": "generated_token"
    }
    ```

### Login

- **URL:** `/login`
- **Method:** `POST`
- **Payload:**
    ```json
    {
        "email": "user@example.com",
        "password": "password123"
    }
    ```
- **Response:**
    ```json
    {
        "token": "generated_token"
    }
    ```

### AddPost

- **URL:** `/posts`
- **Method:** `POST`
- **Headers:**
    ```json
    {
        "Authorization": "Bearer token"
    }
    ```
- **Payload:**
    ```json
    {
        "text": "This is a new post"
    }
    ```
- **Response:**
    ```json
    {
        "postID": 1
    }
    ```

### GetPosts

- **URL:** `/posts`
- **Method:** `GET`
- **Headers:**
    ```json
    {
        "Authorization": "Bearer token"
    }
    ```
- **Response:**
    ```json
    [
        {
            "postID": 1,
            "text": "This is a new post"
        }
    ]
    ```

### DeletePost

- **URL:** `/posts/{postID}`
- **Method:** `DELETE`
- **Headers:**
    ```json
    {
        "Authorization": "Bearer token"
    }
    ```
- **Response:**
    ```json
    {
        "message": "Post deleted successfully"
    }
    ```

## Additional Features

- **Token-Based Authentication:** Utilizes JWT for securing endpoints.
- **Payload Validation:** Ensures payload size for posts does not exceed 1 MB.
- **Response Caching:** Caches responses for the `GetPosts` endpoint for up to 5 minutes using `cachetools`.

## Usage

- Run the FastAPI server and interact with the endpoints using tools like Postman or cURL.
- Ensure proper headers and payloads are provided as per the endpoint requirements.

# Oncoclock - Smart Radiotherapy Treatment Planner

Welcome to the Treatment Planner App made for JunctionX Budapest 2023! This application is designed to help professionals plan and schedule radiotherapy treatments effectively. 

A live demo (frontend that interacts with the backend directly) is available at: http://164.90.219.192:8080

It consists of two main components: the backend and the frontend.

## Backend

The backend of the app is built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+. To run the backend, follow these steps:

1. Navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2. Install the required dependencies. It's recommended to set up a virtual environment first:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Run the FastAPI application:
    ```bash
    uvicorn main:app --reload
    ```

   The backend will now be running on [http://localhost:8080](http://localhost:8080). You can access the FastAPI Swagger documentation at [http://localhost:8080/docs](http://localhost:8080/docs) to explore the available API endpoints.

## Frontend

The frontend is a static web application that can be served directly. The HTML, CSS, and JavaScript files are all processed on the client side. To run the frontend, follow these steps:

1. Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

2. Open the `index.html` file in your preferred web browser. You can do this by double-clicking the file or using a simple web server like `http-server`:
    ```bash
    npx http-server
    ```

   The frontend will now be accessible at [http://localhost:8000](http://localhost:8000).

   Other tools (like Python http.server) could also be used for the same purpose.

## Configuration

By default, the backend runs on port 8080, and the frontend runs on port 8000. If you need to change these ports, update the configuration in the respective components.

### Backend Configuration

The backend configuration can be found in the `backend/main.py` file. Look for the following line to change the port:

```python
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")
```

Update the `port` parameter to your desired value.

### Frontend Configuration

The frontend does not require any server configuration by default. If you decide to use a different server or change the port, update the configuration accordingly in your chosen setup.

If you encounter any issues or have suggestions, please create an issue in the repository. 
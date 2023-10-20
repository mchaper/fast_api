# FastAPI Python Web API

This is a Python web API application built using the FastAPI library. The application reads a local image and provides two main endpoints: one for retrieving image attributes and another for generating image thumbnails. The thumbnail endpoint allows you to specify the desired resolution using the `?resolution` query parameter.

## Functionality

### Image Attributes Endpoint

- **Endpoint**: `/attributes`
- **Description**: This endpoint returns the attributes of the local image.

### Image Thumbnail Endpoint

- **Endpoint**: `/thumbnail`
- **Description**: This endpoint generates an image thumbnail. You can specify the resolution using the `?resolution` query parameter.

## Running the Application in Python

1. **Set up a Virtual Environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

2. **Install Dependencies:**   

   ```bash
    pip install -r requirements.txt

3. **Run the FastAPI Application:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000

4. Access the application in your browser at http://localhost:8000   


## Building and Running the Docker Image

To run your FastAPI application in a Docker container, follow these steps:

### Build the Docker Image:
    docker build -t fastapi:1.0.0 app

### Run the Docker Container:
    docker run -d -p 8000:8000 fastapi:1.0.0

Your FastAPI application will be available at http://localhost:8000.

## API Documentation
The API documentation is generated automatically by FastAPI and is available at http://localhost:8000/docs. You can explore the available endpoints and make test requests using the Swagger-based interactive documentation.

## License 
MIT License

Copyright (c) 2023 Miguel Chapela Rivas



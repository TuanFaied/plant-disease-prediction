# Plant Disease Prediction

This project aims to predict plant diseases using a machine learning model. The project is divided into two main parts: the frontend and the backend.

## Project Overview

Plant Disease Prediction leverages machine learning to identify diseases in plants from images. This can help farmers and gardeners detect issues early and take appropriate actions to save their crops.

## Installation

### Backend

1. Clone the repository:
    ```sh
    git clone https://github.com/TuanFaied/plant-disease-prediction.git
    cd plant-disease-prediction/backend
    ```

2. Create a Python virtual environment:
    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```

4. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

5. Run the backend server:
    ```sh
    python app.py
    ```

### Frontend

1. Navigate to the frontend directory:
    ```sh
    cd ../frontend
    ```

2. Install dependencies:
    ```sh
    npm install
    ```

3. Run the frontend application:
    ```sh
    npm start
    ```

## Usage

### Backend

- The backend provides a REST API for the frontend to interact with the machine learning model.
- It is built using Flask

### Frontend

- The frontend is a web application that allows users to upload images of plant leaves.
- It interacts with the backend to get predictions and displays the results to the user.

### Google Colab Link

For training the model, you can use the provided Google Colab notebook:
[Google Colab Link](https://colab.research.google.com/drive/1FmbMFc1EcbUwDrGJNr8KO4SLgi38VHYY?usp=sharing)



# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files and buffering output
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt into the container at /app
COPY requirements.txt /app/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container
COPY . /app

# Expose the port the app will run on
EXPOSE 8501

# Command to run the application using Gunicorn
# Replace 'dashboard:app' with your Flask app's module and app name if different
CMD ["gunicorn", "--bind", "0.0.0.0:8501", "dashboard:server"]

# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt (you will create this file in the next step)
COPY requirements.txt /app/

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port your app will run on
EXPOSE 8501

# Use Gunicorn to serve the app in production
CMD ["gunicorn", "-b", "0.0.0.0:8050", "dashbord:server"]

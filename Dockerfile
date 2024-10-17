# Use an official Python 3.12 runtime as a base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Update pip to the latest version
RUN python -m pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8501

# Run the app with Gunicorn when the container launches
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8501", "dashboard:server"]

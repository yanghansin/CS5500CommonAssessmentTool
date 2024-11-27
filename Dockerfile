# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3-pip libmariadb-dev libmariadb-dev-compat build-essential pkg-config && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the port your app runs on
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

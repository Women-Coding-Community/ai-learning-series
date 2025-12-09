# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for some python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# [optional] Add FastAPI/Uvicorn to requirements if not present
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install fastapi uvicorn pydantic

# Copy the rest of the application code
COPY . .

# Expose the port (Cloud Run defaults to 8080)
EXPOSE 8080

# Command to run the API server
CMD ["python", "api.py"]
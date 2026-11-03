# Use official Python image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependencies file
COPY requirements.txt .

# Install dependencies (no cache to reduce image size)
RUN pip install  --no-cache-dir -r requirements.txt

# Copy all project code
COPY . .

# Expose the port the app will listen on
EXPOSE 8000

# Command to run the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
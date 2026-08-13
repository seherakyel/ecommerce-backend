# Start with a lightweight version of Python
FROM python:3.12-slim

# Working directory inside the container
WORKDIR /app

# First, just copy the requirements (for the cache)
COPY requirements.txt .

# Install the libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
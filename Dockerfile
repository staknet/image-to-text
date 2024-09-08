# Use a base image with Python
FROM python:3.11-slim

# Install Tesseract
RUN apt-get update && \
    apt-get install -y tesseract-ocr

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . /app
WORKDIR /app

# Set the command to run your application
CMD ["python", "app.py"]

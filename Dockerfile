# Stage 1: Build
FROM python:3.11-slim AS builder

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install Tesseract again in the final image
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*

# Copy only the necessary files from the builder stage
COPY --from=builder /app /app

# Copy the application code from the current directory to the /app directory in the final image
COPY app.py .

# Copy templates and static files
COPY templates templates
COPY static static

# Set the command to run your application
CMD ["python", "app.py"]

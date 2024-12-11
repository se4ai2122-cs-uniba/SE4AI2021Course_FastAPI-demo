# Set base image
FROM python:3.10.15-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Set work directory
WORKDIR /fastAPIapp

# Copy the FastAPI project
COPY . .

# Expose port
EXPOSE 8000

# Run the FastAPI application
CMD ["fastapi", "run", "app/api.py", "--port", "8000"]
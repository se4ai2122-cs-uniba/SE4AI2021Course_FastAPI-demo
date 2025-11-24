# SET BASE IMAGE
FROM python:3.10.15-slim-bookworm

# SET ENVIRONMENT VARIABLES
# Flush stdout/stderr immediately for realtime logs
ENV PYTHONUNBUFFERED=1
# Skip .pyc generation to keep the image lean
ENV PYTHONDONTWRITEBYTECODE=1
# Disable pip cache to avoid persisting downloaded wheels
ENV PIP_NO_CACHE_DIR=1
# Skip pip's version check to speed up installs
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# INSTALL DEPENDENCIES
WORKDIR /fastAPIapp
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# COPY RUNTIME SOURCES AND MODELS
COPY app ./app
COPY models ./models

# EXPOSE THE APPLICATION PORT
EXPOSE 55000

# RUN THE FASTAPI APPLICATION
CMD ["fastapi", "run", "app/api.py", "--port", "55000"]
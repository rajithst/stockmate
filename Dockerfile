# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Copy uv from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    # uv configuration
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the project definition files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
# --frozen: error if lockfile is out of date
# --no-dev: skip dev dependencies
# --no-install-project: don't install the package itself yet
RUN uv sync --frozen --no-dev --no-install-project

# Copy the application code
COPY README.md ./
COPY app ./app
COPY alembic.ini ./
COPY alembic ./alembic

# Install the project itself
RUN uv sync --frozen --no-dev

# Place the virtualenv in the path
ENV PATH="/app/.venv/bin:$PATH"

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Expose the port that the application listens on
EXPOSE 8080

# Run the application
# We use sh -c to expand the PORT environment variable
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]

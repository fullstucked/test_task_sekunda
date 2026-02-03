FROM python:3.13-slim AS base

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Disable development dependencies
ENV UV_NO_DEV=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local

# Create non-root user
RUN useradd -m appuser

WORKDIR .

# Copy only dependency files first for caching
COPY pyproject.toml uv.lock .

# Install dependencies into global environment
RUN uv sync --frozen --no-dev
# Copy application code
COPY . .

# Switch to non-root user
USER appuser

EXPOSE 8000
CMD ["/bin/sh", "-c", "alembic upgrade head && uv run src/handbook/main.py"]

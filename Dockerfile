
FROM python:3.12

ENV APP_HOME=/app
WORKDIR $APP_HOME

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create a virtual environment
RUN uv venv .venv --python python3.12
ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN uv pip install -r requirements.txt

# Copy application code
COPY . .

EXPOSE 3000 5055

ENTRYPOINT ["python", "main.py"]
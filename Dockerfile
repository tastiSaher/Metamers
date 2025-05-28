FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
ENV UV_PROJECT_ENVIRONMENT=1
RUN uv sync --no-dev

COPY . .

ENTRYPOINT ["uv","run"]
CMD ["example_1D.py"]

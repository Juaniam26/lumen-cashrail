FROM python:3.14.7-slim@sha256:caaf356f40667c496d405780745b9ac25771c189a51dfcc42430d531ea09f8a2

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN addgroup --system cashrail && adduser --system --ingroup cashrail cashrail
COPY pyproject.toml ./
COPY cashrail_runtime ./cashrail_runtime
RUN python -m pip install --upgrade pip && python -m pip install .
USER cashrail
EXPOSE 8000
CMD ["uvicorn", "cashrail_runtime.api:app_from_environment", "--factory", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--no-server-header"]

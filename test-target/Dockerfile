# 1. Supported Python, slim variant (Python 3.9 is end-of-life)
FROM python:3.13-slim

# 2. Sensible Python defaults for containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# 3. Create an unprivileged user with a fixed numeric UID/GID
RUN groupadd --system --gid 10001 app \
 && useradd --system --uid 10001 --gid app --no-create-home app

# 4. Install dependencies first, from a pinned requirements file
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip uninstall -y pip

# 5. Copy the app code with COPY (not ADD)
COPY app.py .

# 6. Drop root privileges
USER 10001:10001

EXPOSE 5000

# 7. Health check without curl
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')"]

# 8. Production server; SECRET_KEY is passed at runtime with docker run -e
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
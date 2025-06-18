# 1. Base image
FROM python:3.10-slim

# 2. Set working dir & unbuffered output
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# 3. Install OS-level deps for Postgres client & Alembic
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# 4. Copy & install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your app code
COPY . .

# 6. Expose and default command
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

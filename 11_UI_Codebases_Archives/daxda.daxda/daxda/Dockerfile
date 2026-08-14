FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (layer-cached)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run as non-root
RUN useradd -m daxda && chown -R daxda:daxda /app
USER daxda

EXPOSE 8080

CMD ["uvicorn", "daxda.api.main:app", "--host", "0.0.0.0", "--port", "8080"]

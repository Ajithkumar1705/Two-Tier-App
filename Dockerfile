FROM python:3.12-slim

# Run as non-root user
RUN useradd -m appuser
WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

USER appuser
EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["python", "app.py"]
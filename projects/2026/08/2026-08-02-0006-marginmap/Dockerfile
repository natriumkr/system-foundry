FROM python:3.12-alpine

WORKDIR /app
COPY app/ /app/

EXPOSE 8080
CMD ["python3", "-m", "http.server", "8080", "--directory", "/app"]

FROM python:3.12-alpine
WORKDIR /app
COPY app/ ./app/
EXPOSE 4175
CMD ["python3","-m","http.server","4175","-d","app"]

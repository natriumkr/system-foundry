FROM python:3.12-alpine
WORKDIR /app
COPY app/ ./app/
EXPOSE 4174
CMD ["python3","-m","http.server","4174","-d","app"]

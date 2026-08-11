FROM python:3.12-alpine
WORKDIR /app
COPY app/ /app/
EXPOSE 4173
CMD ["python3","-m","http.server","4173","--directory","/app"]

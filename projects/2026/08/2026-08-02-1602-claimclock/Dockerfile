FROM python:3.12-slim
WORKDIR /app
COPY app ./app
RUN mkdir -p /app/data && useradd --create-home claimclock && chown -R claimclock:claimclock /app
USER claimclock
ENV CLAIMCLOCK_HOST=0.0.0.0 CLAIMCLOCK_PORT=8080 CLAIMCLOCK_DB_PATH=/app/data/claimclock.db
EXPOSE 8080
CMD ["python3", "-m", "app.server"]

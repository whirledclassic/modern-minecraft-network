FROM python:3.12-slim
WORKDIR /app
COPY app.py /app/app.py
COPY static /app/static
COPY templates /app/templates
RUN mkdir -p /data
EXPOSE 8080
CMD ["python", "-u", "/app/app.py"]

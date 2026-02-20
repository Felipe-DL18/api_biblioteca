FROM python:3.9-alpine
#RUN apt-get update && \
    #apt-get install python3.11 python3.11-dev python3-pip -y

WORKDIR /app
COPY requirements.txt . 
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

CMD ["python3", "app/app.py"]
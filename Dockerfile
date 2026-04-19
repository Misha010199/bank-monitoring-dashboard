FROM python:3.9

WORKDIR /app

COPY app-code/ .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
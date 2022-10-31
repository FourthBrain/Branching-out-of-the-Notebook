FROM python:3.10-slim

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

RUN rm /tmp/requirements.txt

COPY /app /app

COPY /model /model

WORKDIR /app

EXPOSE 5000

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]


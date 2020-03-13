FROM ubuntu:18.04
FROM python:3.7 

ADD . /app
WORKDIR /app

RUN pip install pillow
RUN pip install onnxruntime
RUN pip install numpy

RUN chmod +x /app/main.py
CMD python3 /app/main.py

FROM ubuntu:20.04

RUN apt update && apt install -y python3

RUN apt install -y python3-pip 

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

CMD ["python3", "procedimiento.py"]
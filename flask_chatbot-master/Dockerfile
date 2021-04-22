FROM ubuntu:16.04

RUN apt update -y && \
    apt install -y python3-pip python3

COPY ./requirements.txt /app/requirements.txt

WORKDIR /flask_chatbot-master

COPY . /flask_chatbot-master

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "index.py" ]

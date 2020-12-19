FROM python:3.9-buster

ADD . /work
WORKDIR /work
RUN pip install -r requirements.txt

CMD ["tail", "-f", "/dev/null"]
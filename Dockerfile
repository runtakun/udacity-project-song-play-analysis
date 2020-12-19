FROM python:3.9-buster

# ADD . /work
WORKDIR /work
CMD ["./init.sh"]
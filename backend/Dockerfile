# Using lightweight alpine image
FROM python:3.7-alpine

# Installing packages
RUN apk update 
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev


WORKDIR /usr/src/app


#Install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Defining working directory and adding source code
COPY bootstrap.sh ./
COPY orangecat ./orangecat

#Start app
EXPOSE 3000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]

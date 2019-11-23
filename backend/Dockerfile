# Using lightweight alpine image
FROM python:3.7-alpine

# Installing packages
RUN apk update 
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev

# Defining working directory and adding source code
WORKDIR /usr/src/app
COPY bootstrap.sh ./
COPY orangecat ./orangecat
COPY requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt


#Start app
EXPOSE 5000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]

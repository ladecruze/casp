FROM python:3-alpine
ADD . /CASP
WORKDIR /
ENV FLASK_APP=CASP
ENV FLASK_RUN_HOST=0.0.0.0
ENV DB_USERNAME=postgres
ENV DB_PASSWORD=root
RUN apk update 
RUN apk add gcc musl-dev libffi-dev openssl-dev libpq-dev python3-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "flask","--debug", "run","-p","8000" ]
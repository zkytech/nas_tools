FROM python:3.9-alpine
RUN apk add git
WORKDIR /app
COPY ./run.sh /app/run.sh
CMD [ "run.sh" ]

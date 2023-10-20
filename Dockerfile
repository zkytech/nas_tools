FROM python:3.9-alpine
RUN apk add git
WORKDIR /app
COPY ./run.sh /app/init.sh
RUN chmod +x /app/init.sh
CMD [ "/app/init.sh" ]

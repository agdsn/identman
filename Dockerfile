FROM alpine:3.14
RUN apk add --update nodejs npm bash

WORKDIR /opt

COPY --link .. /app
RUN addgroup -S frontend
RUN adduser -S frontend

USER frontend
WORKDIR /home/frontend


ENTRYPOINT ["bash"]
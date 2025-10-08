FROM alpine:3.14 AS build
RUN apk add --update nodejs npm bash

WORKDIR /opt

RUN addgroup -S frontend
RUN adduser -S frontend

USER frontend
WORKDIR /opt/identman

COPY frontend/package.json /opt/identman
RUN npm install
COPY frontend /opt/identman

ARG REACT_APP_API
ENV REACT_APP_API=$REACT_APP_API

RUN npm run build

FROM nginx:alpine
COPY --from=build /opt/identman/build /usr/share/nginx/html

EXPOSE 80
EXPOSE 443
CMD ["nginx", "-g", "daemon off;"]
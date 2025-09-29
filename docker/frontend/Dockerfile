FROM alpine:3.14 as build
RUN apk add --update nodejs npm bash

WORKDIR /opt

COPY --link frontend /opt/identman
RUN addgroup -S frontend
RUN adduser -S frontend
RUN chown -R frontend:frontend identman

USER frontend

WORKDIR /opt/identman

RUN npm run build

FROM nginx:alpine
COPY --from=build /opt/identman/build /usr/share/nginx/html

EXPOSE 80
EXPOSE 443
CMD ["nginx", "-g", "daemon off;"]
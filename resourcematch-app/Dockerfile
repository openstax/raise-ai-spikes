FROM node:20 as base

WORKDIR /code

COPY package.json .
COPY package-lock.json .

RUN npm install

COPY . .

FROM base as builder

RUN npm run build

FROM nginx:1.25 as deploy

COPY --from=builder /code/nginx.conf /etc/nginx/templates/default.conf.template

COPY --from=builder /code/dist/client /usr/share/nginx/html

FROM base as dev

CMD ["npm", "run", "dev"]
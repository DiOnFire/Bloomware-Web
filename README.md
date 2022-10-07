# Bloomware-Web
The first version of the Bloomware server part. It was made by me and supported by me until I decided to completely leave the project.
The frontend does not use any frameworks and is not protected.

## Frameworks

- FastAPI
- Alembic
- Jinja
- SQL Alchemy

# How to use

- Download all this shit.
- Run ```gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app```.
- Done.

## Deploy on Linux with NGINX

- (my personal recommendation) Use [PM2](https://pm2.io/) process manager.
- Download [NGINX](https://nginx.org/).
- Setup NGINX and use this config:

```
server {
  listen 80;
  server_name {your's server IP} {your's server domain}
  location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }
}
```
- Done.

happy hacking :^)

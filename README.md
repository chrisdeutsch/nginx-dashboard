# NGINX Dashboard

A simple dashboard using Plotly's Dash to show basic analytics parsed from NGINX
log files.

## Quickstart

Place your NGINX log files in `data/` and run the app as follows:

```bash
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Docker Compose

`docker-compose.yml`:

```bash
---
version: "3"
services:
  dashboard:
    build: .
    container_name: nginx_dashboard
    volumes:
      - /home/chris/swag/config/log/nginx:/app/data:ro
    environment:
      - TZ=Europe/Berlin
    ports:
      - "10.0.0.1:8000:8000/tcp"
```

## Limitations

- Currently only support for the default NGINX log format.

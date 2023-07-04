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

## Limitations

- Currently only support for the default NGINX log format.
- No caching implemented: parses the logfiles on every update.

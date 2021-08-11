#!/bin/sh

gunicorn --log-level debug --reload -b 0.0.0.0:8080 --timeout=15 --worker-class=noonutil.v1.fastapiutil.RequestKillerWorker --workers 10 appfoo.web:app

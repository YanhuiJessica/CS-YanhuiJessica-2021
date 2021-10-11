#!/bin/sh

sed -i "s/actf{test_flag}/$FLAG/" /app/app.py

export FLAG=not_flag
FLAG=not_flag

/usr/local/bin/flask run -h 0.0.0.0 -p 80
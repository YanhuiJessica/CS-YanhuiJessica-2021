FROM python:3.9

LABEL Author="YanhuiJessica" Github="https://github.com/YanhuiJessica"

ENV FLASK_APP=app.py FLASK_ENV=production

COPY ./app /app

RUN python3 -m pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && chmod +x /app/entrypoint.sh

WORKDIR /app

CMD [ "/bin/sh", "-c", "/app/entrypoint.sh" ]
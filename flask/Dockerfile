FROM python:3

RUN groupadd -r flask && useradd --no-log-init -r -g flask flask

WORKDIR /usr/src/app
RUN mkdir db
RUN mkdir files

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R flask:flask /usr/src/app/

EXPOSE 5000/tcp

USER flask
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]


ENTRYPOINT ["./gunicorn.sh"]

#Server Dockerfile

FROM python:3.10-slim
WORKDIR /app

COPY server/ /app/server/
COPY public_key.pem /app/
RUN python3 -m pip install vtece4564-gamelib
CMD ["/usr/local/bin/python3", "-m", "server"]



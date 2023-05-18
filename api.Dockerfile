#api dockerfile

FROM python:3.10-slim
WORKDIR /app
COPY api/ /app/api/
COPY private_key.pem /app/
RUN python3 -m pip install flask vtece4564-gamelib
CMD ["/usr/local/bin/python3", "-m", "api"]




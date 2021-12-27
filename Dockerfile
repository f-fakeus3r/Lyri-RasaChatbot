FROM python:3.8-slim

USER root
WORKDIR /app
COPY . .
RUN pip install -r /app/requirements.txt

USER 1001

# set entrypoint for interactive shells

CMD ["bash"]
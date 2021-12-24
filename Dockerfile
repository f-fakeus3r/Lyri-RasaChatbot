FROM rasa/rasa-sdk:latest
WORKDIR /app
COPY . .
USER root
RUN pip install -r /app/requirements.txt
COPY ./actions /app/actions
USER 1001
ENTRYPOINT ["rasa", "shell"]
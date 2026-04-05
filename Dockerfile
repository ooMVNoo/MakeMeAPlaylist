FROM ubuntu:24.04
WORKDIR /app
COPY . /app
RUN apt update && apt install -y python3 python3-pip && pip3 install spotipy flask scikit-learn pandas python-dotenv --break-system-packages
ENTRYPOINT ["python3"]
CMD ["app.py"]
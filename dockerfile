# syntax=docker/dockerfile:1

# base python-alpine image for custom image
FROM python:alpine

# create working directory and install pip dependencies
WORKDIR /Hanekawa-san
RUN apk update
RUN apk add --no-cache libffi libffi-dev gcc musl-dev linux-headers opus opus-dev opus-tools curl
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# copy python project files from local to /Hanekawa-san image working directory
COPY . .
# copy latest ffmpeg-static to bin/ . By default bin/ has a ffmpeg static for dev, this is updating
COPY --from=mwader/static-ffmpeg:latest /ffmpeg bin/ffmpeg

# run the bot
CMD ["python3", "-Ou", "main.py"]

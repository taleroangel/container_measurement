MAINTAINER "Angel D. Talero (angelgotalero@outlook.com)"

FROM docker.io/library/alpine:latest

COPY . /home/application
WORKDIR /home/application

# Install dependencies
RUN ["apk", "add", "--no-cache", "build-base", "linux-headers", "perf", "python3", "py3-opencv", "py3-pip", "python3-dev"]

# Build-system installation and setup
RUN ["pip3", "install", "glances", "colorama", "bottle"]

# Ports
EXPOSE 24111
EXPOSE 24112

# Entry point
ENTRYPOINT ["sh", "./scripts/runner.sh"]

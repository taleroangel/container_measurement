MAINTAINER "Angel D. Talero (angelgotalero@outlook.com)"

FROM docker.io/library/alpine:latest

COPY . /home/application
WORKDIR /home/application

# Install dependencies
RUN ["apk", "update"]
RUN ["apk", "add", "build-base", "pkgconf", "cmake", "ninja", "python3", "py3-pip", "py3-setuptools", "py3-wheel", "opencv", "opencv-dev", "fmt-dev"]

# Build-system installation and setup
RUN ["pip3", "install", "meson", "conan", "glances"]
RUN ["conan", "profile", "detect"]
RUN ["conan", "install", ".", "--build=missing"]

# Compilation
RUN ["conan", "build", "."]

# Entry point
ENTRYPOINT ["sh", "./scripts/run_perf.sh"]
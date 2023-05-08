MAINTAINER "Angel D. Talero (angelgotalero@outlook.com)"

FROM docker.io/library/alpine:latest

COPY . /home/application
WORKDIR /home/application

# Install dependencies
RUN ["apk", "add", "--no-cache", "build-base", "pkgconf", "cmake", "ninja", "python3", "python3-dev", "py3-pip", "py3-setuptools", "py3-wheel", "opencv", "opencv-dev", "fmt-dev", "perf"]

# Build-system installation and setup
RUN ["pip3", "install", "meson", "conan", "glances", "bottle"]
RUN ["conan", "profile", "detect"]
RUN ["conan", "install", ".", "--build=missing"]

# Compilation
RUN ["conan", "build", "."]

# Ports
EXPOSE 24111
EXPOSE 24112

# Entry point
ENTRYPOINT ["sh", "./scripts/glances_server.sh"]

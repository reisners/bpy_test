FROM "ubuntu:21.04"

RUN apt update \
    && apt install -y apt-utils \
    && apt install -y software-properties-common \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt install -y python3.9-dev \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1 \
    && apt install -y sudo \
    && apt install -y git \
    && apt install -y llvm

COPY blender-as-python-module /source

ARG PYTHON_SITE_PACKAGES=/usr/lib/python3.9/site-packages
ENV PYTHON_SITE_PACKAGES=${PYTHON_SITE_PACKAGES}
ENV PYTHONPATH=${PYTHON_SITE_PACKAGES}

#RUN /source/install && /source/build
RUN apt install -y vim

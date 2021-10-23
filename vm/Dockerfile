FROM "ubuntu:20.04"

RUN apt update \
    && apt install -y apt-utils \
    && apt install -y software-properties-common \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt install -y python3.8 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1 \
    && apt install -y sudo \
    && apt install -y git \
    && apt install -y llvm

COPY blender-as-python-module/install /install
COPY blender-as-python-module/build /build
COPY blender-as-python-module/blender /source
RUN /install && /build

ARG PYTHON_SITE_PACKAGES /usr/lib/python3.8/site-packages
ENV PYTHONPATH ${PYTHON_SITE_PACKAGES}

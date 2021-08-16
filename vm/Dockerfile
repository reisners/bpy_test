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

ADD blender-as-python-module/install /install
ADD blender-as-python-module/build /build
ADD blender-as-python-module/blender /blender
RUN /install && /build

ENV PYTHONPATH=/usr/lib/python3.8/site-packages

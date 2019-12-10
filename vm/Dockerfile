FROM "ubuntu:18.04"

ADD install_deps.sh /tmp

RUN apt update \
	&& apt install -y apt-utils \
	&& apt install -y software-properties-common \
	&& add-apt-repository -y ppa:deadsnakes/ppa \
	&& apt install -y python3.7 \
	&& add-apt-repository -y ppa:freecad-maintainers/freecad-stable \
	&& apt install -y freecad-python3 \
	&& apt install -y sudo \
	&& /tmp/install_deps.sh

ENV PYTHONPATH=/work/blender/site-packages

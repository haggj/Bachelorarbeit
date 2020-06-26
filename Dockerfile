FROM ubuntu:18.04

WORKDIR /usr/src/app

COPY container/requirements.txt ./

#Install python dependencies
RUN apt-get -y update
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1

#Install valgrind
RUN apt-get -y install valgrind
RUN apt-get -y install sudo

#Install go dependencies
RUN apt-get -y install git
RUN apt-get -y install golang-1.10
ENV PATH="/usr/lib/go-1.10/bin:${PATH}"
RUN go get "github.com/cloudflare/circl/dh/sidh"

#install openssl and libgmp3
RUN apt-get -y install libssl-dev
RUN apt-get -y install  libgmp3-dev


COPY container .

#Default command
CMD [ "python3", "benchmarking.py" ]

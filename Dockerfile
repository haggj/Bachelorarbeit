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

#install libgmp3
RUN apt-get -y install  libgmp3-dev

COPY openssl openssl

#install openssl from source with debug symbols
RUN mkdir /opt/openssl
RUN tar xfvz openssl/openssl-1.1.1g.tar.gz --directory /opt/openssl
RUN cd /opt/openssl/openssl-1.1.1g; ./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl -g3 -ggdb --debug
RUN cd /opt/openssl/openssl-1.1.1g; make
RUN cd /opt/openssl/openssl-1.1.1g; make install

COPY container .

#Default command
CMD [ "python3", "benchmarking.py" ]

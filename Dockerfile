FROM ubuntu:18.04

WORKDIR /usr/src/app

# Install valgrind
RUN apt-get -y update
RUN apt-get -y install valgrind
RUN apt-get -y install sudo
RUN apt-get -y install git
RUN apt-get -y install wget
RUN apt-get -y install wget
RUN apt-get -y install -y unzip

# Install python
COPY container/requirements.txt ./
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1

# Install libgmp3 and wget
RUN apt-get -y install  libgmp3-dev

COPY openssl openssl

# Install openssl from source with debug symbols
# RUN mkdir /opt/openssl
# RUN tar xfvz openssl/openssl-1.1.1g.tar.gz --directory /opt/openssl
# RUN cd /opt/openssl/openssl-1.1.1g; ./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl -g3 -ggdb --debug -O3
# RUN cd /opt/openssl/openssl-1.1.1g; make
# RUN cd /opt/openssl/openssl-1.1.1g; make install

# Download and compile PQCrypto-SIDH
RUN mkdir Microsoft
RUN mkdir Microsoft/.src
RUN mkdir Microsoft/.src/x64
RUN mkdir Microsoft/.src/generic
RUN git clone https://github.com/microsoft/PQCrypto-SIDH.git Microsoft/.src/x64
RUN cp -r Microsoft/.src/x64/* Microsoft/.src/generic/
RUN cd Microsoft/.src/x64; make ARCH=x64 CC=gcc OPT_LEVEL=FAST USE_MULX=TRUE USE_ADX=TRUE
RUN cd Microsoft/.src/generic; make ARCH=x64 CC=gcc OPT_LEVEL=GENERIC USE_MULX=FALSE USE_ADX=FALSE

# Prepare SIKE
COPY container/SIKE/.src SIKE/.src
RUN unzip SIKE/.src/optimized.zip -d SIKE/.src/
RUN unzip SIKE/.src/x64.zip -d SIKE/.src/
RUN unzip SIKE/.src/reference.zip -d SIKE/.src/

# Install go dependencies
RUN wget https://dl.google.com/go/go1.15.2.linux-amd64.tar.gz
RUN sudo tar -xvf go1.15.2.linux-amd64.tar.gz
RUN sudo mv go /usr/local
ENV GOROOT=/usr/local/go 
ENV PATH=$GOROOT/bin:$PATH 
RUN go get "golang.org/x/sys/cpu"
RUN go get "github.com/cloudflare/circl/"
RUN sed -i 's/+build noasm,arm64 !amd64/+build noasm !arm64,!amd64/' /root/go/src/github.com/cloudflare/circl/dh/sidh/internal/p434/arith_generic.go
RUN sed -i 's/ import "golang.org\/x\/crypto\/sha3"//' /root/go/src/github.com/cloudflare/circl/internal/sha3/doc.go

# Install perf
RUN apt-get install -y linux-tools-common linux-tools-generic linux-tools-`uname -r`

COPY container .

#Default command
CMD [ "python3", "benchmarking.py" ]
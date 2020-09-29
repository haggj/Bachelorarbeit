FROM ubuntu:18.04

WORKDIR /usr/src/app

# Install valgrind
RUN apt-get -y update
RUN apt-get -y install valgrind
RUN apt-get -y install sudo

# Install go dependencies
RUN apt-get -y install git
RUN apt-get -y install golang-1.10
ENV PATH="/usr/lib/go-1.10/bin:${PATH}"
RUN go get "github.com/cloudflare/circl/dh/sidh"

# Install libgmp3 and wget
RUN apt-get -y install  libgmp3-dev
RUN apt-get -y install wget

COPY openssl openssl

# Install openssl from source with debug symbols
RUN mkdir /opt/openssl
RUN tar xfvz openssl/openssl-1.1.1g.tar.gz --directory /opt/openssl
RUN cd /opt/openssl/openssl-1.1.1g; ./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl -g3 -ggdb --debug -O3
RUN cd /opt/openssl/openssl-1.1.1g; make
RUN cd /opt/openssl/openssl-1.1.1g; make install

# Download and compile PQCrypto-SIDH
RUN mkdir Microsoft
RUN mkdir Microsoft/.src
RUN mkdir Microsoft/.src/x64
RUN mkdir Microsoft/.src/generic
RUN git clone https://github.com/microsoft/PQCrypto-SIDH.git Microsoft/.src/x64
RUN cp -r Microsoft/.src/x64/* Microsoft/.src/generic/
RUN cd Microsoft/.src/x64; make ARCH=x64 CC=gcc OPT_LEVEL=FAST USE_MULX=TRUE USE_ADX=TRUE
RUN cd Microsoft/.src/generic; make ARCH=x64 CC=gcc OPT_LEVEL=GENERIC USE_MULX=FALSE USE_ADX=FALSE

# Download and compile SIKE
RUN mkdir SIKE; mkdir SIKE/.src
RUN wget https://sike.org/files/sike.tar.gz
RUN tar -xf sike.tar.gz -C SIKE/.src/ --strip-components 1



# Install python
COPY container/requirements.txt ./
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1

COPY container .

#Default command
CMD [ "python3", "benchmarking.py" ]
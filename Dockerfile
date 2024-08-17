FROM ubuntu:24.04 as builder

RUN apt-get update && apt-get install --no-install-recommends -yq \
     build-essential \
     ca-certificates \
     automake \
     autoconf \
     libtool \
     git \
     g++ \
     wget
WORKDIR /build
RUN git clone https://github.com/ttsou/turbofec
RUN git clone https://github.com/proto17/dji_droneid
WORKDIR /build/dji_droneid
RUN git checkout 7fa0fc4988f88c6f608e86c003e204171d892fa3
WORKDIR /build/turbofec
RUN autoreconf -i && ./configure && make install && ldconfig -v
WORKDIR /build/dji_droneid/cpp
RUN wget https://raw.githubusercontent.com/d-bahr/CRCpp/master/inc/CRC.h
RUN g++ -Wall remove_turbo.cc -o remove_turbo -I. -I/usr/local/include -L/usr/local/lib -lturbofec

FROM ubuntu:24.04

RUN apt-get update && apt-get install --no-install-recommends -yq \
     ca-certificates \
     git \
     patch \
     octave \
     octave-signal \
     python3
WORKDIR /build
COPY --from=builder /usr/local /usr/local
COPY --from=builder /build/dji_droneid /build/dji_droneid
RUN ldconfig -v
RUN ldd /build/dji_droneid/cpp/remove_turbo
WORKDIR /build/dji_droneid
COPY process_file.patch process_file.patch
RUN patch -p1 < process_file.patch
WORKDIR /root
COPY samples2djidroneid.py samples2djidroneid.py
COPY decode_djidroneid.py decode_djidroneid.py
RUN /root/samples2djidroneid.py --help
ENTRYPOINT ["/root/samples2djidroneid.py"]

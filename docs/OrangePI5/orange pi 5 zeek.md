---
layout: default
title: orange pi 5 zeek
nav_order: 1
parent: OrangePI5
---
                

# Zeek 설치

Zeek 기본 컨테이너는 전부 x86/amd64 아키텍처만 지원한다.  
arm 지원 컨테이너는 알아서 컴파일해서 써야 한다.  

## Build
git에서 docker 파일 clone 받는다.  
```sh
git clone https://github.com/zeek/zeek-docker.git
```

maxmind 라이선스 키를 export한다.(maxmind 가입 및 키 등록)  
```sh
export MAXMIND_LICENSE_KEY=<value of your license key>
```

디렉토리를 이동한다.  

```sh
cd zeek-docker
```

빌드 전에 Docker 파일을 일부 수정한다.  

```Dockerfile
# bro
#
# VERSION               0.1

# Checkout and build Zeek
FROM debian:bullseye as builder
MAINTAINER Justin Azoff <justin.azoff@gmail.com>

ENV WD /scratch

RUN mkdir ${WD}
WORKDIR /scratch

RUN apt-get update && apt-get upgrade -y && echo 2021-03-01
RUN apt-get -y install build-essential git bison flex gawk cmake swig libssl-dev libmaxminddb-dev libpcap-dev python3.9-dev libcurl4-openssl-dev wget libncurses5-dev ca-certificates zlib1g-dev --no-install-recommends

ARG ZEEK_VER=4.2.0
ARG BUILD_TYPE=Release
ENV VER ${ZEEK_VER}
ADD ./common/buildbro ${WD}/common/buildbro
RUN ${WD}/common/buildbro zeek ${VER} ${BUILD_TYPE}

# For testing
ADD ./common/getmmdb.sh /usr/local/getmmdb.sh
ADD ./common/bro_profile.sh /usr/local/bro_profile.sh

# Get geoip data
FROM debian:bullseye as geogetter
ARG MAXMIND_LICENSE_KEY
RUN apt-get update && apt-get -y install wget ca-certificates --no-install-recommends

# For testing
#ADD ./common/getmmdb.sh /usr/local/bin/getmmdb.sh
COPY --from=builder /usr/local/getmmdb.sh /usr/local/bin/getmmdb.sh
RUN mkdir -p /usr/share/GeoIP
RUN /usr/local/bin/getmmdb.sh ${MAXMIND_LICENSE_KEY}
# This is a workaround for the case where getmmdb.sh does not create any files.
RUN touch /usr/share/GeoIP/.notempty

# Make final image
FROM debian:bullseye
ARG ZEEK_VER=4.2.0
ENV VER ${ZEEK_VER}
#install runtime dependencies
RUN apt-get update \
    && apt-get -y install --no-install-recommends libpcap0.8 libssl1.1 libmaxminddb0 python3.9 net-tools \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/zeek-${VER} /usr/local/zeek-${VER}
COPY --from=geogetter /usr/share/GeoIP/* /usr/share/GeoIP/
RUN rm -f /usr/share/GeoIP/.notempty
RUN ln -s /usr/local/zeek-${VER} /bro
RUN ln -s /usr/local/zeek-${VER} /zeek

# For testing
#ADD ./common/bro_profile.sh /etc/profile.d/zeek.sh
COPY --from=builder /usr/local/bro_profile.sh /etc/profile.d/zeek.sh

env PATH /zeek/bin/:$PATH
# CMD /bin/bash -l

ADD https://raw.githubusercontent.com/blacktop/docker-zeek/master/scripts/conn-add-geodata.zeek \
  /zeek/share/zeek/site/geodata/conn-add-geodata.zeek
ADD https://raw.githubusercontent.com/blacktop/docker-zeek/master/scripts/log-passwords.zeek \
  /zeek/share/zeek/site/passwords/log-passwords.zeek
ADD ./run.sh /run.sh
CMD /run.sh
```

run.sh 파일을 만든다.

```sh
zeekctl deploy
sleep infinity
```

빌드합시다.  

```sh
make build-stamp_4.2.0
```

만약 재빌드를 해야할 경우 build-stamp_4.2.0 파일을 삭제하고 다시 위 make 명령어를 실행한다.  
broplatform/bro:4.2.0라는 이미지가 생성되었다.  

## Docker Compose 파일
docker-compose 파일을 작성한다.  

```yml
version: '3.2'

services:
  zeek:
    image: broplatform/bro:4.2.0
    container_name: zeek
    restart: always
    cap_add:
      - net_raw
      - net_admin
    network_mode: host
    volumes:
      - /etc/localtime:/etc/localtime
      - ./logs:/usr/local/zeek-4.2.0/logs
      - ./current:/usr/local/zeek-4.2.0/spool/zeek
      - ./node.cfg:/usr/local/zeek-4.2.0/etc/node.cfg
      - ./local.zeek:/usr/local/zeek-4.2.0/share/zeek/site/local.zeek
```

디렉토리를 생성한다.

```sh
sudo mkdir ./logs
sudo mkdir ./current
```

설정 파일을 생성한다.  
인터페이스에 적절한 인터페이스명을 작성한다.

```ini
[zeek]
type=standalone
host=localhost
interface=eth0
```

local.zeek 파일을 작성한다.  
이 파일은 zeek 실행 시킨 후 /usr/local/zeek-4.2.0/share/zeek/site/local.zeek 파일 맨 마지막에 `@load policy/tuning/json-logs.zeek`만 추가해도 된다.  

```ini
##! Local site policy. Customize as appropriate.
##!
##! This file will not be overwritten when upgrading or reinstalling!

# Installation-wide salt value that is used in some digest hashes, e.g., for
# the creation of file IDs. Please change this to a hard to guess value.
redef digest_salt = "asldkjdflkdlkjkdfsjkdjfk";

# This script logs which scripts were loaded during each run.
@load misc/loaded-scripts

# Apply the default tuning scripts for common tuning settings.
@load tuning/defaults

# Estimate and log capture loss.
@load misc/capture-loss

# Enable logging of memory, packet and lag statistics.
@load misc/stats

# Load the scan detection script.  It's disabled by default because
# it often causes performance issues.
#@load misc/scan

# Detect traceroute being run on the network. This could possibly cause
# performance trouble when there are a lot of traceroutes on your network.
# Enable cautiously.
#@load misc/detect-traceroute

# Generate notices when vulnerable versions of software are discovered.
# The default is to only monitor software found in the address space defined
# as "local".  Refer to the software framework's documentation for more
# information.
@load frameworks/software/vulnerable

# Detect software changing (e.g. attacker installing hacked SSHD).
@load frameworks/software/version-changes

# This adds signatures to detect cleartext forward and reverse windows shells.
@load-sigs frameworks/signatures/detect-windows-shells

# Load all of the scripts that detect software in various protocols.
@load protocols/ftp/software
@load protocols/smtp/software
@load protocols/ssh/software
@load protocols/http/software
# The detect-webapps script could possibly cause performance trouble when
# running on live traffic.  Enable it cautiously.
#@load protocols/http/detect-webapps

# This script detects DNS results pointing toward your Site::local_nets
# where the name is not part of your local DNS zone and is being hosted
# externally.  Requires that the Site::local_zones variable is defined.
@load protocols/dns/detect-external-names

# Script to detect various activity in FTP sessions.
@load protocols/ftp/detect

# Scripts that do asset tracking.
@load protocols/conn/known-hosts
@load protocols/conn/known-services
@load protocols/ssl/known-certs

# This script enables SSL/TLS certificate validation.
@load protocols/ssl/validate-certs

# This script prevents the logging of SSL CA certificates in x509.log
@load protocols/ssl/log-hostcerts-only

# If you have GeoIP support built in, do some geographic detections and
# logging for SSH traffic.
@load protocols/ssh/geo-data
# Detect hosts doing SSH bruteforce attacks.
@load protocols/ssh/detect-bruteforcing
# Detect logins using "interesting" hostnames.
@load protocols/ssh/interesting-hostnames

# Detect SQL injection attacks.
@load protocols/http/detect-sqli

#### Network File Handling ####

# Enable MD5 and SHA1 hashing for all files.
@load frameworks/files/hash-all-files

# Detect SHA1 sums in Team Cymru's Malware Hash Registry.
@load frameworks/files/detect-MHR

# Extend email alerting to include hostnames
@load policy/frameworks/notice/extend-email/hostnames

# Uncomment the following line to enable detection of the heartbleed attack. Enabling
# this might impact performance a bit.
@load policy/protocols/ssl/heartbleed

# Uncomment the following line to enable logging of connection VLANs. Enabling
# this adds two VLAN fields to the conn.log file.
# @load policy/protocols/conn/vlan-logging

# Uncomment the following line to enable logging of link-layer addresses. Enabling
# this adds the link-layer address for each connection endpoint to the conn.log file.
# @load policy/protocols/conn/mac-logging

# Uncomment this to source zkg's package state
# @load packages

# Output to JSON
@load policy/tuning/json-logs.zeek
```

이제 실행한다.
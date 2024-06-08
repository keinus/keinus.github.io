---
layout: default
title: orange pi 5 filebeat zeek
nav_order: 1
parent: OrangePI5
---
                

# Run Filebeat on Docker for zeek
파일 비트를 도커로 실행시키고 zeek 로그를 es로 전송하도록 한다.

## Zeek module Setup
일단 docker 이미지를 받는다.

```sh
sudo docker pull docker.elastic.co/beats/filebeat:8.6.1
```

filebeat.docker.yml 파일을 작성한다.  

```yaml
# filebeat modules
filebeat.modules:
- module: zeek
  capture_loss:
    enabled: true
    var.paths: ["/current/capture_loss.log"]
  connection:
    enabled: true
    var.paths: ["/current/conn.log"]
  dce_rpc:
    enabled: true
    var.paths: ["/current/dce_rpc.log"]
  dhcp:
    enabled: true
    var.paths: ["/current/dhcp.log"]
  dnp3:
    enabled: true
    var.paths: ["/current/dnp3.log"]
  dns:
    enabled: true
    var.paths: ["/current/dns.log"]
  dpd:
    enabled: true
    var.paths: ["/current/dpd.log"]
  files:
    enabled: true
    var.paths: ["/current/files.log"]
  ftp:
    enabled: true
    var.paths: ["/current/ftp.log"]
  http:
    enabled: true
    var.paths: ["/current/http.log"]
  intel:
    enabled: true
    var.paths: ["/current/intel.log"]
  irc:
    enabled: true
    var.paths: ["/current/irc.log"]
  kerberos:
    enabled: true
    var.paths: ["/current/kerberos.log"]
  modbus:
    enabled: true
    var.paths: ["/current/modbus.log"]
  mysql:
    enabled: true
    var.paths: ["/current/mysql.log"]
  notice:
    enabled: true
    var.paths: ["/current/notice.log"]
  ntlm:
    enabled: true
    var.paths: ["/current/ntlm.log"]
  ntp:
    enabled: true
    var.paths: ["/current/ntp.log"]
  ocsp:
    enabled: true
    var.paths: ["/current/oscp.log"]
  pe:
    enabled: true
    var.paths: ["/current/pe.log"]
  radius:
    enabled: true
    var.paths: ["/current/radius.log"]
  rdp:
    enabled: true
    var.paths: ["/current/rdp.log"]
  rfb:
    enabled: true
    var.paths: ["/current/rfb.log"]
  signature:
    enabled: false
    var.paths: ["/current/signature.log"]
  sip:
    enabled: true
    var.paths: ["/current/sip.log"]
  smb_cmd:
    enabled: true
    var.paths: ["/current/smb_cmd.log"]
  smb_files:
    enabled: true
    var.paths: ["/current/smb_files.log"]
  smb_mapping:
    enabled: true
    var.paths: ["/current/smb_mapping.log"]
  smtp:
    enabled: true
    var.paths: ["/current/smtp.log"]
  snmp:
    enabled: true
    var.paths: ["/current/snmp.log"]
  socks:
    enabled: true
    var.paths: ["/current/socks.log"]
  ssh:
    enabled: true
    var.paths: ["/current/ssh.log"]
  ssl:
    enabled: true
    var.paths: ["/current/ssl.log"]
  stats:
    enabled: true
    var.paths: ["/current/stats.log"]
  syslog:
    enabled: true
    var.paths: ["/current/syslog.log"]
  traceroute:
    enabled: true
    var.paths: ["/current/traceroute.log"]
  tunnel:
    enabled: true
    var.paths: ["/current/tunnel.log"]
  weird:
    enabled: true
    var.paths: ["/current/weird.log"]
  x509:
    enabled: true
    var.paths: ["/current/x509.log"]


setup.kibana:
  host: "kibana:5601"
  username: "elastic"
  password: "rlaqudwls1"
  ssl:
    enabled: true
    key: "/certs/es01/es01.key"
    certificate_authorities: ["/certs/ca/ca.crt"]
    certificate: "/certs/es01/e01.crt"

output.elasticsearch:
  hosts: ['es01:9200']
  username: 'elastic'
  password: 'rlaqudwls1'
  protocol: "https"
  ssl:
    enabled: true
    key: /certs/es01/es01.key
    certificate: /certs/es01/es01.crt
    certificate_authorities: /certs/ca/ca.crt

# ================================= Processors =================================
processors:
  - add_host_metadata:
      when.not.contains.tags: forwarded
  - add_cloud_metadata: ~
  - add_docker_metadata: ~
  - add_kubernetes_metadata: ~
```

docker-compose.yml 파일에 추가한다.

```yaml
  filebeat:
    image: docker.elastic.co/beats/filebeat:8.6.1
    container_name: filebeat
    restart: always
    volumes:
      - /etc/localtime:/etc/localtime
      - ./zeek/current:/current
      - ./filebeat.docker.yml:/usr/share/filebeat/filebeat.yml:ro
      - certs:/certs
```
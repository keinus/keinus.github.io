---
layout: default
title: WSL2 Bridge 설정
nav_order: 1
parent: ETC
---
                

## WSL2 Bridge 설정(Win11, WSL 0.66.2.0)
### 패키지 설치
WSL 내에서,  
  
`sudo apt install net-tools`
  
### WSL 닫기
관리자모드의 Windows Powershell에서,  
  
`wsl --shutdown`

### WSL 설정파일 추가

윈도우의 홈디렉토리에 아래 내용으로 `.wslconfig` 파일 추가

```
[network]
generateResolvConf = false

[wsl2]
networkingMode=bridged
vmSwitch=External Bridge
```
  
### WSL에 네트워크 설정(매 재부팅마다)
```
wsl -d Ubuntu-20.04 -u root ip addr add 192.168.200.55/24 broadcast 192.168.200.255 dev eth0
wsl -d Ubuntu-20.04 -u root route add default gw 192.168.200.1 dev eth0 
wsl -d Ubuntu-20.04 -u root "echo nameserver 8.8.8.8\r\n nameserver 1.1.1.1 > /etc/resolv.conf"
```
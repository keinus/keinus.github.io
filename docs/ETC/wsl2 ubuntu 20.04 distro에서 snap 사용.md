---
layout: default
title: wsl2 ubuntu 20.04 distro에서 snap 사용
nav_order: 1
parent: ETC
---
                

### 문제점
wsl2의 ubuntu 20.04에서 snap을 사용하면 아래와 같은 에러가 나옵니다.

```
error: cannot communicate with server: Post http://localhost/v2/snaps/microk8s: dial unix /run/snapd.socket: connect: no such file or directory
```

그래서 snap daemon을 실행하려하면 아래의 에러가 나옵니다.

```
System has not been booted with systemd as init system (PID 1). Can't operate.
Failed to connect to bus: Host is down
```

### 해결법
```sh
sudo apt-get update && sudo apt-get install -yqq daemonize dbus-user-session fontconfig
sudo daemonize /usr/bin/unshare --fork --pid --mount-proc /lib/systemd/systemd --system-unit=basic.target
exec sudo nsenter -t $(pidof systemd) -a su - $LOGNAME
```

### .bashrc에 추가
```sh
sudo echo "sudo daemonize /usr/bin/unshare --fork --pid --mount-proc /lib/systemd/systemd --system-unit=basic.target
exec sudo nsenter -t $(pidof systemd) -a su - $LOGNAME" >> ~/.bashrc
```


Done!

---
layout: default
title: wsl2 ubuntu 20.04 distro에서 microk8s 설치 및 실행
nav_order: 1
parent: ETC
---
                

### 준비

이전 글을 참고하여 wsl2에서 snap을 실행합니다.

### 설치
https://microk8s.io/docs/getting-started


```
sudo snap install microk8s --classic --channel=1.21/stable
```

설치 완료.

### 설정
```
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
su - $USER
```

### util 설정
kubectl만 쳐도 되도록 bashrc에 추가

```
echo "alias kubectl='microk8s kubectl'" >> ~/.bashrc
```

### 확인

```
microk8s status --wait-ready
```

![16963-2022-3-11-20-26.png](/files/16963-2022-3-11-20-26.png) 
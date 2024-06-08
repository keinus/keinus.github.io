---
layout: default
title: Centos7에 openstack을 devstack으로 설치 시 안될 경우
nav_order: 1
parent: ETC
---
                

OS 체크에서 에러나는 경우에는 openrc 파일에 아래와 같이 추가해준다.

```
export os_VENDOR=CentOS
```
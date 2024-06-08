---
layout: default
title: opnfv 설치
nav_order: 1
parent: ETC
---
                

https://makerj.tistory.com/291
https://opnfv-compass4nfv.readthedocs.io/en/stable-gambia/release/installation/preconditions.html

두 페이지를 참조했습니다.

가상 머신 상에서 설치하는 것을 기본으로 합니다.

일단 가상머신(32thread, 64G ram, 1T 디스크, 2 nic)에 ubuntu 14.04를 설치합니다.

설치 후 root 계정 password를 설정합니다.

`sudo passwd root`

root로 계정을 전환한 후 아래 명령어로 관련 패키지를 설치한다.

```
apt install libvirt-bin qemu qemu-kvm virt-manager git
```

http://artifacts.opnfv.org/compass4nfv.html

위 사이트에 들어가 opnfv 파일을 다운로드 받는다.

properties 파일도 같이 받는다.

`git clone https://gerrit.opnfv.org/gerrit/compass4nfv`

위 명령어로 compass4nfv 파일을 받는다.

properties 파일에서 OPNFV_GIT_SHA1을 찾아 해당 스트링을 복사하여 아래 처럼 체크아웃한다.

`git checkout 5838841f09950160f907e15fc14282449f6652af`

설정을 위해 아래 파일을 연다.

compass4nfv/deploy/conf/network_cfg.yaml

적절히 설정.

위에서 다운로드 받은 tar.gz 파일 압축 풀어서 compath4nfv/deploy/install에 복사한다.

deploy.sh를 실행한다.

이런거 다 때려치고 아래 명령어로 하는게 젤 편하다.

curl https://raw.githubusercontent.com/opnfv/compass4nfv/stable/gambia/quickstart.sh | bash




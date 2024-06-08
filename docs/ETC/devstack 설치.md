https://naleejang.tistory.com/ 블로그 글 참조


stack 계정 추가 후 stack 계정으로 전환

```
sudo useradd -U -G sudo -s /bin/bash -m stack
sudo chmod u+w /etc/sudoers
sudo echo "stack ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
sudo chmod u-w /etc/sudoers
sudo passwd stack
su stack
cd ~
```

sw 설치

```
yum install git
yum install python-devel
yum install python36-devel
yum install gcc
```

```
sudo apt install git
sudo apt install python-dev
sudo apt install python36-dev
sudo apt install gcc
```


devstack 다운로드

```
git clone https://git.openstack.org/openstack-dev/devstack
cd devstack
```

설정

```
vi local.conf


[[local|localrc]]
HOST_IP=192.168.56.101
FLOATING_RANGE=192.168.0.224/27
FIXED_RANGE=10.11.12.0/24
FIXED_NETWORK_SIZE=256
FLAT_INTERFACE=eno3
ADMIN_PASSWORD=secret
DATABASE_PASSWORD=secret
RABBIT_PASSWORD=secret
SERVICE_PASSWORD=secret
```

추가 설정

```
openrc에 아래 줄 추가

export os_VENDOR=CentOS
```

설치
```
./stack.sh
```


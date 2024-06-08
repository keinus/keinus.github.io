---
layout: default
title: CentOS에서 sudo 명령어 사용하기
nav_order: 1
parent: ETC
---
                

CentOS에서 일반 유저는 권한을 받아야 한다.

```
1. root로 사용자 전환 (su -)
2. /etc/sudoers의 파일 permission 변경
   # chmod u+w /etc/sudoers
3. /etc/sudoers에 일반 사용자 등록
   # vi /etc/sudoers 후

   가장 아랫 줄에 다음 문장을 추가하고 저장한다.
   userid      ALL=(ALL)    ALL 입력
   (userid에게 sudo 권한을 부여한다)
   
   %group    ALL=(ALL)    NOPASSWD: ALL
   (그룹에 sudo 권한을 주고 Passwd입력을 받지 않고 싶을 경우)

4. /etc/sudoers 퍼미션 원복
   /etc/sudoers는 440 퍼미션이어야 함
    # chmod u-w /etc/sudoers
```
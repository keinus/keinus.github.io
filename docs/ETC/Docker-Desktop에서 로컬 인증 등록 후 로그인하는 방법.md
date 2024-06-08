---
layout: default
title: Docker-Desktop에서 로컬 인증 등록 후 로그인하는 방법
nav_order: 1
parent: ETC
---
                

.crt 파일을 오른쪽 클릭 후 "인증서 설치"를 누른다.
 - 로컬 컴퓨터 -> 모든 인증서를 다음 저장소에 저장 -> 신뢰할 수 있는 루트 인증 기관 -> 설치

로그인 시 https를 빼고 <IP>:<PORT>로 로그인 한다.
 - docker login -u <user> -p <pw> <ip>:<443 or ssl port>

사용
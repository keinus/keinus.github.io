### apt 리포지토리 설정 열기

```sh
sudo vi /etc/apt/sources.list
```

### replace로 변경
```vim
:%s/kr.archive.ubuntu.com/mirror.kakao.com
```

단, 배포판에 따라 "kr."이 안 붙어 있을 수 있음.

### 명령어로
```bash
sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
```
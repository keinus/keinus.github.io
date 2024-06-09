---
layout: default
title: wsl2 chrome 설치
nav_order: 1
parent: WSL2
---
                

### 다운로드
```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```

### 설치
```
sudo apt install ./google-chrome-stable_current_amd64.deb
```

### 폰트 설치
```
sudo apt-get install language-pack-ko
```

### locale 설치
```
sudo locale-gen ko_KR.UTF-8
```

### 폰트 다운로드 및 설치
```
wget http://cdn.naver.com/naver/NanumFont/fontfiles/NanumFont_TTF_ALL.zip
unzip NanumFont_TTF_ALL.zip -d NanumFont
rm -f NanumFont_TTF_ALL.zip
sudo mv ./NanumFont/* /usr/share/fonts/
fc-cache -r
```


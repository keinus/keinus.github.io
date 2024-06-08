https://rottk.tistory.com/entry/Self-signed-certificate-%EB%A5%BC-%EC%8B%A0%EB%A2%B0%ED%95%A0-%EC%88%98-%EC%9E%88%EB%8A%94-%EC%9D%B8%EC%A6%9D%EC%84%9C%EB%A1%9C-%EC%B6%94%EA%B0%80%ED%95%98%EA%B8%B0

주로 사내망에서 ssl proxy를 써서 내부 사원의 id/pw를 빼내가고 있는 경우 https 사이트에서 인증 실패로 에러 메시지가 나온다.

일단 회사에서 제공하는 ca 인증서도 제대로 제공하는 경우가 별로 없기 때문에(지들도 시스템이 어떻게 돌아가는지 모른다.) 아래와 같은 방법으로 ca 인증서를 가져온다.

```sh
echo quit | openssl s_client -showcerts -servername www.naver.com -connect www.naver.com:443 > cacert.pem
```

파일 하단의 ca 인증서만 남기고 나머지는 지운다.  
두번째 BEGIN CERTIFICATE 부분만 남기면 된다.

```
-----BEGIN CERTIFICATE----- 
111111111111111111111111
-----END CERTIFICATE-----

여기서부터
-----BEGIN CERTIFICATE-----
111111111111111111111111
-----END CERTIFICATE----- 
여기까지만 남기고 다 지운다.

--- Server certificate 

```

아래 스크립트를 써도 된다.

```
echo quit | \ openssl s_client -showcerts -servername <서버주소> -connect <서버주소:포트> < /dev/null | \ awk '/-----BEGIN CERTIFICATE-----/,/-----END CERTIFICATE-----/ \ { \ if(/-----BEGIN CERTIFICATE-----/) \ {a++}; \ out="cert"a".pem"; \ print >out \ }'
```

위 파일(cacert.pem)을 복사하고 적용한다.

```
sudo cp cacert.pem /usr/loca/share/ca-certificates/cacert.crt
sudo update-ca-certificates
```

제대로 되는지 확인한다.

```
curl https://naver.com
```

에러가 안나면 적용이 제대로 된거다.
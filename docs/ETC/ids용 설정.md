---
layout: default
title: ids용 설정
nav_order: 1
parent: ETC
---
                

NIC 들은 일반적으로 상위계층으로 전송시 해당MAC 주소와 broadcast MAC 주소를 제외한 다른 주소를 목적지로 가진 프레임은 폐기한다.

 

다른 호스트간의 통신도 모니터링 할려면 이것을 해제한다.

```
# ifconfig eth0 promisc
```


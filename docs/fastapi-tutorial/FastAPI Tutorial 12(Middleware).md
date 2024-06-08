## Middleware

FastAPI 어플리케이션에서 Middleware를 작성할 수 있다.  
Spring으로 치면 filter 역할을 하는 코드다.  
제공하는 기능은 아래와 같다.  

- 매 request 마다 실행
- 매 response 마다 실행

### 구현
아래와 같이 구현한다.

```py
import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

위 코드는 매 request마다 실행하는 코드를 구현한 것이다.  
request 객체는 함수의 전달인자로 전달되며, 실제 해당 request를 실행하도록 하는 call_next 함수도 전달된다.
response 객체는 call_next를 호출하여 얻는다.
위 예제는 모든 request 컨트롤러에 대해 컨트롤러의 처리 시간을 측정하여 response 헤더에 "X-Process-Time"이란 이름으로 처리 시간을 추가하여 리턴하는 코드다.



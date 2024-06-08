## 들어가기 전
### OpenAPI
OpenAPI Specification(OAS)은 HTTP API를 JSON 또는 YAML을 통해 표준 인터페이스를 정의

### Swagger 
https://swagger.io/
위의 OpenAPI와 관련된 작성, 빌드, 문서화 등을 도와주는 오픈소스 프레임워크(툴)

# FastAPI Specification
## Base
### 기초 코드(Skeloton Code)
```py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```


`from fastapi import FastAPI`
FastAPI를 임포트. FastAPI는 Starlette를 직접 상속하는 클래스이기 때문에 Starlette의 기능을 전부 사용할 수 있음.
기본적으로 Starlette 자체가 flask와 유사하게 작성된 프레임워크

'app = FastAPI()'
어플리케이션의 엔트리포인트이며, 프로세스의 메인 인스턴스. 메인 스레드.
uvicorn 실행 시 인자로 <modulename>:<instance name> 형식으로 실행하게 됨
`uvicorn main:app --reload`
만약 인스턴스 이름을 다르게 지정하면 uvicorn 실행 시 다르게 실행해야함
`my_awesome_api = FastAPI()`
위와 같이 생성할 경우
`uvicorn main:my_awesome_api --reload`
처럼 실행해야 함

경로 라우팅의 경우 아래처럼 app.<METHOD>("<PATH>") 형식을 사용함
`@app.get("/")`
위와 같이 설정할 경우, "GET /" 요청을 처리하는 컨트롤러를 선언하겠다고 정의하는 것임

`async def root():`
위는 그냥 python 함수. 컨트롤러라 함(MVC 패턴). 위 경로 라우팅 설정의 핸들러

`    return {"message": "Hello World"}`
위 코드는 컨트롤러 처리 후 컨텐츠 리턴코드. 리턴한 컨텐츠는 response body에 붙어서 호출한 브라우저나 agent에 전달됨



# Handling Errors
서비스에서 발생하는 에러나 request, response 시에 발생하는 에러 등을 처리할 수 있다.

## HTTPException
에러 리턴 시 HTTPException을 사용한다.

```
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

HTTPException 발생 시 함수는 종료되고 HTTP 에러를 클라이언트에 리턴한다.
에러를 직접 리턴하는 것보다 HTTPException을 발생 시키는 것이 관리 측면 등에서 더 유리하다.
위 코드 같은 경우 예외를 발생 시키면 404 에러와 바디에 Item not found를 붙여서 리턴한다.

### Custom Header
HTTPException의 헤더 값을 변경하고 싶을 경우 아래와 같이 headers를 사용한다.

```
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}
```

### Custom error handler
에러 핸들러를 별도로 구현하여 사용하고 싶은 경우 아래와 같이 예외 클래스 선언, 해당 예외의 핸들러 선언, 코드에서 예외 발생을 통해 사용할 수 있다.

```
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


app = FastAPI()


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}

```

### 기본 예외 핸들러 교체
기본으로 사용되는 예외 핸들러를 변경할 수 있다.
아래의 예시는 RequestValidationError 핸들러를 내가 구현한 코드로 변경하는 예시코드이다.
HTTPException을 바꿀 경우, 아래와 같이 StarletteHTTPExcepton을 바꿔야 한다.
전달인자의 request는 Request 객체(request header/body)이고 exc는 기본 Error handler의 response 객체이다.


```
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}

```

### 단순 필터로 사용할 경우
기본 에러 핸들러를 사용하고, 중간 필터로 에러 로깅만 할 경우 아래와 같이 사용한다.
핸들러 override는 동일하고, 원본 함수를 import해서 호출한다.

```
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}
```

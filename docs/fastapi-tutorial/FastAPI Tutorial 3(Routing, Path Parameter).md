---
layout: default
title: FastAPI Tutorial 3(Routing, Path Parameter)
nav_order: 3
parent: fastapi-tutorial
---
                

# Routing
기본적으로 python 문법과 starlette의 기본 기능을 따라간다.
또한, starlette 자체가 flask와 거의 비슷하게 구현했기 때문에 flask와 동작도 거의 동일하다고 생각하면 된다.

## HTTP request method
각 메서드별 동작은 rfc7231 section-4를 참조(https://datatracker.ietf.org/doc/html/rfc7231#section-4)

### 지원 메서드
@app.get()
@app.post()
@app.put()
@app.delete()
@app.options()
@app.head()
@app.patch()
@app.trace()


# Path Parameter
### 경로 매개변수
python의 string format을 사용하여 url path에 매개변수 또는 변수를 선언할 수 있음

```
@app.get("/items/{item_id}")
async def read_item(item_id: int):
```

URL의 "{}" 내에 선언한 변수명을 함수 argument로 선언하면 해당 argument로 변수가 할당됨.
타입 힌팅을 같이 사용하면 변수를 자동으로 형변환하여 할당함

`@app.get("/users/{user_id}/items/{item_id}")`
와 같이 경로 중간에 변수를 넣어도 된다.

함수 선언 시 파라미터의 순서는 중요하지 않다. 알아서 값을 할당한다. 다만, 가독성을 위해 가급적 순서대로 작성할 것을 권한다.

### Data Validation
FastAPI는 path parameter의 data validation을 Pydantic으로 수행한다.
위 경로 매개변수에 int 형으로 타입을 지정했는데 불구하고, int 형으로 변환되는 값이 아닌 다른 값을 입력할 경우 예외 핸들러가 실행되고 예외 객체가 리턴된다.

```
REQ : GET http://127.0.0.1:8000/items/foo
RESPONSE:
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

### 순서 문제
만약, "/usr/admin"이라는 고정 경로 라우팅과 "/usr/{user_id}"이라는 string을 path parameter로 갖는 경로 라우팅이 있을 경우, 먼저 선언한 쪽이 우선 실행된다.

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```

위와 같이 구현했을 경우, "/users/me"를 요청하면 read_user_me() 함수가 실행되지만

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}
```

위와 같이 구현했을 경우, "/users/me"를 요청하면 read_user(user_id: str) 함수가 실행된다.

### Enum 사용
아래 코드와 같은 형태로 Enum을 path parameter의 타입으로 사용할 수 있다.
값의 종류가 str이고, Enum을 사용할 경우 아래 코드와 같이 class ModelName(str, Enum) 둘을 상속 받는 클래스를 선언하고 enum 처럼 사용하면 된다.
str <-> Enum 간 형변환이 자동으로 이루어지기 때문에 리턴 시 Enum 형일 경우 자동으로 str로 리턴된다.

```
from enum import Enum

from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
```

### 경로 타입(str) path parameter
일단, 이건 작성은 하지만 쓰지 말길 권고한다. OpenAPI 표준에도 없으며, 의도하지 않은 동작을 할 가능성이 크다.
아래와 같은 값을 받고 싶으면 POST를 쓰도록 하자.

개발자에 따라서는 URL을 통한 parameter로 path 경로를 받고 싶어하는 경우도 있다.
예를 들어, "images/{file_path}" 로 API를 구현하고 {file_path}의 값으로 "/home/admin/file.txt" 와 같은 특정 파일 위치를 parameter로 받고 싶어하는 경우가 있다.
이 경우 agent에서는 "images/home/admin/file.txt"과 같이 호출되기 때문에 FastAPI의 라우터는 일단 "images/home/admin" 경로를 먼저 찾고 해당 경로의 핸들러가 없으니 404를 리턴할 것이다.

```
from fastapi import FastAPI

app = FastAPI()

@app.get("images/{file_path}")
async def read_user(file_path: str):
    return {"files": file_path}
```
![3271-2022-4-1-21-24.png](../images/3271-2022-4-1-21-24.png) 


path를 받기 위해 

> images/{file_path:path}

와 같이 선언할 수 있다.

아래 코드처럼 구현하면 된다.

```
from fastapi import FastAPI

app = FastAPI()

@app.get("images/{file_path:path}")
async def read_user(file_path:str):
    return {"files": file_path}
```
![25598-2022-4-1-21-26.png](../images/25598-2022-4-1-21-26.png)

200 OK로 정상적으로 리턴됨을 알 수 있다. 

## Path 클래스
Path 함수를 통해 Path 클래스를 사용하여 path parameter에 대한 제약 사항을 설정할 수 있는 방법도 제공한다.
Path 클래스(params.Path)를 사용해보자.

```
from typing import Optional

from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get")
):
    return {"item_id": item_id}
```

위처럼 Path 함수를 import하고 호출하면 Path 객체가 리턴된다.
Path 함수로 설정할 수 있는 값은 코드 뒤져보면 나온다.

```
    default: Any,
    *,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    regex: Optional[str] = None,
    example: Any = Undefined,
    examples: Optional[Dict[str, Any]] = None,
    deprecated: Optional[bool] = None,
    include_in_schema: bool = True,
    **extra: Any,
```

### 값에 대한 제약
gt, ge, lt, le는 float 기반으로 값에 대한 제약을 설정한다.

- gt: 크거나(greater than)
- ge: 크거나 같은(greater than or equal)
- lt: 작거나(less than)
- le: 작거나 같은(less than or equal)

### 길이 제약
Path 길이를 제약할 수 있다.
어차피 http의 URL은 스펙에는 제약이 없으나 각 webserver 별로 최대 길이가 정해져 있다.(보통 10k 이상 길이를 지원하는 서버는 없고 가끔 1024 byte로 빡빡하게 거는 경우도 있다.)

- max_length : 최대 길이
- min_length : 최소 길이

### 정규식
정규식을 걸 수 있다.
굳이 정규식을 써야하나 싶지만... 뭐 지원한다하니..
C-style string 정규식은 어차피 안될거 같으니 js용 정규식을 사용하면 될거 같다.

https://developer.mozilla.org/ko/docs/Web/JavaScript/Guide/Regular_Expressions

### default
Path에 default를 걸지 말자. 
Path에 default를 걸고 싶다면, 그냥 상위 경로의 함수를 만들어야 한다. 
Path는 특정 객체에 대한 ID를 의미한다.(절대 행위를 path로 쓰지 않아야 한다.) 특정 객체를 지정하는 ID에 디폴트 값은 있을 수 없다.
시간이 남아돈다면 항상 API 작성 후 리팩토링할 때 path에 대해 다시 생각해보고 맞는지 검토해야 한다.


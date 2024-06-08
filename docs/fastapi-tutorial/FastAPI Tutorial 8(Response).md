---
layout: default
title: FastAPI Tutorial 8(Response)
nav_order: 8
parent: fastapi-tutorial
---
                

# Response 
## Response Model
Response body에 들어갈 content를 Model로 지정하여 리턴할 수 있다.
기본적인건 Model과 같으니 위 Model을 우선 참조.
기본적인 response model의 작동 방식은 OpenAPI에 대한 description과 validation이다.

```
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item

```

위와 같이 구현했을 경우 fastapi의 pydantic은 리턴 데이터(item)에 대해 response_model로 선언한 Item 클래스로 "변환"과 함께 "validation"을 수행하고 이후 response body에 JSON 형태로 변환한 Item의 인스턴스를 붙여 리턴한다.
OpenAPI로 documentation 하는건 당연하다.

Output을 위한 별도 모델을 만들 필요는 없다. 모델은 모델이고, 인스턴스는 인스턴스다.

단, 아래와 같은 코드도 가능하다.

```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user
```

코드에서 보다시피 request model(UserIn)에는 password가 있으나 response model(UserOut)에는 없다.
그리고 input으로 들어온 데이터를 그대로 output으로 내보낸다.
Pydantic은 Input의 데이터(키)가 더 많은 것은 에러처리를 하지 않는다. 해당 모델로 선언한 각 attribute가 있으면 해당 attribute로만 데이터를 채워서 인스턴스를 생성한다.

### response_model_exclude_unset
Model은 기본값을 설정할 수 있고 이것은 response model에서도 동일하다.
하지만 가끔 시스템에 따라서 디폴트 밸류나 설정되지 않은 값은 response body에 추가하지 않기를 원하는 시스템도 있다.
이럴 경우 response_model_exclude_unset=True로 설정하면 비어있는 값은 response body의 JSON 모델에서 삭제하여 전송한다.

```
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]
```

### response_model_include and response_model_exclude
모델에 따라서 response 시 무조건 추가되어야할 attribute와 빼야할 attribute가 있을 수 있다.(ex. 위 예시의 password 같은)
옵션 명에서 알 수 있듯 추가/삭제할 attribute를 지정할 수 있다.

```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]
```

### 모델 융합
두개의 모델을 합쳐 리턴할 수 있다.

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]
```

### 리스트 리턴
리스트로 리턴할 수 있다.

```
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str


items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]


@app.get("/items/", response_model=List[Item])
async def read_items():
    return items
```

### 일반 dict 리턴

```
from typing import Dict

from fastapi import FastAPI

app = FastAPI()


@app.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}

```

## Status Code
리턴 코드(HTTP CODE)를 지정할 수 있다.

```
from fastapi import FastAPI

app = FastAPI()


@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}
```

```
from fastapi import FastAPI, status

app = FastAPI()


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
```


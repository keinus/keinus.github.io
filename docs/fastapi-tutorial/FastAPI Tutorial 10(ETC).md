# Extras
## Extra Data Types

UUID: 
A standard "Universally Unique Identifier", common as an ID in many databases and systems. 
In requests and responses will be represented as a str.

datetime.datetime:
A Python datetime.datetime.
In requests and responses will be represented as a str in ISO 8601 format, like: 2008-09-15T15:53:00+05:00.

datetime.date:
Python datetime.date.
In requests and responses will be represented as a str in ISO 8601 format, like: 2008-09-15.

datetime.time:
A Python datetime.time.
In requests and responses will be represented as a str in ISO 8601 format, like: 14:23:55.003.

datetime.timedelta:
A Python datetime.timedelta.
In requests and responses will be represented as a float of total seconds.
Pydantic also allows representing it as a "ISO 8601 time diff encoding", see the docs for more info.

frozenset:
In requests and responses, treated the same as a set:
In requests, a list will be read, eliminating duplicates and converting it to a set.
In responses, the set will be converted to a list.
The generated schema will specify that the set values are unique (using JSON Schema's uniqueItems).

bytes:
Standard Python bytes.
In requests and responses will be treated as str.
The generated schema will specify that it's a str with binary "format".

Decimal:
Standard Python Decimal.
In requests and responses, handled the same as a float.


## Cookie
쿠키 함수 선언해서 쿠키 값을 가져올 수 있다.


```
from typing import Optional

from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}
```

## Header
헤더 선언으로 request header 값을 가져올 수 있다.
argument 명에 해당하는 request header 값을 가져와 할당한다.

```
from typing import Optional, Dict

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(
    user_agent: Optional[str] = Header(None)
    , accept: Optional[str] = Header(None)
    ):
    return {"User-Agent": user_agent, 
            "accept":accept}
```

## Tags
OpenAPI 각 함수별 Tag(그룹핑)를 달 수 있다.

```
from typing import Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()


@app.post("/items/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item


@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]
```

### Tags with Enums
Enum으로 달 수 있다.

```
from enum import Enum

from fastapi import FastAPI

app = FastAPI()


class Tags(Enum):
    items = "items"
    users = "users"


@app.get("/items/", tags=[Tags.items])
async def get_items():
    return ["Portal gun", "Plumbus"]


@app.get("/users/", tags=[Tags.users])
async def read_users():
    return ["Rick", "Morty"]
```

## 설명
OpenAPI에 설명을 코드 레벨로 달 수 있다.

```
from typing import Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()


@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item
```

## 주석
주석 달면 해당 내용이 OpenAPI에 추가된다. Markdown 스타일이 적용되니 markdown 식으로 작성해도 된다.
가급적 pep 표준이나 google style로 달도록 하자. 
response_description으로 response 객체에 대한 설명도 넣을 수 있다.

```
from typing import Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()


@app.post("/items/", response_model=Item, summary="Create an item",
                     response_description="The created item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

```
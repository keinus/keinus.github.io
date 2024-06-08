# Model
모델 작성하는 방법을 알아보자.
</br>

## 기본 문법
기본적으로 모델은 아래처럼 작성한다.
모든 모델은 pydantic에 의해 자동으로 JSON<->Object로 변환되므로 body, content 등 argument로 사용할 수 있다.

```
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
```

만약 각 속성 별 제약사항을 걸거나 OpenAPI에 자세한 설명 등을 기록하고 싶은 경우 Field를 사용한다.

### Field
Field는 모델의 각 속성에 여러 제약사항과 설명 등을 적용할 수 있도록하는 함수다. 

```
from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None
```

위처럼 모델을 작성하여 각 속성 별 상세 설명이나 최대 길이 등을 설정할 수 있다.
필드에 설정할 수 있는 항목은 아래와 같다.

```
    default: Any = Undefined,
    *,
    default_factory: Optional[NoArgAnyCallable] = None,
    alias: str = None,
    title: str = None,
    description: str = None,
    exclude: Union['AbstractSetIntStr', 'MappingIntStrAny', Any] = None,
    include: Union['AbstractSetIntStr', 'MappingIntStrAny', Any] = None,
    const: bool = None,
    gt: float = None,
    ge: float = None,
    lt: float = None,
    le: float = None,
    multiple_of: float = None,
    max_digits: int = None,
    decimal_places: int = None,
    min_items: int = None,
    max_items: int = None,
    unique_items: bool = None,
    min_length: int = None,
    max_length: int = None,
    allow_mutation: bool = True,
    regex: str = None,
    discriminator: str = None,
    repr: bool = True,
    **extra: Any,
```

### List fields

리스트로 선언하고 생성하면 리스트를 사용할 수 있다. 
리스트에 타입 선언까지 하면 해당 타입의 리스트로 생성된다.
set 타입도 지정할 수 있다. set() 함수를 사용한다.

```
from typing import List, Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: list = []
    str_tags: List[str] = []
    set_tags: Set[str] = set()


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

### Submodel
내부 서브 모델을 선언할 수 있다.
아래와 같이 Image 모델을 생성하고 Item 모델의 attribute로 Image를 선언하면 된다.
모든 모델은 타입으로 취급되므로 Item 리스트를 선언하면 List->Item->Image 순으로 데이터가 구축된다.

```
from typing import Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []
    image: Optional[Image] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```


### URL 타입
타입 중 HttpUrl 타입이 있다. 해당 타입은 http url인지 유효성 체크를 위해 사용되고 marshal/unmarshal을 통해 str으로 취급된다.

```
from typing import Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()
    url: HttpUrl


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

### Dict 타입 request body
사용에 따라서 객체로 변환하지 않고 key-value 타입으로 가져와 사용해야할 경우가 있다.
이 경우 body를 Dict로 선언한다.

```
from typing import Dict

from fastapi import FastAPI

app = FastAPI()


@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights
```


## ETC
### schema_extra
OpenAPI 문서에 예시를 작성할 수 있다. 
내부에 Config 클래스를 선언하고 attribute로 schema_extra를 선언하며 key로 "example"을 value로 클래스의 각 attribute의 예시값을 작성하면 된다.
아래와 같은 문법을 사용한다.

```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }
```

### 예시 값
위 schema_extra보다 차라리 각 attribute를 Field로 선언하고 Field에 example을 할당하는게 나아보인다.

```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str = Field(..., example="Foo")
    description: Optional[str] = Field(None, example="A very nice Item")
    price: float = Field(..., example=35.4)
    tax: Optional[float] = Field(None, example=3.2)


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

### request body에 선언
위의 예시는 객체 자체에 할당되지만 만약 함수별로 예시값이 달라져야할 경우 함수의 argument에 예시를 줄 수 있다.

```
from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        ...,
        example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
```

위의 경우 하나만 선언되었는데 하나의 함수에서 경우의 수에 따라 각자 다른 예시 값을 지정해줄 수 있다.

```
from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        ...,
        example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results

@app.post("/items/{item_id}")
async def post_item(
    item_id: int,
    item: Item = Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
```

## Extra Model
여러 모델 사용 시 아래와 같은 용법이 있다.

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


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Optional[str] = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
```

### 중복 attribute 회피
같은 attribute가 많으면 아래와 같이 중복 코드를 줄일 수 있다.

```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

```

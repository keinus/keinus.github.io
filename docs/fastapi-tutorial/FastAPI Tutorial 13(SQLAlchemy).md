## SQLAlchemy
python의 RDB를 위한 ORM 라이브러리(프레임워크?)  
데이터베이스의 종류에 관계없이 코드 레벨의 호환성을 제공할 수 있다.(DB에 대한 접속 설정, 어댑터만 작성된다면 실제 로직 코드는 건드리지 않아도 된다.)  
또한, 로직 개발자의 경우 ORM에 통달할 경우 SQL을 몰라도 소프트웨어 구현이 가능하다.

### ORM
Object-Relational Mapping의 약자.  
인스턴스의 객체와 RDB 테이블간의 매핑 테이블을 만들어서 인스턴스의 객체가 수정되면 자동으로 RDB 테이블의 row도 수정되도록 구현하자는 프레임워크. 객체 수정 후 commit할 시 persistent에 적용된다라고들 표현한다.  
ORM에 따라 툴, 프레임워크, 라이브러리 등의 명칭으로 사용된다.
ORM은 그 구현 방법에 따라 다르게 작동되며 쿼리 최적화나 매핑 방식에 따라 처리 속도가 천차만별이니 SQL 쿼리도 잘 알아야하고 ORM의 규칙도 잘 알아야한다.
기본적으로 sprint-boot-jpa를 적당히 안다고 가정하고 아래 tutorial을 작성한다. 

### 파일 구조
```
.
└── sql_app
    ├── __init__.py
    ├── crud.py
    ├── database.py
    ├── main.py
    ├── models.py
    └── schemas.py

```

### import SQLAlchemy

database.py 파일을 작성해보자.  
아래와 같이 SQLAlchemy로 데이터베이스에 연결할 수 있다.  
SQLALCHEMY_DATABASE_URL이 어떤 데이터베이스에 연결할지를 설정하는 URL이고, 이것은 타 ORM이나 데이터베이스 커넥터와 동일한 문법을 사용한다.  
본 예제에서는 sqlite를 사용한다.   
create_engine() 함수로 엔진 객체를 생성한다. connect_args는 각 RDB에 따라 연결을 위한 옵션을 설정한다.  
sessionmaker() 함수로 세션 객체를 생성한다.  
declarative_base() 함수로 베이스 클래스를 생성한다. 이후, ORM 모델 작성 시 이 베이스 클래스를 상속 받는다.

```py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

### Create the database models

모델 파일을 작성한다.(models.py)  
아래 코드처럼 모델 클래스는 기본적으로 Base 클래스를 상속받아 작성한다.(database.py에서 Base 클래스를 import한다.)
__tablename__는 해당 모델의 테이블명이고 이것은 RDB와 동일하게 작성되어야 한다.(자동으로 테이블을 생성하거나 생성된 테이블과 연결할 때 사용한다.)  
각 컬럼은 Column 함수를 사용한다. Type은 sqlalchemy에서 객체를 제공한다.
- 일반 : Column(<Type>)
- primary 키 : primary_key를 True로 설정한다.
- foreign 키 : ForeignKey() 함수를 사용하며, 전달인자로 "테이블.컬럼"을 설정한다.
- Unique : unique를 True로 설정한다.
- index 설정 : index를 True로 설정한다.
- 조인 : relationship() 함수를 사용한다.

```py
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
```

### Create the relationships
두 테이블(모델)의 관계성 설정을 위해 사용한다.  
위 예시 코드를 예를 들면, User의 특정 인스턴스내에 items 리스트를 가지고 있으며, 만약 특정 유저가 가지고 있는 items 리스트에 접근하면 아래 Item 테이블에서 데이터를 조회하여 제공한다.  
relationship 함수는 두 모델에 대해 상호 연결 관계를 설정하며, 1:N 관계의 경우 N에서 ForeignKey를 통해 1과 연결한다.
테이블의 실제 컬럼과 모델의 실제 컬럼은 다르게 설정된다.
또한, User의 items 접근 시 또는 Item의 owner 접근 시 내부적으로 sql 쿼리를 작성하여 실행하도록 되어 있다.
따라서, 시스템에서 최적화된 형식이 아닐 경우 쿼리가 비효율적으로 작성되어 실행될 수 있으며, 데이터베이스에 따라 실행 시간이 달라질 수 있다.

## Create Pydantic models

entity 모델의 로컬 사용을 위한 object 모델(schemas)를 생성해야 한다.
fastapi에서는 pydantic model을 사용하며, schema로 부른다.
아래 예시와 같이 schemas.py 파일을 구현한다.


```py
from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
```

이제, pydantic 모델을 이용해 sqlalchemy의 entity model 즉, rdb 테이블에 접근할 수 있다.

```py
    class Config:
        orm_mode = True
```

모델 내에 innerclass로 들어가는 Config 클래스는 예약어이고 orm_mode도 예약어이다.  
이렇게 설정할 경우 해당 클래스는 ORM 모델에서 데이터를 읽어올 수 있도록 내부적으로 구성된다.

## CRUD
sqlalchemy의 문법을 그대로 따라한다.


```py
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
```

### Entity 초기화
아래 코드를 FastAPI 인스턴스 생성 전에 실행할 경우 DB에 model 형태로 태이블을 생성한다.

```
models.Base.metadata.create_all(bind=engine)
```


## 예시코드
- sql_app/database.py:
```py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

- sql_app/models.py:
```py
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
```

- sql_app/schemas.py:
```py
from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
```
- sql_app/crud.py:
```py
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
```
- sql_app/main.py:
```py
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
```

위의 예시코드는 FasAPI 공식 문서의 예시코드라서 기본 문법만 설명하는 코드라고 보면 된다.   
익숙해지면 적절히 변형하여 사용하면 된다.

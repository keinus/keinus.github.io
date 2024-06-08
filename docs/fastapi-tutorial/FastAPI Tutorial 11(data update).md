## jsonable_encoder()

jsonable_encoder() 함수를 통해 object가 json 형태로 변환될 수 있는지 확인할 수 있다.  
예를 들어 datetime 형의 경우, 그대로 json 형태로 저장될 수 없기 때문에 str로 변환해야하는데 그러한 작업을 자동으로 해준다.  


```
class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded
```

변환 시 빠진 데이터가 있을 경우 객체의 디폴트 값이 들어간다.
만약, request body가 아래와 같을 경우 입력하지 않은 데이터인 tax, tags는 기본값인 10.5와 []가 들어간다.

```
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

## Using Pydantic's exclude_unset parameter

item.dict(exclude_unset=True)로 설정하여 받아오면 Item 모델에 대해 request body에서 설정하지 않은 데이터는 제외하고(디폴트 value를 사용하지 않고) 나머지 데이터로만 dict를 생성하여 리턴한다.

```
@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item
```


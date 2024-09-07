from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# FastAPI 애플리케이션 객체를 생성합니다.
app = FastAPI()

# 아이템 모델을 정의합니다.
# 'text'는 문자열이며 기본값은 None이고, 'is_done'은 불리언 값으로 기본값은 False입니다.
class Item(BaseModel):
    text: str = None
    is_done: bool = False

# 생성된 아이템들을 저장할 리스트를 초기화합니다.
items = []

# 루트 경로('/')에 대한 GET 요청을 처리하는 엔드포인트를 정의합니다.
# 사용자가 루트 경로에 접근하면 "Hello World" 메시지를 반환합니다.
@app.get("/")
def root():
    return {"message": "Hello World"}

# /items 경로에 POST 요청을 처리하는 엔드포인트를 정의합니다.
# 새로운 아이템을 생성하고 items 리스트에 추가합니다.
# 요청 본문에서 전달된 아이템을 추가한 후 전체 아이템 목록을 반환합니다.
@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items

# /items 경로에 GET 요청을 처리하는 엔드포인트를 정의합니다.
# 아이템 목록을 최대 'limit' 개수만큼 반환합니다.
# 기본적으로 최대 10개의 아이템을 반환하며, 'limit' 파라미터로 제한할 수 있습니다.
@app.get("/items", response_model=list[Item])
def list_items(limit: int = 10):
    return items[0:limit]

# /items/{item_id} 경로에 GET 요청을 처리하는 엔드포인트를 정의합니다.
# 특정 ID의 아이템을 반환합니다.
# 만약 해당 ID의 아이템이 존재하지 않으면 404 상태 코드를 반환합니다.
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# FastAPI 애플리케이션을 uvicorn을 사용하여 실행합니다.
# 이 코드는 애플리케이션을 ASGI 서버로 실행하는 데 사용됩니다.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

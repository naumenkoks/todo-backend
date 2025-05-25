from typing import List
from fastapi import FastAPI
from pydantic_settings import BaseSettings
from resources import EntryManager, Entry
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

class Settings(BaseSettings):
    data_folder: str = '/tmp/'

settings = Settings()

@app.get("/")
async def hello_world(name: str = "World"):
    return {"Hello": name}

@app.get("/api/entries/")
async def get_entries():
    entry_manager = EntryManager(settings.data_folder)
    entry_manager.load()
    return [entry.json() for entry in entry_manager.entries]


@app.get('/api/get_data_folder/')
async def get_data_folder():
    return {'folder': settings.data_folder}

@app.post('/api/save_entries/')
async def save_entries(data: List[dict]):
    entry_manager = EntryManager(settings.data_folder)

    for item in data:
        entry = Entry.from_json(item)
        entry_manager.entries.append(entry)

    entry_manager.save()

    return {'status': 'success'}

origins = [
    "https://wexler.io"  # адрес на котором запускаете бэк-энд
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    # Список разрешенных доменов
    allow_credentials=True,   # Разрешить Cookies и Headers
    allow_methods=["*"],      # Разрешить все HTTP методы
    allow_headers=["*"],      # Разрешить все хедеры
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
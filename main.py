import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Any, Dict
import json
import os
from dotenv import load_dotenv

# загрузка из .env
load_dotenv()
SETTINGS_PATH = os.getenv('SETTINGS_FILE_PATH', '/home/krakenrf/krakensdr_doa/_share/settings.json')
HOST = os.getenv('RC_HOST', '0.0.0.0')
PORT = int(os.getenv('RC_PORT', 8833))

app = FastAPI(
    title="Remote Control",
    description="Удаленное управление настройками Kraken",
)

@app.get("/", summary="Главная страница")
async def root():
    return {"message": "Привет! Это API для удаленного изменения настроек пеленгатора. Документация: /docs"}

@app.get("/status/", summary="Текущее состояние API", responses={
    200: {
        "description": "Возвращает сообщение",
        "content": {
            "application/json": {
                "example": {"status": "В работе", "settings_path": "/home/some_path/"}
            }
        },
    },
})
def check_status():
    """Эндпоинт вывода статуса API"""
    return {"status": "В работе", "settings_path": SETTINGS_PATH}

@app.post("/settings/", summary="Задать новые настройки", responses={
    200: {
        "description": "Возвращает сообщение",
        "content": {
            "application/json": {
                "example": {"message": "Настройки изменены"}
            }
        },
    },
    400: {"description": "Неизвестная ошибка"},
    404: {"description": "Некорректный путь к файлу, необходимо изменить SETTINGS_FILE_PATH в файле .env"}
})
def change_settings(settings_dict: Dict[str, Any]):
    """Эндпоинт изменения настроек"""
    try:
        with open(SETTINGS_PATH, "w") as file:
            file.write(json.dumps(settings_dict))
    except FileNotFoundError:
        return JSONResponse(content={"message": "Файл с настройками не найден"}, status_code=404,
                     headers={"Content-Type": "application/json"})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "Неизвестная ошибка"}, status_code=400,
                            headers={"Content-Type": "application/json"})
    return {"message": "Настройки изменены"}


@app.get("/settings/", summary="Прочитать настройки", responses={
    200: {"description": "Возвращает настройки",},
    400: {"description": "Неизвестная ошибка"},
    404: {"description": "Некорректный путь к файлу, необходимо изменить SETTINGS_FILE_PATH в файле .env"}
})
def read_settings():
    """Эндпоинт получения настроек"""
    try:
        with open(SETTINGS_PATH, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return JSONResponse(content={"message": "Файл с настройками не найден"}, status_code=404,
                     headers={"Content-Type": "application/json"})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "Неизвестная ошибка"}, status_code=400,
                            headers={"Content-Type": "application/json"})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
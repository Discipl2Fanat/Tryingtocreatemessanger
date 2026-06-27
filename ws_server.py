import asyncio
import websockets
import json

# Множество для хранения всех активных подключений (браузеров)
CONNECTED_USERS = set()

async def handle_connection(websocket):
    # Регистрируем нового пользователя, когда он открывает сайт
    CONNECTED_USERS.add(websocket)
    print(f"[СЕТЬ] Новое подключение! Всего в сети: {len(CONNECTED_USERS)}")
    
    try:
        async for message in websocket:
            # Получаем сообщение от одного пользователя (оно уже содержит имя и Rich Text)
            print(f"[СООБЩЕНИЕ] Пересылаю: {message}")
            
            # Тихо, без суеты рассылаем это сообщение ВСЕМ остальным участникам
            if CONNECTED_USERS:
                # Фильтруем, чтобы не отправлять сообщение обратно самому себе
                targets = [user for user in CONNECTED_USERS if user != websocket]
                if targets:
                    await asyncio.gather(*[user.send(message) for user in targets])
                    
    except websockets.exceptions.ConnectionClosed:
        print("[СЕТЬ] Пользователь покинул чат.")
    finally:
        # Обязательно удаляем пользователя из списка при отключении
        CONNECTED_USERS.remove(websocket)
        print(f"[СЕТЬ] Подключение закрыто. Осталось в сети: {len(CONNECTED_USERS)}")

async def main():
    # Сервер слушает порт 8765. 0.0.0.0 означает прием запросов со всех интерфейсов.
    async with websockets.serve(handle_connection, "0.0.0.0", 8765):
        print("==============================================")
        print(" WebSocket сервер запущен ")
        print(" Слушаю порт: 8765 | Ожидаю подключения...      ")
        print("==============================================")
        await asyncio.Future()  # Держит сервер запущенным вечно

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[СТОП] Сервер остановлен администратором.")

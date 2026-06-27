import asyncio
import websockets

# Список всех подключенных браузеров
CLIENTS = set()

async def handle_client(websocket):
    # Регистрируем новый браузер в сети
    CLIENTS.add(websocket)
    try:
        async for message in websocket:
            # Когда приходит сообщение, тихо пересылаем его ВСЕМ остальным
            # Исключая того, кто его отправил
            broadcast_tasks = [
                client.send(message) for client in CLIENTS if client != websocket
            ]
            if broadcast_tasks:
                await asyncio.gather(*broadcast_tasks)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        # Удаляем браузер из списка, если он отключился
        CLIENTS.remove(websocket)

async def main():
    # Сервер слушает порт 8765 на всех интерфейсах (0.0.0.0)
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        print("WebSocket сервер Брдыща запущен на порту 8765...")
        await asyncio.future() # Работаем вечно без лишней суеты

asyncio.run(main())

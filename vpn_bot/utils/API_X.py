import aiohttp
import uuid
import secrets
from data.config import dict_server_x


async def add_user_x(user_name, protocol, number_server):
    """добавить конфиг пользователя"""
    dict_payload = {1: "",
                    2: {
        "username": user_name,
        "proxies": {
            "vless": {
                "id": str(uuid.uuid4()),
                "flow": "xtls-rprx-vision"
            }
        },
        "inbounds": {
            "vless": [
                "VLESS TCP REALITY",
            ]
        },
        "expire": 0,
        "data_limit": 0,
        "data_limit_reset_strategy": "no_reset"
    },
                    3: {
        "username": user_name,
        "proxies": {
            "vmess": {
            "id": str(uuid.uuid4())
        }
        },
        "inbounds": {
            "vmess": [
            "VMess TCP"
        ]

        },
        "expire": 0,
        "data_limit": 0,
        "data_limit_reset_strategy": "no_reset"
    },
                    4: {
        "username": user_name,
        "proxies": {
            "trojan": {
                "password": str(uuid.uuid4()),
                "flow": ""
            },
        },
        "inbounds": {
            "trojan": [
                "Trojan Websocket TLS"
            ],
        },
        "expire": 0,
        "data_limit": 0,
        "data_limit_reset_strategy": "no_reset"
    },
                    5: {
        "username": user_name,
        "proxies": {
            "shadowsocks": {
                "password": secrets.token_urlsafe(16),
                "method": "chacha20-poly1305"
            }

        },
        "inbounds": {
            "shadowsocks": [
                "Shadowsocks TCP"
            ],
        },
        "expire": 0,
        "data_limit": 0,
        "data_limit_reset_strategy": "no_reset"
    }}
    
    url = f"http://{dict_server_x[number_server]['ip_address']}/api/user"  # Замените на фактический URL

    headers = {
        "Authorization": f"Bearer {dict_server_x[number_server]['x_token']}",
        "Content-Type": "application/json"
    }

    # Игнорирование SSL-проверки
    connector = aiohttp.TCPConnector(ssl=False)

    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.post(url, json=dict_payload[protocol], headers=headers) as response:
            if response.status == 200:
                response_data = await response.json()
                return response_data['links'][0]
            else:
                print("Failed to add user. Status code:", response.status)


async def get_access_token_x(number_server):
    """Получить токен для панели"""
    url = f"http://{dict_server_x[number_server]['ip_address']}/api/admin/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "password",
        "username": "Admin",  # логин от админки
        "password": "Admin",  # пасс от админки
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }

    # Игнорирование SSL-проверки
    connector = aiohttp.TCPConnector(ssl=False)

    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.post(url, data=data, headers=headers) as response:
            if response.status == 200:
                json_response = await response.json()
                access_token = json_response.get("access_token")
                return access_token
            else:
                print(f"Не удалось получить токен доступа : {response.status}")
                return None


async def delete_user_x(user_name, number_server):
    """Удалить конфиг юзера"""
    url = f"http://{dict_server_x[number_server]['ip_address']}/api/user/{user_name}"

    headers = {
        'accept': 'application/json',
        'Authorization': f"Bearer {dict_server_x[number_server]['x_token']}"
    }

    # Игнорирование SSL-проверки
    connector = aiohttp.TCPConnector(ssl=False)

    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.delete(url, headers=headers) as response:
            if response.status == 200:
                print("User deleted successfully")
                return True
            else:
                print(f"Failed to delete user. Status code: {response.status}")
                return False


async def modify_user_status_x(user_name, status: str, number_server):
    """изменить статус пользователя активен/не активаен active, disabled"""
    url = f"http://{dict_server_x[number_server]['ip_address']}/api/user/{user_name}"

    headers = {
        'accept': 'application/json',
        'Authorization': f"Bearer {dict_server_x[number_server]['x_token']}"
    }

    data = {
        "status": status
    }

    # Игнорирование SSL-проверки
    connector = aiohttp.TCPConnector(ssl=False)

    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.put(url, json=data, headers=headers) as response:
            if response.status == 200:
                print(f"Статус пользователя {user_name} успешно изменен на '{status}'.")
            else:
                print(f"Ошибка при выполнении запроса. Статус код: {response.status}")


# loop = asyncio.get_event_loop()
# loop.run_until_complete(modify_user_status("123123_01", "active"))
# loop.run_until_complete(add_user('123123_01'))
# loop.run_until_complete(delete_user('sukanaxyu123'))
# access_token = loop.run_until_complete(get_access_token())
# print("Access Token:", access_token)
import logging
import requests
import qrcode
from db import mysql


async def add_peer(url_server, admin_password, name_peer: str):
    """Возвращает когда заполнен сервер {'error': 'Maximum number of clients reached.'}
       Возвращает когда успешно {'name': '6189180632_05',
                                'address': '10.8.0.2',
                                'privateKey':
                                'cPZaanufxuSB1A2drdIuUJHKk0rU5mTi2Kq8j1cOGWE=',
                                'publicKey': 'YM142jHVrZQUB9glBZaTcI/zIZIJ5CMzKnAuXYuc3lk=',
                                'preSharedKey': 'uKTt1NPkAz49djnqlddKd4wyz6MBJg/Ot/jdgd8L424=',
                                'createdAt': '2023-03-31T09:18:09.062Z',
                                'updatedAt': '2023-03-31T09:18:09.062Z',
                                'enabled': True}"""
    try:
        session = requests.Session()
        response = session.post(f"{url_server}/api/session", json={"password": admin_password}, timeout=3)
        if not response.raise_for_status():
            response = session.post(f"{url_server}/api/wireguard/client", json={"name": name_peer})
            session.delete(f"{url_server}/api/session")
            return response.json()
    except Exception as e:
        logging.exception(e)
        return {"error": "error"}
    

async def check_count_peer_with_user_id(user_id: str):
    """Возвращает новое имя конфига пользователя str"""
    all_config = await mysql.get_user_device(user_id)
    list_name_user_config = [name['config_name'] for name in all_config]
    number_use = len(list_name_user_config)
    while True:
        number_use += 1
        new_name = f"{user_id}_{str(number_use).rjust(2, '0')}"
        if new_name not in list_name_user_config:
            break
    return new_name


async def get_user_info_from_server(url_server, admin_password, peer_name: str):
    session = requests.Session()
    response = session.post(f"{url_server}/api/session", json={"password": admin_password})
    if not response.raise_for_status():
        response = session.get(f"{url_server}/api/wireguard/client")
        result = response.json()
        user_info = [user for user in result if user['name'] == peer_name]
        session.delete(f"{url_server}/api/session")
        try:
            return user_info[0]
        except IndexError:
            return 
    

async def delete_peer(url_server, admin_password, peer_id: str):
    try:
        session = requests.Session()
        response = session.post(f"{url_server}/api/session", json={"password": admin_password}, timeout=2)
        if not response.raise_for_status():
            response = session.delete(f"{url_server}/api/wireguard/client/{peer_id}")   
            session.delete(f"{url_server}/api/session")     
            return True
    except Exception as e:
        return False


async def create_conf_file(user_data, number_server, public_key, tariff=1):
    """возвращает str путь до файла с qr кодом"""
    data = f"[Interface]\nPrivateKey = {user_data['privateKey']}\nAddress = {user_data['address']}\nDNS = 1.1.1.1\n[Peer]\nPublicKey = {public_key}\nPresharedKey = {user_data['preSharedKey']}\nAllowedIPs = 0.0.0.0/0, ::/0\nPersistentKeepalive = 0\nEndpoint = {user_data['end_point']}"
    if tariff == 2:
        data = f"[Interface]\nPrivateKey = {user_data['privateKey']}\nAddress = {user_data['address']}\nDNS = 1.1.1.1\n[Peer]\nPublicKey = {public_key}\nPresharedKey = {user_data['preSharedKey']}\nAllowedIPs = 147.75.208.0/20, 185.89.216.0/22, 31.13.24.0/21, 31.13.64.0/19, 31.13.96.0/19, 45.64.40.0/22, 66.220.144.0/20, 69.63.176.0/20, 69.171.224.0/19, 74.119.76.0/22, 102.132.96.0/20, 103.4.96.0/22, 129.134.0.0/16, 157.240.0.0/16, 173.252.64.0/18, 179.60.192.0/22, 185.60.216.0/22, 204.15.20.0/22\nPersistentKeepalive = 0\nEndpoint = {user_data['end_point']}"
    img = qrcode.make(data)
    img.save(f"./qr_code/{number_server}/{user_data['name']}.png")
    with open(f"./conf_file/{number_server}/{user_data['name']}.conf", "w") as file:
            file.write(data)
    return f"./qr_code/{number_server}/{user_data['name']}.png", f"./conf_file/{number_server}/{user_data['name']}.conf"


async def enable_disable_config(url_server, admin_password, peer_id: str, status: str) -> int:
    session = requests.Session()
    response = session.post(f"{url_server}/api/session", json={"password": admin_password})
    if not response.raise_for_status():
        response = session.post(f"{url_server}/api/wireguard/client/{peer_id}/{status}")
        session.delete(f"{url_server}/api/session")
        return response.status_code



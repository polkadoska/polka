import aiomysql
from data import config
import logging


async def create_conn():
    conn = await aiomysql.connect(
        host=config.HOST_DB,
        user=config.USER_DB,
        password=config.PASSWORD_DB,
        db=config.DATABASE_DB,
        charset='utf8mb4',
        cursorclass=aiomysql.cursors.DictCursor
    )
    return conn


async def close_conn(conn):
    conn.close()


async def add_user(user_id, user_name, referal, sum_tariff):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = "INSERT INTO `users` (`user_id`, `user_name`, `referal`, `sum_tariff`) VALUES(%s, %s, %s, %s)"
        await cursor.execute(query, (user_id, user_name, referal, sum_tariff))
        await conn.commit()
    await close_conn(conn)


async def get_sum_tariff():
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"SELECT * FROM `config_bot`"
        await cursor.execute(query)
        data = await cursor.fetchone()
    await close_conn(conn)
    return data


async def get_balance(user_id):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"SELECT balance FROM `users` WHERE user_id = '{user_id}'"
        await cursor.execute(query)
        data = await cursor.fetchone()
    await close_conn(conn)
    return data


async def add_config(user_id: str, 
                     config_name: str, 
                     number_server: int, 
                     tariff: int, 
                     date_end, 
                     id_server: str, 
                     type_device: int, 
                     protocol: int):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = "INSERT INTO `config` (`user_id`, `config_name`, `number_server`, `tariff`, `date_end`, `id_server`, `type_device`, `protocol`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        await cursor.execute(query, (user_id, config_name, number_server, tariff, date_end, id_server, type_device, protocol))
        await conn.commit()
    await close_conn(conn)


async def exist_user(user_id: str):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"SELECT * FROM `users` WHERE `user_id` = {user_id}"
        await cursor.execute(query)
        data = await cursor.fetchall()
    await close_conn(conn)
    return bool(len(data))


async def get_all_configs_and_users():
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"""SELECT c.protocol, c.config_name, c.number_server, c.id_server, u.user_id, u.balance, u.friend, u.warn, u.sum_tariff
                    FROM config as c
                    JOIN users as u ON c.user_id = u.user_id;"""
        await cursor.execute(query)
        data = await cursor.fetchall()
    await close_conn(conn)
    return data


async def get_all_users_info():
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"SELECT * FROM `users`"
        await cursor.execute(query)
        data = await cursor.fetchall()
    await close_conn(conn)
    return data


async def get_user_info(user_id: str):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"SELECT * FROM `users` WHERE `user_id` = {user_id}"
        await cursor.execute(query)
        result = await cursor.fetchone()
        query2 = f"SELECT * FROM `config` WHERE `user_id` = {user_id}"
        await cursor.execute(query2)
        configs = await cursor.fetchall()
        result['count_configs'] = len(configs)
    await close_conn(conn)
    return result


async def get_users_info():
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"SELECT * FROM `users`"
        await cursor.execute(query)
        data = await cursor.fetchall()
    await close_conn(conn)
    return data


async def get_users_info_where(number_server: int):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"SELECT `user_id` FROM `config` WHERE number_server = {number_server}"
        await cursor.execute(query)
        data = await cursor.fetchall()
    await close_conn(conn)
    return data


async def get_user_device(user_id: str):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"""SELECT c.*, u.sum_tariff
                    FROM config c
                    JOIN users u ON c.user_id = u.user_id
                    WHERE c.user_id = {user_id};"""
        await cursor.execute(query)
        data = await cursor.fetchall()
    await close_conn(conn)
    return data


async def get_user_change_device(config_name: str):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"SELECT * FROM `config` WHERE `config_name` = '{config_name}'"
        await cursor.execute(query)
        data = await cursor.fetchone()
    await close_conn(conn)
    return data


async def get_config_info(id: str):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"SELECT * FROM `config` WHERE `id_server` = '{id}'"
        await cursor.execute(query)
        data = await cursor.fetchone()
    await close_conn(conn)
    return data


async def get_my_referal(user_id: str):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"SELECT * FROM `users` WHERE `referal` = '{user_id}'"
        await cursor.execute(query)
        data = await cursor.fetchall()
    await close_conn(conn)
    return data


async def get_stat():
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"""SELECT 
  COUNT(CASE WHEN number_server = 1 THEN 1 END) AS count_server_1,
  COUNT(CASE WHEN number_server = 2 THEN 1 END) AS count_server_2,
  COUNT(CASE WHEN number_server = 3 THEN 1 END) AS count_server_3,
  COUNT(CASE WHEN number_server = 4 THEN 1 END) AS count_server_4,
  COUNT(CASE WHEN number_server = 5 THEN 1 END) AS count_server_5,
  COUNT(CASE WHEN number_server = 6 THEN 1 END) AS count_server_6,
  COUNT(*) AS count_config,
  (SELECT COUNT(*) FROM users) AS count_users
FROM config;"""
        await cursor.execute(query)
        data = await cursor.fetchone()
    await close_conn(conn)
    return data


async def delete_peer(config_name: str):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"DELETE FROM config WHERE `config_name` = '{config_name}'"
        await cursor.execute(query)
        await conn.commit()
    await close_conn(conn)


async def set_friend(user_id: str, status: str):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"UPDATE users SET friend = '{status}' WHERE `user_id` = '{user_id}'"
        await cursor.execute(query)
        await conn.commit()
    await close_conn(conn)


async def set_referal_balance(user_id: str, amount: int):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"UPDATE users SET `referal_balance` = `referal_balance` + {amount} WHERE `user_id` = '{user_id}'"
        await cursor.execute(query)
        await conn.commit()
    await close_conn(conn)


async def un_referal_balance(user_id: str, amount: int):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"UPDATE users SET `referal_balance` = `referal_balance` - {amount} WHERE `user_id` = '{user_id}'"
        await cursor.execute(query)
        await conn.commit()
    await close_conn(conn)


async def set_warn_and_get_user_info(user_id: str, warn: int):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"UPDATE users SET warn = warn + {warn} WHERE `user_id` = '{user_id}'"
        await cursor.execute(query)
        await conn.commit()
        query2 = f"SELECT * FROM `users` WHERE `user_id` = '{user_id}'"
        await cursor.execute(query2)
        result = await cursor.fetchone()
        query3 = f"SELECT * FROM `config` WHERE `user_id` = '{user_id}'"
        await cursor.execute(query3)
        configs = await cursor.fetchall()
        result['count_configs'] = len(configs)
    await close_conn(conn)
    return result


async def set_balance_and_get_user_info(user_id: str, balance: int):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"UPDATE users SET balance = balance + {balance}, warn = 0 WHERE `user_id` = '{user_id}'"
        await cursor.execute(query)
        await conn.commit()
        query2 = f"SELECT * FROM `users` WHERE `user_id` = '{user_id}'"
        await cursor.execute(query2)
        result = await cursor.fetchone()
        query3 = f"SELECT * FROM `config` WHERE `user_id` = '{user_id}'"
        await cursor.execute(query3)
        configs = await cursor.fetchall()
        result['count_configs'] = len(configs)
    await close_conn(conn)
    return result


async def un_balance_and_get_user_info(user_id: str, balance: int):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"UPDATE users SET balance = balance - {balance} WHERE `user_id` = '{user_id}'"
        await cursor.execute(query)
        await conn.commit()
        query2 = f"SELECT * FROM `users` WHERE `user_id` = '{user_id}'"
        await cursor.execute(query2)
        result = await cursor.fetchone()
    await close_conn(conn)
    return result


async def set_pay_bonus(pay_bonus):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"UPDATE config_bot SET `pay_bonus` = {pay_bonus}"
        await cursor.execute(query)
        await conn.commit()
    await close_conn(conn)



async def set_price(price):
    conn = await create_conn()
    async with conn.cursor() as cursor:
        query = f"UPDATE config_bot SET `price` = {price}"
        await cursor.execute(query)
        await conn.commit()
    await close_conn(conn)

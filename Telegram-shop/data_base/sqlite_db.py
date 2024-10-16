import mysql.connector as sq

from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Alonikx1337-',
        database='stariy_bot'
    )
    if base:
        print('Соединение успешно')
    cur = base.cursor(buffered=True)
    cur.execute('CREATE TABLE IF NOT EXISTS catalog(product_id INT AUTO_INCREMENT, img VARCHAR(255),'
                'name VARCHAR(100), description VARCHAR(100), price INT,'
                'quantity INT, category VARCHAR(100), PRIMARY KEY(product_id))')
    cur.execute('CREATE TABLE IF NOT EXISTS cart(cart_num INT AUTO_INCREMENT,'
                'user_id INT, product_id INT, product_title VARCHAR(100), price INT, PRIMARY KEY(cart_num))')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO catalog(img, name, description, price, quantity, category) VALUES(%s,%s,%s,%s,%s,%s)',
                    tuple(data.values()))
        base.commit()


async def sql_read(message):
    cur.execute('SELECT * FROM catalog;')
    for ret in cur.fetchall():
        await bot.send_photo(message.from_user.id, ret[1], f'{ret[2]}\nОписание: {ret[3]}\nЦена: {ret[4]} руб.\n'
                                                           f'Количество: {ret[5]}\nКатегория: {ret[6]}')


async def sql_read_table(var):
    cur.execute(f'SELECT * FROM {var};')
    return cur.fetchall()


async def sql_read_product_id(product_id):
    cur.execute(f'SELECT * FROM catalog WHERE product_id={product_id};')
    return cur.fetchall()


async def sql_read_category(var):
    cur.execute(f'SELECT * FROM catalog WHERE category="{var}";')
    return cur.fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE FROM catalog WHERE name = %s;', (data,))
    cur.execute('DELETE FROM cart WHERE product_title = %s;', (data,))
    base.commit()


async def cart_adding_sql(message_id, product_id, product_title, price):
    cur.execute(f'INSERT INTO cart(user_id, product_id, product_title, price) VALUES(%s,%s,%s,%s);', [message_id,
                                                                                                      product_id,
                                                                                                      product_title,
                                                                                                      price])
    cur.execute(f'UPDATE catalog SET quantity=quantity-1 WHERE product_id = {product_id};')
    base.commit()


async def cart_deleting_sql(product_id):
    cur.execute(f'DELETE FROM cart WHERE product_id = {product_id} LIMIT 1;')
    cur.execute(f'UPDATE catalog SET quantity=quantity+1 WHERE product_id = {product_id};')
    base.commit()


async def cart_product_checking(product_id):
    cur.execute(f'SELECT * FROM cart WHERE product_id = {product_id};')
    return cur.fetchall()


async def cart_checking(user_id):
    cur.execute(f'SELECT * FROM cart WHERE user_id = {user_id};')
    return cur.fetchall()


async def quantity_sql_add(product_id):
    cur.execute(f'UPDATE catalog SET quantity=quantity+1 WHERE product_id = {product_id};')
    base.commit()


async def quantity_sql_delete(product_id):
    cur.execute(f'UPDATE catalog SET quantity=quantity-1 WHERE product_id = {product_id};')
    base.commit()


async def cart_clear():
    cur.execute(f'DELETE FROM cart;')
    base.commit()


async def cart_clear_after_offer(user_id):
    cur.execute(f'DELETE FROM cart WHERE user_id = {user_id};')
    base.commit()

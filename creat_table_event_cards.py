import psycopg2
import sshtunnel

# Подключаемся к базе данных 
sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

NAME = "cashdb"
USER = "cashgenius"
HOST = "bandydan-3203.postgres.pythonanywhere-services.com"
PORT = 13203
PASSWORD = "lsdS4.eWqQlf!d"

with sshtunnel.SSHTunnelForwarder(
    ('ssh.pythonanywhere.com'),
    ssh_username='bandydan',
    ssh_password='3RJzTOcl#Ic*',
    remote_bind_address=(HOST, PORT)
) as tunnel:
    conn = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host='127.0.0.1',
        port=tunnel.local_bind_port,
        database=NAME
    )
"""# Удаляем существующую таблицу, если она существует
with conn.cursor() as cur:
    cur.execute('DROP TABLE IF EXISTS event_cards;')
    conn.commit()"""
# Создаем таблицу для хранения карточек событий
with conn.cursor() as cur:
    cur.execute('''
    CREATE TABLE event_cards (
    id SERIAL PRIMARY KEY,
    categories TEXT NOT NULL,
    text TEXT NOT NULL,
    time INTEGER,
    relationships_with_family INTEGER,
    relationships_with_friends INTEGER,
    skills INTEGER,
    health INTEGER,
    motivation INTEGER,
    money INTEGER,
    ubytki INTEGER,
    property_type TEXT
    );
    ''')
    conn.commit()

# Закрываем соединение с базой данных
conn.close()
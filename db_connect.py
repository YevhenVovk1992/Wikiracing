import psycopg2
import threading

from typing import Union


class ConnectToPostgres:
    user = 'postgres'
    password = 'postgres'
    host = "127.0.0.1"
    port = "5432"

    def __init__(self, database):
        self.database = database

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            return self.conn
        except psycopg2.OperationalError:
            pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
            self.conn.close()


def get_page_from_db(title: str) -> Union[dict, None]:
    page_dict = {}
    links_list = []
    with ConnectToPostgres('wikiracing') as db:
        cursor = db.cursor()
        cursor.execute(f"""select article.title from links
        inner join article on article.article_id = links.link
        where links.parent = (select article_id from article where title = '{title.replace("'", "/")}')
        order by links.link""")
        link = cursor.fetchall()
    if link:
        for el in link:
            links_list.append(el[0].replace("/", "'"))
        page_dict.update({
            'title': title,
            'links': links_list
        })
        return page_dict
    return None


def create_connection(link: str, title_id: tuple) -> None:
    with ConnectToPostgres('wikiracing') as db:
        cursor = db.cursor()
        cursor.execute(f"""select article_id from article where title = '{link.replace("'", "/")}'""")
        check_link = cursor.fetchone()
        if not check_link:
            cursor.execute(
                f"""INSERT into article(title)
                    values ('{link.replace("'", "/")}')"""
            )
            cursor.execute(f"""INSERT into links(parent, link) values (
                                '{title_id[0]}',
                                (select article_id from article where title = '{link.replace("'", "/")}')
                                )""")
        else:
            cursor.execute(f"""INSERT into links(parent, link) values (
                            '{title_id[0]}', {check_link[0]}
                            )""")


def write_page_to_db(title: str, links_list: list) -> None:
    tasks = []
    with ConnectToPostgres('wikiracing') as db:
        cursor = db.cursor()
        cursor.execute(f"""select article_id from article where title = '{title.replace("'", "/")}'""")
        title_id = cursor.fetchone()
        if not title_id:
            cursor.execute(f"""INSERT into article(title) values ('{title.replace("'", "/")}')""")
            cursor.execute(f"""select article_id from article where title = '{title.replace("'", "/")}'""")
            title_id = cursor.fetchone()
    for el in links_list:
        thread = threading.Thread(target=create_connection, args=(el, title_id))
        thread.start()
        tasks.append(thread)
    for itm in tasks:
        itm.join()


def create_table_in_db() -> None:
    with ConnectToPostgres('wikiracing') as db:
        cursor = db.cursor()
        query1 = """CREATE TABLE IF NOT EXISTS article
(article_id SERIAL primary key, title varchar(150) not null);"""
        query2 = """CREATE TABLE IF NOT EXISTS links
(link_id SERIAL primary key, parent INT not null, link INT not null);"""
        cursor.execute(query1)
        cursor.execute(query2)

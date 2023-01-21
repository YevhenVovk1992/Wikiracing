import psycopg2

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
        # cursor.execute(f"""select title from article where title = '{title.replace("'", "/")}'""")
        # page = cursor.fetchone()

        cursor.execute(f"""select article.title from links
    inner join article on article.article_id = links.link
    where links.parent = (select article_id from article where title = '{title.replace("'", "/")}')
    order by links.link""")
        link = cursor.fetchall()
        for el in link:
            links_list.append(el[0].replace("/", "'"))

        if link:
            page_dict.update({
                'title': title,
                'links': links_list
            })
            return page_dict
    return None


def write_page_to_db(title: str, links_list) -> None:

    with ConnectToPostgres('wikiracing') as db:
        cursor = db.cursor()
        cursor.execute(f"""select article_id from article where title = '{title.replace("'", "/")}'""")
        title_id = cursor.fetchone()
        if not title_id:
            cursor.execute(f"""INSERT into article(title) values ('{title.replace("'", "/")}')""")

    with ConnectToPostgres('wikiracing') as db:
        cursor = db.cursor()
        for link in links_list:
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


def create_table_in_db() -> None:
    with ConnectToPostgres('wikiracing') as db:
        cursor = db.cursor()
        query1 = """CREATE TABLE IF NOT EXISTS article
(article_id SERIAL primary key, title varchar(150) not null);"""
        query2 = """CREATE TABLE IF NOT EXISTS links
(link_id SERIAL primary key, parent INT not null, link INT not null);"""
        cursor.execute(query1)
        cursor.execute(query2)

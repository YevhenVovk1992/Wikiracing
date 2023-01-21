import datetime
import threading
import time
import wikipedia

from typing import List

from db_connect import create_table_in_db, write_page_to_db, get_page_from_db


class WikiRacer:
    requests_per_minute = 100
    links_per_page = 200

    def print_path(self, data, received_chain=None):
        if received_chain is None:
            received_chain = []
        received_chain.insert(0, data['title'])
        if data['parent']:
            self.print_path(data['parent'], received_chain=received_chain)
        return received_chain

    def find_path(self, start: str, finish: str) -> List[str]:
        root_page = target_page = None
        G = {}
        request_count = 0
        language = "uk"
        now_time = datetime.datetime.now()
        wikipedia.set_lang(language)
        create_table_in_db()
        try:
            root_page = wikipedia.page(start.lower())
            target_page = wikipedia.page(finish.lower())
        except wikipedia.exceptions.DisambiguationError as e:
            print('\nDisambiguation Selection (Choose one of these or use another term)')
            for option in e.options:
                print('\t' + option)
            print()
        except wikipedia.exceptions.PageError as e:
            pass
        G[root_page.title] = {
            'title': root_page.title,
            'distance': 0,
            'parent': None
        }
        Q = [G[root_page.title]]
        while Q:
            delta = datetime.datetime.now() - now_time
            current = Q[0]
            Q = Q[1:]
            try:
                page_from_db = get_page_from_db(current['title'])
                if page_from_db:
                    print('Get from DB: ', page_from_db['title'])
                    links = page_from_db['links']
                else:
                    request_count += 1
                    if request_count > self.requests_per_minute and delta.seconds <= 60:
                        sleep_time = 60 - delta.seconds
                        print(
                            f"Can not run more than {self.requests_per_minute} requests! Please, wait {sleep_time} seconds."
                        )
                        time.sleep(sleep_time)
                        now_time = datetime.datetime.now()
                        request_count = 0
                    current_page = wikipedia.page(current['title'])
                    print('Get page:', current_page.title)
                    links = current_page.links
                    if len(links) > self.links_per_page:
                        links = links[:self.links_per_page]
                    write_to_db_thread = threading.Thread(target=write_page_to_db, args=(current['title'], links))
                    write_to_db_thread.start()
                for link in links:
                    if link not in G:
                        G[link] = {
                            'title': link,
                            'distance': current['distance'] + 1,
                            'parent': current
                        }
                        if link == target_page.title:
                            print('\n%s found!' % link)
                            return self.print_path(G[link])
                        Q.append(G[link])
            except wikipedia.exceptions.DisambiguationError as e:

                # Disambiguation Page
                G[e.title] = {
                    'title': e.title,
                    'distance': current['distance'] + 1,
                    'parent': current
                }

                # Adds every link on disambiguation page to queue
                for option in e.options:
                    if option not in G:
                        G[option] = {
                            'title': option,
                            'distance': current['distance'] + 2,
                            'parent': G[e.title]
                        }
                        if option == target_page.title:
                            print(f'\n{option} found!')
                            return self.print_path(G[option])
                        Q.append(G[option])
            except wikipedia.exceptions.PageError as e:

                # Skips over the item in the queue if it results in a page error.
                pass


if __name__ == "__main__":
    racer = WikiRacer()
    # print(racer.find_path('дружба', 'рим'))
    # print(racer.find_path('Мітохондріальна ДНК', 'Вітамін K'))
    # print(racer.find_path('Марка (грошова одиниця)', 'Китайський календар'))
    print(racer.find_path('Фестиваль', 'Пілястра'))
    # print(racer.find_path('Дружина (військо)', '6 жовтня'))
import os
import time
from dataclasses import asdict
import requests
from celery import Celery, schedules
import sqlite3
from ukrnet import Controller

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.news',
        'schedule': 30,
    },
    'drop_db_day': {
        'task': 'tasks.drop_db',
        'schedule': schedules.crontab(minute=5, hour=14),
    }
}
beat_dburi = 'sqlite:///../api/un_news_last_day.db'

celery.conf.update(
    {'beat_dburi': beat_dburi}
)
celery.conf.timezone = 'UTC'

news_controller = Controller()


@celery.task(name='tasks.add')
def add(x: int, y: int) -> int:
    time.sleep(5)
    return x + y


# sched = BackgroundScheduler(daemon=True)
# sched.add_job(drop_lite_db, 'cron', hour=12, minute=55)
# sched.start()

@celery.task(name="tasks.drop_db")
def drop_lite_db():
    try:
        sqlite_connection = sqlite3.connect(os.path.abspath('/home/nikmoz/PyCharmProgect/news-api/api'
                                                            '/un_news_last_day.db'))
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_delete_query = """DELETE FROM un_news_search"""
        cursor.execute(sql_delete_query)
        sqlite_connection.commit()
        print("Запись успешно удалена")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


@celery.task(name="tasks.news")
def parse_news():
    try:
        print(requests.get("http://web:5001/api/v1/check").json())
        parsed_news = list(map(asdict, news_controller.get_last_news()))
        requests.post("http://web:5001/api/v1/news", json=parsed_news, headers={'x-api-key': 'qwe1asd2zxc3'})
    except ConnectionError:
        print("Error with server")

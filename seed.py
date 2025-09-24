from datetime import datetime
import faker
from random import randint, choice
import sqlite3

NUMBER_USERS = 10
NUMBER_TASKS = 30
STATUS_LIST = ['new', 'in progress', 'completed']


def generate_fake_data(number_users, number_tasks, status_list):
    fake_users = []
    fake_tasks = []
    fake_status = [(s,) for s in status_list]
    # print(status_list, fake_status)

    fake_data = faker.Faker()

    for _ in range(number_users):
        fullname = fake_data.name()
        email = fake_data.unique.email()
        fake_users.append((fullname, email))

    for _ in range(number_tasks):
        title = fake_data.sentence(nb_words=5)
        description = fake_data.text(max_nb_chars=100)
        status_id = randint(1, len(status_list))
        user_id = randint(1, number_users)
        fake_tasks.append((title, description, status_id, user_id))

    return fake_users, fake_tasks, fake_status


def insert_data_to_db(users, tasks, status):
    with sqlite3.connect('tasks.db') as con:
        cur = con.cursor()
        cur.executemany("INSERT INTO users(fullname, email) VALUES (?, ?)", users)
        cur.executemany("INSERT INTO status(name) VALUES (?)", status)
        cur.executemany(
            "INSERT INTO tasks(title, description, status_id, user_id) VALUES (?, ?, ?, ?)", 
            tasks
        )
        con.commit()

if __name__ == "__main__":
    users, tasks, status = generate_fake_data(NUMBER_USERS, NUMBER_TASKS, STATUS_LIST)
    insert_data_to_db(users, tasks, status)
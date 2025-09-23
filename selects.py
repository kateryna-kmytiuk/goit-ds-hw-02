import sqlite3

def execute_query(sql):
    with sqlite3.connect('tasks.db') as con:
        cur = con.cursor()
        sql_type = sql.strip().split()[0].upper()

        if sql_type == "SELECT":
            cur.execute(sql)
            return cur.fetchall()
        else:
            cur.execute(sql)
            con.commit()
            return f"{sql_type} запит виконано."


sql = [
"""
SELECT t.title, t.description, s.name as status, u.fullname as user
FROM tasks t
INNER JOIN status s ON t.status_id = s.id
INNER JOIN users u ON t.user_id = u.id
WHERE t.user_id = 1
""",
"""
SELECT t.title, t.description, s.name as status, u.fullname as user
FROM tasks t
INNER JOIN status s ON t.status_id = s.id
INNER JOIN users u ON t.user_id = u.id
WHERE s.name = 'new'
""",
"""
UPDATE tasks 
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 5
""",
"""
SELECT u.fullname
FROM users u
WHERE id NOT IN (SELECT user_id FROM tasks)
""",
"""
INSERT INTO tasks (title, description, status_id, user_id)
VALUES ('New Task', 'This is a new task description.', 1, 2)
""",
"""
SELECT * FROM tasks t
WHERE t.status_id <> (SELECT id FROM status WHERE name = 'completed')
""",
"""
DELETE FROM tasks WHERE id = 31
""",
"""
SELECT * FROM users u
WHERE u.email LIKE '%@example.com'
""",
"""
UPDATE users SET fullname = 'Rebecca Andrews' WHERE id = 6
""",
"""
SELECT s.name, COUNT(t.status_id) FROM tasks t
INNER JOIN status s ON t.status_id = s.id
GROUP BY s.id
""",
"""
SELECT t.title, t.description, u.fullname, u.email 
FROM tasks t 
INNER JOIN users u ON t.user_id = u.id
WHERE u.email LIKE '%@example.com'
""",
"""
SELECT * FROM tasks t
WHERE t.description IS NULL
""",
"""
SELECT u.fullname, t.title, t.description FROM tasks t
INNER JOIN users u ON t.user_id = u.id
WHERE t.status_id = (SELECT id FROM status WHERE name = 'in progress')
""",
"""
SELECT u.fullname, COUNT(t.id) FROM users u
LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.id
"""
]


for i in range(len(sql)):
    print(f"Запит {i+1}:")
    print(execute_query(sql[i]))



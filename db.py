import sqlite3 as sql
from User import User
from Report import Report

DB_FILE_NAME = "db.db"

def Init():
    conn = sql.connect(DB_FILE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL,
            password TEXT NOT NULL,
            vk TEXT NOT NULL,
            account INTEGER NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_login TEXT NOT NULL,
            routes INTEGER NOT NULL,
            passengers INTEGER NOT NULL,
            fuel_bonus INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    
    print("Database initialized")

# ! users

def add_user(user:User) -> dict[str, str]:
    conn = sql.connect(DB_FILE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (login, password, vk, account) VALUES (?, ?, ?, ?)", 
                (user.login, user.password, user.vk, user.account))
    conn.commit()
    conn.close()
    return {"status": "ok"}

def get_user(login:str):
    conn = sql.connect(DB_FILE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT login, password, vk, account FROM users WHERE login = ?", (login,))
    user = cursor.fetchone()
    conn.close()
    return User.to_user(user)

def get_users() -> list[User]:
    conn = sql.connect(DB_FILE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT login, password, vk, account FROM users")
    users = cursor.fetchall()
    conn.close()
    users = [User.to_user(user) for user in users]
    return users

# ! reports

def add_report(report : Report):
    try:
        conn = sql.connect(DB_FILE_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reports (user_login, routes, passengers, fuel_bonus) VALUES (?, ?, ?, ?)", 
                    (report.user_login, report.routes, report.passengers, report.fuel_bonus))
        conn.commit()
        conn.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}    
def get_reports():
    conn = sql.connect(DB_FILE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports")
    reports = cursor.fetchall()
    conn.close()
    reports = [Report.to_report(report) for report in reports]
    return reports

def delete_report(report_id:int):
    conn = sql.connect(DB_FILE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reports WHERE id = ?", (report_id,))
    conn.commit()
    conn.close()


# if __name__ == "__main__":
#     con = sql.connect(DB_FILE_NAME)
#     cur = con.cursor()
#     cur.execute("DROP TABLE reports")
#     con.commit()
#     con.close()

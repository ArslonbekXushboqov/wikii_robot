import sqlite3 as sql

with sql.connect("userdata.db") as con:
    cur=con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS user(
        name TEXT,
        chat_id INTEGER,
        lang VARCHAR)''')
    con.commit()

def insert_user_data(name, chat_id, lang):
    cur.execute('SELECT * FROM user WHERE chat_id = ?', (chat_id,))
    res = cur.fetchone()
    if res is None:
        cur.execute("INSERT INTO user(name, chat_id, lang)VALUES(?,?,?)", (name, chat_id, lang,))
    con.commit()

def uplang(lang, chatid):
    cur.execute("SELECT lang FROM user WHERE chat_id = ?",(chatid,))
    l = cur.fetchall()
    for la in l:
        lan = la[0]
    
    cur.execute("UPDATE user SET lang = ? WHERE lang = ?", (lang, lan))
    con.commit()
def detect_lang(chat_id):
    cur.execute("SELECT lang FROM user WHERE chat_id=?",(chat_id,))
    res=cur.fetchone()[0]
    return res
def stat():
    cur.execute("SELECT count(*) FROM user")
    res = cur.fetchone()
    return res[0]
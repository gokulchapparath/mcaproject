import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "aru",
                           passwd = "aru12345678",
                           db = "wireless")
    c = conn.cursor()

    return c, conn
		
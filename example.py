import sqlite3
import streamlit as st

# st.write("example")
# conn = sqlite3.connect('customers.db')
# conn.row_factory = sqlite3.Row  

# c = conn.cursor()
# try:
    
#     listOfTables = c.execute(
#   """SELECT name FROM sqlite_master WHERE type='table'
#   AND name='users'; """).fetchall()
#     st.write(listOfTables, len(listOfTables))
#     if len(listOfTables) == 0:
#         print("dsfsd")
#         # c.execute('''CREATE TABLE customers
#         #                 (name text, address text, phone text)''')
#         # c.commit()
#         c.execute('''CREATE TABLE users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     userName VARCHAR(500) NOT NULL,
#     email  VARCHAR(500) NOT NULL UNIQUE,
#     password VARCHAR(500) NOT NULL
# );''')
#         conn.commit()
        
#     else:
#         # c.execute("INSERT INTO users VALUES (email, password)", ( 'email', 'password'))
#         # conn.commit()
#         insert_stmt = ("INSERT INTO users(username, email, password)" "VALUES (%s, %s, %s)")
#         data = ('username', 'email', 'hashed_password[0]')
#         #print(data,"?????????????????/")
#         c.execute(insert_stmt, data)
#         conn.commit()
#         # c.execute("SELECT * from customers")
#         # st.write(c.fetchall())
#         # print("KKKKKKKKK", c.fetchall())
#         # for row in c.fetchall():
#         #      print(row)
#         conn.close()

#     # if  len(c.fetchall()) == 0:
#     #         c.execute('''CREATE TABLE customers
#     #                     (name text, address text, phone text)''')
#     #         conn.commit()
#     #         c.execute("SELECT * from customers")
#     #         st.write(c.fetchall())

#     # conn.close()

# except Exception as e:
#       st.write(e)

conn = st.connection('mysql', type='sql')
st.write(conn,"+++++++++++++++++++++++=")
df = conn.query('SELECT * from users;', ttl=0)
# st.write(df,"ffffffffffffffffffffffffff")
import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
import mysql.connector
import time
import bcrypt

# mydb = mysql.connector.connect(
#     host= "127.0.0.1",
#     user= "satya",
#     password= "satya",
#     database= "streamlit",
#     autocommit=True
# )
# conn = st.connection('mysql', type='sql', autocommit=True)
# print(conn,"ccccccccccccc")
# # Perform query.
# df = conn.query('SELECT * from users;', ttl=0)
# print(df,"ffffffffffffffffffffffffff", df.to_dict())
# for row in df.to_dict():
#     print(row,type(row))
mydb = mysql.connector.connect(
    host= "192.168.0.106",
    user= "user",
    password= "password",
    database= "streamlit",
    autocommit=True
)
mycursor = mydb.cursor(dictionary=True)
    


def fetch_users():
    """
    Fetch Users
    :return Dictionary of Users:
    """
    mycursor.execute('select * from users')
    data = mycursor.fetchall()
    # #print(data)
    # st.write(data)

    return data
def get_user_emails():
    """
    Fetch User Emails
    :return List of user emails:
    """
    mycursor.execute('select * from users')
    users = mycursor.fetchall()
    #print(users,"?????????------------------")
    emails = []

    for user in users:
        emails.append(user['email'])
    
    return emails


def get_usernames():
    """
    Fetch Usernames
    :return List of user usernames:
    """
    mycursor.execute('select * from users')
    users = mycursor.fetchall()
    usernames = []
    for user in users:
        usernames.append(user['userName'])
    return usernames


def validate_email(email):
    """
    Check Email Validity
    :param email:
    :return True if email is valid else False:
    """
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$" #tesQQ12@gmail.com

    if re.match(pattern, email):
        return True
    return False


def validate_username(username):
    """
    Checks Validity of userName
    :param username:
    :return True if username is valid else False:
    """

    pattern = "^[a-zA-Z0-9 ]*$"
    if re.match(pattern, username):
        return True
    return False

# def showAccount():
#     #print("sssssssssssssss")
def sign_up():
    try:
        with st.form('signup'):
            st.subheader(':green[Sign Up]')
            email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
            username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
            password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
            password2 = st.text_input(':blue[Confirm Password]', placeholder='Confirm Your Password', type='password')
            btn1, bt2, btn3, btn4, btn5 = st.columns(5)
            with btn3:
                st.form_submit_button('Sign Up')
            
            if email:
                if validate_email(email):
                    if email not in get_user_emails():
                        if validate_username(username):
                            if username not in get_usernames():
                                if len(username) >= 2:
                                    if len(password1) >= 6:
                                        if password1 == password2:
                                            # Add User to DB
                                            hashed_password = stauth.Hasher([password2]).generate()
                                            # insert_user(email, username, hashed_password[0])
                                            insert_stmt = (
                                            "INSERT INTO users(username, email, password)" "VALUES (%s, %s, %s)")
                                            data = (username, email, hashed_password[0])
                                            #print(data,"?????????????????/")
                                            mycursor.execute(insert_stmt, data)
                                            mydb.commit()
                                            st.success('Account created successfully!!')
                                            st.balloons()
                                        else:
                                            st.warning('Passwords Do Not Match')
                                    else:
                                        st.warning('Password is too Short')
                                else:
                                    st.warning('Username Too short')
                            else:
                                st.warning('Username Already Exists')

                        else:
                            st.warning('Invalid Username')
                    else:
                        st.warning('Email Already exists!!')
                else:
                    st.warning('Invalid Email')

            # btn1, bt2, btn3, btn4, btn5 = st.columns(5)

            # with btn3:
            #     st.form_submit_button('Sign Up')
    except Exception as e:
        st.error(e)

def insert_period(period, incomes, expenses, comment, email,type, id):
    #print(period, incomes, expenses, comment, email)
    # try: 
    

    """Returns the report on a successful creation, otherwise raises an error"""

    sql = "SELECT * FROM users WHERE email = %s;"
    adr = (email,)
    mycursor.execute(sql, adr)
    result = mycursor.fetchone()
    userId = None
    #print(userId,"LLL", result)
    if result:
        userId = result['id']
    if (type == 'new'):
        insert_stmt = (
        "INSERT INTO savings(salary, other_income, rent, groceries, other_expenses, savings, month_year, user_id, comments)" "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        data = (incomes['Salary'], incomes['Other Income'], expenses['Rent'], expenses['Groceries'], expenses['Other Expenses'], expenses['Savings'], period, userId, comment )
        mycursor.execute(insert_stmt, data)
        mydb.commit()
        if data:    
            st.success("Data saved!")
    elif type == 'update':
        print ("ddddddddddd")
        sql = "UPDATE savings SET salary = %s, other_income = %s, rent = %s, groceries = %s,  other_expenses = %s, savings = %s, comments = %s WHERE id = %s"
        val = (incomes['Salary'], incomes['Other Income'], expenses['Rent'], expenses['Groceries'], expenses['Other Expenses'], expenses['Savings'], comment, id)

        mycursor.execute(sql, val)

        mydb.commit()

        return True



    # except Exception as e:
    #     st.error(e.args)

def get_data_period(period, username):
    #print(period, username)
    try:
        sql = "SELECT * FROM users WHERE email = %s;"
        adr = (username,)
        mycursor.execute(sql, adr)
        # #print(mycursor.fetchall()[0]['id'],">>>>>>>>>>>>>>>>>>>>>>")
        userId = mycursor.fetchall()[0]['id']
        #print(userId,"uer")
        sql = "SELECT * FROM savings WHERE user_id = %s and month_year = %s;"
        adr = (userId,period)
        mycursor.execute(sql, adr)
        data = mycursor.fetchone()
        #print(data,"ddddddddddddddddddddddddddddd")
        return data
    except Exception as e:
        #print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        st.error(e)
    # st.write(mycursor.fetchall())

def updatePassword(email,password):
    #print(email,"EEEEEEEEEEEEEEEEEEEEEEEEEEe")
    try:
        newPassword = stauth.Hasher([password]).generate()
        # st.write(newPassword[0], password,bcrypt.checkpw(password.encode(),newPassword[0].encode()))
        # h = '$2b$12$qKUPeDdgGPwpXdURs9T8BeuNChgzl3oK92z7zrjm0qoklux3YzfTW'
        # p = 'Techv1@3'
        # st.write( bcrypt.checkpw(p.encode(),h.encode()),"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")

        sql = "UPDATE users SET password = %s WHERE email = %s"
        val = (newPassword[0], email)

        mycursor.execute(sql, val)

        mydb.commit()
        st.write(mycursor.rowcount)

        return True
    except Exception as e:
        st.error(e)
# self.password.encode(), 
#             self.credentials['usernames'][self.username]['password'].encode()
        


        
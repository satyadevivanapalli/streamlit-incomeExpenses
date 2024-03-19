import streamlit as st
import streamlit_authenticator as stauth
# from dependancies import sign_up, fetch_users
from dependancies import fetch_users, sign_up
st.set_page_config(page_title='Streamlit', page_icon='🐍', initial_sidebar_state='collapsed')

try:
    sign_up()
    # credentials = {}
    # Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)
    # username, authentication_status, email = Authenticator.forgot_password('sidebar')
except Exception as e:
    st.error(e)
# import smtplib
# import streamlit as st


# import string
# import random

# def generate_random_pw(length: int=16) -> str:
#     letters = string.ascii_letters + string.digits
#     return ''.join(random.choice(letters) for i in range(length)).replace(' ','')

# st.write(generate_random_pw())

# server = smtplib.SMTP('smtp.gmail.com',587)
# server.starttls()
# server.login("streamlitsatya@gmail.com", 'nevb ahzo ehby gcrt')
# server.sendmail('streamlitsatya@gmail.com','streamlitsatya@gmail.com',"HHHHHHHHHHHHHHHHHH")
# print("generate_random_pw")


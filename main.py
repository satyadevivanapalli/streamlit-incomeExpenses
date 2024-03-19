import streamlit as st
import streamlit_authenticator as stauth
# from dependancies import sign_up, fetch_users
from dependancies import fetch_users, sign_up
st.set_page_config(page_title='Streamlit', page_icon='🐍', initial_sidebar_state='collapsed')


 
# with tab3:
#     st.header('Topic C')
#     st.write('Topic C content')


try:
    users = fetch_users()
    # print(users)
    emails = []
    usernames = []
    passwords = []
    for user in users:
        # print(user)
        emails.append(user[1])
        usernames.append(user[2])
        passwords.append(user[3])
        # print(emails, usernames, passwords)
    credentials = {'usernames': {}}
    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

    # # Add content to each tab
    # authentication_status = ''
    # Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)
    # email, authentication_status, username = Authenticator.login('main')
    # if authentication_status:
    #     pass
    # else:
    #     tab_titles = ['Login', 'Registration']
    #     tab1, tab2 = st.tabs(tab_titles)
    #     st.markdown("""
    # <style>

    #     .stTabs [data-baseweb="tab-list"] {
    #         gap: 2px;
    #     }

    #     .stTabs [data-baseweb="tab"] {
    #         height: 50px;
    #         white-space: pre-wrap;
    #         border-radius: 4px 4px 0px 0px;
    #         gap: 1px;
    #         padding-top: 10px;
    #         padding-bottom: 10px;
    #         margin-left:10%

    #     }

    #     .stTabs [aria-selected="true"] {
    #         background-color: #FFFFFF;
    #     }
    #     .st-emotion-cache-gielgn p { font-size: 25px }
    # .stTabs [data-baseweb="tab-list"] {
    #                 gap: 25%
    # }

    # </style>""", unsafe_allow_html=True)

    #     with tab1:
    #         'ssss' 
        
    #     with tab2:
    #         sign_up()
    print(credentials)
    st.write(credentials)
    

    Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)
    email, authentication_status, username = Authenticator.login('main')
    # email, authentication_status, username = Authenticator.login(':green[Login]', 'main')
    info, info1 = st.columns(2)

    if not authentication_status:
        sign_up()
        st.checkbox("already have account")
    if username:
        if username in usernames:
            if authentication_status:
                st.markdown("""
<style>

	.stTabs{
		visibility: hidden
    }
</style>""", unsafe_allow_html=True)
                # let User see app
                st.sidebar.subheader(f'Welcome {username}')
                Authenticator.logout('Log Out', 'sidebar')

                st.subheader('This is the home page')
                st.markdown(
                    """
                    ---
                    Created with ❤️ by SnakeByte
                    
                    """
                )

            elif not authentication_status:
                with info:
                    st.error('Incorrect Password or username')
            else:
                with info:
                    st.warning('Please feed in your credentials')
        else:
            with info:
                st.warning('Username does not exist, Please Sign up')






except Exception as e:
    st.error(e)

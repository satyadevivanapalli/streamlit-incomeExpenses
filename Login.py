import bcrypt
import streamlit as st
import streamlit_authenticator as stauth
# from dependancies import sign_up, fetch_users
from dependancies import fetch_users, sign_up, insert_period, get_data_period, updatePassword

import calendar  # Core Python Module
from datetime import datetime  # Core Python Module

import plotly.graph_objects as go  # pip install plotly
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
import time

import streamlit.components.v1 as components
import matplotlib.pyplot as plt

import plotly.express as px
import json
import webbrowser

import pandas as pd


# -------------- SETTINGS --------------
incomes = ["Salary", "Other Income"]
expenses = ["Rent", "Groceries" , "Other Expenses", "Savings"]
currency = "Rupees"
page_title = "Income and Expense Tracker"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
# # --------------------------------------
# st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
# conn = st.connection('mysql', type='sql', autocommit=True)
# st.write(conn,"+++++++++++++++++++++++=")



# --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
years = [datetime.today().year, datetime.today().year + 1]
months = tuple(calendar.month_name[1:])
with open('data.json', 'r') as file:
    data = json.load(file)

# st.markdown("""
#     <style>
#         .st-emotion-cache-1qqhz9z {
#             padding-top:1rem !important;
#         }

#     </style>""", unsafe_allow_html=True)


# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Replace the chart with several elements:

def resetPassowrd(userPwd, email):
    with st.sidebar.form('reset_password',clear_on_submit=False):
            st.subheader('Rest Password')
            password = st.text_input('Current password', placeholder='Current password', type='password', key = 'current_password')
            new_password = st.text_input('New password', placeholder='New password', type='password', key = 'new_password')
            new_password_repeat = st.text_input('Repeat password', placeholder='Repeat password', type='password', key = 'repeat_password')
            
            
            if st.form_submit_button('Reset Password'):
                if not password:
                    st.error("please enter current password")
                elif not new_password:
                    st.error("please enter New password")
                elif not new_password_repeat:
                    st.error("please enter Repeat password")
                elif new_password != new_password_repeat:
                    st.error('New and current passwords are the same')
                elif bcrypt.checkpw(password.encode(),userPwd.encode()):
                    if len(new_password) >= 6:
                        # st.write( bcrypt.checkpw(password.encode(),userPwd.encode()),"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
                        update = updatePassword(email,new_password)
                        if update:
                            st.success("Password updated successfully")
                            st.write(st.session_state.current_password)
                            st.session_state.current_password = ''
                            # st.session_state['new_password'] = ''
                            # st.session_state['repeat_password'] = ''
                    else:
                        st.warning('Password is too Short')
                else:
                        st.warning('current Password is not valid')

    
def ChangeButtonColour(widget_label, font_color, background_color='transparent'):
    htmlstr = f"""
        <script>
            var elements = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < elements.length; ++i) {{ 
                if (elements[i].innerText == '{widget_label}') {{ 
                    elements[i].style.color ='{font_color}';
                    elements[i].style.background = '{background_color}'
                }}
            }}
        </script>
        """
    components.html(f"{htmlstr}", height=0, width=0)

def change_name(name):
    st.session_state['button'] = name
def dataVisualization():
    Income = ['Salary', 'Other Income']
    amount = [4500, 2500]
    colors=['green', 'rosybrown', 'black', 'yellow']

    cols = st.columns([1, 1],gap='large')

    data = get_data_period(str(year) + "_" + str(month), email)

    if (data):
        # st.write(data)
        with cols[0]:
            incomeLables = ['salary','other income']
            incomeValues = [data['salary'], data['other_income']]
            # st.write(incomeLables, incomeValues)
            fig = px.pie(values=incomeValues, names=incomeLables,
                        title= 'Income Chart',
                        height=500, width=600,color_discrete_sequence=colors)
            fig.update_layout(margin=dict(l=20, r=20, t=30, b=20),font=dict(color='red', size=15))
            st.plotly_chart(fig, use_container_width=True)
        with cols[1]:
            # st.write("Expenses Chart")
            expenseLables = ['rent','groceries', 'other_expenses', 'savings']
            expenseValues = [data['rent'], data['groceries'], data['other_expenses'], data['savings']]
            fig1 = px.pie(values=expenseValues, names=expenseLables,
                        title= 'Expense Chart',
                        height=500, width=600,color_discrete_sequence=colors)
            fig1.update_layout(margin=dict(l=20, r=20, t=30, b=20),font=dict(color='red', size=15))
            st.plotly_chart(fig1, use_container_width=True)

try:
    
    # st.sidebar.w(f'Welcome {email}')

    users = fetch_users()
    ##print(users)
    emails = []
    usernames = []
    passwords = []
    #print(users,"UUUUUUUUUUUUUUUUU")
    # for user in users:
    #     ##print(user,"LLL")
    #     emails1.append(user[1])
    #     usernames1.append(user[2])
    #     passwords1.append(user[3])
    for user in users:
        # ##print(user)
        emails.append(user['email'])
        usernames.append(user['userName'])
        passwords.append(user['password'])
    ##print(emails,":::::::::::")
    ##print(usernames,"usernames")

    ##print(passwords,"password")

    # ##print(emails1, usernames1, passwords1,">>>>>>>>>>>>>>>>")

    credentials = {'usernames': {}}
    for index in range(len(emails)):
        credentials['usernames'][emails[index]] = {'name': usernames[index], 'password': passwords[index]}

    Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)
    username, authentication_status, email = Authenticator.login('main')
    if not authentication_status:
        c1, c2,c3,c4 = st.columns(4)
        # c1, c2 = st.columns([.5,1])
        # col1, col2 = st.beta_columns([.5,1])


        # st.write("[Forgot Password](/Forgot_Password)")
        with c1:
            st.write('<a href="/Forgot_Password" target="_self" style="color: white">Forgot Password</a>', unsafe_allow_html=True)
        with c2:
            st.write('<a href="/Signup" target="_self" style="color: white">Create account</a>', unsafe_allow_html=True)
    
    # email, authentication_status, username = Authenticator.login(':green[Login]', 'main')
    info, info1 = st.columns(2)
    # st.write('<a href="/Reset_Password" target="_self">Reset Password</a>', unsafe_allow_html=True)
    # st.write("<a href='#' id='Reset Password'>Reset Password</a>", unsafe_allow_html=True)

    # if st.button("Reset Password"):

    #print(username, authentication_status, email,"LLLLLLLLLLLLLLL", credentials)
    
    # if st.session_state["authentication_status"]:
    #     if Authenticator.reset_password(st.session_state["username"]):
    #         st.success('Password modified successfully')
        

    # st.write(st.session_state)
    ##print(usernames,"UUUUUUUUUUUUUUU")
    if email:
        if email in emails:
            if authentication_status:
                st.sidebar.subheader(f'Welcome {email}')
                #print(st.session_state,"??????????????????????",credentials)
                # st.write(credentials['usernames'][email])
                resetPassowrd(credentials['usernames'][email]['password'], email)
                Authenticator.logout('Log Out', 'sidebar')

                # data = Authenticator.reset_password('Rest Password',"sidebar")
                
                st.markdown("""
    <style>

        .st-emotion-cache-79elbk {
            visibility:hidden !important;
            height:0px;
        }
        .st-emotion-cache-1y4p8pa {
                            padding-top:0px !important;
        }

    </style>""", unsafe_allow_html=True)

                st.title(page_title + " " + page_icon)

                # --- NAVIGATION MENU ---
                selected = option_menu(
                    menu_title=None,
                    options=["Data Entry", "Data Visualization"],
                    icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
                    orientation="horizontal",
                )
                

                options = list(range(len(months)))
                # st.write( months)
                
                # value = st.selectbox("Select Month", options, format_func=lambda x: months[x], key="month")
                col1, col2 = st.columns(2)
                month = col1.selectbox("Select Month", months, key="months")
                year = col2.selectbox("Select Year:", years, key="year")
                if selected == "Data Entry":
                    
                        
                    # st.header(f"Data Entry in {currency}")
                    details = []
                    details = get_data_period(str(year) + "_" + str(month), email)
                    if details:
                        details['Salary'] = details['salary']
                        details['Other Income'] = details['other_income']
                        details['other expenses'] = details['other_expenses']
                        totalIncome = details['salary'] + details['other_income']
                        totalExpenses = details['rent'] + details['groceries'] + details['other_expenses'] + details['savings']
                        # st.write('Total Income: ', f"{totalIncome:,}", u'\u20B9')
                        # st.write('Total Expenses: ', f"{totalExpenses:,}", u'\u20B9')
                        # st.write('Balance: ', f"{(totalIncome - totalExpenses):,}", u'\u20B9')
                        # st.write("Comments: ", details['comments'])
                        totalIncomeText = st.empty()
                        totalExpensesText = st.empty()
                        balanceText = st.empty()
                        commentText = st.empty()
                        Incometext = 'Total Income: ' + f"{totalIncome:,}" + u'\u20B9'
                        expensestext = 'Total Expenses: ' + f"{totalExpenses:,}" + u'\u20B9'
                        commentT = "Comments: " + details['comments']
                        balanceT = 'Balance: ' + f"{(totalIncome - totalExpenses):,}" + u'\u20B9'
                        # Replace the placeholder with some text:
                        totalIncomeText.write(Incometext)
                        totalExpensesText.write(expensestext)
                        balanceText.write(balanceT)
                        commentText.write(commentT)

                    with st.form("entry_form"):
                        if details and len(details.keys()) > 0:
                            with st.expander("Income", expanded=True):
                                for income in incomes:
                                    ##print(income)
                                    st.number_input(f"{income}:", min_value=0, format="%i", step=10, key=income, value=details[income])

                            with st.expander("Expenses", expanded=True):
                                for expense in expenses:
                                    st.number_input(f"{expense}:", min_value=0, format="%i", step=10, key=expense, value=details[expense.lower()])
                            with st.expander("Comment", expanded=True):
                                comment = st.text_area("",value=details['comments'], placeholder="Enter a comment here ...")
                        else:
                            with st.expander("Income"):
                                for income in incomes:
                                    st.number_input(f"{income}:", min_value=0, format="%i", step=10, key=income)
                            with st.expander("Expenses"):
                                for expense in expenses:
                                    st.number_input(f"{expense}:", min_value=0, format="%i", step=10, key=expense)
                            with st.expander("Comment"):
                                comment = st.text_area("", placeholder="Enter a comment here ...")

                        "---"
                        submitted = False
                        submitted = st.form_submit_button("Update Entry") if (details and len(details.keys()) > 0) else st.form_submit_button("Add Entry")
                        if submitted:
                            with st.spinner('Wait for it...'):
                                st.write(st.session_state)
                                period = str(year) + "_" + str(month)
                                incomes = {income: st.session_state[income] for income in incomes}
                                expenses = {expense: st.session_state[expense] for expense in expenses}

                                if details: 
                                    updated = insert_period(period, incomes, expenses,comment, email, "update", details['id'])
                                    if updated:
                                        with totalIncomeText.container():
                                            totalIncome = st.session_state['Salary'] + st.session_state['Other Income']
                                            text = 'Total Income: ' + f"{totalIncome:,}" + u'\u20B9'
                                            st.write(text)
                                        with totalExpensesText.container():                                        
                                            totalExpenses = st.session_state['Rent'] + st.session_state['Groceries'] + st.session_state['Other Expenses'] + st.session_state['Savings']
                                            expensestext = 'Total Expenses: ' + f"{totalExpenses:,}" + u'\u20B9'
                                            st.write(expensestext)
                                        with balanceText.container():
                                            balanceT = 'Balance: ' + f"{(totalIncome - totalExpenses):,}" + u'\u20B9'
                                            st.write(balanceT)
                                        with commentText.container():
                                            st.write("Comments: ", comment)


                                else:
                                    insert_period(period, incomes, expenses,comment, email, "new",0)
                                time.sleep(1)

                        else:
                            print("KKKKKKKKKKKKKKKKKKKK")
                if selected == "Data Visualization":
                    # st.header("Data Visualization")
                    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
                    # labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
                    # sizes = [15, 30, 45, 10]
                    # explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

                    # fig1, ax1 = plt.subplots()
                    # ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                    #         shadow=True, startangle=90)
                    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                    # st.pyplot(fig1)
                    
                    dataVisualization()
                    # pie_chart_data = data['pie_chart']
                    # plt.pie(pie_chart_data['sizes'], labels=pie_chart_data['labels'], colors='#000000')
                    # st.pyplot( plt )



                    # with st.form("saved_periods"):
                    #     # period = st.selectbox("Select Period:", get_all_periods())
                    #     submitted = st.form_submit_button("Plot Period")


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


# def getPeriod():
#     st.write(st.session_state["month"],">>>>")


def generate_key(icon, button_key):
    key_dict = {}
    key_dict[button_key] = icon
    return {'label':button_key,'key':button_key}



# def getDetails():
#     #print("ll")
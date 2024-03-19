import streamlit as st
import streamlit_authenticator as stauth
# from dependancies import sign_up, fetch_users
from dependancies import fetch_users, sign_up, insert_period, get_data_period

import calendar  # Core Python Module
from datetime import datetime  # Core Python Module

import plotly.graph_objects as go  # pip install plotly
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
import time

import streamlit.components.v1 as components




# -------------- SETTINGS --------------
incomes = ["Salary", "Other Income"]
expenses = ["Rent", "Groceries" , "Other Expenses", "Savings"]
currency = "Rupees"
page_title = "Income and Expense Tracker"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
# --------------------------------------
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)


# --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
years = [datetime.today().year, datetime.today().year + 1]
months = tuple(calendar.month_name[1:])



# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

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

try:
    users = fetch_users()
    #print(users)
    emails = []
    usernames = []
    passwords = []
    print(users,"UUUUUUUUUUUUUUUUU")
    # for user in users:
    #     #print(user,"LLL")
    #     emails1.append(user[1])
    #     usernames1.append(user[2])
    #     passwords1.append(user[3])
    for user in users:
        # #print(user)
        emails.append(user['email'])
        usernames.append(user['userName'])
        passwords.append(user['password'])
    #print(emails,":::::::::::")
    #print(usernames,"usernames")

    #print(passwords,"password")

    # #print(emails1, usernames1, passwords1,">>>>>>>>>>>>>>>>")

    credentials = {'usernames': {}}
    for index in range(len(emails)):
        credentials['usernames'][emails[index]] = {'name': usernames[index], 'password': passwords[index]}
    #print(credentials,"cccccccccccccccccc")

    Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)
    username, authentication_status, email = Authenticator.login('sidebar')
    print(username, authentication_status, email,"LLLLLLLLLLLLLLL")
    # email, authentication_status, username = Authenticator.login(':green[Login]', 'main')
    info, info1 = st.columns(2)
    #print(usernames,"UUUUUUUUUUUUUUU")
    if email:
        if email in emails:
            if authentication_status:
                st.sidebar.subheader(f'Welcome {email}')
                Authenticator.logout('Log Out', 'sidebar')
                st.markdown("""
    <style>

        .st-emotion-cache-79elbk {
            visibility:hidden !important
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
                        print(details,">>>")
                        print(u'\u20B9')

                        details['Salary'] = details['salary']
                        details['Other Income'] = details['other_income']
                        details['other expenses'] = details['other_expenses']
                        totalIncome = details['salary'] + details['other_income']
                        totalExpenses = details['rent'] + details['groceries'] + details['other_expenses'] + details['savings']
                        st.write('Total Income: ', f"{totalIncome:,}", u'\u20B9')
                        st.write('Total Expenses: ', f"{totalExpenses:,}", u'\u20B9')
                        st.write('Balance: ', f"{(totalIncome - totalExpenses):,}", u'\u20B9')
                        st.write("Comments: ", details['comments'])
                        totalIncome = 6666
                    with st.form("entry_form"):
                        if details and len(details.keys()) > 0:
                            with st.expander("Income", expanded=True):
                                for income in incomes:
                                    #print(income)
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
                            period = str(year) + "_" + str(month)
                            incomes = {income: st.session_state[income] for income in incomes}
                            expenses = {expense: st.session_state[expense] for expense in expenses}
                            if details: 
                                insert_period(period, incomes, expenses,comment, email, "update", details['id'])
                            else:
                                insert_period(period, incomes, expenses,comment, email, "new")
                            
                        else:
                            print("KKKKKKKKKKKKKKKKKKKK")
                if selected == "Data Visualization":
                    st.header("Data Visualization")
                    with st.form("saved_periods"):
                        # period = st.selectbox("Select Period:", get_all_periods())
                        submitted = st.form_submit_button("Plot Period")


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



def getDetails():
    print("ll")
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
users = fetch_users()
emails = []
usernames = []
passwords = []

for user in users:
    emails.append(user['email'])
    usernames.append(user['userName'])
    passwords.append(user['password'])

def loginSignup():
    try:
        credentials = {'usernames': {}}
        for index in range(len(emails)):
            credentials['usernames'][emails[index]] = {'name': usernames[index], 'password': passwords[index]}
        Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)
        username, authentication_status, email = Authenticator.login('sidebar')
        info, info1 = st.columns(2)
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
                    selected = option_menu(
                        menu_title=None,
                        options=["Data Entry", "Data Visualization"],
                        icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
                        orientation="horizontal",
                    )

                    options = list(range(len(months)))
                    col1, col2 = st.columns(2)
                    month = col1.selectbox("Select Month", months, key="months")
                    year = col2.selectbox("Select Year:", years, key="year")
                    if selected == "Data Entry":
                        details = []
                        details = get_data_period(str(year) + "_" + str(month), email)
                        if details:
                            updateDataEntry(month, year, email, details)
                        else:
                            details = {}
                            details['salary'] = 1000
                            # updateDataEntry(month, year, email, details)
    except Exception as e:
        st.error(e)

def updateText(details):
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
def updateDataEntry(month, year, email,details):
    updateText(details)
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
        

        "---"
        submitted = False
        submitted = st.form_submit_button("Update Entry") if (details and len(details.keys()) > 0) else st.form_submit_button("Add Entry")
        if submitted:
            period = str(year) + "_" + str(month)
            incomes1 = {income: st.session_state[income] for income in incomes}
            expenses1 = {expense: st.session_state[expense] for expense in expenses}
            if details: 
                insert_period(period, incomes1, expenses1,comment, email, "update", details['id'])
                details = get_data_period(str(year) + "_" + str(month), email)
                updateText(details)
            else:
                insert_period(period, incomes1, expenses1,comment, email, "new")
    
if __name__ == "__main__": 
    loginSignup()

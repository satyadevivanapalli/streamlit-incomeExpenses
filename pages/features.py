import plotly.express as px
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


data = {
    'Income': ['Salary', 'Other Income'],
    'gold': [100000, 56000],
    'silver': [4,4],
    'bronze': [8, 2],
    'sum': [24, 7]
}
Income = ['Salary', 'Other Income']
amount = [4500, 2500]


df = pd.DataFrame(data)
st.dataframe(df)
print(px.colors.sequential.RdBu,"???????????????????")

cols = st.columns([1, 1])
colors=['green', 'rosybrown', 'gray', 'saddlebrown']
with cols[0]:
    medal_type = st.selectbox('Medal Type', ['gold', 'silver', 'bronze'])
    print(medal_type)
    fig = px.pie(df, values=amount, names=Income,
                 title=f'number of {medal_type} medals',
                 height=400, width=500,color_discrete_sequence=colors)
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20),paper_bgcolor='yellow', font=dict(color='red', size=30))
    st.plotly_chart(fig, use_container_width=True)


with cols[1]:
    st.text_input('sunburst', label_visibility='hidden', disabled=True)
    fig2 = px.pie(df, values=['ctry', 'gold', 'silver', 'bronze'],
                      height=300, width=200)
    fig2.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
    st.plotly_chart(fig2, use_container_width=True)

fig3 = px.pie(values = [20, 50, 37, 18],
             names = ['G1', 'G2', 'G3', 'G4'],
             color = ['G1', 'G2', 'G3', 'G4'],
             color_discrete_map = {'G1': '#30BFDD',
                                   'G2': '#8690FF',
                                   'G3': '#ACD0F4', 
                                   'G4': '#F7C0BB'})


# df_hire_status = pd.DataFrame(data)

# colours = {'status 1': 'rgb(43, 182, 94)',      #2BB65E
#                    'status 2': 'rgb(0, 143, 245)',      #008FF5
#                    'status 3' : 'rgb(242,233,78)',     #F2E94E
#                    'status 4' : 'rgb(205,20,28)',       #CD141C
#                    'status 5' : 'rgb(255,147,2)'        #FF9302
#                   }
# data['status_pie'] = px.pie(df_hire_status,
#                               values ='plant_id',
#                               color = 'colors',
#                               color_discrete_map = colours,
#                               names = 'hire_status'
#                              )

# st.write(px)



labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]

# fig, ax = plt.subplots()
# ax.pie(sizes, labels=labels)

# fig, ax = plt.subplots()
# ax.pie(sizes, labels=labels, autopct='%1.1f%%',
#        pctdistance=1.25, labeldistance=.6)
# st.write(fig)

# explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

# fig, ax = plt.subplots()
# ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
#        shadow=True, startangle=90)
# plt.show()
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels,
       colors=['olivedrab', 'rosybrown', 'gray', 'saddlebrown'])
st.write(fig)

df = px.data.tips()
print(px.data.tips())
fig = px.pie(df, values='tip', names='day',color_discrete_sequence=px.colors.sequential.RdBu)
# fig.show()
st.write(fig)
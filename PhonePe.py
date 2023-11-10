import streamlit as st
import git
import os
import json
import pandas as pd
import pymysql
import requests
import plotly.express as px
from streamlit_option_menu import option_menu
import warnings
warnings.filterwarnings(action = 'ignore')

layout="wide"
initial_sidebar_state="expanded"
primaryColor= "#739192"
backgroundColor="#D9E7EA"
secondaryBackgroundColor="#5B8E90"
textColor="#0E0E0E"
font="serif"


# SQL Connections
myconnection = pymysql.connect(host = '127.0.0.1',user='root',passwd='Logi@2908',database = "PhonePe")
cur = myconnection.cursor()
cur.execute("USE PhonePe")


# def functions
def Aggregated_Trans():
    path = "C:/Users/Logambal/Desktop/Phonepe-Project/pulse/data/aggregated/transaction/country/india/state/"

    agg_state_list = os.listdir(path)

    data = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_Type': [],'Transaction_Count': [], 'Transaction_Amount': []}

    for i in agg_state_list:
        path_i = path +i +'/'                
        agg_year_list = os.listdir(path_i)      
        for j in agg_year_list:
            path_j = path_i + j +'/'       
            agg_year_json = os.listdir(path_j)  

            for k in agg_year_json:
                path_k = path_j + k            
                f = open(path_k, 'r')
                d = json.load(f)

                for z in d['data']['transactionData']:
                        name = z['name']
                        count = z['paymentInstruments'][0]['count']
                        amount = z['paymentInstruments'][0]['amount']

                        data['State'].append(i)
                        data['Year'].append(j)
                        data['Quarter'].append('Q'+str(k[0]))
                        data['Transaction_Type'].append(name)
                        data['Transaction_Count'].append(count)
                        data['Transaction_Amount'].append(amount)

    return data
# def function for Aggregated User
def Aggregated_User():
    path_1 = "C:/Users/Logambal/Desktop/Phonepe-Project/pulse/data/aggregated/user/country/india/state/"
    agg_state_list = os.listdir(path_1)
    data1 = {'State': [], 'Year': [], 'Quarter': [], 'User_Brand': [], 'User_Count': [], 'User_Percentage': []}
    for i in agg_state_list:
        path_i = path_1 + i + '/'
        agg_year_list = os.listdir(path_i)

        for j in agg_year_list:
            path_j = path_i + j + '/'
            agg_year_json = os.listdir(path_j)

            for k in agg_year_json:
                path_k = path_j + k
                f = open(path_k, 'r')
                d1 = json.load(f)
                try:
                    for z in d1['data']['usersByDevice']:
                        brand = z['brand']
                        count = z['count']
                        percentage = z['percentage']*100

                        data1['State'].append(i)
                        data1['Year'].append(j)
                        data1['Quarter'].append('Q'+str(k[0]))
                        data1['User_Brand'].append(brand)
                        data1['User_Count'].append(count)
                        data1['User_Percentage'].append(percentage)
                except:
                    pass
        return data1        
# def function for Map Trans
def Map_Trans():
    path_2="C:/Users/Logambal/Desktop/Phonepe-Project/pulse/data/map/transaction/hover/country/india/state/"
    map_trans_list=os.listdir(path_2)
    data2= {'State': [], 'Year': [], 'Quarter': [],'District_Name':[],'District_Count':[],'District_Amount':[]}
    for i in map_trans_list:
        path_i=path_2 + i +'/'
        map_year_list=os.listdir(path_i)
        for j in map_year_list:
            path_j=path_i + j + '/'
            map_json_list=os.listdir(path_j)
            for k in map_json_list:
                path_k=path_j + k
                f = open(path_k, 'r')
                d2 = json.load(f)
                for z in d2['data']['hoverDataList']:
                    name =z['name'].split(' district')[0]
                    count=z['metric'][0]['count']
                    amount=z['metric'][0]['amount']

                    data2['State'].append(i)
                    data2['Year'].append(j)
                    data2['Quarter'].append('Q'+str(k[0]))
                    data2['District_Name'].append(name)
                    data2['District_Count'].append(count)
                    data2['District_Amount'].append(amount)
    return data2
#  def function Map User
def Map_User():
    path_3 = "C:/Users/Logambal/Desktop/Phonepe-Project/pulse/data/map/user/hover/country/india/state/"
    map_user_list = os.listdir(path_3)

    data3 = {'State': [], 'Year': [], 'Quarter': [], 'District_Name': [], 'Registered_User': [], 'App_Opens': []}

    for i in map_user_list:
        path_i = path_3 + i + '/'
        map_year_list = os.listdir(path_i)

        for j in map_year_list:
            path_j = path_i + j + '/'
            map_year_json = os.listdir(path_j)

            for k in map_year_json:
                path_k = path_j + k
                f = open(path_k, 'r')
                d3 = json.load(f)

                for z_key, z_value in d3['data']['hoverData'].items():
                    district = z_key.split(' district')[0]
                    reg_user = z_value['registeredUsers']
                    app_opens = z_value['appOpens']

                    data3['State'].append(i)
                    data3['Year'].append(j)
                    data3['Quarter'].append('Q'+str(k[0]))
                    data3['District_Name'].append(district)
                    data3['Registered_User'].append(reg_user)
                    data3['App_Opens'].append(app_opens)
    return data3
# def function for Top Trans
def Top_Trans():
    path_4="C:/Users/Logambal/Desktop/Phonepe-Project/pulse/data/top/transaction/country/india/state/"
    top_trans_list=os.listdir(path_4)

    data4 = {'State': [], 'Year': [], 'Quarter': [], 'District_Name': [],'Transaction_Count': [], 'Transaction_Amount': []}
    for i in top_trans_list:
        path_i = path_4 + i + '/'
        top_year_list=os.listdir(path_i)

        for j in top_year_list:
            path_j = path_i + j + '/'
            top_json_list = os.listdir(path_j)

            for k in top_json_list:
                path_k = path_j + k
                f = open(path_k,'r')
                d4 = json.load(f)

                for z in d4['data']['districts']:
                    name = z['entityName']
                    count = z['metric']['count']
                    amount = z['metric']['amount']


                    data4['State'].append(i)
                    data4['Year'].append(j)
                    data4['Quarter'].append('Q'+str(k[0]))
                    data4['District_Name'].append(name)
                    data4['Transaction_Count'].append(count)
                    data4['Transaction_Amount'].append(amount)
                    
    return data4
# def function for Top User
def Top_User():
    path_5 = "C:/Users/Logambal/Desktop/Phonepe-Project/pulse/data/top/user/country/india/state/"
    top_user_list = os.listdir(path_5)

    data5 = {'State': [], 'Year': [], 'Quarter': [],'District_Name': [],'Registered_Users': []}

    for i in top_user_list:
        path_i = path_5 + i + '/'
        top_year_list = os.listdir(path_i)

        for j in top_year_list:
            path_j = path_i + j + '/'
            top_json_list = os.listdir(path_j)

            for k in top_json_list:
                path_k = path_j + k
                f = open(path_k,'r')
                d5 = json.load(f)

                for z in d5['data']['districts']:
                    name = z['name']
                    user = z['registeredUsers']


                    data5['State'].append(i)
                    data5['Year'].append(j)
                    data5['Quarter'].append('Q' + str(k[0]))
                    data5['District_Name'].append(name)
                    data5['Registered_Users'].append(user)
                    
        return data5
    
with st.sidebar:
        SELECT = option_menu(None,
                options = ["🏡Home","⚙️Features","🌍Data Insights","🔚Exit"],
                default_index=0,
                orientation="vertical",
                styles={"container": {"width": "90%"},
                        "icon": {"color": "white", "font-size": "18px"},
                        "nav-link": {"font-size": "18px"}})
                       


if SELECT == "🏡Home":
    st.header("PulseViz: Unlocking PhonePe Insights")
    st.subheader("**Unlocking the Power of Data Insights**")
    st.write("Welcome to PhonePe Pulse Data Visualization and Exploration, your gateway to unravel the fascinating world of digital payments and consumer trends in India. Dive into the depths of data, harness the power of insights, and embark on a journey that transforms raw information into actionable knowledge")

    st.subheader("**The Pulse of Digital Payments**")
    st.write("PhonePe Pulse is a repository of invaluable data, offering a real-time glimpse into how millions of people across India are engaging with digital payments. Our tool empowers you to make sense of this data, unleashing its potential for your specific needs.")

    st.subheader("**How to Get Started**")
    st.write("Using our tool is a breeze. Navigate through the sidebar options to uncover the data, tailor your visualizations, and gather actionable insights that inform your decisions.Ready to embark on your journey? Click **Features** to explore the multitude of tools waiting at your fingertips!")

elif SELECT == "⚙️Features":
    st.subheader('Exploring Essential Data Dimensions:')
    st.write('Discover the foundational data dimensions that serve as the backbone of PhonePe Pulse insights.')
    st.markdown("""
        - **Geographic Scope:** Unlock insights from across all states in India.
        - **Temporal Analysis:** Dive into the past and future with data spanning from 2018 to 2023.
        - **Quarterly Insights:** Explore data through the lens of quarters, from Q1 (Jan to Mar) to Q4 (Oct to Dec).""")
    
    st.subheader('Transaction Insights: Diving Deeper:')
    st.write('Take a deep dive into the world of digital transactions at the state level, segmented by diverse payment types.')
    st.markdown("""
    - **Recharge & Bill Payments:** Uncover trends in recharges and bill payments.
    - **Peer-to-Peer Payments:** Explore the dynamics of person-to-person transactions.
    - **Merchant Payments:** Investigate the world of merchant payments and commerce.
    - **Financial Services:** Delve into financial service transactions.
    - **Others:** Discover miscellaneous transaction types shaping India's digital landscape.""")

    st.subheader('State Wise User Insights by Device Brand:')
    st.write('Explore user data, segmented by popular device brands at the state level,Discover insights into user preferences with a range of device brands, including Apple, Samsung, Xiaomi, and more.')

    st.subheader('Mapping Transactions: Insights at a Glance')
    st.write('Visualize the complete landscape of digital transactions, both in terms of the total transaction count and the overall transaction value. Explore this data at both the state and district levels, gaining a bird eye view of India digital payment ecosystem.')
    st.subheader('User Mapping: Unveiling User Engagement')
    st.write('Peek into the realm of user engagement. Discover the total number of registered users and the frequency of app opens by these users at the state and district levels. This view provides essential insights into the ways users interact with digital payments across regions.')

    st.subheader('Uncover Top Transactions: Year-Quarter Edition')
    st.write('Intrigued by the most impactful transactions? This feature lets you explore the top transactions for a selected Year-Quarter combination. Dive into the data to uncover the top 10 states, districts, and pincodes that have witnessed significant transaction activity, offering you a precise understanding of regional payment trends.')
    st.subheader('Top User Insights: The Power of Numbers')
    st.write('User data can tell an insightful story. Identify the regions with the highest number of registered users for your chosen Year-Quarter combination. Explore the top 10 states, districts, and pincodes where user engagement is thriving, empowering you with valuable insights for decision-making and strategy development.')
    
elif SELECT == "🌍Data Insights":
    Option = st.sidebar.selectbox("Regional Insights Analysis", (None,"GitHub Data to DataFrame","State-Specific Exploration", "In-Depth District Analysis", "Leading Top Payment Categories"))
    if Option == "GitHub Data to DataFrame":
        tab1,tab2,tab3= st.tabs(["📍 State Wise Data", "📌 District Wise Data", "📊 Top Category"])
        with tab1:
                st.subheader("Aggregated Transaction")
                df = pd.DataFrame(Aggregated_Trans())
                st.dataframe(df)
                st.subheader("Aggregated User")
                df1 = pd.DataFrame(Aggregated_User())
                st.dataframe(df1)
        with tab2:
                st.subheader("Map Transaction")
                df2 = pd.DataFrame(Map_Trans())
                st.dataframe(df2)
                st.subheader("Map User")
                df3 = pd.DataFrame(Map_User())
                st.dataframe(df3)
        with tab3:
                st.subheader("Top Transcation")
                df4 = pd.DataFrame(Top_Trans())
                st.dataframe(df4)
                st.subheader("Top User")
                df5 = pd.DataFrame(Top_User())
                st.dataframe(df5)
      
    if Option == "State-Specific Exploration":
        tabs1,tabs2 = st.tabs(["Transaction Trends by State","User Behavior by State"])
        with tabs1:
            #Map or india(Aggregate Transaction)
            st.subheader("Geospatial Insights: Mapping Transaction Activity in India")
            cur.execute("SELECT State , SUM(Transaction_count) AS Total_Trans_Count, SUM(Transaction_amount) AS Total_Trans_Amount FROM aggregated_transaction GROUP BY State;")
            Map = cur.fetchall()
            Map_ToUse1 = pd.DataFrame(Map,columns=['State','Total_Trans_Count','Total_Trans_Amount'])
            Map_ToUse1.index=Map_ToUse1.index+1
            fig = px.choropleth(Map_ToUse1,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='Total_Trans_Amount',
            hover_data=['Total_Trans_Count', 'Total_Trans_Amount'], 
            labels={'Total_Trans_Amount': 'Total Amount', 'Total_Trans_Count': 'Total Count'},
            color_continuous_scale=['#116467','#0f5a5c','#0d5052','#0b4648','#0a3c3d','#083233','#062829','#116467','#287376','#408385','#589294','#70a2a3','#88b1b3', '#9fc1c2','#b7d0d1','#cfe0e0','#e7efef','#ffffff'])
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(
            width=100,  
            height=500)
            st.plotly_chart(fig,use_container_width=True)
            
            tabu1,tabu2 = st.tabs(["State_Wise Transaction Amount Trends","State_Wise Transaction Count Trends"])
            with tabu1:
                st.subheader("Bar Chart Of Transaction Amount Analysis")
                # Transaction Amount (Bar Chart)
                cur.execute("SELECT State, SUM(Transaction_amount) AS Total_Trans_Amount FROM aggregated_transaction GROUP BY State ORDER BY Total_Trans_Amount DESC;")
                BarChart1 = cur.fetchall()
                BarChart_ToUse1 = pd.DataFrame(BarChart1,columns=['State','Total_Trans_Amount'])
                fig = px.bar(BarChart_ToUse1, x="State", y="Total_Trans_Amount", title="State Vs Transaction Amount",color="State",
                            hover_data = ['State','Total_Trans_Amount'],labels={'Total_Trans_Amount':'Total_Transaction_Amount'})
                fig.update_traces(marker_color='teal') 
                fig.update_xaxes(title_font=dict(size=18, family='serif', color='black'), title_text='State')
                fig.update_yaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Total Transaction Amount')
                fig.update_layout(width=400,height=700)
                st.plotly_chart(fig,use_container_width=True)
                
                # Bar chart(for whole Transaction Type)
                st.subheader("Bar Chart For Total Transaction Type")
                cur.execute("SELECT Transaction_type, SUM(Transaction_amount) as Gtotal_trans_amount FROM aggregated_transaction GROUP BY Transaction_type ORDER BY Gtotal_trans_amount DESC;")
                BarChart2 = cur.fetchall()
                BarChart_ToUse2 = pd.DataFrame(BarChart2,columns=['Transaction_type','Gtotal_trans_amount'])
                fig = px.bar(BarChart_ToUse2, x="Transaction_type", y="Gtotal_trans_amount", title="Transaction Type Vs Total Transaction Amount",color="Transaction_type",
                            hover_data = ['Transaction_type','Gtotal_trans_amount'])
                fig.update_traces(marker_color='teal') 
                fig.update_xaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Transaction Type')
                fig.update_yaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Total Transaction Amount')
                fig.update_layout(width=10,height=500)
                st.plotly_chart(fig,use_container_width=True)
                
                # Transaction Type(Pie Chart)
                # opions
                st.subheader("Transaction Amount Analysis by Type")
                cols1, cols2, cols3 = st.columns(3)
                with cols1:
                    state = st.selectbox("Select A State",('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu',
                            'Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Lakshadweep','Ladakh','Madhya Pradesh',
                            'Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana',
                            'Tripura','Uttar Pradesh','Uttarakhand','West Bengal'), key="state1_select")
                with cols2:
                    year = st.selectbox("Select A Year",(2018,2019,2020,2021,2022,2023), key="year1_select")
                with cols3:
                    quarter = st.selectbox("Select A Quarter",("Q1","Q2","Q3","Q4"), key="quarter1_select")   
                #  Transaction Type(Dataframe) 
                cur.execute(f"SELECT State, Transaction_type, Transaction_amount FROM aggregated_transaction WHERE Quarter = '{quarter}'and State = '{state}' and year = '{year}';")
                dfs = cur.fetchall()
                dfs = pd.DataFrame(dfs,columns=['State','Transaction_type','Transaction_amount'])
                st.dataframe(dfs)
                #  Transaction Type(Pie Chart)
                cur.execute(f"SELECT Transaction_type, Transaction_amount FROM aggregated_transaction WHERE Quarter = '{quarter}'and State = '{state}' and year = '{year}';")
                PieChart2 = cur.fetchall()
                PieChart_ToUse2 = pd.DataFrame(PieChart2,columns=['Transaction_type','Transaction_amount'])
                colors =  ['mediumturquoise', 'teal', 'darkcyan', 'cadetblue', 'lightseagreen']
                fig = px.pie(PieChart_ToUse2, names="Transaction_type", values="Transaction_amount", title="Transaction Type Vs Transaction Amount",
                            color_discrete_sequence=colors)
                fig.update_traces(textposition='inside', textinfo='label+percent')
                fig.update_layout(width=300, height=400)
                st.plotly_chart(fig,use_container_width=True)


            with tabu2:
                # Transaction Count (Bar Chart)
                cur.execute("SELECT State,SUM(Transaction_count) AS Total_Trans_Count FROM aggregated_transaction GROUP BY State ORDER BY Total_Trans_Count DESC;")
                BarChart2 = cur.fetchall()
                BarChart_ToUse2 = pd.DataFrame(BarChart2,columns=['State','Total_Trans_Count'])
                fig = px.bar(BarChart_ToUse2, x="State", y="Total_Trans_Count", title="State Vs Transaction Count",color="State",
                            hover_data = ['State','Total_Trans_Count'],labels={'Total_Trans_Amount':'Total_Transaction_Count'})
                fig.update_xaxes(title_font=dict(size=18, family='serif', color='black'), title_text='State')
                fig.update_yaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Total Transaction Count')
                fig.update_traces(marker_color='teal') 
                fig.update_layout(width=400,height=700)
                st.plotly_chart(fig,use_container_width=True)
                # Bar Chart
                st.subheader("Bar Chart For Total Transaction Count Type")
                cur.execute("SELECT Transaction_type, SUM(Transaction_count) as Gtotal_trans_count FROM aggregated_transaction GROUP BY Transaction_type ORDER BY Gtotal_trans_count DESC;")
                BarChart2 = cur.fetchall()
                BarChart_ToUse2 = pd.DataFrame(BarChart2,columns=['Transaction_type','Gtotal_trans_count'])
                fig = px.bar(BarChart_ToUse2, x="Transaction_type", y="Gtotal_trans_count", title="Transaction Type Vs Total Transaction Count",color="Transaction_type",
                            hover_data = ['Transaction_type','Gtotal_trans_count'])
                fig.update_traces(marker_color='teal') 
                fig.update_xaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Transaction Type')
                fig.update_yaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Total Transaction Count')
                fig.update_layout(width=10,height=500)
                st.plotly_chart(fig,use_container_width=True)
                #  Transaction Type(Dataframe)
                st.subheader("Trasaction Count Analysis By Type")
                cols1, cols2, cols3 = st.columns(3)
                with cols1:
                    state = st.selectbox("Select A State",('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu',
                            'Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Lakshadweep','Ladakh','Madhya Pradesh',
                            'Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana',
                            'Tripura','Uttar Pradesh','Uttarakhand','West Bengal'), key="state2_select")
                with cols2:
                    year = st.selectbox("Select A Year",(2018,2019,2020,2021,2022,2023), key="year2_select")
                with cols3:
                    quarter = st.selectbox("Select A Quarter",("Q1","Q2","Q3","Q4"), key="quarter2_select") 
                st.subheader("Transaction Count Analysis by Type") 
                cur.execute(f"SELECT State, Transaction_type, Transaction_count FROM aggregated_transaction WHERE Quarter = '{quarter}'and State = '{state}' and year = '{year}';")
                dfs = cur.fetchall()
                dfs = pd.DataFrame(dfs,columns=['State','Transaction_type','Transaction_count'])
                st.dataframe(dfs)
                #  Transaction Type(Pie Chart)
                cur.execute(f"SELECT Transaction_type, Transaction_count FROM aggregated_transaction WHERE Quarter = '{quarter}'and State = '{state}' and year = '{year}';")
                PieChart2 = cur.fetchall()
                PieChart_ToUse2 = pd.DataFrame(PieChart2,columns=['Transaction_type','Transaction_count'])
                colors =['mediumturquoise', 'teal', 'darkcyan', 'cadetblue', 'lightseagreen']
                fig = px.pie(PieChart_ToUse2, names="Transaction_type", values="Transaction_count", title="Transaction Type Vs Transaction Count",
                            color_discrete_sequence=colors)
                fig.update_traces(textposition='inside', textinfo='label+percent')
                fig.update_layout(width=300, height=400)
                st.plotly_chart(fig,use_container_width=True)
        
        with tabs2:
            # Aggregated User (Map For India)
            st.subheader("Geospatial Insights: Mapping Users Activity in India")
            cur.execute("SELECT State, SUM(User_count) AS Gtotal_user_count, SUM(User_percentage) AS Gtotal_user_percentage FROM aggregated_user GROUP BY State ORDER BY Gtotal_user_count DESC;")
            Map = cur.fetchall()
            Map_ToUse1 = pd.DataFrame(Map,columns=['State','Gtotal_user_count','Gtotal_user_percentage'])
            Map_ToUse1.index=Map_ToUse1.index+1
            fig = px.choropleth(Map_ToUse1,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='State',
            hover_data=['Gtotal_user_count', 'Gtotal_user_percentage'], 
            labels={'Gtotal_user_count': 'Total User Count', 'Gtotal_user_percentage': 'Total User Percentage'},
            color_continuous_scale=['#116467','#0f5a5c','#0d5052','#0b4648','#0a3c3d','#083233','#062829','#116467','#287376','#408385','#589294','#70a2a3','#88b1b3', '#9fc1c2','#b7d0d1','#cfe0e0','#e7efef','#ffffff'])
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(
                            width=300,  
                            height=500)
            st.plotly_chart(fig,use_container_width=True)

            tabss1,tabss2=st.tabs(['State_Wise User Brand Trends','State_Wise User Count Trends'])
            with tabss1:            
                # Bar Chart (User Brand)
                cur.execute("SELECT User_brand, SUM(User_count) AS Total_User_count FROM aggregated_user GROUP BY User_brand ORDER BY Total_User_count DESC;")
                BarChart1 = cur.fetchall()
                BarChart_ToUse1 = pd.DataFrame(BarChart1,columns=['User_brand','Total_User_count'])
                fig = px.bar(BarChart_ToUse1, x="User_brand", y="Total_User_count", title="User brand Vs Total User count",color="User_brand",
                            hover_data = ['User_brand','Total_User_count'])
                fig.update_traces(marker_color='teal') 
                fig.update_xaxes(title_font=dict(size=18, family='serif', color='black'), title_text='User brand')
                fig.update_yaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Total User count')
                fig.update_layout(width=400,height=700)
                st.plotly_chart(fig,use_container_width=True)

                st.subheader("State-Wise User Brand Analysis")
                cols1, cols2, cols3 = st.columns(3)
                with cols1:
                    state = st.selectbox("Select A State",('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu',
                            'Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Lakshadweep','Ladakh','Madhya Pradesh',
                            'Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana',
                            'Tripura','Uttar Pradesh','Uttarakhand','West Bengal'), key="state3_select")
                with cols2:
                    Brand = st.selectbox("Select A Brand",('Xiaomi','Samsung','Vivo','Oppo','Others','Realme','Apple','Motorola','OnePlus','Huawei','Lenovo','Tecno','Micromax','Infinix','Asus','Gionee','Lava','HMD Global','Lyf','COOLPAD'))
                with cols3:
                    year = st.selectbox("Select A Year",(2018,2019,2020,2021,2022), key="year3_select")
                    
                #  Transaction Type(Dataframe) 
                cur.execute(f"SELECT State,Quarter, User_count FROM aggregated_user WHERE User_brand='{Brand}' and state='{state}' AND year = '{year}';")
                dfs = cur.fetchall()
                dfs = pd.DataFrame(dfs,columns=['State','Quarter','User_count'])
                st.dataframe(dfs)
                #  Transaction Type(Pie Chart)
                cur.execute(f"SELECT State,Quarter, User_count FROM aggregated_user WHERE User_brand='{Brand}' and state='{state}' AND year = '{year}';")
                PieChart2 = cur.fetchall()
                PieChart_ToUse2 = pd.DataFrame(PieChart2,columns=['State','Quarter','User_count'])
                colors =  ['mediumturquoise', 'teal', 'darkcyan', 'cadetblue', 'lightseagreen']
                fig = px.pie(PieChart_ToUse2, names="Quarter", values="User_count", title="User Brand Analysis",
                            color_discrete_sequence=colors)
                fig.update_traces(textposition='inside', textinfo='label+percent')
                fig.update_layout(width=300, height=400)
                st.plotly_chart(fig,use_container_width=True)
            with tabss2:
                # Bar Chart(Aggregated Users)
                cur.execute("SELECT State,SUM(User_count) as Brand_User_Count FROM aggregated_user GROUP BY State ORDER BY Brand_User_Count DESC;")
                BarChart1 = cur.fetchall()
                BarChart_ToUse1 = pd.DataFrame(BarChart1,columns=['State','Brand_User_Count'])
                fig = px.bar(BarChart_ToUse1, x="State", y="Brand_User_Count", title="State Vs Brand User Count",color="Brand_User_Count",
                            hover_data = ['State','Brand_User_Count'])
                fig.update_traces(marker_color='teal') 
                fig.update_xaxes(title_font=dict(size=18, family='serif', color='black'), title_text='State')
                fig.update_yaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Brand User Count')
                fig.update_layout(width=400,height=700)
                st.plotly_chart(fig,use_container_width=True)

                st.subheader("State-Wise User Count nd Percentage Analysis")
                cols1, cols2, cols3 = st.columns(3)
                with cols1:
                    state = st.selectbox("Select A State",('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu',
                            'Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Lakshadweep','Ladakh','Madhya Pradesh',
                            'Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana',
                            'Tripura','Uttar Pradesh','Uttarakhand','West Bengal'), key="state4_select")
                with cols2:
                    year = st.selectbox("Select A Year",(2018,2019,2020,2021,2022), key="year4_select")
                with cols3:
                    quarter = st.selectbox("Select A Quarter",("Q1","Q2","Q3","Q4"), key="quarter4_select")
                    
                #  Transaction Type(Dataframe) 
                cur.execute(f"SELECT User_Brand, User_count,User_percentage FROM aggregated_user WHERE State='{state}' AND Quarter='{quarter}' AND year='{year}' ;")
                dfs = cur.fetchall()
                dfs = pd.DataFrame(dfs,columns=['User_Brand','User_count','User_percentage'])
                st.dataframe(dfs)
                #  Transaction Type(Pie Chart)
                cur.execute(f"SELECT User_Brand, User_count,User_percentage FROM aggregated_user WHERE State='{state}' AND Quarter='{quarter}' AND year='{year}' ;")
                PieChart2 = cur.fetchall()
                PieChart_ToUse2 = pd.DataFrame(PieChart2,columns=['User_Brand','User_count','User_percentage'])
                colors =  ['mediumturquoise', 'teal', 'darkcyan', 'cadetblue', 'lightseagreen']
                fig = px.pie(PieChart_ToUse2, names="User_Brand", values="User_count", title="Analyzing user brand preferences based on user count and percentage.",
                            color_discrete_sequence=colors)
                fig.update_traces(textposition='inside', textinfo='label+percent')
                fig.update_layout(width=300, height=400)
                st.plotly_chart(fig,use_container_width=True)

    if Option == "In-Depth District Analysis":
        tabs3,tabs4 = st.tabs(["Transaction Trends by District","User Behavior by District"])
        with tabs3:
            #Map for india(Map Transaction)
            st.subheader("Geospatial Insights: Mapping Transaction Activity in India")
            cur.execute("SELECT State,SUM(District_count) as District_count, SUM(District_amount) as District_amount FROM map_transaction GROUP BY State;")
            Map = cur.fetchall()
            Map_ToUse1 = pd.DataFrame(Map,columns=['State','District_count','District_amount'])
            Map_ToUse1.index=Map_ToUse1.index+1
            fig = px.choropleth(Map_ToUse1,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='District_amount',
            hover_data=['District_count', 'District_amount'], 
            labels={'District_count': 'Total District Count', 'District_amount': 'Total District Amount'},
            color_continuous_scale=['#116467','#0f5a5c','#0d5052','#0b4648','#0a3c3d','#083233','#062829','#116467','#287376','#408385','#589294','#70a2a3','#88b1b3', '#9fc1c2','#b7d0d1','#cfe0e0','#e7efef','#ffffff'])
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(
            width=100,  
            height=500)
            st.plotly_chart(fig,use_container_width=True)

            tabu1,tabu2 = st.tabs(["District Transaction Amount","District Transaction Count"])
            with tabu1:
                st.subheader("Bar Chart Of District Transaction Amount Analysis")
                # Transaction Amount (Bar Chart)
                cur.execute("SELECT State, SUM(District_amount) as District_amount FROM map_transaction GROUP BY State ORDER BY District_amount DESC;")
                BarChart1 = cur.fetchall()
                BarChart_ToUse1 = pd.DataFrame(BarChart1,columns=['State','District_amount'])
                fig = px.bar(BarChart_ToUse1, x="State", y="District_amount", title="State Vs District Transaction Amount",color="State",
                            hover_data = ['State','District_amount'],labels={'Total_Trans_Amount':'Total_Transaction_Amount'})
                fig.update_traces(marker_color='teal') 
                fig.update_xaxes(title_font=dict(size=18, family='serif', color='black'), title_text='State')
                fig.update_yaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Total District Transaction Amount')
                fig.update_layout(width=400,height=700)
                st.plotly_chart(fig,use_container_width=True)
                
                st.subheader("District-Wise Transaction Amount Analysis")
                cols1, cols2, cols3 = st.columns(3)
                with cols1:
                    state = st.selectbox("Select A State",('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu',
                            'Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Lakshadweep','Ladakh','Madhya Pradesh',
                            'Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana',
                            'Tripura','Uttar Pradesh','Uttarakhand','West Bengal'), key="state5_select")
                with cols2:
                    year = st.selectbox("Select A Year",(2018,2019,2020,2021,2022), key="year5_select")
                with cols3:
                    quarter = st.selectbox("Select A Quarter",("Q1","Q2","Q3","Q4"), key="quarter5_select")
                    
                    
                #  Transaction Type(Dataframe) 
                cur.execute(f"SELECT District_name, District_amount  AS District_Trans_Amount FROM map_transaction WHERE Quarter = '{quarter}' and State = '{state}' and year = '{year}';")
                dfs = cur.fetchall()
                dfs = pd.DataFrame(dfs,columns=['District_name','District_Trans_Amount'])
                st.dataframe(dfs)
                #  Transaction Type(Pie Chart)
                cur.execute(f"SELECT District_name, District_amount  AS District_Trans_Amount FROM map_transaction WHERE Quarter = '{quarter}' and State = '{state}' and year = '{year}';")
                PieChart1 = cur.fetchall()
                PieChart_ToUse1 = pd.DataFrame(PieChart1,columns=['District_name','District_Trans_Amount'])
                colors =  ['mediumturquoise', 'teal', 'darkcyan', 'cadetblue', 'lightseagreen']
                fig = px.pie(PieChart_ToUse1, names="District_name", values="District_Trans_Amount", title="District Transaction Amount Analysis",
                            color_discrete_sequence=colors)
                fig.update_traces(textposition='inside', textinfo='label+percent')
                fig.update_layout(width=300, height=400)
                st.plotly_chart(fig,use_container_width=True)
                
            with tabu2:
                st.subheader("Bar Chart Of District Transaction Count Analysis")
                # Transaction Amount (Bar Chart)
                cur.execute("SELECT State, SUM(District_count) as District_count FROM map_transaction GROUP BY State ORDER BY District_count DESC;")
                BarChart1 = cur.fetchall()
                BarChart_ToUse1 = pd.DataFrame(BarChart1,columns=['State','District_count'])
                fig = px.bar(BarChart_ToUse1, x="State", y="District_count", title="State Vs District Transaction Count",color="State",
                            hover_data = ['State','District_count'],labels={'Total_Trans_Amount':'Total_Transaction_Amount'})
                fig.update_traces(marker_color='teal') 
                fig.update_xaxes(title_font=dict(size=18, family='serif', color='black'), title_text='State')
                fig.update_yaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Total District Transaction Count')
                fig.update_layout(width=400,height=700)
                st.plotly_chart(fig,use_container_width=True)
                
                st.subheader("District-Wise Transaction Count Analysis")
                cols1, cols2, cols3 = st.columns(3)
                with cols1:
                    state = st.selectbox("Select A State",('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu',
                            'Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Lakshadweep','Ladakh','Madhya Pradesh',
                            'Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana',
                            'Tripura','Uttar Pradesh','Uttarakhand','West Bengal'), key="state6_select")
                with cols2:
                    year = st.selectbox("Select A Year",(2018,2019,2020,2021,2022), key="year6_select")
                with cols3:
                    quarter = st.selectbox("Select A Quarter",("Q1","Q2","Q3","Q4"), key="quarter6_select")
                    
                    
                #  Transaction Type(Dataframe) 
                cur.execute(f"SELECT District_name, District_count  AS District_Trans_count FROM map_transaction WHERE Quarter = '{quarter}' and State = '{state}' and year = '{year}';")
                dfs = cur.fetchall()
                dfs = pd.DataFrame(dfs,columns=['District_name','District_Trans_Count'])
                st.dataframe(dfs)
                #  Transaction Type(Pie Chart)
                cur.execute(f"SELECT District_name, District_count  AS District_Trans_Count FROM map_transaction WHERE Quarter = '{quarter}' and State = '{state}' and year = '{year}';")
                PieChart1 = cur.fetchall()
                PieChart_ToUse1 = pd.DataFrame(PieChart1,columns=['District_name','District_Trans_Count'])
                colors =  ['mediumturquoise', 'teal', 'darkcyan', 'cadetblue', 'lightseagreen']
                fig = px.pie(PieChart_ToUse1, names="District_name", values="District_Trans_Count", title="District Transaction Count Analysis",
                            color_discrete_sequence=colors)
                fig.update_traces(textposition='inside', textinfo='label+percent')
                fig.update_layout(width=300, height=400)
                st.plotly_chart(fig,use_container_width=True)
                
        with tabs4:

            st.subheader("Geospatial Insights: Mapping User Activity in India")
            cur.execute("SELECT state,sum(Registered_User) as Registered_User,sum(App_Opens) as App_Opens from map_user group by state ORDER BY Registered_User DESC;")
            Map = cur.fetchall()
            Map_ToUse8 = pd.DataFrame(Map,columns=['State','Registered_User','App_Opens'])
            Map_ToUse8.index=Map_ToUse8.index+1
                           
            fig = px.choropleth(Map_ToUse8,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='State',
            hover_data=['Registered_User', 'App_Opens'], 
            labels={'Registered_User': 'Registered User', 'App_Opens': 'App Opens'},
            color_continuous_scale='plasma')
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(
            width=100,  
            height=500)
            st.plotly_chart(fig,use_container_width=True)

            tabu1,tabu2 = st.tabs(["PhonePe User Registrations at the District Level","PhonePe App Openers at the District Level"])
            with tabu1:
                st.subheader("Bar Chart of User Registrations at the District Level")
                # Transaction Amount (Bar Chart)
                cur.execute("SELECT state, SUM(Registered_User) AS Registered_User FROM map_user GROUP BY state ORDER BY Registered_User DESC;")
                BarChart1 = cur.fetchall()
                BarChart_ToUse1 = pd.DataFrame(BarChart1,columns=['State','Registered_User'])
                fig = px.bar(BarChart_ToUse1, x="State", y="Registered_User", title="State Vs Registered User",color="State",
                            hover_data = ['State','Registered_User'],labels={'Registered_User':'Total_Registered_User'})
                fig.update_traces(marker_color='teal') 
                fig.update_xaxes(title_font=dict(size=18, family='serif', color='black'), title_text='State')
                fig.update_yaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Total Registered User')
                fig.update_layout(width=400,height=700)
                st.plotly_chart(fig,use_container_width=True)
                
                st.subheader("District-Wise Registered User Analysis")
                cols1, cols2, cols3 = st.columns(3)
                with cols1:
                    state = st.selectbox("Select A State",('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu',
                            'Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Lakshadweep','Ladakh','Madhya Pradesh',
                            'Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana',
                            'Tripura','Uttar Pradesh','Uttarakhand','West Bengal'), key="state7_select")
                with cols2:
                    year = st.selectbox("Select A Year",(2018,2019,2020,2021,2022), key="year7_select")
                with cols3:
                    quarter = st.selectbox("Select A Quarter",("Q1","Q2","Q3","Q4"), key="quarter7_select")
                    
                    
                #  Transaction Type(Dataframe) 
                cur.execute(f"SELECT District_name, SUM(Registered_User) as Registered_User FROM map_user WHERE State='{state}' AND Year='{year}' AND Quarter ='{quarter}' group by state,District_name;")
                dfs = cur.fetchall()
                dfs = pd.DataFrame(dfs,columns=['District_name','Registered_User'])
                st.dataframe(dfs)
                #  Transaction Type(Pie Chart)
                cur.execute(f"SELECT District_name, SUM(Registered_User) as Registered_User FROM map_user WHERE State='{state}' AND Year='{year}' AND Quarter ='{quarter}' group by state,District_name;")
                PieChart1 = cur.fetchall()
                PieChart_ToUse1 = pd.DataFrame(PieChart1,columns=['District_name','Registered_User'])
                colors =  ['mediumturquoise', 'teal', 'darkcyan', 'cadetblue', 'lightseagreen']
                fig = px.pie(PieChart_ToUse1, names="District_name", values="Registered_User", title="District Registered User Analysis",
                            color_discrete_sequence=colors)
                fig.update_traces(textposition='inside', textinfo='label+percent')
                fig.update_layout(width=300, height=400)
                st.plotly_chart(fig,use_container_width=True)
                
            with tabu2:
                st.subheader("Bar Chart of App Openers at the District Level")
                # Transaction Amount (Bar Chart)
                cur.execute("SELECT state, SUM(App_Opens) AS App_Opens FROM map_user GROUP BY state ORDER BY App_Opens DESC;")
                BarChart1 = cur.fetchall()
                BarChart_ToUse1 = pd.DataFrame(BarChart1,columns=['State','App_Opens'])
                fig = px.bar(BarChart_ToUse1, x="State", y="App_Opens", title="State Vs App Opens",color="State",
                            hover_data = ['State','App_Opens'],labels={'App_Opens':'App Openers'})
                fig.update_traces(marker_color='teal') 
                fig.update_xaxes(title_font=dict(size=18, family='serif', color='black'), title_text='State')
                fig.update_yaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Total App Openers')
                fig.update_layout(width=400,height=700)
                st.plotly_chart(fig,use_container_width=True)
                
                st.subheader("District-Wise App Openers Analysis")
                cols1, cols2, cols3 = st.columns(3)
                with cols1:
                    state = st.selectbox("Select A State",('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu',
                            'Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Lakshadweep','Ladakh','Madhya Pradesh',
                            'Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana',
                            'Tripura','Uttar Pradesh','Uttarakhand','West Bengal'), key="state8_select")
                with cols2:
                    year = st.selectbox("Select A Year",(2018,2019,2020,2021,2022), key="year8_select")
                with cols3:
                    quarter = st.selectbox("Select A Quarter",("Q1","Q2","Q3","Q4"), key="quarter8_select")
                    
                    
                #  Transaction Type(Dataframe) 
                cur.execute(f"SELECT District_name, SUM(App_Opens) as App_Opens FROM map_user WHERE State='{state}' AND Year='{year}' AND Quarter ='{quarter}' group by state,District_name;")
                dfs = cur.fetchall()
                dfs = pd.DataFrame(dfs,columns=['District_name','App_Opens'])
                st.dataframe(dfs)
                #  Transaction Type(Pie Chart)
                cur.execute(f"SELECT District_name, SUM(App_Opens) as App_Opens FROM map_user WHERE State='{state}' AND Year='{year}' AND Quarter ='{quarter}' group by state,District_name;")
                PieChart1 = cur.fetchall()
                PieChart_ToUse1 = pd.DataFrame(PieChart1,columns=['District_name','App_Opens'])
                colors =  ['mediumturquoise', 'teal', 'darkcyan', 'cadetblue', 'lightseagreen']
                fig = px.pie(PieChart_ToUse1, names="District_name", values="App_Opens", title="District App Openers Analysis",
                            color_discrete_sequence=colors)
                fig.update_traces(textposition='inside', textinfo='label+percent')
                fig.update_layout(width=300, height=400)
                st.plotly_chart(fig,use_container_width=True) 

    if Option == "Leading Top Payment Categories":
        tabs5,tabs6 = st.tabs(["Top Transaction Trends By District","Top User Behavior By District"])
        with tabs5:
            st.write("The **top ten districts** in terms of transaction amount and transaction count in PhonePe are all dominated by the presence of digital payments. These districts showcase a **high volume of financial activities** and a strong preference for cashless transactions.")
            tab4,tab5=st.tabs(['Top Transaction Amount','Top Transaction Count'])
            with tab4:
                st.subheader("Bar chart of Top Transaction Amount")
                # Top Transaction (Bar Chart)
                cur.execute("SELECT State,SUM(Transaction_amount) as Transaction_amount FROM top_transaction GROUP BY State ORDER BY Transaction_amount DESC;")
                BarChart1 = cur.fetchall()
                BarChart_ToUse1 = pd.DataFrame(BarChart1,columns=['State','Transaction_amount'])
                fig = px.bar(BarChart_ToUse1, x="State", y="Transaction_amount", title="State Vs Total Transaction Amount",color="State",
                            hover_data = ['State','Transaction_amount'],labels={'Transaction_amount':'Total Transaction Amount'})
                fig.update_traces(marker_color='teal') 
                fig.update_xaxes(title_font=dict(size=18, family='serif', color='black'), title_text='State')
                fig.update_yaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Total Transaction Amount')
                fig.update_layout(width=400,height=700)
                st.plotly_chart(fig,use_container_width=True)

                st.subheader("Top Transaction Amount By District")
                cols1, cols2, cols3 = st.columns(3)
                with cols1:
                    state = st.selectbox("Select A State",('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu',
                            'Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Lakshadweep','Ladakh','Madhya Pradesh',
                            'Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana',
                            'Tripura','Uttar Pradesh','Uttarakhand','West Bengal'), key="state9_select")
                with cols2:
                    year = st.selectbox("Select A Year",(2018,2019,2020,2021,2022), key="year9_select")
                with cols3:
                    quarter = st.selectbox("Select A Quarter",("Q1","Q2","Q3","Q4"), key="quarter9_select")

                cur.execute(f"SELECT district_name, transaction_amount FROM top_transaction WHERE state='{state}' and year='{year}'and quarter='{quarter}'GROUP BY transaction_amount ,district_name ORDER BY transaction_amount desc LIMIT 10;")
                dfs = cur.fetchall()
                dfs = pd.DataFrame(dfs,columns=['District_name','Transaction_Amount '])
                st.dataframe(dfs)
                #  Transaction Type(Pie Chart)
                cur.execute(f"SELECT district_name, transaction_amount FROM top_transaction WHERE state='{state}' and year='{year}'and quarter='{quarter}'GROUP BY transaction_amount ,district_name ORDER BY transaction_amount desc LIMIT 10;")
                PieChart1 = cur.fetchall()
                PieChart_ToUse1 = pd.DataFrame(PieChart1,columns=['District_name','Transaction_Amount'])
                colors =  ['mediumturquoise', 'teal', 'darkcyan', 'cadetblue', 'lightseagreen']
                fig = px.pie(PieChart_ToUse1, names="District_name", values="Transaction_Amount", title="Top Transaction Amount",
                            color_discrete_sequence=colors)
                fig.update_traces(textposition='inside', textinfo='label+percent')
                fig.update_layout(width=300, height=400)
                st.plotly_chart(fig,use_container_width=True) 

            with tab5:
                st.subheader("Bar chart of Top Transaction Count")
                # Top Transaction (Bar Chart)
                cur.execute("SELECT State,SUM(Transaction_count) as Transaction_count FROM top_transaction GROUP BY State ORDER BY Transaction_count DESC;")
                BarChart1 = cur.fetchall()
                BarChart_ToUse1 = pd.DataFrame(BarChart1,columns=['State','Transaction_count'])
                fig = px.bar(BarChart_ToUse1, x="State", y="Transaction_count", title="State Vs Total Transaction Count",color="State",
                            hover_data = ['State','Transaction_count'],labels={'Transaction_amount':'Total Transaction Count'})
                fig.update_traces(marker_color='teal') 
                fig.update_xaxes(title_font=dict(size=18, family='serif', color='black'), title_text='State')
                fig.update_yaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Total Transaction Count')
                fig.update_layout(width=400,height=700)
                st.plotly_chart(fig,use_container_width=True)

                st.subheader("Top Transaction count By District")
                cols1, cols2, cols3 = st.columns(3)
                with cols1:
                    state = st.selectbox("Select A State",('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu',
                            'Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Lakshadweep','Ladakh','Madhya Pradesh',
                            'Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana',
                            'Tripura','Uttar Pradesh','Uttarakhand','West Bengal'), key="state10_select")
                with cols2:
                    year = st.selectbox("Select A Year",(2018,2019,2020,2021,2022), key="year10_select")
                with cols3:
                    quarter = st.selectbox("Select A Quarter",("Q1","Q2","Q3","Q4"), key="quarter10_select")

                cur.execute(f"SELECT district_name, transaction_count FROM top_transaction WHERE state='{state}' and year='{year}'and quarter='{quarter}'GROUP BY transaction_count ,district_name ORDER BY transaction_count desc LIMIT 10;")
                dfs = cur.fetchall()
                dfs = pd.DataFrame(dfs,columns=['District_name','Transaction_Count'])
                st.dataframe(dfs)
                #  Transaction Type(Pie Chart)
                cur.execute(f"SELECT district_name, transaction_count FROM top_transaction WHERE state='{state}' and year='{year}'and quarter='{quarter}'GROUP BY transaction_count ,district_name ORDER BY transaction_count desc LIMIT 10;")
                PieChart1 = cur.fetchall()
                PieChart_ToUse1 = pd.DataFrame(PieChart1,columns=['District_name','Transaction_Count'])
                colors =  ['mediumturquoise', 'teal', 'darkcyan', 'cadetblue', 'lightseagreen']
                fig = px.pie(PieChart_ToUse1, names="District_name", values="Transaction_Count", title="Top Transaction Count",
                            color_discrete_sequence=colors)
                fig.update_traces(textposition='inside', textinfo='label+percent')
                fig.update_layout(width=300, height=400)
                st.plotly_chart(fig,use_container_width=True) 
        

        with tabs6:
            st.subheader("Bar chart of Top Registered Users")
            # Top Transaction (Bar Chart)
            cur.execute("SELECT State, SUM(registered_users) AS total_registered_users FROM top_user GROUP BY state ORDER BY total_registered_users DESC;")
            BarChart1 = cur.fetchall()
            BarChart_ToUse1 = pd.DataFrame(BarChart1,columns=['State','total_registered_users'])
            fig = px.bar(BarChart_ToUse1, x="State", y="total_registered_users", title="State Vs Total Registered Users",color="State",
                        hover_data = ['State','total_registered_users'],labels={'total_registered_users':'Total Registered Users'})
            fig.update_traces(marker_color='teal') 
            fig.update_xaxes(title_font=dict(size=18, family='serif', color='black'), title_text='State')
            fig.update_yaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Total Registered Users')
            fig.update_layout(width=400,height=700)
            st.plotly_chart(fig,use_container_width=True)

            st.subheader("Top Registered Users By District")
            cols1, cols2, cols3 = st.columns(3)
            with cols1:
                state = st.selectbox("Select A State",('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu',
                        'Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Lakshadweep','Ladakh','Madhya Pradesh',
                        'Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana',
                        'Tripura','Uttar Pradesh','Uttarakhand','West Bengal'), key="state11_select")
            with cols2:
                year = st.selectbox("Select A Year",(2018,2019,2020,2021,2022), key="year11_select")
            with cols3:
                quarter = st.selectbox("Select A Quarter",("Q1","Q2","Q3","Q4"), key="quarter11_select")

            cur.execute(f"SELECT district_name, registered_users FROM top_user WHERE state='{state}' and year='{year}'and quarter='{quarter}' GROUP BY registered_users, district_name, quarter, year, state ORDER BY registered_users desc LIMIT 10;")
            dfs = cur.fetchall()
            dfs = pd.DataFrame(dfs,columns=['District_name','Registered_Users'])
            st.dataframe(dfs)
            #  Transaction Type(Pie Chart)
            cur.execute(f"SELECT district_name, registered_users FROM top_user WHERE state='{state}' and year='{year}'and quarter='{quarter}' GROUP BY registered_users, district_name, quarter, year, state ORDER BY registered_users desc LIMIT 10;")
            PieChart1 = cur.fetchall()
            PieChart_ToUse1 = pd.DataFrame(PieChart1,columns=['District_name','Registered_Users'])
            colors =  ['mediumturquoise', 'teal', 'darkcyan', 'cadetblue', 'lightseagreen']
            fig = px.pie(PieChart_ToUse1, names="District_name", values="Registered_Users", title="Top Registered Users",
                        color_discrete_sequence=colors)
            fig.update_traces(textposition='inside', textinfo='label+percent')
            fig.update_layout(width=300, height=400)
            st.plotly_chart(fig,use_container_width=True)


elif SELECT == "🔚Exit":
    st.header(" Understanding Transaction Dynamics Across India!")
    st.subheader("**State-wise Transaction Insights:**")
    st.write("""
            - Telangana records the highest transaction amount by state.
            - Mizoram observes the lowest transaction volume.
            - In 2023, Karnataka takes the lead, while Lakshadweep had the lowest in 2018, with notable quarterly variations.""")
    st.subheader("**Mobile Brand and Regional PhonePe Trends:**")
    st.write("""
            - Xiaomi emerges as the dominant mobile brand nationwide.
            - Coolpad experiences lower usage frequency.
            - Maharashtra shows a significant PhonePe user base, contrasting with lesser adoption in Lakshadweep.""")
    st.subheader("**District-level Transaction Overview:**")
    st.write("""
            - Telangana stands out for the highest total transaction amounts.
            - Hyderabad tops districts, with Dibang Valley at the opposite end.""")
    st.subheader("**User Registration and App Activity:**")
    st.write("""
            - Maharashtra boasts the highest number of registered users and active app openers.
            - Conversely, Lakshadweep reports the lowest figures, with no app openings in 2018.""")
    st.subheader("**Top Transaction Counts by State:**")
    st.write("""
            - Telangana leads in both the highest transaction amounts and counts.
            - Karnataka secures the top spot in transaction counts, with Mizoram at the bottom.""")
    st.subheader("**Top Registered User Highlights:**")
    st.write("""
            - Karnataka exhibits the highest number of registered users.
            - Lakshadweep has the least registered user count.""")
    
    but=st.button("EXIT!")
    if but:
        st.write("Thanks For Using This Platfrom. Hope You Gained Some Knowledge About PhonePe and Its Transaction and useage!")
        st.balloons()
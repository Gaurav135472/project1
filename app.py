import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='Startup Analysis')

df = pd.read_csv('startup_cleaned1.csv')

df['date'] = df['date'].str.replace('05/072018', '05/07/2018')
df['date'] = df['date'].str.replace('01/07/015', '01/07/2015')
df['date'] = df['date'].str.replace('12/05.2015', '12/05/2015')
df['date'] = df['date'].str.replace('13/04.2015', '13/04/2015')
df['date'] = df['date'].str.replace('15/01.2015', '15/01/2015')
df['date'] = df['date'].str.replace('22/01//2015', '22/01/2015')
df['date'] = df['date'].str.replace(r'(\d{4})-(\d{2})-(\d{2})', r'\3/\2/\1', regex=True)

df['date'] = pd.to_datetime(df['date'],format='%d/%m/%Y', dayfirst=True)

def load_overall_analysis():
    st.title('Overall Analysis')

    col1, col2 , col3, col4 = st.columns(4)

    with col1:
        total = round(df['amount'].sum())
    # total money invested
        st.metric('Total', str(total) + ' Million')
    with col2:
        # max amount infused in a startup

        max_funcding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

        st.metric('Maximum', str(max_funcding) + ' Million')

    with col3:

        # avg money invested on startup
        avg_funding = df.groupby('startup')['amount'].sum().mean()

        st.metric('Average Money Invested ', str(round(avg_funding)) + ' Million')
    
    with col4:
        # total number of funded startup 
        num_startup = df['startup'].nunique()
        st.metric('Number of Startup', str(round(num_startup)) + ' Million')

    st.header('MoM Graph')

    selected_type = st.selectbox('Select Type',['MoM Investmented Amount', 'MoM startup Number'])
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    plt.close('all')

    if selected_type == 'MoM startup Number':
        # Group by year and month, counting the number of startups
        temp_df = df.groupby(['year', 'month'])['startup'].size().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)

            # Create the plot
        fig4, ax4 = plt.subplots()
        ax4.plot(temp_df['x_axis'], temp_df['startup'])
        ax4.set_xlabel('Month-Year')
        ax4.set_ylabel('Startup Count')
        ax4.tick_params(axis='x',which='both', labelsize=6, rotation=90)
        fig4.tight_layout()
        st.pyplot(fig4)

    else:
        # Group by year and month, summing the investment amounts
        temp_df2 = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        temp_df2['x_axis'] = temp_df2['month'].astype(str) + '-' + temp_df2['year'].astype(str)

        # Create the plot
        fig4, ax4 = plt.subplots()
        ax4.plot(temp_df2['x_axis'], temp_df2['amount'])
        ax4.set_xlabel('Month-Year')
        ax4.set_ylabel('Investment Amount')
        ax4.tick_params(axis='x',which='both', labelsize=6, rotation=90)
        st.pyplot(fig4)

    col1, col2 = st.columns(2)
    with col1:
    # top startup

        temp_df = df.groupby('year').max()
        fig, ax = plt.subplots()
        ax.bar(temp_df.index, temp_df['amount'])
        ax.set_title('Top Investment in Each Year')
        ax.set_xlabel('Years')
        ax.set_ylabel('Amount')
        st.pyplot(fig)

    with col2:
        # creating the pie chart on the sectors 
        temp_df = df.groupby('vertical').size().sort_values(ascending=False).head(10)
        fig5, ax5 = plt.subplots()
        ax5.pie(temp_df, labels=temp_df.index, autopct='%0.01f%%')
        ax5.set_title('Sector wise Investment')
        plt.tight_layout()
        st.pyplot(fig5)

def load_investor_detail(investor):
    st.title(investor)

    # load recent five investment of the investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.write("Amount in Million USD")
    st.dataframe(last5_df)

    # biggest investment

    st.subheader('Biggest Investments')
    col1, col2 = st.columns(2)

    big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
    with col1:
        st.dataframe(big_series)
    with col2:
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

     # In which year invested the most with line chart
    st.subheader("YoY Investment Details")    
    col7, col8 = st.columns(2)
    df['year'] = df['date'].dt.year
    YOY_invest_data = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum().sort_index()
    with col7:
        st.dataframe(YOY_invest_data)
    with col8:
        fig2, ax2 = plt.subplots()
        ax2.plot(YOY_invest_data.index, YOY_invest_data.values)
        st.pyplot(fig2)

        # In which sector invested the most with pie chart
    st.subheader("Sectors Invested IN")    
    col3, col4 = st.columns(2)
    sect_invest_df = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
    with col3:
        st.dataframe(sect_invest_df)
    with col4:
        fig, ax = plt.subplots()
        ax.pie(sect_invest_df, labels=sect_invest_df.index, autopct='%0.01f%%')
        st.pyplot(fig)

    # In which stage invested the most with pie chart
    st.subheader("Round Details")    
    col5, col6 = st.columns(2)
    round_detail = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
    with col5:
        st.dataframe(round_detail)
    with col6:
        fig, ax = plt.subplots()
        ax.pie(round_detail, labels=round_detail.index, autopct='%0.01f%%')
        st.pyplot(fig)

        # Pertner With Whome Invested The Most
    st.subheader("Pertner With Whome Invested The Most")    
    col9, col10 = st.columns(2)
    investor_list = df['investors'][df['investors'].str.contains(investor)].str.split(',').explode().str.strip()
    final_list = investor_list[investor_list != investor].value_counts().head()
    with col9:
        st.dataframe(final_list)
    with col10:
        fig, ax = plt.subplots()
        ax.pie(final_list, labels=final_list.index, autopct='%0.01f%%')
        st.pyplot(fig)

st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Investor'])

if option == 'Overall Analysis':
        load_overall_analysis()
elif option == 'Investor':
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(sorted(set(df['investors'].str.split(',').sum()))))
    btn2 = st.sidebar.button('Find Investor Detail')
    if btn2:
        load_investor_detail(selected_investor)
    


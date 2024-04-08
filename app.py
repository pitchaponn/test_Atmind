import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def load_data():
    return pd.read_csv("C:/Users/Asus/Desktop/test_data.csv")
df = load_data()
@st.cache_data
def preprocess_data(df):
    #menu_populartity
    menu_popularity = df['Menu'].value_counts().reset_index()
    menu_popularity.columns = ['Menu', 'Orders']
    fig_menu_popularity = px.bar(menu_popularity, x='Menu', y='Orders', title='Popularity of Each Food Menu')
    #quantity_sold
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month
    category_monthly_count = df.groupby(['Category', 'Month']).size().reset_index(name='Count')
    food_data = category_monthly_count[category_monthly_count['Category'] == 'food']
    drink_data = category_monthly_count[category_monthly_count['Category'] == 'drink']
    fig_quantity_sold = go.Figure()
    fig_quantity_sold.add_trace(go.Scatter(x=food_data['Month'], y=food_data['Count'], mode='lines', name='Food'))
    fig_quantity_sold.add_trace(go.Scatter(x=drink_data['Month'], y=drink_data['Count'], mode='lines', name='Drink'))
    fig_quantity_sold.update_layout(title='Overall Quantity of Menu Sold by Category',
                                     xaxis_title='Month',
                                     yaxis_title='Quantity Sold')
    #monthle_sales
    category_monthly_sales = df.groupby(['Category', 'Month'])['Price'].sum().reset_index()
    food_data = category_monthly_sales[category_monthly_sales['Category'] == 'food']
    drink_data = category_monthly_sales[category_monthly_sales['Category'] == 'drink']
    fig_monthly_sales = go.Figure()
    fig_monthly_sales.add_trace(go.Scatter(x=food_data['Month'], y=food_data['Price'], mode='lines', name='Food'))
    fig_monthly_sales.add_trace(go.Scatter(x=drink_data['Month'], y=drink_data['Price'], mode='lines', name='Drink'))
    fig_monthly_sales.update_layout(title='Overall Sales by Category',
                                    xaxis_title='Month',
                                    yaxis_title='Sales Amount')
    #menu_sales
    menu_monthly_sales = df.groupby(['Menu', 'Month'])['Price'].sum().reset_index()
    fig_menu_sales = px.bar(menu_monthly_sales, x='Menu', y='Price', color='Month',
                title='Sales of Each Menu Ordered Each Month',
                labels={'Price': 'Sales Amount', 'Menu': 'Menu Name', 'Month': 'Month'})
    fig_menu_sales.update_layout(xaxis={'categoryorder':'total descending'})
    #staff
    if '.' in df['Serve Time'].iloc[0]:  
        df['Serve Time'] = pd.to_datetime(df['Serve Time'], format='%Y-%m-%d %H:%M:%S.%f') 
    else:
        df['Serve Time'] = pd.to_datetime(df['Serve Time'], format='%Y-%m-%d %H:%M:%S') 

    df['Serve Hour'] = df['Serve Time'].dt.hour
    df['Serve Minute'] = df['Serve Time'].dt.minute
    order_time = pd.to_datetime(df['Hour'].astype(str) + ':' + df['Minute'].astype(str), format='%H:%M')
    serve_time = pd.to_datetime(df['Serve Hour'].astype(str) + ':' + df['Serve Minute'].astype(str), format='%H:%M')
    df['Time Difference'] = (serve_time - order_time).dt.total_seconds() / 60
    menu_items_per_day = df.groupby(['Day Of Week', 'Menu']).size().reset_index(name='Menu Count')
    avg_orders_per_day = menu_items_per_day.groupby('Day Of Week')['Menu Count'].mean().reset_index(name='Average Orders')
    avg_kitchen_staff_per_day = df.groupby('Day Of Week')['Kitchen Staff'].mean().reset_index(name='Average Kitchen Staff')
    avg_drinks_staff_per_day = df.groupby('Day Of Week')['Drinks Staff'].mean().reset_index(name='Average Drinks Staff')
    avg_processing_time_per_day = df.groupby('Day Of Week')['Time Difference'].mean().reset_index(name='Average Processing Time')
    
    fig_staff = px.bar(avg_orders_per_day, x='Day Of Week', y='Average Orders', title='Average Orders per Day of Week')
    fig_staff.add_bar(x=avg_kitchen_staff_per_day['Day Of Week'], y=avg_kitchen_staff_per_day['Average Kitchen Staff'],
                name='Average Kitchen Staff')
    fig_staff.add_bar(x=avg_drinks_staff_per_day['Day Of Week'], y=avg_drinks_staff_per_day['Average Drinks Staff'],
                name='Average Drinks Staff')
    fig_staff.add_scatter(x=avg_processing_time_per_day['Day Of Week'], y=avg_processing_time_per_day['Average Processing Time'],
                    mode='lines+markers', name='Average Processing Time', yaxis='y2')
    fig_staff.update_layout(xaxis=dict(title='Day of Week'),
                    yaxis=dict(title='Average Count'),
                    yaxis2=dict(title='Average Processing Time (minutes)', overlaying='y', side='right'),
                    legend=dict(y=1.2, x=1),
                    barmode='group')
    
    return fig_menu_popularity, fig_quantity_sold, fig_monthly_sales, fig_menu_sales, fig_staff

def main():
    st.title("Live Streamlit Dashboard")
    df = load_data()
    fig_menu_popularity, fig_quantity_sold, fig_monthly_sales, fig_menu_sales, fig_staff = preprocess_data(df)
    right_col, left_col = st.columns((40, 1))
    with right_col:
        st.plotly_chart(fig_menu_popularity)
        st.plotly_chart(fig_quantity_sold)
    with left_col:
        st.plotly_chart(fig_monthly_sales)
        st.plotly_chart(fig_menu_sales)
    st.plotly_chart(fig_staff)

    if st.button('Update Data'):
        df = load_data()
        st.spinner('Updating data...')
        fig_menu_popularity, fig_quantity_sold, fig_monthly_sales, fig_menu_sales, fig_staff = preprocess_data(df)
        with right_col:
            st.plotly_chart(fig_menu_popularity)
            st.plotly_chart(fig_quantity_sold)
        with left_col:
            st.plotly_chart(fig_monthly_sales)
            st.plotly_chart(fig_menu_sales)
        st.plotly_chart(fig_staff)

if __name__ == "__main__":
    main()
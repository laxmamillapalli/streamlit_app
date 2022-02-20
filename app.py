import streamlit as st
import datetime as dt
import json
import stocks
import numpy as np
import models
import math
import pandas as pd
dates_file = open("./data/dates.json")
dates_dict = json.load(dates_file)
dates_file.close()

models_dict = {'EMA Strategy' : models.EMA_strategy_Returns, 
                'SMA Strategy': models.SMA_strategy_Returns}


stocks_dict = stocks.stocks_dict
for each in dates_dict:
    dates_dict[each] = dt.datetime.strptime(dates_dict[each], "%Y-%m-%d")

st.sidebar.header("Data Cow")
sidebar_menu = ('Home', 'Download OHLCV', 'Modelling', 'Models Results')
page = st.sidebar.radio( "Select page:", sidebar_menu)
st.title(page)
if page == 'Home':
    st.header("Welcome to Data Cow!")
    col1, col2 = st.columns([2,7])
    with col1:
        st.image("./images/Pic.jpg")
        st.write("I am Laxminag Mamillapalli. Nice to meet you.")
    with col2:
        st.bar_chart(np.random.randn(25, 3))
    st.write("This is a personal app to analyze stocks.")
elif page == 'Download OHLCV':
    col1, col2, col3 = st.columns(3)
    start_date = col1.date_input(label="Select start date: ",
                            value=dates_dict['min_date'],
                            min_value=dates_dict['min_date'],
                            max_value=dates_dict['max_date'])
    end_date = col2.date_input(label="Select end date: ",
                            value=dates_dict['max_date'],
                            min_value=dates_dict['min_date'],
                            max_value=dates_dict['max_date'])
    
    ticker = col3.selectbox('Ticker:', list(stocks_dict.keys()))
    df = stocks.get_daily_data(ticker, start_date, end_date)
    st.write(f"Daily data for {ticker} below:")
    st.dataframe(df)
elif page == 'Modelling':
    col1_1, col2_1 = st.columns(2) 
    ticker = col1_1.selectbox('Ticker:', list(stocks_dict.keys()))
    selected_model = col2_1.selectbox('Model:', list(models_dict.keys()))

    col1_2, col2_2 = st.columns(2) 
    Fast_MA=col1_2.slider('Fast Moving Avg:', value = 5, max_value = 300, min_value = 0)
    Slow_MA=col2_2.slider('Slow Moving Avg:', value = Fast_MA+1, max_value = 300, min_value = Fast_MA+1)
    (df, strategy_ret, buy_hold_ret, buy_only_ret, sell_only_ret) = models_dict[selected_model](ticker=ticker, Fast_MA=Fast_MA, Slow_MA=Slow_MA)
    strategy_cagr = round(100*(math.exp(strategy_ret/15)-1), 3)
    buy_hold_cagr = round(100*(math.exp(buy_hold_ret/15)-1),3)
    buy_only_cagr = round(100*(math.exp(buy_only_ret/15)-1), 3)
    sell_only_cagr = round(100*(math.exp(sell_only_ret/15)-1), 3)
    st.header("CAGR - Returns%")
    col1_3, col2_3, col3_3, col4_3 = st.columns(4)
    col1_3.metric(selected_model, strategy_cagr)
    col2_3.metric("Buy-Hold", buy_hold_cagr)
    col3_3.metric("Buy Only", buy_only_cagr)
    col4_3.metric("Sell Only", sell_only_cagr)
    st.write(f"FastMA = {Fast_MA}, SlowMA = {Slow_MA}")
    st.write(f"Daily data for {ticker} below:")
    st.write(df.head())
    st.write(df.tail())
elif page == 'Models Results':
    col1, col2, col3 = st.columns(3)
    start_date = col1.date_input(label="Select start date: ",
                            value=dates_dict['min_date'],
                            min_value=dates_dict['min_date'],
                            max_value=dates_dict['max_date'])
    end_date = col2.date_input(label="Select end date: ",
                            value=dates_dict['max_date'],
                            min_value=dates_dict['min_date'],
                            max_value=dates_dict['max_date'])
    ticker = col3.selectbox('Ticker:', list(stocks_dict.keys()))
    df = stocks.get_daily_data(ticker, start_date, end_date)
    drawdown = models.get_drawdown(df['Close'])
    st.write(f"Max Drawdown is {np.nanmin(drawdown, 0)}")
    st.area_chart(drawdown)
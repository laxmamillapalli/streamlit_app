import numpy as np
import stocks


def calculate_returns(df):
    df['Returns'] = df['Log Returns'] * df['Signal'].shift(1)
    df['Returns-OB'] = df['Log Returns'] * df['Signal-OB'].shift(1)
    df['Returns-OS'] = df['Log Returns'] * df['Signal-OS'].shift(1)
    df['Buy-Hold'] = df['Log Returns'].cumsum()
    df['Strategy'] = df['Returns'].cumsum()
    df['Strategy-OB'] = df['Returns-OB'].cumsum()
    df['Strategy-OS'] = df['Returns-OS'].cumsum()
    df.bfill(inplace=True)
    return df


def get_drawdown(series):
    series_change = series.pct_change()
    wealth_index = 1000*(1+series_change).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdown = (wealth_index - previous_peaks)/previous_peaks
    return drawdown


def SMA_strategy_Returns(ticker, Fast_MA, Slow_MA):
    df = stocks.get_daily_data(ticker)
    df['Log Returns'] = np.log(df['Close']/df['Close'].shift(1))
    df['MASlow'] = df['Close'].rolling(Slow_MA).mean()
    df['MAFast'] = df['Close'].rolling(Fast_MA).mean()
    df['Signal'] = np.where(df['MAFast']>df['MASlow'],1,-1)
    df['Signal-OB'] = np.where(df['MAFast']>df['MASlow'],1,0)
    df['Signal-OS'] = np.where(df['MAFast']>df['MASlow'],0,-1)
    df = calculate_returns(df)
    return (df, df['Strategy'][-1], df['Buy-Hold'][-1], df['Strategy-OB'][-1], df['Strategy-OS'][-1])


def EMA_strategy_Returns(ticker, Fast_MA, Slow_MA):
    df = stocks.get_daily_data(ticker)
    df['Log Returns'] = np.log(df['Close']/df['Close'].shift(1))
    df['MASlow'] = df['Close'].ewm(Slow_MA).mean()
    df['MAFast'] = df['Close'].ewm(Fast_MA).mean()
    df['Signal'] = np.where(df['MAFast']>df['MASlow'],1,-1)
    df['Signal-OB'] = np.where(df['MAFast']>df['MASlow'],1,0)
    df['Signal-OS'] = np.where(df['MAFast']>df['MASlow'],0,-1)
    df = calculate_returns(df)
    return (df, df['Strategy'][-1], df['Buy-Hold'][-1], df['Strategy-OB'][-1], df['Strategy-OS'][-1])


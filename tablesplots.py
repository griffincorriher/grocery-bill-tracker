import streamlit as st
from dataconnection import read_data, clear_worksheet
import plotly.graph_objects as go

def tablesplots(disableClearWorksheetButton=True):
    df = read_data()
    st.subheader("Current pay period grocery receipts")
    st.dataframe(df[df['pay period'] == df['pay period'].max()])


    if st.button("Clear worksheet", disabled = disableClearWorksheetButton):
        clear_worksheet()    

    # Group both by 'grocery date' and 'pay period'
    grocery_by_date = df.groupby('grocery date', as_index=False)['grocery bill'].sum().sort_values('grocery date').reset_index(drop=True)
    grocery_by_period = df.groupby('pay period', as_index=False)['grocery bill'].sum().sort_values('pay period').reset_index(drop=True)


    fig = go.Figure()
    # Line plot for grocery date
    fig.add_trace(go.Scatter(
        x=grocery_by_date['grocery date'],
        y=grocery_by_date['grocery bill'],
        mode='lines+markers',
        name='By Grocery Date',
        line=dict(color='blue'),
    ))

    # Bar plot for pay period
    fig.add_trace(go.Bar(
        x=grocery_by_period['pay period'],
        y=grocery_by_period['grocery bill'],
        name='By Pay Period',
        marker_color='orange',
        opacity=0.6,
    ))

    # Layout
    fig.update_layout(
        title='Grocery Bill Over Time',
        xaxis_title='Date',
        yaxis_title='Grocery Bill',
        barmode='overlay',  # or 'group' or 'stack'
        legend_title='Grouping',
        xaxis_type='date',
    )
    fig.update_xaxes(ticklabelmode="period", tickformat="%Y-%m-%d")
    
    # Show in Streamlit
    st.plotly_chart(fig)
    

    # import pandas as pd

    # adf = pd.DataFrame(dict( date=["2020-01-10", "2020-02-10", "2020-03-10", "2020-04-10", "2020-05-10", "2020-06-10"], value=[1,2,3,1,2,3] ))
    # fig = go.Figure()
    # fig.add_trace(go.Scatter( name="Raw Data", mode="markers+lines", x=adf["date"], y=adf["value"], marker_symbol="star" ))
    # fig.add_trace(go.Scatter( name="Start-aligned", mode="markers+lines", x=adf["date"], y=adf["value"], xperiod="M1", xperiodalignment="start" ))
    # fig.add_trace(go.Scatter( name="Middle-aligned", mode="markers+lines", x=adf["date"], y=adf["value"], xperiod="M1", xperiodalignment="middle" ))
    # fig.add_trace(go.Scatter( name="End-aligned", mode="markers+lines", x=adf["date"], y=adf["value"], xperiod="M1", xperiodalignment="end" ))
    # fig.add_trace(go.Bar( name="Middle-aligned", x=adf["date"], y=adf["value"], xperiod="M1", xperiodalignment="middle" ))
    # fig.update_xaxes(showgrid=True, ticklabelmode="period")
    # st.plotly_chart(fig)

    return
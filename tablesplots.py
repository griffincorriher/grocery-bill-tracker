import streamlit as st
from dataconnection import read_data, clear_worksheet
import plotly.graph_objects as go

def tablesplots():
    df = read_data()
    st.dataframe(df[df['pay period'] == df['pay period'].max()])

    if st.button("Clear worksheet", disabled=True):
        clear_worksheet()

    # Group both by 'grocery date' and 'pay period'
    grocery_by_date = df.groupby('grocery date', as_index=False)['grocery bill'].sum()
    grocery_by_period = df.groupby('pay period', as_index=False)['grocery bill'].sum()

    fig = go.Figure()

    # Line plot for grocery date
    fig.add_trace(go.Scatter(
        x=grocery_by_date['grocery date'],
        y=grocery_by_date['grocery bill'],
        mode='lines+markers',
        name='By Grocery Date',
        line=dict(color='blue')
    ))

    # Bar plot for pay period
    fig.add_trace(go.Bar(
        x=grocery_by_period['pay period'],
        y=grocery_by_period['grocery bill'],
        name='By Pay Period',
        marker_color='orange',
        opacity=0.6
    ))

    # Layout
    fig.update_layout(
        title='Grocery Bill Over Time',
        xaxis_title='Date',
        yaxis_title='Grocery Bill',
        barmode='overlay',  # or 'group' or 'stack'
        legend_title='Grouping',
    )

    # Show in Streamlit
    st.plotly_chart(fig)

    # st.line_chart(data=df, x='grocery date', y='grocery bill')

    # Display the table      



    return
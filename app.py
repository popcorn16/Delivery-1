# ***************************************
# Imports
# ***************************************
# Dash
# from turtle import color
# from matplotlib.colors import rgb2hex

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# Div.
import pandas as pd
import numpy as np
import calendar

# Plotly
import plotly.express as px
import plotly.graph_objects as go

# ***************************************
# Get data
# ***************************************
import datamodel
order = datamodel.get_data()
df_year = datamodel.get_year()
df_month = datamodel.get_month()




# ***************************************
# Diagram1 - Sales by Employees
# ***************************************
fig_employee = px.histogram(order,
    x='emp_name', y='total',
    color='type', title='Sales by employees',
    hover_data=[],
    labels={'total':'total sales', 'emp_name':'Employee', 'type':'Product category'})
fig_employee.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',
xaxis_tickangle=45)

fig_product = px.histogram(order, 

    x='productname', y='total',
    color='type', title='Sales by different products',
    hover_data=[],
    labels={'total':'total sales', 'productname':'Product', 'type':'Product category'})

# fig_product.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig_product.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',
xaxis_tickangle=45)


# ***************************************
# Activate the app
# ***************************************

dash_app = dash.Dash(__name__)
app = dash_app.server


# ***************************************
# Layout
# ***************************************
dash_app.layout = html.Div(children=[
    html.Div(className='row', children=[
        html.Div(className='four columns div-user-controls', children=[
            html.H2('Sales made by each employee'),
            html.P('Select filters from dropdown'),
            
        ]),
        html.Div(className='eight columns div-for-charts bg-grey', children=[
        dcc.Graph(id="sales_employee", figure=fig_employee)
    ])
]),

    html.Div(className='row', children=[
        html.Div(className='four columns div-user-controls', children=[
            html.H2('Sales sorted by products'),
            html.P('Select filters from dropdown'),

        ]),

        html.Div(className='eight columns div-for-charts bg-grey', children=[
            dcc.Graph(id="sales_product", figure=fig_product)
        ])
    ])
])


# ***************************************
# Callbacks
# ***************************************

@dash_app.callback(
    Output('sales_employee', 'figure'),

    [Input('drop_month', 'value')],
    [Input('drop_year', 'value')],
    )

def update_graph1(drop_month, drop_year):
    if drop_year:
        if drop_month:
            #Data i drop_month og drop_year
            order_fig1 = order.loc[(order['orderyear'] == drop_year) & (order['ordermonth'] == drop_month)]

        else:
            #Data i drop_year
            order_fig1 = order.loc[order['orderyear'] == drop_year]


    else:
        if drop_month:
        #Data i drop_month
            order_fig1 = order.loc[order['ordermonth'] == drop_month]
    
    
        else:
            # Ingen data
            order_fig1 = order


    return {'data':[go.Bar(
        x = order_fig1['emp_name'],
        y = order_fig1['total']
    
    )]}

def update_graph2(drop_month2, drop_year2):
    if drop_year2:
        if drop_month2:

            #Data i både drop_month og drop_year
            order_fig2 = order.loc[(order['orderyear'] == drop_year2) & (order['ordermonth'] == drop_month2)]
        
        
        else:
            # Data i drop_year
            order_fig2 = order.loc[order['orderyear'] == drop_year2]

    else:

        if drop_month2:
            # Data i drop_month
            order_fig2 = order.loc[order['ordermonth'] == drop_month2]

        else:
            # Ingen data
            order_fig2 = order

            
    return {'data':[go.Bar(
        x = order_fig2['productname'],
        y = order_fig2['total']
    )]}

#hotfix virkede ikke :( 2 fejl når webseveren køres.
suppress_callback_exceptions=True

# ***************************************
# Run the app
# ***************************************
if __name__ == '__main__':
    dash_app.run_server(debug=True)
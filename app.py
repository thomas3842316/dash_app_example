
# coding: utf-8

# In[6]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
df = pd.read_csv('nama_10_gdp_1_Data.csv')


df = pd.read_csv('nama_10_gdp_1_Data.csv', na_values=':',usecols=["TIME","UNIT","GEO","NA_ITEM","Value"])
df['Value']=df['Value'].str.replace(',','').astype(float)
df=df.dropna()
df=df[~df.GEO.str.contains("Eur") ==True]
df=df[~df.UNIT.str.contains("Current prices, million euro")]
df=df[~df.UNIT.str.contains("Chain linked volumes, index 2010=100")]
df.rename(columns={'NA_ITEM':'Indicator','TIME':'Year','GEO':'Country','UNIT':'Value Type'},inplace=True)

app = dash.Dash(__name__)
server = app.server


indicators = df['Indicator'].unique()
country = df['Country'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis_column_1',
                options=[{'label': i, 'value': i} for i in indicators],
                value = 'Gross domestic product at market prices'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='yaxis_column_1',
                options=[{'label': i, 'value': i} for i in indicators],
                value = 'Final consumption expenditure'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        step=None,
        marks={str(year): str(year) for year in df['Year'].unique()}
    ),
    
    html.Div(style={'height':50}),

    
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in country],
                value = 'Netherlands'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='yaxis_column_2',
                options=[{'label': i, 'value': i} for i in indicators],
                value = 'Final consumption expenditure'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='b-graphic')
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis_column_1', 'value'),
     dash.dependencies.Input('yaxis_column_1', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_1, yaxis_column_1, year_value):
    dff = df[df['Year'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator'] == xaxis_column_1]['Value'],
            y=dff[dff['Indicator'] == yaxis_column_1]['Value'],
            text=dff[dff['Indicator'] == yaxis_column_1]['Country'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_1,
                
            },
            yaxis={
                'title': yaxis_column_1,
                
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }



@app.callback(
    dash.dependencies.Output('b-graphic', 'figure'),
    [dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('yaxis_column_2', 'value')])

def update_graph( country,yaxis_column_2):
    dff = df[df['Country'] == country]
    return {
        'data': [go.Scatter(
            x= dff['Year'].unique(),
            y=dff[dff['Indicator'] == yaxis_column_2]['Value'],
            text=dff[dff['Indicator'] == yaxis_column_2]['Country'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Years',
                
            },
            yaxis={
                'title': yaxis_column_2,
                
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server()



import pandas as pd
import plotly as plt
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html, Input, Output
import datetime





#--------------------------------------

df = pd.read_csv("Catalogue_A.csv")

mark_values = {1874:'1874',1924:'1924',1974:'1974',2020:'2020'}



app = dash.Dash(__name__)

#print(df.head())
df.columns = ['test']

#df.drop()

df = df.test.str.split(";", expand=True)
df = df.drop([3, 4, 5, 6, 7, 8], axis = 1)
years = []
months = []
days = []
for index, row in df.iterrows():
    row[1] = float(row[1]) + float(row[2])

    [year, month, day] = row[0].split('-')
    years.append(int(year))
    months.append(int(month))
    days.append(int(day))
df = df.drop([2], axis = 1)

df['DateTime'] = df[0]
df['Sunspot Data'] = df[1]
df = df.drop([1], axis = 1)
df = df.drop([0], axis = 1)

df['Year'] = years
df['Month'] = months
df['Day'] = days



print(df)
def moving_average(df, number):
    new_df = df['Sunspot Data'].rolling(number).mean()
    new_df.dropna(inplace = True)

    df_final = new_df.to_frame()
    df_final = df_final.join(df['DateTime'])
    return df_final





#Modulus function for task 2
#Takes dataframe and Sunspot Cycle as value
#Creates column for modulated values
#Returns dataframe with new column 
def modulus(df, value):
    df["Modulus"] = ""
    modulated_list = []
    for index,row in df.iterrows():
        dateslist = (df["DateTime"][index]).split("-")
        date = float(dateslist[0])+(float(dateslist[1])/12) + (float(dateslist[2])/365)
        modulated = date % value
        modulated_list.append(modulated)
    
    df["Modulus"] = modulated_list
        
        
    return df





#'width': '90vh', 'height': '90vh', 

app.layout = html.Div([

        dcc.Graph(id='the_graph',style={'display': 'inline-block'}),
        dcc.Graph(id='graph2',style={'height': '42.5vh', 'display': 'inline-block'}) ,

        html.Label("Years"),
        dcc.RangeSlider(id='the_year',
            min=1874,
            max=2020,
            value=[1874,2020],
            tooltip={"placement": "bottom", "always_visible": True},
            updatemode='drag',
            marks=mark_values,
            step=1),

        html.Label("Observation Period (Months)"),
        dcc.Slider(id='observation_period',
            min=1,
            max=12,
            value=3,
            tooltip={"placement": "bottom", "always_visible": True},
            updatemode='drag',
            persistence=True,
            #marks=[mark_values],
            step=1),
        
        
        
        
        
        
        html.Label("Sunspot Cycle (Years)"),
        dcc.Slider(id='sunspot_cycle',
            min=1,
            max=30,
            value=11,
            tooltip={"placement": "bottom", "always_visible": True},
            updatemode='drag',
            marks=mark_values,
            step=1),
        
        
        
        html.H1('Realtime Sun'),
        dash.html.Img(src = 'https://soho.nascom.nasa.gov/data/realtime/hmi_igr/1024/latest.jpg', height = 300, width =300),
       
            
        
        
            
    
        

])



@app.callback(
    Output('the_graph', 'figure'), 
    [Input('the_year', 'value'), Input('observation_period', 'value')])



def update_graph(years, observation_period):


    dff = df[(df['Year']>=years[0])&(df['Year']<=years[1])]
    dfff = moving_average(dff, observation_period)
    
    fig = go.Figure()

    #fig = px.line(dff, x = "DateTime", y = "Sunspot Data")

    
    #fig.update_traces(line = dict(width=0.5), name="Daily")
    fig.add_trace(go.Scatter(x=dff["DateTime"], y=dff["Sunspot Data"], name="Daily", mode="lines", line=dict(width=0.5)))
    fig.add_trace(go.Scatter(x=dfff["DateTime"], y=dfff["Sunspot Data"], name="Smoothed", mode="lines", line=dict(width=0.5)))
    fig.update_layout(
        title="International Sunspot Numbers: Daily Mean and Monthly Smoothed Number", xaxis_title="Year", yaxis_title="# of SunSpots"
    )
    #fig.show()

  
    
    return fig


@app.callback(
    Output('graph2', 'figure'),
    [Input('observation_period', 'value'), Input('sunspot_cycle', 'value')] )

def update_graph2(observation_period, sunspot_cycle):
    dff = moving_average(df, observation_period)
    dfff = modulus(dff, sunspot_cycle)
    
    fig2 = go.Figure()
    fig2 = px.scatter(dfff, x="Modulus", y="Sunspot Data")
    fig2.update_traces(marker=dict(size=1))
    fig2.update_layout(
        title="Sunspot Cycle Variability", xaxis_title="Years", yaxis_title="# of SunSpots"
    )
    
    
    return fig2
        
  
    

if __name__ == '__main__':
    app.run_server(debug=True)


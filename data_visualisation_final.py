import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

data = pd.read_csv("C:\\MY WORK\\DS\\gfg_hackathon\\120 year olympic history\\medals.csv", header=0)
flags = pd.read_csv("C:\\MY WORK\\DS\\gfg_hackathon\\120 year olympic history\\flags_iso.csv", header=0, encoding='latin-1')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("OLYMICPEDIA", style={'textAlign': 'center'}),

    html.Div([
        html.A(html.Button("CHATBOT", style={
            "margin-right": "20px",
            'borderRadius': '10px',
            'padding': '10px',
            'fontSize': '16px',
            'backgroundColor': '#F8F8FF',  # Off-white
            'color': 'black',
            'border': 'none',
            'cursor': 'pointer',
            'textDecoration': 'none',
            'outline': 'none',
            'boxShadow': '0 9px #999'
        }), href="http://127.0.0.1:7861", target="_blank"),
        html.A(html.Button("PLANNERBOT", style={
            "margin-right": "20px",
            'borderRadius': '10px',
            'padding': '10px',
            'fontSize': '16px',
            'backgroundColor': '#F8F8FF',  # Off-white
            'color': 'black',
            'border': 'none',
            'cursor': 'pointer',
            'textDecoration': 'none',
            'outline': 'none',
            'boxShadow': '0 9px #999'
        }), href="http://127.0.0.1:7860", target="_blank"),
    ], style={'textAlign': 'center', 'margin': '20px'}),

    html.H2("Olympic Medal Count Graph", style={'textAlign': 'center'}),
    dcc.Graph(id='medal-count-graph'),
    
    dcc.Slider(id='max-entries-slider', min=1, max=len(data), value=10,
               marks={i: str(i) for i in range(1, len(data) + 1) if i % 10 == 0}, step=1),

    html.H2("Country Medal Count Table", style={'textAlign': 'center'}),
    html.Div(className="app-header",
             children=[
                 html.Div('Plotly Dash', className="app-header--title"),
                 html.Img(src='/bg.jpeg')
             ], id='image-table')
], style={
    'backgroundColor': '#f5f5dc',
    'border': '5px solid darkgrey',
})

@app.callback(
    [Output('medal-count-graph', 'figure'),
     Output('image-table', 'children')],
    [Input('max-entries-slider', 'value')]
)
def update_graph(max_entries):
    # Filter data to only include the selected number of entries
    filtered_data = data[:max_entries]

    fig = go.Figure()

    # Add the Gold, Silver, and Bronze medal counts for each country
    fig.add_trace(go.Bar(x=filtered_data['NOC'], y=filtered_data['Gold'], name='Gold', marker_color='gold'))
    fig.add_trace(go.Bar(x=filtered_data['NOC'], y=filtered_data['Silver'], name='Silver', marker_color='silver'))
    fig.add_trace(go.Bar(x=filtered_data['NOC'], y=filtered_data['Bronze'], name='Bronze', marker_color='brown'))

    fig.update_layout(
        title='Tokyo 2020 Results',
        xaxis_title='Country',
        yaxis_title='Medal Count',
        barmode='stack',  # Set to 'stack' for stacked bar chart
        hovermode='x',    # Enable hover data for each country
       legend=dict(orientation='h', yanchor='middle', xanchor='center', x=0.5, y=1),
        
        # Here's how you can change the background color:
        paper_bgcolor='#f5f5dc',
        plot_bgcolor='#f5f5dc',
        title_x=0.5,
    )

    # Create a table to store image components and medal counts for each country
    table_rows = []
    for idx, country in enumerate(filtered_data['NOC']):
        # Find the corresponding URL for the country
        url = flags.loc[flags['Country'] == country, 'URL'].values[0]

        # Create image component for the country flag
        flag_image = html.Img(src=url, style={'width': '100px', 'height': 'auto'})

        # Get medal counts for each country
        gold_medals = filtered_data.loc[filtered_data['NOC'] == country, 'Gold'].values[0]
        silver_medals = filtered_data.loc[filtered_data['NOC'] == country, 'Silver'].values[0]
        bronze_medals = filtered_data.loc[filtered_data['NOC'] == country, 'Bronze'].values[0]
        total_medals = gold_medals + silver_medals + bronze_medals

        # Create a new table row with flag, country name, and medal counts
        table_rows.append(html.Tr([
            html.Td(flag_image, style={'padding': '30px'}),
            html.Td(country, style={'padding': '30px','color': 'black'}),
            html.Td(gold_medals, style={'padding': '30px','color': 'black'}),
            html.Td(silver_medals, style={'padding': '30px','color': 'black'}),
            html.Td(bronze_medals, style={'padding': '30px','color': 'black'}),
            html.Td(total_medals, style={'padding': '30px','color': 'black'})
        ]))

    # Create the table with all the rows
    header = [
        html.Th("Flag", style={'padding': '30px'}),
        html.Th("Country Name", style={'padding': '30px','color': 'black'}),
        html.Th("Gold Medals", style={'padding': '30px','color': 'black'}),
        html.Th("Silver Medals", style={'padding': '30px','color': 'black'}),
        html.Th("Bronze Medals", style={'padding': '30px','color': 'black'}),
        html.Th("Total Medals", style={'padding': '30px','color': 'black'})
    ]
    image_table = html.Table([html.Thead(html.Tr(header)), html.Tbody(table_rows)], style={'border-spacing': '10px'})

    # Return both the figure and the table of image components and medal counts
    return fig, image_table

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
from flask import Flask
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from dash import dash_table
import os
from data_ingestion import DataIngestion

# Flask server instance
server = Flask(__name__)

# Initialize Dash app with Flask server
app = Dash(__name__, server=server)

# Load the dataset
#obj = DataIngestion() #instance
#df_copy=obj.initiate_data_ingestion() #return Dataset as datafrom  , using MongoDB database
file_path = os.path.join(os.getcwd() , "dataset\google_data_merged.csv") #file path
df_copy= pd.read_csv(file_path)
# Clean the data
df_copy['Price($)'] = df_copy['Price($)'].replace({'\$': '', '₹': ''}, regex=True).astype(float)
df_copy = df_copy.loc[:, ~df_copy.columns.str.contains('^Unnamed')]
df_copy['Installs'] = pd.to_numeric(df_copy['Installs'], errors='coerce') / 1e6  # Convert to millions
# App layout with Google-style theme (whitish green)
app.layout = html.Div(style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'backgroundColor': '#F0F4F3'}, children=[
    html.Div(
        children=[
            html.H1('Google Play Store Dashboard', style={'color': '#34A853', 'textAlign': 'center'}),
            html.Img(src=r'assets\share_google_play_logo.png', style={'borderRadius': '15px', 'display': 'block', 'margin': '0 auto'})
        ]
    ),

    # Two-column layout: Options on the left, plots on the right
    html.Div(style={'display': 'flex', 'width': '100%'}, children=[
        html.Div(style={'flex': '1', 'padding': '20px'}, children=[
            html.H3("Options", style={'textAlign': 'center'}),
            html.Button('Explore Playstore Dataset', id='explore-btn', style={'width': '100%', 'marginBottom': '10px'}),
            html.Button('Download Top Apps', id='download-btn', style={'width': '100%', 'marginBottom': '10px'}),

            # Checklist for column selection
            dcc.Checklist(
                id='column-checklist',
                options=[{'label': col, 'value': col} for col in df_copy.columns],
                value=[],  # No columns selected by default
                labelStyle={'display': 'block'}
            ),

            html.Br(),

            # Dropdown for heatmap selection
            dcc.Dropdown(
                id='heatmap-dropdown',
                options=[{'label': col, 'value': col} for col in df_copy.select_dtypes(include=['float64', 'int64']).columns],
                multi=True,
                placeholder="Select numeric columns for heatmap"
            ),
            html.Br(),

            # Additional dropdown for comparisons
            dcc.Dropdown(
                id='relation-dropdown',
                options=[
                    {'label': 'App vs Rating', 'value': 'app_rating'},
                    {'label': 'Rating vs Category', 'value': 'rating_category'},
                    {'label': 'Rating vs Month', 'value': 'rating_month'},
                    {'label': 'Rating vs Year', 'value': 'rating_year'}
                ],
                placeholder="Select relation plot"
            )
        ]),

        # Main output area
        html.Div(style={'flex': '3', 'padding': '20px'}, children=[
            html.Div(id='dataset-explorer'),
            html.Div(id='top-apps'),
            html.Div(id='heatmap-plot'),
            html.Div(id='summary-text'),
            html.Div(id='comparison-plot')
        ])
    ]),
    
    # Footer
    html.Footer(style={'marginTop': '20px', 'textAlign': 'center'}, children=[
        "Created by Rajat Singh"
    ])
])

# Callback for exploring the dataset
@app.callback(
    Output('dataset-explorer', 'children'),
    [Input('explore-btn', 'n_clicks')]
)
def explore_dataset(n_clicks):
    if n_clicks is None:
        return html.Div()
    return html.Div([
        html.H3("Explore Dataset:", style={'textAlign': 'center'}),
        html.Div(id='data-output')
    ])

# Callback for displaying data based on selected columns
@app.callback(
    Output('data-output', 'children'),
    [Input('column-checklist', 'value')]
)
def display_data(selected_columns):
    if not selected_columns:
        return html.Div("No columns selected", style={'textAlign': 'center'})

    filtered_df = df_copy[selected_columns]

    visuals = []
    for col in selected_columns:
        visuals.append(
            dcc.Graph(
                figure=px.histogram(
                    filtered_df,
                    x=col,
                    title=f'Distribution of {col}',
                    template='plotly_white',
                    color_discrete_sequence=px.colors.qualitative.Plotly
                )
            )
        )
    return html.Div(visuals)

# Callback for showing top-rated apps
@app.callback(
    Output('top-apps', 'children'),
    [Input('download-btn', 'n_clicks')]
)
def show_top_apps(n_clicks):
    if n_clicks is None:
        return html.Div()

    top_10_apps = df_copy[['App', 'Installs']].drop_duplicates().sort_values(by='Installs', ascending=False).head(10)
    top_10_apps["Installs"]= top_10_apps["Installs"].astype(int)
    top_10_apps.rename(columns={"Installs":"Installs(M)"} , inplace=True)

    # Display top apps in a DataTable
    top_apps_table = dash_table.DataTable(
        id='top-apps-table',
        columns=[
            {"name": "App", "id": "App"},
            {"name": "Installs(M)", "id": "Installs(M)"}
        ],
        data=top_10_apps.to_dict('records'),  # Convert DataFrame to dict records
        style_header={
            'backgroundColor': '#34A853',
            'fontWeight': 'bold',
            'color': 'white',
            'textAlign': 'center'
        },
        style_cell={
            'textAlign': 'center',
            'padding': '10px',
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_table={
            'width': '100%',
            'margin': 'auto'
        }
    )

    return html.Div(children=[
        html.H3("Top 10 Apps by Installs in Millions", style={'textAlign': 'center'}),
        top_apps_table
    ])

# Callback for heatmap
@app.callback(
    Output('heatmap-plot', 'children'),
    [Input('heatmap-dropdown', 'value')]
)
def display_heatmap(selected_columns):
    if not selected_columns:
        return html.Div("Select numeric columns for heatmap.", style={'textAlign': 'center'})

    filtered_df = df_copy[selected_columns]
    correlation_matrix = filtered_df.corr()

    fig = px.imshow(correlation_matrix, title="Correlation Heatmap", labels=dict(x='Columns', y='Columns'),
                    color_continuous_scale='Viridis', text_auto=True)

    return dcc.Graph(figure=fig)

# Callback for displaying relations
@app.callback(
    Output('comparison-plot', 'children'),
    [Input('relation-dropdown', 'value')]
)
def display_relation(selected_option):
    if not selected_option:
        return html.Div("Select a relation option.", style={'textAlign': 'center'})

    if selected_option == 'app_rating':
        fig = px.scatter(df_copy, x='App', y='Rating', title="App vs Rating", color='Category', template='plotly_white')
    elif selected_option == 'rating_category':
        fig = px.box(df_copy, x='Category', y='Rating', title="Rating vs Category", template='plotly_white')
    elif selected_option == 'rating_month':
        fig = px.box(df_copy, x='Month', y='Rating', title="Rating vs Month", template='plotly_white')
    else:  # 'rating_year'
        fig = px.box(df_copy, x='Year', y='Rating', title="Rating vs Year", template='plotly_white')

    return dcc.Graph(figure=fig)

# Run Flask/Dash server with debug mode disabled for production
if __name__ == '__main__':
    app.run_server(debug=False, port=8050)

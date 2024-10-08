import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from dash import dash_table
from data_ingestion  import DataIngestion# make sure  to dump cleaned dataset inside MongoDb first , using data_dump.py
import sys
# Load your dataset
try :
    object=DataIngestion()
    df_copy = object.initiate_data_ingestion() #importing dataset from MongoDb Atlas
except Exception as e:
    print(e , sys)    

# Clean the data: Convert the 'Price' column to numeric, remove '$' sign
df_copy['Price($)'] = df_copy['Price($)'].replace({'\$': '', '₹': ''}, regex=True).astype(float)

# Remove unnamed columns
df_copy = df_copy.loc[:, ~df_copy.columns.str.contains('^Unnamed')]

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# App layout
app.layout = html.Div(style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}, children=[
    # Center the title
    html.Div(
        children=[
            html.H1('Google Play Store Dashboard', style={'color': '#34A853', 'textAlign': 'center'}),
            html.Img(src='assets\share_google_play_logo.png',
                     style={'borderRadius': '15px', 'display': 'block', 'margin': '0 auto'})
        ]
    ),

    # Layout with two columns: options on the left and outputs on the right
    html.Div(style={'display': 'flex', 'width': '100%'}, children=[
        html.Div(style={'flex': '1', 'padding': '20px'}, children=[
            html.H3("Options", style={'textAlign': 'center'}),
            html.Button('Explore Playstore Dataset', id='explore-btn', style={'width': '100%', 'marginBottom': '10px'}),
            html.Button('Download Top Apps', id='download-btn', style={'width': '100%', 'marginBottom': '10px'}),
            
            # Checklist for general plot selection
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
                placeholder="Select numeric columns for heatmap",
            ),
            html.Br()
        ]),

        # Main output area
        html.Div(style={'flex': '3', 'padding': '20px'}, children=[
            html.Div(id='dataset-explorer'),  # Placeholder for dataset exploration
            html.Div(id='top-apps'),  # Placeholder for displaying top apps
            html.Div(id='heatmap-plot'),  # Placeholder for heatmap
            html.Div(id='summary-text'),  # Placeholder for summary text
            html.Div(id='relation-plot')  # Placeholder for relation plot
        ])
    ])
])

# Callback for exploring the dataset
@app.callback(
    Output('dataset-explorer', 'children'),
    [Input('explore-btn', 'n_clicks')]
)
def explore_dataset(n_clicks):
    if n_clicks is None:
        return html.Div()  # Return empty if button hasn't been clicked
    
    return html.Div([
        html.H3("Explore Dataset:", style={'textAlign': 'center'}),
        html.Div(id='data-output')  # This div will hold the output of selected columns
    ])

# Callback for displaying data based on selected columns from checkboxes
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
                    color_discrete_sequence=px.colors.qualitative.Plotly  # Best color palette
                )
            )
        )

    return html.Div(visuals)

# Callback for showing top-rated apps after clicking 'Download App'
@app.callback(
    Output('top-apps', 'children'),
    [Input('download-btn', 'n_clicks')]
)
def show_top_apps(n_clicks):
    if n_clicks is None:
        return html.Div()  # Return empty if button hasn't been clicked
    
    # Get top 10 apps by installs
    top_apps = df_copy[['App', 'Installs']].sort_values(by='Installs', ascending=False).head(10)

    app_names = [
        html.Div(
            f"{row['App']} (Installs: {row['Installs']})", 
            style={'textAlign': 'center'}
        )
        for index, row in top_apps.iterrows()
    ]

    return html.Div([
        html.H3("Top 10 Apps by Installs:", style={'textAlign': 'center'}),
        *app_names  # Unpack app names into the Div
    ])

# Callback to display the heatmap of correlations
@app.callback(
    Output('heatmap-plot', 'children'),
    [Input('heatmap-dropdown', 'value')]
)
def display_heatmap(selected_columns):
    if not selected_columns:
        return html.Div("Select numeric columns for heatmap.", style={'textAlign': 'center'})

    # Select only numeric columns for correlation
    filtered_df = df_copy[selected_columns]

    # Calculate the correlation matrix
    correlation_matrix = filtered_df.corr()

    # Create a heatmap using Plotly with annotations
    fig = px.imshow(
        correlation_matrix,
        title="<b>Correlation Heatmap</b>",
        labels=dict(x='Columns', y='Columns'),
        color_continuous_scale='Viridis',
        text_auto=True  # Enable annotations
    )

    return dcc.Graph(figure=fig)

# Callback for displaying summary text based on selected options
@app.callback(
    Output('summary-text', 'children'),
    [Input('column-checklist', 'value')]
)
def update_summary(selected_columns):
    if not selected_columns:
        return "Select options to see the summary."
    
    # Filter to keep only numerical columns
    numerical_columns = df_copy.select_dtypes(include=['float64', 'int64']).columns.intersection(selected_columns)

    if numerical_columns.empty:
        return "No numerical columns selected for summary."

    # Generate summary statistics
    summary_df = df_copy[numerical_columns].describe().reset_index()

    # Create a DataTable to display the summary
    summary_table = dash_table.DataTable(
        data=summary_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in summary_df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        page_size=10  # Number of rows per page
    )

    return summary_table

# Callback for displaying the relationship between App, Month, and Year
@app.callback(
    Output('relation-plot', 'children'),
    [Input('column-checklist', 'value')]
)
def display_relation(selected_columns):
    if not selected_columns or 'Month' not in selected_columns or 'Year' not in selected_columns:
        return html.Div("Select 'Month' and 'Year' to see the relationship with App.", style={'textAlign': 'center'})

    # Create a scatter plot for App, Month, and Year
    fig = px.scatter(
        df_copy,
        x='Month',
        y='Year',
        color='App',
        title='Relationship between App, Month, and Year',
        color_discrete_sequence=px.colors.qualitative.Plotly  # Best color palette
    )

    return dcc.Graph(figure=fig)




# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


# Import the required libraries
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data into Pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# List of years for the period 1980-2023 inclusive
year_list = [i for i in range(1980, 2024, 1)]

# Initialize a Dash application
app = dash.Dash(__name__)

# Create the layout of the app
# TASK 1- Add title
app.layout = html.Div([
    html.H1('Automobile Sales Statistics Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),

# TASK 2- Add two drop down menus
    html.Div([
        html.Label('Select Statistics: '),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'},
            ],
            value='Select Statistics',
            placeholder='Select a report type'
        ),
    ], style={'textAlign': 'center', 'width': '80%', 'padding': '3px', 'font-size': 20}),

    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': str(i), 'value': i} for i in year_list],
            placeholder='Select a year'
        ),
    ], style={'textAlign': 'center', 'width': '80%', 'padding': '3px', 'font-size': 20}),

    # Initial skeleton
    # Create a 2x2 grid for charts
    html.Div([
        html.Div(id='chart1', className='chart-item', style={'border': '2px solid #000', 'border-radius': '10px', 'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.3)', 'background-color': 'lightblue'}),
        html.Div(id='chart2', className='chart-item', style={'border': '2px solid #000', 'border-radius': '10px', 'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.3)', 'background-color': 'lightgreen'}),
    ], style={'display': 'flex', 'flex-wrap': 'wrap'}),

    # Add the second row of charts
    html.Div([
        html.Div(id='chart3', className='chart-item', style={'border': '2px solid #000', 'border-radius': '10px', 'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.3)', 'background-color': 'lightpink'}),
        html.Div(id='chart4', className='chart-item', style={'border': '2px solid #000', 'border-radius': '10px', 'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.3)', 'background-color': 'lightyellow'}),
    ], style={'display': 'flex', 'flex-wrap': 'wrap'}),
])
   
# Task 2.3 - output container
    # Add the output-container
    html.Div(id='output-container', className='chart-grid', style={'display': 'block'}),
])

# TASK 2.4: Creating Callbacks and Define the callback function to update the input container based on the selected statistics and the output container
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)

# Define update_input_container
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False  # Enable the select-year dropdown
    else:
        return True  # Disable the select-year dropdown

@app.callback(
    [Output('chart1', 'children'), Output('chart2', 'children'), Output('chart3', 'children'), Output('chart4', 'children')],
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)

# Define update_output_container
def update_output_container(selected_statistics, selected_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

# TASK 2.5: Create and display graphs for Recession Report Statistics
        # Plot 1: Automobile sales fluctuate over the Recession Period (year-wise) using a line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title='Automobile Sales Fluctuation Over Recession Period (Year-wise)')
        )

        # Plot 2: Calculate the average number of vehicles sold by vehicle type and represent it as a Bar chart
        vehicle_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(vehicle_sales, x='Vehicle_Type', y='Automobile_Sales', title='Average Number of Vehicles Sold by Vehicle Type')
        )

        # Plot 3: Pie chart for the total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type', title='Total Expenditure Share by Vehicle Type During Recessions')
        )

        # Plot 4: Develop a Bar chart for the effect of the unemployment rate on vehicle type and sales
        unemployment_effect = recession_data.groupby('Vehicle_Type')['unemployment_rate'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemployment_effect, x='Vehicle_Type', y='unemployment_rate', title='Effect of Unemployment Rate on Vehicle Type and Sales')
        )

        return R_chart1, R_chart2, R_chart3, R_chart4

# TASK 2.6: Create and display graphs for Yearly Report Statistics
    elif selected_statistics == 'Yearly Statistics' and selected_year:
        # Filter the data based on the selected year
        yearly_data = data[data['Year'] == selected_year]

        # Plot 1: Yearly Automobile sales using a line chart for the whole period.
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, x='Year', y='Automobile_Sales', title='Yearly Automobile Sales (Whole Period)')
        )

        # Plot 2: Total Monthly Automobile sales using a line chart.
        Y_chart2 = dcc.Graph(
            figure=px.line(data, x='Month', y='Automobile_Sales', title=f'Total Monthly Automobile Sales in the year {selected_year}')
        )

        # Plot 3: Bar chart for the average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', title=f'Average Vehicles Sold by Vehicle Type in the year {selected_year}')
        )

        # Plot 4: Total Advertisement Expenditure for each vehicle using a pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type', title=f'Total Advertisement Expenditure by Vehicle Type in the year {selected_year}')
        )

        return Y_chart1, Y_chart2, Y_chart3, Y_chart4

    else:
        return [None, None, None, None]

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
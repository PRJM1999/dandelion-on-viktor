from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from munch import munchify

import plotly.graph_objects as go

from src.charts import flood_plot, plotly_flood_plot


def clear_epw_charts():
    plt.close('all')


def clear_epw_chart(element_id):
    plt.figure(element_id)
    plt.clf()


def color_pallete_presets():
    return munchify({
        'blue_to_red_8': [
            'darkblue', 'blue', 'cyan', 'greenyellow', 'yellow', 'orange', 'red', 'darkred'
        ],
        'blue_to_red_10': [
            '#2c2977', '#38429b', '#4252a4', '#4b62ad', '#68b8e7', '#53b848',
            'darkorange', 'red', 'firebrick', 'maroon'
        ],
        'blue_to_red_7': [
            '#4252a4', '#4b62ad', '#68b8e7', '#53b848', '#ee8522', '#ea2b24', '#b12224'
        ],
        'blue_to_gray': ['lightskyblue', 'darkslategray'],
        'blue_to_gray_11': [
            '#6fdcfb', '#6bcde9', '#68bfd8', '#65b1c7', '#62a3b6', '#5f95a5',
            '#5b8793', '#587982', '#556b71', '#525d60', '#4f4f4f'
        ]
    })


def epw_data(epw, value):
    month = epw["month"]
    day = epw["day"]
    hour = epw["hour"]
    day_of_year = []
    data = []

    for i, val in enumerate(value):
        day_of_year.append(i // 24 + 1)
        datum = {
            "index": i,
            "month": month[i],
            "day": day[i],
            "hour": hour[i],
            "day_of_year": day_of_year[i],
            "value": val
        }
        data.append(datum)

    # print(data)
    return data


def val_C_to_F(value, index, arr):
    arr[index] = 32 + value * 1.8


def convert_C_to_F(array):
    for index, value in enumerate(array):
        val_C_to_F(value, index, array)
    return array


def epw_temp_flood_plot(epw: pd.DataFrame):
    print('printing TempFloodPlot')
    selected_columns = ['year', 'month', 'day', 'hour', 'minute', 'dryBulbTemperature']
    data = epw[selected_columns]
    # Convert the date and time fields into a datetime object
    data['datetime'] = pd.to_datetime(data[['year', 'month', 'day', 'hour', 'minute']])
    # Extract the day of the year for x-axis
    data['day_of_year'] = data['datetime'].dt.dayofyear
    # Compute minutes from midnight for y-axis
    data['minutes'] = data['datetime'].dt.hour * 60 + data['datetime'].dt.minute

    # Aggregate data by day of year and minutes
    agg_data = data.groupby(['minutes', 'day_of_year']).mean()['dryBulbTemperature'].unstack()

    # Create a heatmap
    heatmap = go.Heatmap(
        z=agg_data.values,  # Data values
        x=agg_data.columns,  # Day of year on x-axis
        y=agg_data.index,  # Minutes on y-axis
        colorscale='jet',  # Color scale for the heatmap
        colorbar=dict(
            title='Temperature (°C)',  # Title for the color bar indicating temperature in Celsius
            titleside='right'
        )
    )

    # Layout configuration, including custom tick marks
    layout = go.Layout(
        title='Dry Bulb Temperature Distribution',
        xaxis=dict(
            title='Month',
            tickmode='array',
            tickvals=[15, 46, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349],
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),
        yaxis=dict(
            title='Time of Day',
            tickmode='array',
            tickvals=[0, 180, 360, 540, 720, 900, 1080, 1260, 1380],
            ticktext=['12 AM', '3 AM', '6 AM', '9 AM', '12 PM', '3 PM', '6 PM', '9 PM', '11 PM']
        )
    )

    # Creating the figure with data and layout
    fig = go.Figure(data=[heatmap], layout=layout)
    return fig


def epw_utc_i_flood_plot(epw):
    print('printing UTCIFloodPlot')
    data = epw['utciResults']['utci']
    units = '°C'
    color_range = color_pallete_presets().blue_to_red_10
    color_gradient = [-40, -27, -13, 0, 9, 26, 32, 38, 46]
    return flood_plot(data, units, color_range, color_gradient, True)


def epw_comfort_flood_plot(epw):
    print('printing ComfortFloodPlot')
    data = epw['utciResults']['comfortRating']
    units = ''
    color_range = color_pallete_presets().blue_to_red_7
    color_gradient = [-3, -2, -1, 0, 1, 2, 3]
    return flood_plot(data, units, color_range, color_gradient, False)


def epw_rh_flood_plot(epw):
    print('printing RH FloodPlot')
    selected_columns = ['year', 'month', 'day', 'hour', 'minute', 'relativeHumidity']
    data = epw[selected_columns]
    # Convert the date and time fields into a datetime object
    data['datetime'] = pd.to_datetime(data[['year', 'month', 'day', 'hour', 'minute']])
    # Extract the day of the year for x-axis
    data['day_of_year'] = data['datetime'].dt.dayofyear
    # Compute minutes from midnight for y-axis
    data['minutes'] = data['datetime'].dt.hour * 60 + data['datetime'].dt.minute

    # Aggregate data by day of year and minutes
    agg_data = data.groupby(['minutes', 'day_of_year']).mean()['relativeHumidity'].unstack()

    # Create a heatmap
    heatmap = go.Heatmap(
        z=agg_data.values,  # Data values
        x=agg_data.columns,  # Day of year on x-axis
        y=agg_data.index,  # Minutes on y-axis
        colorscale='blues',  # Color scale for the heatmap
        colorbar=dict(
            title='Relative Humidity',  # Title for the color bar indicating temperature in Celsius
            titleside='right'
        )
    )

    # Layout configuration, including custom tick marks
    layout = go.Layout(
        title='Relative Humidity %',
        xaxis=dict(
            title='Month',
            tickmode='array',
            tickvals=[15, 46, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349],
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),
        yaxis=dict(
            title='Time of Day',
            tickmode='array',
            tickvals=[0, 180, 360, 540, 720, 900, 1080, 1260, 1380],
            ticktext=['12 AM', '3 AM', '6 AM', '9 AM', '12 PM', '3 PM', '6 PM', '9 PM', '11 PM']
        )
    )

    # Creating the figure with data and layout
    fig = go.Figure(data=[heatmap], layout=layout)
    return fig


def epw_cloud_flood_plot(epw):
    print('printing Cloud cover FloodPlot')
    selected_columns = ['year', 'month', 'day', 'hour', 'minute', 'totalSkyCover']
    data = epw[selected_columns]
    # Convert the date and time fields into a datetime object
    data['datetime'] = pd.to_datetime(data[['year', 'month', 'day', 'hour', 'minute']])
    # Extract the day of the year for x-axis
    data['day_of_year'] = data['datetime'].dt.dayofyear
    # Compute minutes from midnight for y-axis
    data['minutes'] = data['datetime'].dt.hour * 60 + data['datetime'].dt.minute

    # Aggregate data by day of year and minutes
    agg_data = data.groupby(['minutes', 'day_of_year']).mean()['totalSkyCover'].unstack()

    # Create a heatmap
    heatmap = go.Heatmap(
        z=agg_data.values,  # Data values
        x=agg_data.columns,  # Day of year on x-axis
        y=agg_data.index,  # Minutes on y-axis
        colorscale='blues',  # Color scale for the heatmap
        colorbar=dict(
            title='Relative Humidity',  # Title for the color bar indicating temperature in Celsius
            titleside='right'
        )
    )

    # Layout configuration, including custom tick marks
    layout = go.Layout(
        title='Cloud Cover %',
        xaxis=dict(
            title='Month',
            tickmode='array',
            tickvals=[15, 46, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349],
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),
        yaxis=dict(
            title='Time of Day',
            tickmode='array',
            tickvals=[0, 180, 360, 540, 720, 900, 1080, 1260, 1380],
            ticktext=['12 AM', '3 AM', '6 AM', '9 AM', '12 PM', '3 PM', '6 PM', '9 PM', '11 PM']
        )
    )

    # Creating the figure with data and layout
    fig = go.Figure(data=[heatmap], layout=layout)
    return fig


def epw_wind_rose(epw_data):
    print('Printing Wind Rose Graph')

    stats_df = epw_data.get_wind_stats()

    # Creating the wind rose plot
    wind_rose = go.Barpolar(
        r=stats_df['Frequency'],
        theta=stats_df['Wind Direction Bin'],
        marker=dict(
            color=stats_df['Average_Speed'],
            colorscale='blues',  # You can choose a different color scale as needed
            cmin=stats_df['Average_Speed'].min(),
            cmax=stats_df['Average_Speed'].max()
        ),
        hoverinfo='r+theta'
    )

    # Layout configuration
    layout = go.Layout(
        title='Wind Rose',
        polar=dict(
            radialaxis=dict(
                visible=False,  # Change this to True
                range=[0, stats_df['Frequency'].max()]  # Make sure this is set to the max of Frequency, not Average_Speed
            )
        ),
        legend=dict(title='Wind Speed (m/s)')
    )


    # Creating the figure with data and layout
    fig = go.Figure(data=[wind_rose], layout=layout)
    return fig


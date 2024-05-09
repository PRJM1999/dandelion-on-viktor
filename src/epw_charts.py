from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from ladybug.epw import EPW


def clear_epw_charts():
    plt.close('all')


def clear_epw_chart(element_id):
    plt.figure(element_id)
    plt.clf()

    arr[index] = 32 + value * 1.8


def epw_temp_flood_plot(epw: EPW):
    datetimes = [datetime.strptime(dt_str, "%d %b %H:%M") for dt_str in epw.dry_bulb_temp.datetime_strings]
    day_of_year_list = [dt.timetuple().tm_yday for dt in datetimes]
    minute_list = [dt.hour * 60 + dt.minute for dt in datetimes]


    # Create a heatmap
    heatmap = go.Heatmap(
        z=epw.dry_bulb_temp.values,  # Data values
        x=day_of_year_list,  # Day of year on x-axis
        y=minute_list,  # Minutes on y-axis
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


def epw_rh_flood_plot(epw: EPW):
    datetimes = [datetime.strptime(dt_str, "%d %b %H:%M") for dt_str in epw.relative_humidity.datetime_strings]
    day_of_year_list = [dt.timetuple().tm_yday for dt in datetimes]
    minute_list = [dt.hour * 60 + dt.minute for dt in datetimes]


    # Create a heatmap
    heatmap = go.Heatmap(
        z=epw.relative_humidity.values,  # Data values
        x=day_of_year_list,  # Day of year on x-axis
        y=minute_list,  # Minutes on y-axis
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


def epw_cloud_flood_plot(epw: EPW):
    datetimes = [datetime.strptime(dt_str, "%d %b %H:%M") for dt_str in epw.total_sky_cover.datetime_strings]
    day_of_year_list = [dt.timetuple().tm_yday for dt in datetimes]
    minute_list = [dt.hour * 60 + dt.minute for dt in datetimes]

    # Create a heatmap
    heatmap = go.Heatmap(
        z=epw.total_sky_cover.values,  # Data values
        x=day_of_year_list,  # Day of year on x-axis
        y=minute_list,  # Minutes on y-axis
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


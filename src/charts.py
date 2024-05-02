import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from plotly import graph_objects as go


def plotly_flood_plot(data: pd.DataFrame, x: str, y: str, z: str):
    # Aggregate data by month and hour
    agg_data = data.groupby([y, x]).mean()[z].unstack()

    # Create a heatmap
    heatmap = go.Heatmap(
        z=agg_data.values.tolist(),  # Convert DataFrame to list for Plotly
        x=agg_data.columns.tolist(),  # Hours on x-axis
        y=agg_data.index.tolist(),  # Months on y-axis
        colorscale='Viridis',  # Choose your preferred colorscale
    )

    layout = go.Layout(
        title=z,
        xaxis=dict(title=x),
        yaxis=dict(title=y)
    )

    fig = go.Figure(data=[heatmap], layout=layout)
    return fig


def flood_plot(data, units, color_range, color_gradient=[], legend_as_range=False, legend_notes=[]):
    # Define chart variables
    hours_in_day = 24
    typical_leap_year = 2020
    typical_non_leap_year = 2021
    # Get an example year format from data size
    typical_year = typical_leap_year if len(data) == 8760 else typical_non_leap_year
    # Define chart dimensions
    margin = {'top': 5, 'right': 20, 'bottom': 25, 'left': 50, 'spacing': 20}
    width = 1200
    height = 200
    legend_width = 200 if legend_notes else 75

    # Compute remaining dimensions
    chart_width = width - margin['left'] - margin['spacing'] - legend_width - margin['right']
    chart_height = height - margin['top'] - margin['bottom']
    col_width = chart_width / (len(data) / hours_in_day) + 0.5  # 0.5 extra to account for no border around rectangles
    row_height = chart_height / hours_in_day + 0.5  # 0.5 extra to account for no border around rectangles

    # If colorGradient values are not provided, then create an array that fits the data
    if not color_gradient:
        color_gradient = fit_data_to_color_range(data, color_range)

    # Define scales to translate between chart values and data
    y_scale = mdates.DateFormatter('%I %p')
    x_scale = mdates.DateFormatter('%B')

    # Define color scale
    color_scale = plt.cm.colors.LinearSegmentedColormap.from_list('custom', color_range)

    # Precompute date arrays for efficiency
    x_dates = [np.datetime64(f'{typical_year}-01-01') + np.timedelta64(int(i / hours_in_day), 'D') for i in range(len(data))]
    y_dates = [np.datetime64('2000-01-01') + np.timedelta64(i % hours_in_day, 'h') for i in range(len(data))]

    # Build chart
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # Add the rectangles that create the flood plot
    for i, d in enumerate(data):
        rect = plt.Rectangle((mdates.date2num(x_dates[i]), mdates.date2num(y_dates[i])),
                             col_width, row_height, color=color_scale(d))
        ax.add_patch(rect)

    # Set axis labels
    ax.set_xlabel('Month')
    ax.set_ylabel('Time of Day')

    # Add the legend
    # if legend_as_range:
    #     add_legend_with_label_as_range(ax, color_scale, units)
    # else:
    #     add_legend(ax, color_scale, units, legend_notes)

    return plt


def add_legend(chart_container, x, y, color_scale, units, legend_height, legend_notes):
    # Domain is reversed to show legend from max to min rather min to max as it's defined
    color_domain = sorted(color_scale.domain())
    color_width = 18
    spacing = 5

    # Define y position scales
    y_position = {color: y + i * (legend_height / len(color_domain)) for i, color in enumerate(color_domain)}

    # Create legend container
    legend_container = chart_container.append('g')

    # Create a group for each entry
    entries = legend_container.selectAll('g')
    entries = entries.data(color_domain).enter().append('g').attr('class', 'legend').attr('transform', lambda d: f'translate({x}, {y_position[d]})')

    # Add a color rectangle to entry group
    colors = entries.append('rect')
    colors.attr('width', color_width).attr('height', legend_height / len(color_domain)).attr('fill', lambda d: color_scale(d)).attr('stroke', 'dimgray').attr('stroke-width', 0.5)

    # Add label to entry group
    labels = entries.append('text')
    labels.attr('x', color_width + spacing).attr('y', (legend_height / len(color_domain)) / 2).attr('dy', '0.35em').text(lambda d: f'{round(d * 2) / 2} {units}').style('font-size', 10)

    # Add note to entry group
    if legend_notes:
        notes = entries.append('text')
        notes.attr('x', color_width + spacing + 25).attr('dx', spacing).attr('y', (legend_height / len(color_domain)) / 2).attr('dy', '0.35em').text(lambda d, i: legend_notes[i]).style('font-size', 10)


def add_legend_with_label_as_range(chart_container, x, y, color_scale, units, legend_height):
    # Domain is reversed to show legend from max to min rather min to max as it's defined
    color_domain = sorted(color_scale.domain())
    color_domain.append(color_domain[-1] - 5)

    color_width = 18
    spacing = 5

    # Define y position scales
    y_position = {color: y + i * (legend_height / len(color_domain)) for i, color in enumerate(color_domain)}

    # Create legend container
    legend_container = chart_container.append('g')

    # Add a color rectangle to entry group
    colors = legend_container.selectAll('rect')
    colors = colors.data(color_domain).enter().append('rect')
    colors.attr('transform', lambda d: f'translate({x}, {y_position[d]})')
    colors.attr('width', color_width).attr('height', legend_height / len(color_domain))
    colors.attr('fill', lambda d: color_scale(d + 2))  # Value+1 unit to make sure correct color band is displayed
    colors.attr('stroke', 'dimgray').attr('stroke-width', 0.5)

    # Add label to entry group
    labels = legend_container.selectAll('text')
    labels = labels.data(color_domain[:-1]).enter().append('text')
    labels.attr('transform', lambda d: f'translate({x}, {y_position[d]})')
    labels.attr('x', color_width + spacing).attr('y', (legend_height / len(color_domain)))
    labels.attr('dy', '0.35em').text(lambda d: f'{round(d * 2) / 2} {units}').style('font-size', 10)


def fit_data_to_color_range(data, color_range):
    # Fit data to requested colors
    # Calculate the value (or limit) for each color and push each value into array
    # If only two colors requested, return min max only and scale will handle it
    data_min = min(data)
    data_max = max(data)
    extent = data_max - data_min
    gradient_step = extent / (len(color_range) - 1)  # -1 to give correct stepping between min and max
    gradient_values = [data_min + i * gradient_step for i in range(len(color_range))]
    # If 2 colors provided, then only min max can be used
    if len(color_range) == 2:
        gradient_values = [data_min, data_max]
    return gradient_values

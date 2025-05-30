import polars as pl
import plotly.express as px
import plotly.subplots
import plotly.graph_objects as go

import os
from pprint import pprint
from typing import List
import glob
import time
import datetime

# Define the directory name (adjust if needed)
DATA_DIR = "../history"

def scrape_csv_data(file_path: str) -> pl.DataFrame:
    """
    Returns a list of all files matching the given glob pattern.
    """
    csv_files = glob.glob(file_path)
    # Load each CSV and tag it with timestamp from filename
    dfs = []
    for file_path in csv_files:
        # Extract timestamp from filename (e.g., '2025-05-01.csv')
        filename = os.path.basename(file_path)
        timestamp_str = filename.replace(".csv", "")

        # Read CSV and add a 'Timestamp' column with the extracted date
        df = pl.read_csv(file_path).with_columns([
            pl.lit(timestamp_str).alias("Timestamp")
        ])
        dfs.append(df)

    # Concatenate all into a single DataFrame
    combined_df = pl.concat(dfs)
    combined_df = pre_process_data(combined_df)

    return combined_df

def pre_process_data(df) -> pl.DataFrame:
    """
    Pre-process the DataFrame
    """

    df = df.filter(pl.col("Name") != "Felcloth")
    df = df.filter(pl.col("Name") != "Firebloom")

    return df

def weekly_overview(df: pl.DataFrame) -> go.Figure:
    """
    Create a weekly overview of the data.
    """
    # Unique timestamps represents batch imports
    df = df.select("Timestamp").unique()

    # Append an 'Hour' column for heatmap
    df = df.with_columns([
        pl.col("Timestamp").dt.hour().alias("hour")
    ])

    # Append a weekday column for heatmap
    df = df.with_columns([
        pl.col("Timestamp").dt.weekday().alias("weekday")
    ])

    # Group by hour and weekday, then do a count on occurances
    df = df.select(["hour", "weekday"])
    df = (
        df.group_by(["weekday", "hour"])
        .agg(pl.len().alias("count"))
        .sort(["weekday", "hour"])
    )

    pivoted = df.pivot(
            index="weekday",
            on="hour",
            values="count",
        ).sort('weekday')

    # Convert to pandas DataFrame for plotting
    plot_df = pivoted.to_pandas().set_index('weekday')
    # Switch x and y, to show weekdays on x-axis and hours on y-axis
    plot_df = plot_df.transpose()
    # fill not-a-number values with 0
    plot_df = plot_df.fillna(0) 
    # Rename columns to weekdays
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    plot_df.rename(columns={i: weekdays[int(i-1)] for i in plot_df.columns}, inplace=True)

    # Convert index datatype to int for hours
    plot_df.index = plot_df.index.astype(int)
    # Add missing hours to the index, to ensure all hours are represented
    all_hours = list(range(0, 24))
    plot_df = plot_df.reindex(all_hours, fill_value=0)
    # Sort index to ensure hours are in order
    plot_df = plot_df.sort_index()
    # format as "HH:00"
    plot_df.index = [f"{i:02d}:00" for i in plot_df.index]

    # Plot heatmap
    fig = px.imshow(
        plot_df,
        labels=dict(x="Weekday", y="Hour", color="count"),
        x=plot_df.columns,
        y=plot_df.index,
        title="Weekly Overview of Data points",
    )
    fig.update_xaxes(side="top")

    return fig


def price_supply_history_filter_hours(df: pl.DataFrame, hours: int = 24):
    """
    Create a price and supply history graph
    """

    filter_timestamp = datetime.datetime.now() - datetime.timedelta(hours=hours)

    df = df.filter(
        pl.col('Timestamp') >= pl.lit(filter_timestamp)
    )

    # Create the figure with secondary y-axis
    fig = plotly.subplots.make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces for price
    for herb_name in df["Name"].unique():
        herb_data_filtered = df.filter(pl.col("Name") == herb_name)
        fig.add_trace(
            go.Scatter(
                x=herb_data_filtered["Timestamp"], 
                y=herb_data_filtered["Price"], 
                name=f"4-{herb_name} Price",
                legendgroup="price_graph_4",  # group for graph 4
                legendgrouptitle=dict(text="Graph 4: Price"),
                showlegend=True
            ), 
            secondary_y=False
        )

    # Add traces for supply
    for herb_name in df["Name"].unique():
            herb_data_filtered = df.filter(pl.col("Name") == herb_name)
            fig.add_trace(
                go.Scatter(
                    x=herb_data_filtered["Timestamp"], 
                    y=herb_data_filtered["Available"], 
                    name=f"4-{herb_name} Supply",
                    legendgroup="price_graph_4",  # group for graph 4
                    legendgrouptitle=dict(text="Graph 4: Supply"),
                    showlegend=True
                ), 
                secondary_y=True
            )

    # Set axis titles
    fig.update_layout(
        title_text="Price and Supply Over Time",
        xaxis_title="Timestamp",
        yaxis_title="Price",
        yaxis2_title="Available Supply",
        yaxis2=dict(overlaying="y", side="right")  # Ensure the supply axis is on the right
    )

    return fig


def price_history(df: pl.DataFrame):
    """
    Create a price history graph
    """

    fig = plotly.subplots.make_subplots()

    # Add traces for price
    for herb_name in df["Name"].unique():
        herb_data_filtered = df.filter(pl.col("Name") == herb_name)
        fig.add_trace(
            go.Scatter(
                x=herb_data_filtered["Timestamp"], 
                y=herb_data_filtered["Price"], 
                name=f"2-{herb_name} Price",
                legendgroup="price_graph_2",  # group for graph 2
                legendgrouptitle=dict(text="Graph 2: Price History"),
                showlegend=True
            )
        )
    
    return fig


def price_history_filter_hours(df: pl.DataFrame, hours: int = 24):
    """
    Create a price history graph for last 24h
    """

    filter_timestamp = datetime.datetime.now() - datetime.timedelta(hours=hours)

    df = df.filter(
        pl.col('Timestamp') >= pl.lit(filter_timestamp)
    )

    fig = plotly.subplots.make_subplots()

    # Add traces for price
    for herb_name in df["Name"].unique():
        herb_data_filtered = df.filter(pl.col("Name") == herb_name)
        fig.add_trace(
            go.Scatter(
                x=herb_data_filtered["Timestamp"], 
                y=herb_data_filtered["Price"], 
                name=f"3-{herb_name} Price",
                legendgroup="price_graph_3",  # group for graph 3
                legendgrouptitle=dict(text="Graph 3: Price Periodically"),
                showlegend=True
            )
        )
    
    return fig


def show_plots(plots = List[tuple[str, go.Figure]]):
    """
    Show the plots in the figure.
    """
    # Create subplot layout (e.g., 1 row, 2 columns)
    fig = plotly.subplots.make_subplots(rows=4, cols=1, subplot_titles=[plot[0] for plot in plots])

    for idx, graph_object in enumerate([plot[1] for plot in plots]):
        for trace in graph_object.data:
            fig.add_trace(trace, row=idx+1, col=1)

    fig.update_layout(
        height=3500,
        width=1000,
        title="Postit Overview",
        title_x=0.5,
        legend=dict(
            itemsizing="constant",
            orientation="h",
            # x=0.5,
            # y=0.3,   
            xanchor="center",
            yanchor="bottom",
        ),
        # The colorbar for the heatmap needs to be constrained for more pleasent layout
        coloraxis_colorbar=dict(
            len=0.3,
            thickness=10,
            x=1,
            y=0.89
        )
    )
    fig.show()


if __name__ == "__main__":

    # data_frames = scrape_csv_data('history/*.csv')
    data_frames = pl.read_parquet('parquets/prices.parquet')
    data_frames = pre_process_data(data_frames)

    # Generate figures
    weekly_overview_fig = weekly_overview(data_frames)
    price_history_fig = price_history(data_frames)

    # Generate figure with time interval
    time_interval = 8
    price_history_filtered_fig = price_history_filter_hours(data_frames, hours=time_interval)
    price_supply_history_filter_hours_fig = price_supply_history_filter_hours(data_frames, hours=time_interval)

    # Bundle name and figure
    plots: List[tuple[str, go.Figure]] = [
        ("Data ingestion Coverage", weekly_overview_fig),
        ("Price History", price_history_fig),
        (f"Price History {time_interval}h", price_history_filtered_fig),
        ("Price and Supply History", price_supply_history_filter_hours_fig)
    ]

    # Show the plots
    show_plots(plots)

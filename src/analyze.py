import os
import pprint
from typing import List
import glob
import polars
import plotly.express as px
import plotly.subplots
import plotly.graph_objects

# Define the directory name (adjust if needed)
DATA_DIR = "../history"

def scrape_csv_data(file_path: str) -> List[str]:
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
        df = polars.read_csv(file_path).with_columns([
            polars.lit(timestamp_str).alias("Timestamp")
        ])
        dfs.append(df)

    # Concatenate all into a single DataFrame
    combined_df = polars.concat(dfs)
    combined_df = pre_process_data(combined_df)

    return combined_df

def pre_process_data(df):
    """
    Pre-process the DataFrame
    """
    # We don't need the 'Owned?' and 'Top?' columns
    df = df.drop(["Owned?", "Top?"])

    # Convert 'Timestamp' to datetime
    df = df.with_columns([
        polars.col("Timestamp").str.strptime(polars.Datetime, "%Y-%m-%d-%H-%M")
    ])

    # Convert 'Price' to float
    df = df.with_columns([
        (polars.col("Price") / 10_000)
    ])
    return df

def weekly_overview(df: polars.DataFrame) -> plotly.graph_objects.Figure:
    """
    Create a weekly overview of the data.
    """
    # Unique timestamps represents batch imports
    df = df.select("Timestamp").unique()

    # Append an 'Hour' column for heatmap
    df = df.with_columns([
        polars.col("Timestamp").dt.hour().alias("hour")
    ])

    # Append a weekday column for heatmap
    df = df.with_columns([
        polars.col("Timestamp").dt.weekday().alias("weekday")
    ])

    # Group by hour and weekday, then do a count on occurances
    df = df.select(["hour", "weekday"])
    df = (
        df.group_by(["weekday", "hour"])
        .agg(polars.len().alias("count"))
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


def price_history(df: polars.DataFrame) -> polars.DataFrame:
    """
    Create a price history graph
    """

    price_df = df.to_pandas()

    # Plot line chart
    fig = px.line(
        price_df,
        x="Timestamp",
        y="Price",
        color="Name",  # Each herb gets its own line
        title="Herb Prices Over Time"
    )
    
    return fig



def show_plots(weekly_overview_fig: plotly.graph_objects.Figure, price_history_fig: plotly.graph_objects.Figure):
    """
    Show the plots in the figure.
    """
    # Create subplot layout (e.g., 1 row, 2 columns)
    fig = plotly.subplots.make_subplots(rows=2, cols=1, subplot_titles=["Data ingestion", "Price History", "Avarage Price Weekly"])

    # First plot
    for trace in weekly_overview_fig.data:
        trace.update(
            colorscale='Spectral',
        )
        fig.add_trace(trace, row=1, col=1) 
    
    # Second plot
    [fig.add_trace(trace, row=2, col=1) for trace in price_history_fig.data]

    # Third plot

    fig.update_layout(
        height=2000,
        width=1000,
        title="Postit Overview",
        title_x=0.5,
        legend=dict(
            itemsizing="constant",
            orientation="h",
            x=0.5,
            y=0.3,   
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

    data_frames = scrape_csv_data('history/*.csv')

    # Generate graph figures
    weekly_overview_fig = weekly_overview(data_frames)
    price_history_fig = price_history(data_frames)

    # pprint.pprint(data_frames.select("Name").unique())

    # Show the plots
    show_plots(weekly_overview_fig, price_history_fig)

    # pprint.pprint(data_frames)
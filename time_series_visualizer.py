import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# 1. Import the data and set date as the index
df = pd.read_csv(
    'fcc-forum-pageviews.csv',
    parse_dates=['date'],
    index_col='date'
)

# 2. Clean the data by filtering out the bottom 2.5%
# and top 2.5% of page views
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


# 3. Draw the line plot
def draw_line_plot():
    # Create a copy of the data
    df_line = df.copy()

    # Create the figure and axes
    fig, ax = plt.subplots(figsize=(15, 5))

    # Draw the line chart
    ax.plot(
        df_line.index,
        df_line['value'],
        color='red'
    )

    # Set the title and axis labels
    ax.set_title(
        'Daily freeCodeCamp Forum Page Views 5/2016-12/2019'
    )
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save and return the figure
    fig.savefig('line_plot.png')

    return fig


# 4. Draw the bar plot
def draw_bar_plot():
    # Create a copy of the data
    df_bar = df.copy()

    # Extract year and month from the date index
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Calculate average daily page views for each month
    # grouped by year
    df_bar = (
        df_bar.groupby(['year', 'month'])['value']
        .mean()
        .unstack()
    )

    # Create the bar chart
    fig = df_bar.plot(
        kind='bar',
        figsize=(10, 7),
        legend=True
    ).figure

    # Set the month names in the legend
    months = [
        'January', 'February', 'March', 'April',
        'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December'
    ]

    plt.legend(
        months,
        title='Months'
    )

    # Set axis labels
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')

    # Save and return the figure
    fig.savefig('bar_plot.png')

    return fig


# 5. Draw the box plots
def draw_box_plot():
    # Create a copy of the data
    df_box = df.copy()

    # Reset the index to access the date column
    df_box.reset_index(inplace=True)

    # Extract year and month
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Define the chronological month order
    month_order = [
        'Jan', 'Feb', 'Mar', 'Apr',
        'May', 'Jun', 'Jul', 'Aug',
        'Sep', 'Oct', 'Nov', 'Dec'
    ]

    # Create two adjacent plots
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))

    # Year-wise box plot
    sns.boxplot(
        data=df_box,
        x='year',
        y='value',
        ax=axes[0]
    )

    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month-wise box plot
    sns.boxplot(
        data=df_box,
        x='month',
        y='value',
        order=month_order,
        ax=axes[1]
    )

    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Improve spacing
    fig.tight_layout()

    # Save and return the figure
    fig.savefig('box_plot.png')

    return fig
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
original_df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'])

original_df.head()


# Clean data
# Clean the data by filtering out days when the page views were in the top 2.5% of the dataset or bottom 2.5% of the dataset.
bottom = original_df['value'].quantile(0.025)
top = original_df['value'].quantile(0.975)
df = original_df[(original_df['value'] > bottom)
                 & (original_df['value'] < top)]
print(df)


def draw_line_plot():
    fig, ax = plt.subplots()

    ax.plot(df['date'], df['value'], color='purple')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Draw line plot  reate a draw_line_plot function that uses Matplotlib to draw a line chart similar to "examples/Figure_1.png".  . The label on the x axis should be Date and the label on the y axis should be Page Views.

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


fig = draw_line_plot()
plt.show()


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # Convert date column to datetime and extract year, month, and day
    df_bar['date'] = pd.to_datetime(df_bar['date'])
    df_bar['year'] = df_bar['date'].dt.year
    df_bar['month'] = df_bar['date'].dt.month
    df_bar['month_name'] = df_bar['date'].dt.strftime('%B')  # Full month names

    # Calculate average daily page views for each month grouped by year
    df_bar = df_bar.groupby(
        ['year', 'month', 'month_name']).mean().reset_index()

    # Sort the DataFrame by year and month to ensure correct order
    df_bar.sort_values(by=['year', 'month'], inplace=True)

    # Draw bar plot
    fig, ax = plt.subplots()
    sns.barplot(x='year', y='value', data=df_bar, hue='month_name', ax=ax)

    # Customizing the plot
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    plt.legend(title='Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


fig = draw_bar_plot()
plt.show()


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    # Start drawing the box plots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))

    # Year-wise Box Plot
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month-wise Box Plot
    # Ensure the months are in order
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                   'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box,
                order=month_order, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig


fig = draw_box_plot()
plt.show()

import pandas as pd
import plotly.graph_objects as go


def load(data):
    """
    Load Covid 19 data.

    :param data: Path to CSV file
    :type data: ``str``
    :return: CSV file
    :rtype: :class:`pandas.core.frame.DataFrame`
    """
    return pd.read_csv(data)


def get_daily_total(data):
    """
    Get cumulative sum.

    :param data: New cases by day
    :type data: ``list``
    :return: Cumulative total cases by day
    :rtype: ``list``
    """
    return [t + sum(data[:i]) for i, t in enumerate(data)]


def get_seven_past_days_total(data):
    """
    Get total of past seven days.

    :param data: New cases by day
    :type data: ``list``
    :return: Cumulative total cases in the last seven days
    :rtype: ``list``
    """
    seven_days_running_total = []
    for i, today in enumerate(data):
        if i > 7:
            seven_days_running_total.append(today + sum(data[i-7:i]))
        else:
            seven_days_running_total.append(today + sum(data[:i]))
    return seven_days_running_total


def plot(x, y, title):
    """
    Make a plot.

    :param x: Total number of confirmed cases
    :type x: ``list``
    :param y: Number of confirmed cases in the past week
    :type y: ``list``
    :return: Void
    :rtype: ``None``
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y))

    fig.update_layout(
        xaxis_type='log',
        yaxis_type='log',
        xaxis_title='Total Confirmed Cases',
        yaxis_title='New Confirmed Cases in the last 7 days',
        title_text=title,
        font=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )

    fig.write_image(f'images/{title}.png')
    fig.show()


if __name__ == '__main__':

    covid = load('./data/interpolated.csv')

    belgrade = covid['Belgrade'].tolist()
    serbia = covid['Serbia'].tolist()

    # There are discrepancies here with the official data - this is because
    # my data is missing data from 30.3.2020. - 15.4.2020. -> my interpolated
    # data is off by 137 people (surplus). I suspect that this is probably
    # due to rounding errors in growth factors
    belgrade_daily_total = get_daily_total(belgrade)
    belgrade_seven_days_total = get_seven_past_days_total(belgrade)

    serbia_daily_total = get_daily_total(serbia)
    serbia_seven_days_total = get_seven_past_days_total(serbia)

    plot(x=belgrade_daily_total, y=belgrade_seven_days_total, title='Belgrade')
    plot(x=serbia_daily_total, y=serbia_seven_days_total, title='Serbia')

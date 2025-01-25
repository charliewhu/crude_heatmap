import pandas as pd
import numpy as np
import plotly.graph_objs as go
from datetime import datetime, timedelta


np.random.seed(33)


def main():
    def generate_random_walk(
        num_steps: int,
        start_value: float = 2.0,
        volatility: float = 0.2,
    ):
        """
        Generate a random walk price series

        :param num_steps: Number of steps in the walk
        :param start_value: Starting value of the walk
        :param volatility: Standard deviation of the random steps
        :return: Array of price values
        """
        # Generate random steps
        steps = np.random.normal(loc=0, scale=volatility, size=num_steps)

        # Cumulative sum creates the random walk
        walk = start_value + np.cumsum(steps)

        return walk

    def generate_indics():
        # Setup parameters
        start_date = datetime(2025, 2, 1)
        num_days = 120
        counterparties = [
            # "Shell",
            "BP",
            "Total",
            "Chevron",
            "ExxonMobel",
            "Vitol",
            "Trafigura",
        ]

        # Generate continuous random walk prices
        random_walk_prices = generate_random_walk(num_days)

        trades = []

        for i in range(100):  # Large number of trades
            # Random date within our date range
            bl_date = start_date + timedelta(days=np.random.randint(0, num_days))

            # Find the corresponding price for this date
            date_index = (bl_date - start_date).days

            # Get base price differential
            base_price_diff = random_walk_prices[date_index]

            # Add noise to the price
            noise = np.random.normal(0, 0.15)
            price_diff = round(base_price_diff + noise, 2)

            # Determine trade characteristics
            counterparty = np.random.choice(counterparties)
            trade_type = np.random.choice(
                ["Bid", "Offer"],
                p=[0.5, 0.5],
            )  # More sell-side trades

            # Varied volume distribution
            volume = np.random.choice([500, 950, 1000, 2000], p=[0.1, 0.3, 0.3, 0.3])

            trades.append(
                {
                    "counterparty": counterparty,
                    "type": trade_type,
                    "volume": volume,
                    "bl_date": bl_date,
                    "price_differential": price_diff
                    if trade_type == "Offer"
                    else -price_diff,
                    "unique_id": i,
                }
            )

        # Convert to DataFrame
        df = pd.DataFrame(trades)

        return df, random_walk_prices, start_date

    # Generate the trading data
    df, random_walk_prices, start_date = generate_indics()

    # Create interactive Plotly visualization
    fig = go.Figure()

    # Prepare date array for random walk line
    # walk_dates = [
    #     start_date + timedelta(days=i) for i in range(len(random_walk_prices))
    # ]

    # # Add Random Walk Line first (so it's behind the trades)
    # fig.add_trace(
    #     go.Scatter(
    #         x=walk_dates,
    #         y=random_walk_prices,
    #         mode="lines",
    #         name="Price Differential Trend",
    #         line=dict(color="blue", width=2, dash="dot"),
    #         hoverinfo="skip",
    #     )
    # )

    # Add Sell trades
    sell_trades = df[df["type"] == "Offer"]
    fig.add_trace(
        go.Scatter(
            x=sell_trades["bl_date"],
            y=sell_trades["price_differential"],
            mode="markers",
            name="Offer",
            marker=dict(
                color=[
                    "#f2aaa5" if bl_date < datetime(2025, 3, 15) else "red"
                    for bl_date in sell_trades["bl_date"]
                ],
                size=sell_trades["volume"] / 85,
                opacity=0.7,
                line=dict(color="darkred", width=1),
            ),
            customdata=sell_trades["volume"],
            text=sell_trades["counterparty"],
            hovertemplate="<b>Offer</b><br>"
            + "Date: %{x}<br>"
            + "Price Differential: %{y:.2f}<br>"
            + "Volume: %{customdata}<br>"
            + "Counterparty: %{text}",
        )
    )

    # Add Buy trades
    buy_trades = df[df["type"] == "Bid"]
    fig.add_trace(
        go.Scatter(
            x=buy_trades["bl_date"],
            y=buy_trades["price_differential"],
            mode="markers",
            name="Bid",
            marker=dict(
                color=[
                    "#aaf0ba" if bl_date < datetime(2025, 3, 15) else "green"
                    for bl_date in buy_trades["bl_date"]
                ],
                size=buy_trades["volume"] / 85,
                opacity=0.7,
                line=dict(color="darkgreen", width=1),
            ),
            customdata=buy_trades["volume"],
            text=buy_trades["counterparty"],
            hovertemplate="<b>Bid</b><br>"
            + "Date: %{x}<br>"
            + "Price Differential: %{y:.2f}<br>"
            + "Volume: %{customdata}<br>"
            + "Counterparty: %{text}",
        )
    )

    # Customize layout
    fig.update_layout(
        title="Crude Oil - Differential Heatmap",
        xaxis_title="Bill of Lading Date",
        yaxis_title="Price Differential ($)",
        hovermode="closest",
        height=600,
        width=1200,
        template="simple_white",
    )

    # Print summary statistics
    print("Trading Summary:")
    print(f"Total Trades: {len(df)}")
    print(f"Sell Trades: {len(sell_trades)}")
    print(f"Buy Trades: {len(buy_trades)}")
    print("\nPrice Differential Statistics:")
    print(df["price_differential"].describe())

    # Save the interactive plot (optional)
    # fig.write_html("indics_heatmap.html")

    # Show the plot
    fig.show()


if __name__ == "__main__":
    main()

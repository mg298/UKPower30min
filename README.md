Forecasting UK Electricity Imbalance Prices

In the UK, wholesale electricity is traded every 30 minutes through auctions facilitated by exchanges such as EPEXSpot/Nord Pool. Participants buy or sell electricity at agreed prices through the exchange. If a participant fails to consume or produce the agreed-upon electricity within the 30-minute window, an imbalance volume occurs, which must be settled at an imbalance price determined by Elexon.

Data Sources:

Elexon DETSYSPRICES provides imbalance prices and a proxy for exchange prices.
Historical data for exchange prices is unavailable due to redistribution constraints but are available on the day.

We will use DETSYSPRICES "MAIN PRICE SUMMARY" as the imbalance price and "MARKET PRICE SUMMARY" as the proxy for the exchange price (EPEXSpot/Nord Pool).

Time Lags:

Auctions occur hourly and half-hourly throughout the day, with orders having to have been entered one hour before the half hour slot begins. The system updates approximately 40 seconds before each auction's cutoff time, excluding issues near midnight. For instance, data uploaded at 02:59:21 pertains to the auction starting at 04:00:00 and ending at 04:30:00, with Elexon prices for this slot available between 04:30:00 and 04:59:00.

File Formats:

Data is stored in Parquet files:

/Orders/YYYY_MM_DD.pqt: Contains order data.

INDEX: GMT time of data receipt.
latest_dp_datetime: GMT time rounded up to 30 minutes.
Posn: Position volume.

/DETSYSPRICES/DETSYSPRICES_YYYY_MM_DD.pqt: Provides historical and live imbalance prices. NB the delayed nature of this feed.

INDEX: GMT Time stamp.
MAIN PRICE SUMMARY: Imbalance price.
MARKET PRICE SUMMARY: proxy for Exchange price.

Code:

Executing plot_paper_trading.py generates five files, each with three graphs. The files represent the forecast lead times before trading at the imbalance price. While shorter durations (30 and 60 minutes) are infeasible due to auction timings, the primary focus is on the 90-minute forecast. Longer durations are included to assess sensitivity to latency.

Position and price data are available in Git approximately 35 seconds before the auction's last orders are permitted.

Ubuntu 22.03:
you will need numpy, pandas, pyarrow
sudo apt-get update
sudo apt install python3-numpy python3-pandas
sudo apt install python3-pip
pip install pyarrow

Example of cloning and running the code:-
cd ~
mkdir workspace
cd workspace
git clone https://github.com/mg298/UKPower30min.git .
cd Python
python3 plot_paper_trading.py 

The code for generating orders/data streaming is not available on GitHub. A related paper is https://research-information.bris.ac.uk/en/publications/trading-electricity-markets-using-neural-networks-2

System has been running in a 'stable' form since Dec-2023.
Sample Output:
![Pnl_90](https://github.com/mg298/UKPower30min/assets/31728456/34bd87c1-7211-4ccc-b59b-cdb81b6bdf0b)

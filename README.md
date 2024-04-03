# UKPower30min
UKPower forecasts every 30min.

UK electricity forecasts/positions for UK electricity (Elexon) imbalance prices.

In the UK, every 30minutes, there is an auction for wholesale electricity. A participant buys (sells) electricity in this auction at an agreed price, which is set by the price you match at at the exchange (EPEXSpot/NordPool). If the participant does not consume (produce) all the electricity agreed during this 30min window, there is an imbalance, which must be settled at an 'imbalance price' set by Elexon (https://www.elexon.co.uk/settlement/imbalance-pricing/). For this code, in Elexon DETSYSPRICES (https://bscdocs.elexon.co.uk/guidance-notes/bmrs-api-and-data-push-user-guide), the buyer buys electricity at price "MARKET PRICE SUMMARY" (proxy for exchange price) and sells at "MAIN PRICE SUMMARY" (which is "imbalancePriceAmountGBP"). Historical data for exchange price is not available cannot be redistributed for free. When I have looked at the exchange price, it has been slightly (but statistically significantly) favourable compared to the Elexon distributed "MARKET PRICE SUMMARY".

Time lags: Auctions begin on the hour and half hour throughout the day. The current system is run on a server about 40 seconds before last orders are permitted for each auction (excluding issues near midnight). Consider the situation at 03:00:00 - data is uploaded at about 02:59:21, which allows an order to be send before the 03:00:00 cutoff. This could be used for the auction beginning 04:00:00 and finishing at 04:30:00 and the results for this are not seen until some time between 04:30:00 - 04:59:00.

File formats: parquet files
/Orders/2023_11_23.pqt, data
INDEX is the GMT time we received the data at
latest_dp_datetime is the GMT time as we'd expect to see this from Elexon data (ie rounded up to 30mins)
INDEX                                       latest_dp_datetime   Posn
2024-02-09 00:59:19.940719+00:00 2024-02-09 01:00:00+00:00       3.3

Available from Elexon historically and live
/DETSYSPRICES/
INDEX                           MAIN PRICE SUMMARY  MARKET PRICE SUMMARY
time_stamp                                                         
2023-03-21 00:30:00+00:00                80.0                  99.0

Code: /Python
If you run PlotPaperTrading.py it should generate five files, each containing three graphs. The five files correspond to how many minutes the forecast must be generated before trading at the Imbalance price. I believe the correct feasible length is 90min, as you orders for an auction (at EPEXSpot/Nordpool) are permitted up to one hour before the auction begins, and the auction lasts for 30mins. Ie plots for 30min and 60min are unachievable. 90min is what matters, and the longer durations are included to see how sensitive it is to latency. The files are of the form "Pnl90.png" etc.

The position and price data should be available in git about 35s before last orders for the auction are permitted. The code to generate the orders / stream the data is not uploaded.

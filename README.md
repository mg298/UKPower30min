# UKPower30min
UKPower forecasts every 30min. Public

UK electricity forecasts/positions for UK electricity (Elexon) imbalance prices.

In the UK, every 30minutes, there is an auction for wholesale electricity. A participant buys (sells) electricity in this auction at an agreed price, which is set by the exchange (EPEXSpot/NordPool). If the participant does not consume (produce) all the electricity agreed during this 30min window, there is an imbalance, which must be settled at an 'imbalance price' set by Elexon (https://www.elexon.co.uk/settlement/imbalance-pricing/). For this code, in Elexon DETSYSPRICES (https://bscdocs.elexon.co.uk/guidance-notes/bmrs-api-and-data-push-user-guide), the buyer buys electricity at price "MARKET PRICE SUMMARY" (proxy for exchange price) and sells at "imbalancePriceAmountGBP". Historical data for exchange price is not available for free and cannot be redistributed for free. When I have looked at the exchange price, it has been slightly (but statistically significantly) favourable compared to the Elexon distributed "MARKET PRICE SUMMARY".

EXAMPLE of time lags: the current system is run on a server about 40seconds before last orders are permitted for each auction (excluding issues near midnight). Consider the situation at 03:00:00 - data is uploaded at about 02:59:21, which allows an order to be send before the 03:00:00 cutoff. This could be used for the auction beginning 04:00:00 and finishing at 04:30:00 and the results for this are not seen until some time between 04:30:00 - 04:59:00.

Speak about processing of results - forecasts and P&L calc

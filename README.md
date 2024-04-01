# UKPower30min
UKPower forecasts every 30min. Public

UK electricity forecasts/positions for UK electricity (Elexon) imbalance prices.

In the UK, every 30minutes, there is an auction for wholesale electricity. A participant buys (sells) electricity in this auction at an agreed price, which is set by the exchange (EPEXSpot/NordPool). If the participant does not consume (produce) all the electricity agreed during this 30min window, there is an imbalance, which must be settled at an 'imbalance price' set by Elexon (https://www.elexon.co.uk/settlement/imbalance-pricing/). For this code, in Elexon DETSYSPRICES (https://bscdocs.elexon.co.uk/guidance-notes/bmrs-api-and-data-push-user-guide), the buyer buys electricity at price "MARKET PRICE SUMMARY" (proxy for exchange price) and sells at "imbalancePriceAmountGBP".

Speak about lags

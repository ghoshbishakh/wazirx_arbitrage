# Arbitrage within wazirx

> Arbitrage is the simultaneous purchase and sale of the same asset in different markets in order to profit from tiny differences in the asset's listed price. It exploits short-lived variations in the price of identical or similar financial instruments in different markets or in different forms. ([source](https://www.investopedia.com/terms/a/arbitrage.asp))

Wazirx ([https://wazirx.com](https://wazirx.com)) crypto exchange has essentially four markets:

1. INR
2. USDT
3. WRX
4. BTC


I took some time to check if there are any arbitrage opportunities 😜

This short script uses their API -> [https://github.com/WazirX/wazirx-api](https://github.com/WazirX/wazirx-api)
It constructs a graph of all possible arbitrage paths from INR back to INR. Essentially it is a brute force algorithm that works.
The scrpt can take into account the transaction fee of 0.2% as well as last price, buy price, and sell price.

The results are pretty much what I expected. If we consider last price, then there are many opportunities,
but most of them are useless because of low volume of gap in buy/sell prices. When we consider buy and sell prices then the gain in arbitrage is so less that it will be used up in transaction fees. Therefore when we set the fee to 0.2% , we see that it returns nothing.


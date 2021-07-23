import requests

whitelist = [
    "inr",
    "btc",
    "matic",
    "usdt",
    "doge",
    "wrx",
    "chr",
    "rune",
    "eth",
    "shib",
    "1inch",
    "uft",
    "trx",
    "dock",
    "xlm",
    "enj",
    "etc",
    "xrp"
]

whitelist_on = False

charge = .998

# Make this False, if you want to use buy price and sell price
use_lastprice = True

resultdict = {}

print("Considering transaction fee:" + str(100 - (charge*100)) + "%")

if use_lastprice:
    print("Using lastprice")
else:
    print("Using buy and sell prices")


def getpricechain(chain, starting_dinomination):
    current_dinomination = starting_dinomination
    for x in range(len(chain)):
        node = chain[x]
        print(str(current_dinomination) + " " + chain[x] + " -> ")
        if x < len(chain)-1:
            nextnode = chain[x+1]
            current_dinomination = current_dinomination * graph[node]["destlist"][nextnode]["price"] * charge


def looper(graph, vertex, current_dinomination, chain):
    chain = chain + (vertex, )
    graph[vertex]["color"] = "grey"
    graph[vertex]["current_dinomination"] = current_dinomination
    for next in graph[vertex]["destlist"]:
        if graph[next]["color"] == "white":
            looper(graph, next, current_dinomination*graph[vertex]["destlist"][next]["price"]*charge, chain)
        if graph[next]["color"] == "grey":
            profit = current_dinomination*graph[vertex]["destlist"][next]["price"]*charge - graph[next]["current_dinomination"]
            if profit < 0:
                continue
            resultchain = chain + (next, )
            resultdict[resultchain] = profit

    graph[vertex]["color"] = "white"



res = requests.get("https://api.wazirx.com/api/v2/tickers")

resjson = res.json()

# graph
graph = {}

# build adjascency list
for pair in resjson:
    # print(pair)
    if float(resjson[pair]["last"]) == 0 or float(resjson[pair]["buy"]) == 0 or float(resjson[pair]["sell"]) == 0:
        continue
    dest, src = resjson[pair]["base_unit"], resjson[pair]["quote_unit"]
    if whitelist_on and ((dest not in whitelist) or (src not in whitelist)):
        continue 
    # print(src, dest)
    if src not in graph:
        graph[src] = {"destlist": {}, "color": "white"}
    if dest not in graph:
        graph[dest] = {"destlist": {}, "color": "white"}

    if dest not in graph[src]["destlist"]:
        graph[src]["destlist"][dest] = { "price":  1.0/float(resjson[pair]["sell"])}
        if use_lastprice:
            graph[src]["destlist"][dest] = { "price":  1.0/float(resjson[pair]["last"])}
    
    if src not in graph[dest]["destlist"]:
        graph[dest]["destlist"][src] = { "price":  float(resjson[pair]["buy"])}
        if use_lastprice:
            graph[dest]["destlist"][src] = { "price":  float(resjson[pair]["last"])}

# print(graph)


# start with 1000 INR and go find a circle
starting_dinomination = 1000
current_dinomination = starting_dinomination

looper(graph, "inr", current_dinomination, ())
for k in sorted(resultdict, key=len, reverse=True):
    print(resultdict[k], k)
    print(getpricechain(k, current_dinomination))

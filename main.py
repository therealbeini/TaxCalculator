import pandas as pd

data = pd.read_excel(r'FTX_Trades_2022.xlsx')
array = data.to_numpy()
array = array[::-1]

coin_dict = dict()

profit = 0
loss = 0
for e in array:
    name = e[2]
    if "PERP" not in name:
        continue
    side = e[3]
    size = e[5]
    price = e[6]
    if side == "buy":
        if name not in coin_dict:
            coin_dict[name] = list()
        queue = coin_dict[name]
        if len(queue) == 0:
            coin_dict[name].append([size, price])
        else:
            if queue[0][0] > 0:
                coin_dict[name].append([size, price])
            else:
                while len(queue) > 0:
                    current = queue[0]
                    min_size = min(-current[0], size)
                    profit_loss = min_size * (current[1] - price)
                    if profit_loss > 0:
                        profit += profit_loss
                    else:
                        loss += profit_loss
                    current[0] += min_size
                    size -= min_size
                    if current[0] == 0:
                        queue.pop(0)
                    else:
                        break
    elif side == "sell":
        if name not in coin_dict:
            coin_dict[name] = list()
        queue = coin_dict[name]
        if len(queue) == 0:
            coin_dict[name].append([-size, price])
        else:
            if queue[0][0] < 0:
                coin_dict[name].append([-size, price])
            else:
                while len(queue) > 0:
                    current = queue[0]
                    min_size = min(current[0], size)
                    profit_loss = min_size * (price - current[1])
                    if profit_loss > 0:
                        profit += profit_loss
                    else:
                        loss += profit_loss
                    current[0] -= min_size
                    size -= min_size
                    if current[0] == 0:
                        queue.pop(0)
                    else:
                        break

print(profit)
print(loss)
print(coin_dict)
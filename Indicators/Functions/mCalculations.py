

def F_loadValues( arquivo, symbol, precoAtual ):
    lstValores = []

    lstValores.append( F_avgPrice(arquivo, symbol) )
    lstValores.append( F_profitLoss(precoAtual, arquivo, symbol) )
    lstValores.append( F_sumCoins(arquivo, symbol) )
    lstValores.append( F_amount(arquivo, symbol) )
    lstValores.append( F_updateValue(precoAtual, arquivo, symbol) )

    return lstValores

# --------------------------------------------------------------------------- #
def F_sumCoins(arquivo, symbol):
    valor = 0

    with open(arquivo, 'r') as file:
        for line in file:
            data = line.strip().split(';')

            if len(data) >= 5 and data[0] == symbol:
                valor = float(data[2]) + float(data[4])

    return float(valor)

# --------------------------------------------------------------------------- #
def F_partialGain(pathFile, symbol, percent, partialCoin):

    if percent > 0 and partialCoin > 0:

        avg          = F_avgPrice(pathFile, symbol)
        partialPrice = float(avg) + ((float(percent) * float(avg)) / 100)
        partialGain  = float(partialCoin) * (float(partialPrice) - float(avg))

        return partialGain
    else:
        return 0.0

# --------------------------------------------------------------------------- #
def F_amount(pathFile, symbol):

    totalInvested = 0

    with open(pathFile, 'r') as file:

        for lines in file:
            line = lines.strip().split(';')

            if len(line) >= 5 and line[0] == symbol:
                totalInvested = (float(line[2]) * float(line[1])) + (float(line[4]) * float(line[3]))

    return totalInvested

# --------------------------------------------------------------------------- #
def F_avgPrice(pathFile, symbol):

    total = 0.0
    coin  = F_sumCoins(pathFile, symbol)
    price = F_amount(pathFile, symbol)

    if float(coin) < 1:
        total = 0.0
    else:
        total = float(price) / float(coin)

    return abs(float(total))

#) --------------------------------------------------------------------------- #
def F_updateValue(currentPrice, pathFile, symbol):

    pl           = F_profitLoss(currentPrice, pathFile, symbol)
    invested     = F_amount(pathFile, symbol)
    currentValue = float(pl) + float(invested)

    return currentValue

# --------------------------------------------------------------------------- #
def F_profitLoss(currentPrice, pathFile, symbol):

    avg        = F_avgPrice(pathFile, symbol)
    sumCoins   = F_sumCoins(pathFile, symbol)
    pl         = float(currentPrice) - float(avg)
    profitLoss = float(sumCoins) * float(pl)

    return profitLoss

from itertools import zip_longest


def status(info):
    open_price = float(info[1])
    close_price = float(info[4])
    if close_price > open_price:
        return "BUY"
    return "SELL"


def exponential_moving_average(arr, no):
    new_values = arr
    # new_values = simple_moving_average(arr, no)
    ema = []
    j = 1

    # get n sma first and calculate the next n period ema
    sma = sum(new_values[:no]) / no
    multiplier = 2 / float(1 + no)
    ema.append(sma)

    # EMA(current) = ( (Price(current) - EMA(prev) ) x Multiplier) + EMA(prev)
    ema.append(((new_values[no] - sma) * multiplier) + sma)

    # now calculate the rest of the values
    for i in arr[no + 1 :]:
        tmp = ((i - ema[j]) * multiplier) + ema[j]
        j = j + 1
        ema.append(tmp)

    return ema


def substract_arrays(arr1, arr2):
    merged = reversed(list(zip_longest(reversed(arr1), reversed(arr2), fillvalue=0)))
    merged = list(merged)

    def substract(a):
        if a[1] == 0:
            return 0
        return a[0] - a[1]

    return [substract(a) for a in merged]


def generate_mcda(data):
    cleaned_data = [float("%.2f" % float(x[4])) for x in data]
    ema_12 = exponential_moving_average(cleaned_data, 12)
    ema_26 = exponential_moving_average(cleaned_data, 26)

    mcda_line = substract_arrays(ema_12, ema_26)
    signal_line = exponential_moving_average(mcda_line, 9)
    return [x for x in substract_arrays(mcda_line, signal_line) if x != 0]

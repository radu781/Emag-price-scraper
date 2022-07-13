def sieve_prices(prices: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = [prices[0]]

    for i in range(1, len(prices)):
        if prices[i - 1]["price"] != prices[i]["price"]:
            out.append(prices[i])

    return out

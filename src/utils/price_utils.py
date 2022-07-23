from models.item import Item


class PriceUtils:
    @staticmethod
    def extract_price(price: str) -> float:
        price = price.replace("de la ", "").replace(" Lei", "")
        split = price.split(",")
        small = split[-1]
        price = "".join(p for p in split[:-1]).replace(".", "")
        return float(price) + float(small) / 100

    @staticmethod
    def price_has_updated(item: Item, price: tuple) -> bool:
        return item.id_ == price[1] and PriceUtils.extract_price(
            item.price
        ) != PriceUtils.extract_price(str(price[3]))

    @staticmethod
    def sieve_prices(prices: list[dict[str, str]]) -> list[dict[str, str]]:
        out: list[dict[str, str]] = [prices[0]]

        for i in range(1, len(prices)):
            if prices[i - 1]["price"] != prices[i]["price"]:
                out.append(prices[i])

        return out

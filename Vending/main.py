class Product:

    def __init__(self, name, price):
        self.name = name
        self.__price = price

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value > 0:
            self.__price = value
        else:
            print("Araswori mnishvneloba")


class VendingMachine:

    def __init__(self, products: list, cash_collected=0):
        self.products = products
        self.__cash_collected = 0

    def buy_product(self, product_name):
        for product in self.products:
            if product_name == product_name:
                self.__cash_collected += product.price
                self.products.remove(product)


products = [Product('CocaCola', 2.3), Product('RedBull', 5)]

vendingMachine = VendingMachine(products)
vendingMachine.buy_product("RedBull")

print(vendingMachine)

product = Product("CocaCola", 2.3)
print(product.price)
product.price = 5
print(product.price)
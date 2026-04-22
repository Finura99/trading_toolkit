class Trade:
    def __init__(self, symbol: str, quantity: float, price: float): # init allows to initialise the attributes of an object
        self.symbol = symbol
        self._quantity = quantity # encapsulation (protected) can only be altered in setter methods
        self.price = price

    def trade_value(self) -> float:
        return self._quantity * self.price
    
    def set_quantity(self, value: float): # enforce valdiation rules on quantity instead of modifying it directly...
        if value < 0:
            raise ValueError("Quantity is not positive")
        self._quantity = value

class EquityTrade(Trade): # inheritance...
    
    # create a special method
    def __init__(self, symbol: str, quantity: float, price: float, exchange: str):
        super().__init__(symbol, quantity, price) # inherited attributes

        self.exchange = exchange # extends behaviour from the inherited class

    def trade_value(self):
        return super().trade_value() * 1.01 # fee is polymorphism that overrides base class method behaviour


    
trade = Trade("AAPL", 10, 200) # object (instance of class)
print(trade.symbol)
print(trade.trade_value())



# reverse a string

def reverse_string(symbol: str) -> str:
    return symbol[::-1]

def reverse_string_using_loop(symbol: str) -> str:
    
    result = ""

    for char in symbol:
        result = char + result
    return result

def reverse_string_pointers(s: list):
    s = list[s] #strings are immutable

    left, right = 0, len(s) - 1 # pointers declared

    while left > right: # condition runs until its false
        s[left], s[right] = s[right], s[left] # swap pointed elements

        left +=1 # move pointer right
        right +=1 # move pointer
    
    return "".join(s)
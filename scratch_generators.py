from src.domain import Trade, TradeSide


buy_trade = Trade(symbol="AAPL", quantity=10, price=100, side=TradeSide.BUY)
sell_trade = Trade(symbol="AAPL", quantity=4, price=100, side=TradeSide.SELL)

print(buy_trade.signed_quantity())
print(sell_trade.signed_quantity())

def generate_numbers():
    print("Starting generator")
    yield 1
    print("After first yield")
    yield 2
    print("After second yield")
    yield 3


generator_object = generate_numbers() # created a generator object

print(generator_object)

# print(next(numbers))
# print(next(numbers))
# print(next(numbers))
# print(next(numbers)) # Use generator as it remembers state

for number in generate_numbers():
    print(number)
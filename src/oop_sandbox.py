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
    
    def to_dict(self):
        return {
            "symbol": self.symbol,
            "quantity": self._quantity,
            "price": self.price,
            "trade_value": self.trade_value()
        }

    
trade = Trade("AAPL", 10, 200) # object (instance of class)
##print(trade.symbol)
##print(trade.trade_value())











# reverse a string

def reverse_string(symbol: str) -> str: #O(n)
    return symbol[::-1]

def reverse_string_using_loop(symbol: str) -> str: #O(n2)
    
    result = ""

    for char in symbol:
        result = char + result #O(n)
    return result

def reverse_string_pointers(s: list): #O(n) manual
    s = list[s] # strings are immutable

    left, right = 0, len(s) - 1 # pointers declared

    while left > right: # condition runs until its false
        s[left], s[right] = s[right], s[left] # swap pointed elements

        left +=1 # move pointer right
        right +=1 # move pointer
    
    return "".join(s)


# practise reverse string
def reverse_string(symbol: str):
    #slicing method
    return symbol[::-1] # O(n)

def reverse_string_loop(symbol: str):

    result = ""

    for char in symbol:
        result = char + result
    
    return result # O(n2)

def reversed_string_pointers(s: list) -> str:

    char = list(s)
    left, right = 0, len(char) - 1

    while left < right:
        char[left], char[right] = char[right], char[left]

        left +=1
        right -=1

    return "".join(char) # O(n)

def palindrome_pointers(s: str) -> bool:

    left, right = 0, len(s) -1

    while left < right:
        if s[left] != s[right]:
            return False
    
        left+=1
        right-=1
    return True #O(n) - time O(1) space 

## i would check if the pointers index matches with each other and once the pointers go past each other in the string the loop stop execution.

def is_palindrome(s: str) -> bool:
    
    return s == s[::-1]


# practice removing duplicates from a string (preserve order)
## use a set for uniqueness - O (1) for lookups

def remove_duplicates(s : str) -> str:

    unique = set() # create a set
    result = []

    for char in s:
        if char not in unique:
            unique.add(char)
            result.append(char)

    return "".join(result)


# regular function 
def square(x):
    return x * x

#lambda
square_lambda = lambda x: x * x

numbers = [1, 2, 3]

result = map(lambda x: x * 2, numbers)
list(result)

result = [x * 2 for x in numbers]

##Find the first non-repeating character in a string
## "aabbcde" -> "c"

def non_repeating(s: str) -> str:

    ##string is immutable
    ##convert to a list
    ## two pointers is possible here WRONG ====== ITS A COUNTING / FREQUENCY PROBLEM
    counts = {}

    for char in s:
        counts[char] = counts.get(char, 0) + 1

    for char in s:
        if counts[char] == 1:
            return char

    return None
## time = O(n), space = O(n)


## Second most frequent character in the string
##Example: "aabbbcc" -> "a"


def second_most_freq(s: str) -> str:

    #counting / frequency using dictionary?

    count = {}

    for char in s:
        count[char] = count.get(char, 0) + 1

    freqs = sorted(count.values, reverse=True)

    if len(freqs) < 2:
        return None
    
    second_freqs = freqs[1]

    for char in count:
        if count[char] == second_freqs:
            return char
        

## Find the first duplicate charac in a string
## ex: "abcade" -> "a"

def first_dup(s : str) -> str | None:

    ## using set for uniqueness
    ## retrieve string

    unique = set() #O(1) lookups

    for char in s: #O(n)
        if char in unique:
            return char
        unique.add(char)

    return None

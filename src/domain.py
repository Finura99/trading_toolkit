from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum

class TradeSide(str, Enum): # create an enum for controlled list of valid values
    BUY = "BUY"
    SELL = "SELL"


@dataclass
class Trade:
    symbol: str
    quantity: float
    price: float
    side: TradeSide = TradeSide.BUY # defaults to buy if no argument provided

    # Encapsulation = Trade keeps symbol, quantity, price and validation together

    def __post_init__(self):
        self.symbol = self.symbol.strip().upper()

        if not self.symbol:
            raise ValueError("Symbol is required")
        
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if self.price <= 0:
            raise ValueError("Price should be a positive value")
        
        if isinstance(self.side, str):
            self.side = TradeSide(self.side.upper())
        


    def __str__(self) -> str: # dunder method
        return f"{self.symbol}: {self.quantity:g} @ {self.price:g}"


    def notional_value(self) -> float: # concrete method
        return self.quantity * self.price
    
    def signed_quantity(self) -> float: # helps calculate the net position from multiple trades from the quantity...
        if self.side == TradeSide.BUY:
            return self.quantity
        return -self.quantity



class TradeValidator:
    def validate(self, trade: Trade) -> None:
        if not trade.symbol:
            return ValueError("Symbol is required")
        
        if trade.quantity <= 0:
            return ValueError("Quantity is not positive")
        
        if trade.price <= 0:
            return ValueError("Price is not positive")
        
        

class FeeCalculator(ABC):
    @abstractmethod
    def calculate_fee(self, trade: Trade): 
        pass

    # FeeCalculator defines expected behaviour without exposing implementation details
    # this tells us that any object/class using method calculate fee must adhere to its signature parameters and method name.
    # abstraction applied here
    # essentially like an api contract



class TradeFeeCalculator(FeeCalculator):
    def calculate_fee(self, trade: Trade) -> float:
        return trade.notional_value() * 0.001
    ## isnt this compositon since its bringing in our base class as an obj?


class PercentageFeeCalculator(FeeCalculator):
    def calculate_fee(self, trade: Trade) -> float:
        return trade.notional_value() * 0.001
    
class FixedFeeCalculator(FeeCalculator):
    def calculate_fee(self, trade: Trade) -> float:
        return 2.50

class ZeroFeeCalculator(FeeCalculator):
    def calculate_fee(self, trade: Trade) -> float:
        return 0.0

    
# Polymorphism = FixedFee and PercentageFee use calculate fee method differently



class TradeProcessor:
    def __init__(self, validator: TradeValidator, fee_calculator: PercentageFeeCalculator): # composition here
        self.validator = validator
        self.fee_calculator = fee_calculator
        ## fields to be then turned into objects for use


    def process(self, trade: Trade) -> dict:
        self.validator.validate(trade) # validates the trade

        fee = self.fee_calculator.calculate_fee(trade) # delegates fee calculation
        ## using the objects method ergo composition and polymorphism in the method

        return {
            "symbol": trade.symbol,
            "notional_value": trade.notional_value(),
            "fee": fee,
            "net_value": trade.notional_value() - fee
        }
# Composition = TradeProcessor uses a fee calculator object/s from another class.



@dataclass
class EquityTrade(Trade): # Inheritance because equitytrade is a specialised trade of the base class.
    exchange: str = "NASDAQ"

    def market(self) -> str: # concrete method
        return f"{self.symbol} trades on {self.exchange}"
    

def calculate_positon(trades: list[Trade]) -> float:
    total = 0

    for trade in trades:
        total += trade.signed_quantity() # cehcks whether the trade increases or decreases in position.

    return total
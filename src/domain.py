from dataclasses import dataclass


@dataclass
class Trade:
    symbol: str
    quantity: float
    price: float

    def __post_init__(self):
        self.symbol = self.symbol.strip().upper()

        if not self.symbol:
            raise ValueError("Symbol is required")
        
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if self.price <= 0:
            raise ValueError("Price should be a positive value")
        

    def __str__(self) -> str:
        return f"{self.symbol}: {self.quantity:g} @ {self.price:g}"


    def notional_value(self) -> float:
        return self.quantity * self.price



class TradeValidator:
    def validate(self, trade: Trade) -> None:
        if not trade.symbol:
            return ValueError("Symbol is required")
        
        if trade.quantity <= 0:
            return ValueError("Quantity is not positive")
        
        if trade.price <= 0:
            return ValueError("Price is not positive")
        
        

class TradeFeeCalculator:
    def calculate_fee(self, trade: Trade) -> float:
        return trade.notional_value() * 0.001 ## isnt this compositon since its bringing in our base class as an obj?
    

class PercentageFeeCalculator:
    def calculate_fee(self, trade: Trade) -> float:
        return trade.notional_value() * 0.001
    
class FixedFeeCalculator:
    def calculate_fee(self, trade: Trade) -> float:
        return 2.50
    

class TradeProcessor:
    def __init__(self, validator: TradeValidator, fee_calculator: TradeFeeCalculator): # composition here
        self.validator = validator
        self.fee_calculator = fee_calculator
        ## fields to be then turned into objects for use


    def process(self, trade: Trade) -> dict:
        self.validator.validate(trade)

        fee = self.fee_calculator.calculate_fee(trade)
        ## polymorphism through composition

        return {
            "symbol": trade.symbol,
            "notional_value": trade.notional_value(),
            "fee": fee,
            "net_value": trade.notional_value() - fee
        }
    
    ################## domain object with composition

@dataclass
class EquityTrade(Trade):
    exchange: str

    def market(self) -> str:
        return f"{self.symbol} trades on {self.exchange}"
    
    ## this means equitytrade inherits from trade

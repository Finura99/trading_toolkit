from pydantic import BaseModel


class TradeCreate(BaseModel):
    symbol: str
    quantity: float
    price: float

class TradeResponse(BaseModel):
    symbol: str
    quantity: float
    price: float
    trade_value: float

class PortfolioResponse(BaseModel):
    symbol: str
    total_quantity: float
    average_price: float
    total_value: float
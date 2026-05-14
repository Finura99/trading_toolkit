from pydantic import BaseModel, Field


class TradeCreate(BaseModel):
    symbol: str
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)

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

from pydantic import BaseModel, Field
from src.domain import TradeSide


class TradeCreate(BaseModel):
    symbol: str
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)
    side: TradeSide.BUY

class TradeResponse(BaseModel):
    symbol: str
    quantity: float 
    price: float 
    trade_value: float
    side: TradeSidee

class PortfolioResponse(BaseModel):
    symbol: str
    total_quantity: float
    average_price: float
    total_value: float

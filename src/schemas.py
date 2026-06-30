from pydantic import BaseModel, Field
from src.domain import TradeSide


class TradeCreate(BaseModel):
    symbol: str
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)
    side: TradeSide = TradeSide.BUY

class TradeResponse(BaseModel):
    symbol: str
    quantity: float 
    price: float 
    trade_value: float
    side: TradeSide

class PortfolioResponse(BaseModel):
    symbol: str
    total_quantity: float
    average_price: float
    total_value: float

class PositionResponse(BaseModel):
    symbol: str
    net_quantity: float
    market_price: float
    exposure: float
    

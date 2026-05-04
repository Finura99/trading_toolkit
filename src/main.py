import time
import logging

from fastapi import FastAPI, HTTPException, Query

from src.oop_sandbox import EquityTrade
from src.db import get_connection
from src.schemas import TradeCreate, TradeResponse, PortfolioResponse
from src.services import (create_trade, 
                          get_portfolio,
                          get_trades_by_symbol,
                          get_trades,
                          get_portfolio_by_symbol)

app = FastAPI()

logging.basicConfig(level=logging.INFO)

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }

@app.post("/trades", response_model=TradeResponse)
def create_trade_endpoint(trade: TradeCreate):
    trade_obj = EquityTrade(
        trade.symbol,
        trade.quantity,
        trade.price,
        "NASDAQ"
    )

    conn = get_connection() # get connection

    try:
        return create_trade(conn, trade_obj)
    finally:
        conn.close()


@app.get("/portfolio", response_model=list[PortfolioResponse])
def get_trade_endpoint():

    conn = get_connection()

    try:
        result = get_portfolio(conn)
        return result
    
    finally:
        conn.close()



@app.get("/trades/{symbol}", response_model=list[TradeResponse])
def get_trade_symbol(symbol : str):

    conn = get_connection() # get connection 

    try:
        result = get_trades_by_symbol(conn, symbol) # service layer/business logic
    
        if not result:
            raise HTTPException(status_code=404, detail="Trades not found")

        return result # return dict
    finally:
        conn.close() # close connection



@app.get("/trades", response_model=list[TradeResponse])
def get_trades_endpoint(limit: int = Query(default=5, gt=0, le=100)):

    start = time.time()

    conn = get_connection() # get conenction
    try:
        service_start = time.time()
        result = get_trades(conn, limit)
        logging.info(f"Service layer took {time.time() - service_start:.4f}s")


        if not result:
            raise HTTPException(status_code=404, detail="Trades not found")
        
        logging.info(f"Total request took {time.time() - start:.4f}s")
        
        return result
    
    finally:
        conn.close()


@app.get("/portfolio/{symbol}", response_model=PortfolioResponse)
def get_portfolio_by_symbol_endpoint(symbol: str):

    conn = get_connection()

    try:
        result = get_portfolio_by_symbol(conn, symbol)

        if not result:
            raise HTTPException(status_code=404, detail = "Portfolio position not found")
        
        return result
    
    finally:
        conn.close()
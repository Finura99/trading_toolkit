import time
import logging
import uuid
from fastapi import FastAPI, HTTPException, Query, Request

from src.db import connection_pool
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

@app.middleware("http")
async def log_requests(request: Request, call_next): # using async on a function or statement is a coroutine.

    request_id = str(uuid.uuid4())[:8] # request id for tracing middleware improving observability
    

    start_time = time.time() # clock starts

    # await means pause this task until response is ready, allow other async tasks to continue
    response = await call_next(request) # call_next runs the actual endpoint

    process_time = time.time() - start_time # clock stops

    logging.info(
        f" Request ID: {request_id} | {type(request_id)}"
        f" {request.method} {request.url.path}"
        f" completed in {process_time:.4f}s"
        )
    # request level timing

    return response




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

    conn = get_connection() # uses psycopg2 

    try:
        return create_trade(conn, trade_obj) # service layer
    finally:
        connection_pool.putconn(conn) # use connection pooling instead of opening and closing db conn reducing conn overhead


@app.get("/portfolio", response_model=list[PortfolioResponse])
def get_trade_endpoint():

    conn = get_connection()

    try:
        result = get_portfolio(conn)
        return result
    
    finally:
        connection_pool.putconn(conn) # returning it back in the pool instead of destroying it



@app.get("/trades/{symbol}", response_model=list[TradeResponse])
def get_trade_symbol(symbol : str):

    conn = get_connection() # get connection 

    try:
        result = get_trades_by_symbol(conn, symbol) # service layer/business logic
    
        if not result:
            raise HTTPException(status_code=404, detail="Trades not found") # no resource exists

        return result # return dict
    finally:
        connection_pool.putconn(conn) # back into the reusable pool



@app.get("/trades", response_model=list[TradeResponse])
def get_trades_endpoint(limit: int = Query(default=5, gt=0, le=100)):

    
    conn = get_connection() # get connection
    try:
        service_start = time.time()

        result = get_trades(conn, limit)
        logging.info(f"Service layer took {time.time() - service_start:.4f}s")


        # if not result:
            # raise HTTPException(status_code=404, detail="Trades not found")

        # a 200 ok is better since request was valid for a collection endpoint where the list was empty, 404 is more appropriate for a specific item endpoint.
        
        return result
    
    finally:
        connection_pool.putconn(conn)


@app.get("/portfolio/{symbol}", response_model=PortfolioResponse)
def get_portfolio_by_symbol_endpoint(symbol: str):

    conn = get_connection()

    try:
        result = get_portfolio_by_symbol(conn, symbol)

        if not result:
            raise HTTPException(status_code=404, detail = "Portfolio position not found")
        
        return result
    
    finally:
        connection_pool.putconn(conn)
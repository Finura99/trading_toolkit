import time
import logging
import uuid
from fastapi import FastAPI, HTTPException, Query, Request


from src.db import connection_pool, check_db_connection, db_connection
# from src.db import get_connection
from src.domain import EquityTrade
from src.schemas import TradeCreate, TradeResponse, PortfolioResponse, PositionResponse
from src.services import (create_trade, 
                          get_portfolio,
                          get_trades_by_symbol,
                          get_trades,
                          get_portfolio_by_symbol,
                          get_positions)

app = FastAPI() # instance of the app ?

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
        "status": "ok" # is the fastapi process alive?
    }

## lazygit test

@app.get("/readiness") # can the app serve database backed requests/queries?
def readiness_check():

    if check_db_connection():
        return {
            "status": "ok",
            "database": "active"
        }
    raise HTTPException(
        status_code=503,
        detail={
        "status": "not_ready",
        "database": "unavailable"
    })

@app.post("/trades", response_model=TradeResponse)
def create_trade_endpoint(trade: TradeCreate): #api validation to check if the data has integrity
    
    trade_obj = EquityTrade( # inheritance applied here
        symbol=trade.symbol,
        quantity=trade.quantity,
        price=trade.price,
        exchange="NASDAQ",
    )

    with db_connection() as conn:
        result = create_trade(conn, trade_obj)

        return result #context manager



@app.get("/portfolio", response_model=list[PortfolioResponse])
def get_trade_endpoint():

    with db_connection() as conn:
        result = get_portfolio(conn)

    # database context manager used here for easy read

    
        return result




@app.get("/trades/{symbol}", response_model=list[TradeResponse])
def get_trade_symbol(symbol : str): # (api/schema/API validation)

    with db_connection() as conn:
        result = get_trades_by_symbol(conn, symbol)

        if not result:
            raise HTTPException(status_code=404, detail="Trades not found")
        
        return result



@app.get("/trades", response_model=list[TradeResponse])
def get_trades_endpoint(limit: int = Query(default=5, gt=0, le=100)):

    with db_connection() as conn:
        service_start = time.time()

        result = get_trades(conn, limit)
        logging.info(f"Service layer took {time.time() - service_start:.4f}s")

        return result


@app.get("/portfolio/{symbol}", response_model=PortfolioResponse)
def get_portfolio_by_symbol_endpoint(symbol: str):

    with db_connection() as conn: 
        # one type of connection pattern here which is context manager, used 
        # a try and finally block before and manually opened and closed connections...
        result = get_portfolio_by_symbol(conn, symbol)

        if not result:
            raise HTTPException(status_code=404, detail="Portfolio position not found")
        
        return result
    

@app.get("/positions", response_model=list[PositionResponse])
def get_positions_endpoint():

    with db_connection() as conn: # context manager usage for connection poooling

        result = get_positions(conn)

        if not result:
            raise HTTPException(status_code=404, detail="Positions didn't find anything")
        
        return result

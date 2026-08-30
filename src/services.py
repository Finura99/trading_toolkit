import time
import logging
from fastapi import HTTPException

from src import repository
from src.utils import log_execution
from src.domain import Trade, EquityTrade
from src.constants import SUPPORTED_SYMBOLS



logging.basicConfig(level=logging.INFO)


#------------------------------------------------------------------------


def create_trade(conn, trade: EquityTrade): # parameters
    
    if trade.quantity <= 0:
        raise HTTPException(status_code=400,
                            detail="Quantity must be positive")
    # extra layer of api validation
        

    if trade.symbol.upper() not in SUPPORTED_SYMBOLS:
        raise HTTPException(status_code=400,
                            detail=f"Unsupported symbol: {trade.symbol}")
    # business validations
    

    persisted_trade = repository.insert_trade_repo(conn, trade)
    # persistence goes onto the repository layer / abstraction

    # add business derived data below

    return {
        **persisted_trade, # using double asterisks here for unpacking the dict.
        "trade_value" : trade.notional_value()
    }



def get_portfolio(conn): # aggregates the trade data into an overview for the client to get detailed info of their portfolio.

    return repository.get_portfolio_repo(conn)

# simple one line, as I delegated the persistence in the repository layer.
# doesnt care about SQL, tuples, cursors and fetchall()

def get_trades_by_symbol(conn, symbol: str):

    return repository.get_trades_by_symbol_repo(conn, symbol)



@log_execution
# a decorator is a func that takes another func as an input and returns a new func wrapper that adds extra behaviour
def get_trades(conn, limit: int):
    return repository.get_trades_repo(conn, limit)



def get_portfolio_by_symbol(conn, symbol: str):

    portfolio = repository.get_portfolio_by_symbol_repo(conn, symbol)

    if portfolio == None:
        raise HTTPException(status_code=404, detail="Portfoliio not found")

    return portfolio


@log_execution
def get_positions(conn):
    return repository.get_positions_repo(conn)
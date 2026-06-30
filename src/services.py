import time
import logging
from fastapi import HTTPException

from src.utils import reverse_string, log_execution
from src.domain import Trade, EquityTrade

# add input validation

def validate_input(symbol: str):

    symbol = symbol.strip().upper()

    return symbol



logging.basicConfig(level=logging.INFO)


#------------------------------------------------------------------------


def create_trade(conn, trade: EquityTrade): # parameters
    cursor = conn.cursor()
    # cursor is the sql tool used within the connection

    try: 
        if trade.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be positive")
        
        logging.info(f"Creating trade for symbol={trade.symbol}")
        
        cursor.execute(
            """
            INSERT INTO trades (symbol, side, quantity, price)
            VALUES (%s, %s, %s, %s)
            RETURNING symbol, side, quantity, price;
            """,
            (trade.symbol, trade.side.value, trade.quantity, trade.price)
        ) 
        # db call ?

        row = cursor.fetchone() # returns as a tuple

        logging.info("Before Commit")
        conn.commit() # save changes - DB transaction handling - only used when writing/updating data 
        logging.info("After Commit")

        symbol, quantity, price = row

        

        return {
            "symbol" : symbol,
            "quantity": quantity,
            "price" : price,
            "trade_value" : trade.notional_value(),
            "side": trade.side.value,
        }
    
    except Exception as e:
        logging.error(f"Database transaction failed: {e}")
        conn.rollback()
        raise 
        
    finally:
        cursor.close()


def get_portfolio(conn): # aggregates the trade data into an overview for the client to get detailed info of their portfolio.

    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            symbol,
            SUM(quantity) AS total_quantity,
            SUM(quantity * price) / SUM(quantity) AS average_price,
            SUM(quantity * price) AS total_value
        FROM trades
        GROUP BY symbol;
    """)

    rows = cursor.fetchall() # returns a list of tuples
    cursor.close()

    result = []

    for row in rows: # loop through to append them in the list "result"
        result.append({
            "symbol" : row[0],
            "total_quantity" : row[1],
            "average_price": row[2],
            "total_value": row[3]
        })

    return result



############################################################################################################
# generator


def generate_trade_responses(rows): # helper generator function
    for row in rows:
        symbol, side, quantity, price = row

        trade = Trade(symbol=symbol, quantity=quantity, price=price, side=side)

        yield {
            "symbol": trade.symbol,
            "quantity": trade.quantity,
            "price": trade.price,
            "trade_value": trade.notional_value(),
            "side": trade.side.value,
        } 

# pauses every call and resumes where it left off...
# single source of truth for turning DB rows into API response dictionairies.


############################################################################################################






def get_trades_by_symbol(conn, symbol: str):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT symbol, quantity, price
        FROM trades
        WHERE symbol = %s;
    """, 
    (symbol,)
    )

    rows = cursor.fetchall() # list of tuples
    cursor.close()

    result = []

    for row in rows:

        trade = Trade(symbol=row[0],
                      side=row[1], 
                      quantity=row[2],
                      price=row[3],
                      ) 
        # used a class to rep a trade object for extendability instead of raw dict.

        result.append({
            "symbol" : trade.symbol,
            "quantity" : trade.quantity,
            "price" : trade.price,
            "trade_value": trade.notional_value(),
            "side": trade.side.value,
        })

    return result

@log_execution # a decorator is a func that takes another func as an input and returns a new func wrapper that adds extra behaviour
def get_trades(conn, limit: int):

    cursor = conn.cursor()

    query_start = time.time() # logging latency

    try:
        cursor.execute("""
            SELECT symbol, side, quantity, price
            FROM trades
            LIMIT %s
        """, (limit,)
        )

        logging.info(f"DB query took {time.time() - query_start:.4f}s")

        rows = cursor.fetchall()

        return list(generate_trade_responses(rows))

    finally:
        cursor.close()


def portfolio_row_to_dict(row): # Helper function
    return {
        "symbol": row[0],
        "total_quantity": row[1],
        "average_price": row[2],
        "total_value": row[3],
        
    }


def get_portfolio_by_symbol(conn, symbol: str):

    cursor = conn.cursor() # creates the tool from an already open db conn

    try:
        cursor.execute("""
            SELECT
                symbol,
                SUM(quantity) AS total_quantity,
                SUM(quantity * price) / SUM(quantity) AS average_price,
                SUM(quantity * price) AS total_value
            FROM trades
            WHERE symbol = %s
            GROUP BY symbol
        """,
        (symbol,))

        row = cursor.fetchone() #fetches what we executed...

        if row is None:
            return None # edge case...

        return portfolio_row_to_dict(row)
    
    except Exception as e:
        logging.error(f"Database error: {e}")
        raise # added structured exception logging to improve debugging and observability

    finally:
        cursor.close() # cursor clean up no matter what...



def get_positions(conn):
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                symbol,
                SUM(
                    CASE
                        WHEN side = 'BUY' THEN quantity
                        WHEN side = 'SELL' THEN -quantity
                    END
                ) AS net_quantity
            FROM trades
            GROUP BY symbol;
        """)

        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append({
                "symbol": row[0],
                "net_quantity": row[1],
            })

        return result

    finally:
        cursor.close()


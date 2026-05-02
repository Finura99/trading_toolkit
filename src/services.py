from src.utils import reverse_string, log_execution
from src.oop_sandbox import Trade, EquityTrade

import logging
# add input validation

def validate_input(symbol: str):

    symbol = symbol.strip().upper()

    return symbol

logging.basicConfig(level=logging.INFO)


def create_trade(conn, trade: EquityTrade): # parameters 
    cursor = conn.cursor()

    try: # cursor is the tools used within the connection
        
        logging.info(f"Creating trade for symbol={trade.symbol}")
        
        cursor.execute( 
            """
            INSERT INTO trades (symbol, quantity, price)
            VALUES (%s, %s, %s)
            RETURNING symbol, quantity, price;
            """,
            (trade.symbol, trade.quantity, trade.price)
        )

        row = cursor.fetchone() # returns as a tuple

        logging.info("Before Commit")        
        conn.commit() # save changes - transaction handling
        logging.info("After Commit")
        

        symbol, quantity, price = row

        return {
            "symbol" : symbol,
            "quantity": quantity,
            "price" : price,
            "trade_value" : trade.trade_value()
        }
        
    
    finally:
        cursor.close()


def get_portfolio(conn): # aggregates the trade data into a overview for the client to get detailed info of their portfolio.

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

# generator
def generate_trade(rows):

    trade = Trade.trade_value() # invoke the class as it promotes reusability.

    for row in rows: # lazy sequencing, has a stop iterator
        yield {
            "symbol": row[0],
            "quantity" : row[1],
            "price": row[2],
            "trade_value" : trade
        }
    return list(generate_trade(rows))


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

        trade = Trade(row[0], row[1], row[2]) # used a class to rep a trade object for extendability instead of raw dict.

        result.append({
            "symbol" : trade.symbol,
            "reversed_symbol": reverse_string(row[0]), # first element of the tuple
            "quantity" : trade._quantity,
            "price" : trade.price,
            "trade_value": trade.trade_value()
        }) 

    return result

@log_execution # a decorator is a func that takes another func as an input and returns a new func wrapper that adds extra behaviour
def get_trades(conn, limit: int):

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT symbol, quantity, price
            FROM trades
            LIMIT %s
        """, (limit,)
        )

        rows = cursor.fetchall()
        result = []


        for row in rows:
            symbol, quantity, price = row

            trade = EquityTrade(symbol, quantity, price, "NASDAQ")

            result.append(trade.to_dict()) # method inside equity class

        return result

    finally:
        cursor.close()

def get_portfolio_by_symbol(conn, symbol: str):

    cursor = conn.cursor()

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

        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "symbol": row[0],
            "total_quantity": row[1],
            "average_price" : row[2],
            "total_value" : row[3]
        }

    finally:
        cursor.close() # cursor clean up no matter what 
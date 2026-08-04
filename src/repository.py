import logging
from time import time
from src.domain import EquityTrade


logging.basicConfig(level=logging.INFO)

###########################################

def insert_trade_repo(conn, trade: EquityTrade):
    cursor = conn.cursor()
    # cursor is the sql tool used within the connection

    try:
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

        symbol, side, quantity, price = row # mapping the rows 

        return {
            "symbol" : symbol,
            "side": side,
            "quantity": quantity,
            "price" : price,
        }

    except Exception as e:
        logging.error(f"Database transaction failed: {e}")
        conn.rollback()
        raise
        
    finally:
        cursor.close()



from src.utils import reverse_string, log_execution
# add input validation

def validate_input(symbol: str):

    symbol = symbol.strip().upper()

    return symbol


def create_trade(conn, symbol: str, quantity: float, price: float): # parameters 
    cursor = conn.cursor()

    # insert into db
    try:
        cursor.execute(
            """
            INSERT INTO trades (symbol, quantity, price)
            VALUES (%s, %s, %s)
            RETURNING symbol, quantity, price;
            """,
            (symbol, quantity, price)
        )

        row = cursor.fetchone() # returns as a tuple
        cursor.commit() # write function

        # calculate derived field
        trade_value = row[1] * row[2]

        return {
            "symbol" : row[0],
            "quantity": row[1],
            "price" : row[2],
            "trade_value" : trade_value
        }
    finally:
        cursor.close()


def get_portfolio(conn):

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
    for row in rows:
        yield {
            "symbol": row[0],
            "quantity" : row[1],
            "price": row[2],
            "trade_value" : row[1] * row[2]
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
        result.append({
            "symbol" : row[0],
            "reversed_symbol": reverse_string(row[0]), # first element of the tuple
            "quantity" : row[1],
            "price" : row[2],
            "trade_value": row[1] * row[2]
        })

    return result

@log_execution # a decorator is a func that takes another func as an input and returns a new func wrapper that adds extra behaviour
def get_trades(conn):

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT symbol, quantity, price
            FROM trades
        """
        )

        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append({
                "symbol" : row[0],
                "quantity": row[1],
                "price" : row[2],
                "trade_value": row[1] * row[2]
            })

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
            GROUP BY symbol;
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
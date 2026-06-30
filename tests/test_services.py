from src.services import get_positions


class FakeCursor:
    def execute(self, query):
        self.query = query

    def fetchall(self):
        return [
            ('AAPL', 6, 150, 900),
            ('MSFT', -8, 300, -2400)
        ]
    
    def close(self):
        pass

class FakeConnection:
    def cursor(self):
        return FakeCursor()
    

def test_get_positions_returns_aggregated_positions():
    conn = FakeConnection()

    result = get_positions(conn)

    assert result == [
        {
            "symbol": "AAPL",
            "net_quantity": 6,
            "market_price": 150,
            "exposure": 900,
        },
        {
            "symbol": "MSFT",
            "net_quantity": -8,
            "market_price": 300,
            "exposure": -2400,
        },
    ]
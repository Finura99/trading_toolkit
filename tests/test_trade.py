from src.oop_sandbox import EquityTrade

def test_trade_value():
    trade = EquityTrade("AAPL", 10, 150, "NASDAQ")

    assert trade.trade_value() == 1515
    
import pytest

from src.domain import Trade, TradeValidator, TradeFeeCalculator, TradeProcessor, EquityTrade


def test_trade_calculates_notional_value():
    trade = Trade(symbol="AAPL", quantity=10, price=150)

    assert trade.notional_value() == 1500



def test_trade_normalises_symbol():
    trade = Trade(symbol="  aapl  ", quantity=10, price=150)

    assert trade.symbol == "AAPL"



def test_trade_validates_negative_quantity():
    with pytest.raises(ValueError):
        Trade(symbol="AAPL", quantity=-10, price=150)



def test_trade_rejects_zero_price():
    with pytest.raises(ValueError):
        Trade(symbol="AAPL", quantity=10, price=0)


def test_trade_has_human_readable_string():
    trade = Trade(symbol="AAPL", quantity=10, price=150)

    assert str(trade) == "AAPL: 10 @ 150"


def test_trade_validator_accepts_valid_trade():
    trade = Trade(symbol="AAPL", quantity=10, price=150)

    validator = TradeValidator()

    assert validator.validate(trade) == None

def test_trade_validator_rejects_missing_symbol():
    
    validator = TradeValidator()

    with pytest.raises(ValueError):
        Trade(symbol="", quantity=10, price=150)

def test_trade_fee_calculator_fee():
    trade = Trade(symbol="AAPL", quantity=10, price= 150)
    calculator = TradeFeeCalculator()

    assert calculator.calculate_fee(trade) == 1.5

def test_trade_processor_trade():
    trade = Trade(symbol="AAPL", quantity=10, price=150)

    processor = TradeProcessor(
        validator=TradeValidator(),
        fee_calculator=TradeFeeCalculator(),
    )

    result = processor.process(trade)

    assert result == {
        "symbol": "AAPL",
        "notional_value": 1500,
        "fee": 1.5,
        "net_value": 1498.5,
    }

def test_equity_trade_inherits_trade_behaviour():
    trade = EquityTrade(symbol="MSFT", quantity=5, price=300, exchange="NASDAQ")

    assert trade.market() == f"{trade.symbol} trades on {trade.exchange}"

    

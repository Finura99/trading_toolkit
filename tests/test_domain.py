import pytest

from src.domain import (
                        Trade, 
                        TradeValidator, 
                        TradeProcessor, 
                        EquityTrade,
                        PercentageFeeCalculator,
                        FixedFeeCalculator,
                        TradeFeeCalculator,
                        ZeroFeeCalculator,
                        TradeSide,
                        calculate_positon,
                        calculate_exposure,
                        )


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
        fee_calculator=PercentageFeeCalculator(),
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


def test_trade_processor_uses_percentage_fees():
    trade = Trade(symbol="AAPL", quantity=10, price=150)

    processor = TradeProcessor(
        validator=TradeValidator(),
        fee_calculator=PercentageFeeCalculator()
    )

    result = processor.process(trade)

    assert result["fee"] == 1.5
    assert result["net_value"] == 1498.5


def test_trade_processor_uses_fixed_fee_processor():
    trade = Trade(symbol="AAPL", quantity=10, price=150)

    processor = TradeProcessor(
        validator=TradeValidator(),
        fee_calculator=FixedFeeCalculator()
    )

    result = processor.process(trade)

    assert result["fee"] == 2.5
    assert result["net_value"] == 1497.5

def test_zero_fee_calculator():
    trade = Trade(symbol="AAPL", quantity=10, price=150)

    calculator = ZeroFeeCalculator() 
    # object stored in that variable

    assert calculator.calculate_fee(trade) == 0

def test_trade_processor_uses_zero_fee():
    trade = Trade(symbol="AAPL", quantity=10, price=150)

    processor = TradeProcessor(validator=TradeValidator(), fee_calculator=ZeroFeeCalculator())

    result = processor.process(trade)

    assert result["fee"] == 0.0


def test_buy_trade_has_positive_signed_quantity():
    trade = Trade(symbol="AAPL", quantity=10, price=100, side=TradeSide.BUY)

    assert trade.signed_quantity() == 10

# because its a buy and has a quantity of 10 the signed quantity 
# which tells us the trades positon (+ or -) gives us a positive number 10

def test_sell_trade_has_negative_signed_quantity():
    trade = Trade(symbol="AAPL", quantity=4, price=120, side=TradeSide.SELL)

    assert trade.signed_quantity() == -4


def test_trade_side_string_is_normalised_to_enum():
    trade = Trade(symbol="AAPL", quantity=5, price=100, side="sell") #"sell" needs t obe converted to a "SELL"

    assert trade.side == TradeSide.SELL ## normalises through the dunder method isinstance()
    assert trade.signed_quantity() == -5

def test_invalid_trade_side_raises_value_error():
    with pytest.raises(ValueError):
        Trade(symbol="AAPL", quantity=5, price=100, side="banana")

def test_calculate_positon_from_buy_and_sell_trades():
    trades = [
        Trade(symbol="AAPL", quantity=10, price=100, side=TradeSide.BUY),
        Trade(symbol="AAPL", quantity=4, price=100, side=TradeSide.SELL),
        Trade(symbol="AAPL", quantity=2, price=100, side=TradeSide.BUY),
    ]

    assert calculate_positon(trades) == 8

def test_calculate_exposure_from_positon_and_market_price():
    position = 8
    market_price = 100

    assert calculate_exposure(position, market_price) == 800
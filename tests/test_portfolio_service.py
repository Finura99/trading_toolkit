from src.services import portfolio_row_to_dict


def test_portfolio_row_to_dict_returns_dict():
    row = ("AAPL", 100, 150.25, 15025.00)

    result = portfolio_row_to_dict(row)

    assert result == {
        "symbol": row[0],
        "total_quantity": row[1],
        "average_price": row[2],
        "total_value": row[3],
    }
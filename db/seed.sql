INSERT INTO trades (symbol, side, quantity, price)
VALUES
('AAPL','BUY', 10, 150),
('AAPL', 'BUY', 4, 155),
('TSLA','BUY', 5, 200),
('MSFT','SELL', 8, 300)
ON CONFLICT (symbol) DO NOTHING;

INSERT INTO market_prices (symbol, price)
VALUES
('AAPL', 170),
('TSLA', 220),
('MSFT', 310)
ON CONFLICT (symbol) DO UPDATE
SET price = EXCLUDED.price;
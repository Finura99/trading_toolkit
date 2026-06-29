INSERT INTO trades (symbol, side, quantity, price)
VALUES
('AAPL','BUY', 10, 150),
('AAPL', 'BUY', 4, 155),
('TSLA','BUY', 5, 200),
('MSFT','SELL', 8, 300)
ON CONFLICT (symbol) DO NOTHING;
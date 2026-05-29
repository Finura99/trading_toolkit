INSERT INTO trades (symbol, quantity, price)
VALUES
('AAPL', 10, 150),
('TSLA', 5, 200),
('MSFT', 8, 300)
ON CONFLICT (symbol) DO NOTHING;
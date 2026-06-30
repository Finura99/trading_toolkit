
CREATE TABLE IF NOT EXISTS trades (
    id SERIAL PRIMARY KEY,
    symbol TEXT UNIQUE NOT NULL,
    side TEXT NOT NULL DEFAULT 'BUY',
    quantity NUMERIC NOT NULL,
    price NUMERIC NOT NULL
);

DROP TABLE IF EXISTS market_prices;

CREATE TABLE market_prices (
    symbol TEXT PRIMARY KEY,
    price NUMERIC NOT NULL
);
# Fix

## Debugging Note — Duplicate Symbol Constraint

Problem:
Valid POST /trades requests for AAPL were returning 500 Internal Server Error.

Investigation:
I used curl to reproduce the issue, checked the FastAPI logs, then connected into the Postgres Docker container using psql. I initially inspected the wrong database (`postgres`) before checking my `.env` and realising the app uses `postgres_toolkit`.

Root cause:
The `trades` table had a unique constraint on `symbol` called `trades_symbol_key`. That meant only one trade per symbol was allowed.

Why this was wrong:
In a trading system, multiple trades can exist for the same instrument. The unique field should be the trade `id`, not the `symbol`.

Fix:
I connected to the correct database, inspected the schema with `\d trades`, removed the bad constraint, and verified multiple AAPL trades could now be inserted.

Commands used:

- `docker exec -it postgres-toolkit-local psql -U admin -d postgres_toolkit`
- `\d trades`
- `ALTER TABLE trades DROP CONSTRAINT trades_symbol_key;`
- `SELECT * FROM trades WHERE symbol = 'AAPL';`

Interview explanation:

While testing my trade creation endpoint, I discovered valid duplicate AAPL trades were failing with a 500. I traced the issue from the API logs into Postgres, inspected the table schema, and found a unique constraint on `symbol`. It did not match the trading domain because multiple trades can exist for the same instrument. I fixed the schema so `id` remains unique but `symbol` does not then verified the fix with curl, SQL queries and tests.

from unittest.mock import patch, Mock
from src.db import check_db_connection, db_connection


def test_db_connection_returns_connection_to_pool():
    fake_conn = Mock() # creates a fake connection object. It doesnt actually connect to postgres.
        # its just a stand-in.

    with patch("src.db.connection_pool") as mock_pool: 
        # temporarily replaces the real connection_pool with a fake one.
        
        mock_pool.getconn.return_value = fake_conn # assigning value of the connection to fake conn

        with db_connection() as conn: # ok i know this
            assert conn == fake_conn


        mock_pool.getconn.assert_called_once()  
        mock_pool.putconn.assert_called_once_with(fake_conn)

# System strucutre understanding

          Client (curl / Swagger)

                    │
                    ▼

              FastAPI Router

                    │
                    ▼

             Service Layer

                    │
                    ▼

          Database Layer / Repository

                    │
                    ▼

          PostgreSQL Connection Pool

                    │
                    ▼

               PostgreSQL

## Notes

middleware wraps the whole request cycle

## Future Improvement - Decimal for Financial Values

Current trade quantity and price values use python numeric types that may appear as floats in API responses. For finance style systems, prices and monetary values should ideally use python Decimal and NUMERIC in PostgreSQL to avoid floating-point precision errors.


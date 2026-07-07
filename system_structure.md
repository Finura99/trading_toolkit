
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
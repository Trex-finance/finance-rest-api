from typing import Optional

from fastapi import FastAPI

# region API Initialization

tags_metadata = [
    {
        "name": "metadata",
        "description": "metadata about this open-source project"
    },

    {
        "name": "testing",
        "description": "functions used for testing-purposes only"
    },

    {
        "name": "companies",
        "description": "Manage various financial information about companies.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        }
    }
]

app = FastAPI(
    title="Trex DevOps Team Finance API",
    description="Run various financial scripts, all in one API. This project is an open source project, made by the "
                "members of Trex DevOps",
    version="1.0.0"
)


# endregion

# region Companies

# Output the company CIK
@app.get("/{exchange_name}/{stock_ticker}/company_cik", tags=['companies'])
def get_company_cik(exchange_name: str, stock_ticker: str):
    return {f"{exchange_name}: {stock_ticker}"}


# Output the details of the last submitted filing for {STOCK_TICKER} at {year}.
@app.get("/{exchange_name}/{stock_ticker}/get_last_filling_for_company_in_year", tags=['companies'])
def get_last_filling(exchange_name: str, stock_ticker: str,
                     filling_year: Optional[int] = None):
    return {f"{exchange_name}: {stock_ticker}, year: {filling_year}"}


# Returns true if there is a new filling for this company.
@app.get("/{exchange_name}/{stock_ticker}/is_there_new_filling", tags=['companies'])
def is_there_new_filling(exchange_name: str, stock_ticker: str):
    return {f"{exchange_name}: {stock_ticker}"}


# Writes the last time we checked the company filling to some DB.
@app.post("/{exchange_name}/{stock_ticker}/last_time_checked_for_company_filling", tags=['companies'])
def post_last_filling_time_for_company(exchange_name: str, stock_ticker: str):
    return {f"{exchange_name}: {stock_ticker}"}


# endregion

# region metadata
@app.get("/contributors", tags=['metadata'])
def get_list_of_contributors():
    return {"Trex Team"}


# endregion

# region Testing


@app.get("/test", tags=['testing'])
def print_hello_world():
    return {"Hello world!"}
# endregion

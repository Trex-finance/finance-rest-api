from typing import Optional

from fastapi import FastAPI

# region API Initialization
import sec_finance_functions

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

# TODO: Currently all the functions below work only with the SEC.
# There is no {exchange_name} or something like that. endpoints are hardcoded to go to the SEC.


@app.get("/{stock_ticker}/company_cik", tags=['companies'])
def get_company_cik(stock_ticker: str):
    """
    Output the company CIK listed (applicable only for stocks issues in the SEC, so no exchange name is required)

    :param stock_ticker: the company stock ticker
    :return: the company CIK
    """
    company_cik = sec_finance_functions.get_company_data_by_ticker(stock_ticker).company_cik
    return company_cik


@app.get("/{stock_ticker}/get_last_filling_for_company_in_year", tags=['companies'])
def get_last_filling(stock_ticker: str,
                     filling_year: Optional[int] = None):
    """
    Get the number of fillings of a stock for the given year (or all fillings since the company listing)

    :param stock_ticker: The stock ticker
    :param filling_year: The year in format '2020' for all fillings in 2020, or nothing to
    retrieve all the company filling since listing.

    :return: number of fillings
    """
    company_cik = sec_finance_functions.get_company_data_by_ticker(stock_ticker).company_cik
    all_company_fillings = sec_finance_functions.get_all_company_filings_by_cik(company_cik)
    all_company_fillings_by_year = sec_finance_functions.get_all_fillings_of_year(all_company_fillings, filling_year)
    return all_company_fillings_by_year


# TODO: Add implementation for this function
@app.get("/{stock_ticker}/is_there_new_filling", tags=['companies'])
def is_there_new_filling(stock_ticker: str):
    """
    Returns true if there is a new filling for this company.

    :param stock_ticker: the stock ticker
    :return: true if there is a new filling since the last time we checked, or false if not.
    """
    return {f"Function is not implemented yet"}


# Writes the last time we checked the company filling to some DB.
@app.post("/{stock_ticker}/last_time_checked_for_company_filling", tags=['companies'])
def post_last_filling_time_for_company(stock_ticker: str):
    return {f" {stock_ticker}"}


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

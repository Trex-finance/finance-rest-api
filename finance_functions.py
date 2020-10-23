import time

import requests
from pytictoc import TicToc
from typing import List
from bs4 import BeautifulSoup

from FinanceClasses import *
from constants import *


# REQ: Ticker (AAPL, GOOGL, AMZN)
# Returns: CIK (CENTRAL INDEX KEY)
def get_company_data_by_ticker(ticker):
    ticker = ticker.upper()
    t = TicToc()

    content = requests.get(SEC_COMPANY_TICKERS_DB_URL)
    if 200 <= content.status_code < 300:
        t.tic()
        list_of_companies_data = content.json()

        for index in list_of_companies_data:
            if list_of_companies_data[index]['ticker'] == ticker:
                t.toc(msg=f"CIK for {ticker} found after")

                return Company(
                    company_title=list_of_companies_data[index]['title'],
                    company_ticker=list_of_companies_data[index]['ticker'],
                    company_cik=list_of_companies_data[index]['cik_str']
                )

        t.toc(msg=f"CIK for {ticker} not found, time passed")
        return
    else:
        print(f"Networking error with status code: {content.status_code}")
        return


def get_all_filings_by_cik(cik):
    filling_url = f"{SEC_EDGAR_BASE_URL}/{cik}/index.json"
    print(f"retrieving data from: {filling_url}")

    content = requests.get(filling_url)
    content_json = content.json()['directory']['item']
    filing_data = []

    for i in content_json:
        filing_data.append(FillingMetadata(
            last_modified=i['last-modified'],
            name=i['name'],
            file_type=i['type'],
            size=i['size']
        ))

    print(f"filling data received.")
    return filing_data


# given a list of fillings 'list_of_filling', return the fillings of year 'year'
def get_all_fillings_of_year(list_of_filling: List[FillingMetadata], year):
    returned_list = []

    for filling in list_of_filling:
        if filling.get_year_modified() >= year:
            returned_list.append(filling)
        else:
            break  # The first time we encounter a filling which is less than our required year, we break,
            # because all subsequet fillings will be out of this year as well.
    return returned_list


# filling_list expects a list of filling
def get_all_documents_urls_for_filling(cik, filling_list):
    returned_urls = []

    for filling in filling_list:
        print(f"getting all filling for: {filling}")
        current_url = f"{SEC_EDGAR_BASE_URL}/{cik}/{filling}/index.json"
        content_as_json = requests.get(current_url).json()['directory']['item']
        for file_name in content_as_json:
            returned_urls.append(f"{current_url}/{file_name['name']}")
    return returned_urls


#####################################################################
# Scripts to know when a company has filed anything with the SEC
#####################################################################

# filter_time - if you leave this empty, this will fetch fillings from all time
# TODO: add time filtering, because we fetch the fillings from the company ALL time which takes a lot of time.
def get_company_filling_ping_data_by_company(company, filter_time=""):
    t = TicToc()
    t.tic()
    company_all_filings = get_all_filings_by_cik(company.company_cik, "name")
    sum_of_all_fillings = get_all_documents_urls_for_filling(company.company_cik, company_all_filings)
    time_now = int(time.time())
    print("######################################################################")
    print("######################################################################")
    t.toc(msg="Script ran for")
    print(f"total fillings: {len(sum_of_all_fillings)}")
    print(f"time pinged: {time_now}")
    return CompanyFillingPing(
        company=company,
        total_filling_count=len(sum_of_all_fillings),
        time_pinged=time_now)
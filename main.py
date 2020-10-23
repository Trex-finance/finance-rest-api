from finance_functions import *


def main():
    amazon_data = get_company_data_by_ticker("AMZN")
    print(amazon_data.company_cik)
    fillings = get_all_filings_by_cik(amazon_data.company_cik)
    fillings_filtered_by_year = get_all_fillings_of_year(fillings, 2020)
    print(f"[{time.time()}]: A total of {len(fillings_filtered_by_year)} fillings found")

if __name__ == '__main__':
    main()

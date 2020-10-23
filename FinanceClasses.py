class CompanyFillingPing:
    # total_filling_count = The total filling a company has filled with the SEC
    # time_pinged = the time we checked the company total fillings with the SEC
    def __init__(self, company, total_filling_count, time_pinged):
        self.company = company
        self.total_filling_count = total_filling_count
        self.time_checked = time_pinged


class Company:
    def __init__(self, company_title, company_ticker, company_cik):
        self.company_title = company_title
        self.company_ticker = company_ticker
        self.company_cik = company_cik


# WARNING NOTE: notice that returned JSON is "last-modified" and our object is "last_modified" (the hyphen)
# {'last-modified': '2020-10-05 16:30:56', 'name': '000112760220026535', 'type': 'folder.gif', 'size': ''}
class FillingMetadata:
    def __init__(self, last_modified, name, file_type, size):
        self.last_modified = last_modified
        self.name = name
        self.file_type = file_type
        self.size = size

    def get_year_modified(self):
        return int(self.last_modified.split("-")[0])

""" Parse and aggregate the selfcheck Daily excel file and output csv """

from openpyxl  import load_workbook
from file_util import select_filename
import datetime
import pathlib
import re
import csv
import filename_secrets

production_datasets_path = pathlib.Path(filename_secrets.productionStaging)
selfcheck_data_path =  pathlib.Path(filename_secrets.selfcheckStatistics)

# select input/output filenames
search_string = 'All-Daily-LastWeek-*'
self_check_input_daily = select_filename(selfcheck_data_path, search_string)
print(f'Input Filename: {self_check_input_daily}')

# output file is tagged with the last modification date of the input file
timestamp = datetime.datetime.fromtimestamp(self_check_input_daily.stat().st_mtime)
filepath = "selfcheck-Daily.csv"
self_check_output_daily = production_datasets_path.joinpath(filepath)
print(f'Output Filename: {self_check_output_daily}')

# Identify fields for CSV output
csv_header = ['Date', 'CheckoutSuccess', 'CheckoutFail', 'CheckinSuccess', 'CheckinFail', 'ReturnSessionStartCount', 'ReturnSuccess', 'ReturnFail', 'RenewedSuccess','RenewedFail', 'UserLoginSuccess','UserLoginFail', 'LmsOfflineCount', 'PaymentSuccess', 'PaymentFailed', 'CoinboxEmptyCount', 'SuccessfulTransactions', 'FailedTransactions', 'TotalTransactions']

output_fields = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19]

# Open the workbook and set up access to the worksheet
try:
    workbook  = load_workbook(filename = str(self_check_input_daily), read_only=True)
    worksheet = workbook.active
    worksheet_list = list(worksheet.values)
except  Exception:
    raise("Unable to parse input file")

# append to output file & write header row, if empty
with open(self_check_output_daily, 'a+') as output_file:
    csvwriter = csv.writer(output_file, dialect='excel')
    #csvwriter.writerow(csv_header)

    # Select each row aggregate with a date (dd month yyyy) in the first field (daily total)
    for row in range(0, len(worksheet_list)):
        # clear the list
        csv_output=['null']*len(output_fields)
        # process each row and write to CSV
        if worksheet_list[row][0] == "Total":
            # Final line of spreadsheet
            break
        match = re.match('^\d+\s\w+\s+\d{4}', worksheet_list[row][0])
        if match:
            for element in range(0, len(output_fields)):
                csv_output[element] = worksheet_list[row][output_fields[element]]
            csvwriter.writerow(csv_output)

    # close and terminate
    output_file.close()

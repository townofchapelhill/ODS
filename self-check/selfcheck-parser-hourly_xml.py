""" Parse and aggregate the selfcheck Hourly XML file and output csv """

import csv
import untangle

# import access keys and locations
# import secrets
import filename_secrets


# Identify fields for CSV output
csv_header = ['Date', 'Time', 'Device Name', 'CheckoutSuccess', 'CheckoutFail', 'RenewedSuccess','RenewedFail', 'PaymentSuccess', 'PaymentFailed', 'SuccessfulTransactions', 'FailedTransactions', 'CheckOutBookCount', 'TotalTransactions']
output_fields = ['DeviceName', 'txtCheckoutOkCountRow1', 'txtCheckoutFailedCountRow1', 'txtRenewedOkCountRow1', 'txtRenewedFailedCountRow1', 'txtCashPaymentCountRow1', 'txtCashPaymentFailedCountRow1', 'txtSuccessfulTransactionsCountRow1', 'txtFailedTransactionsCountRow1', 'MediaTypeTotal1', 'txtTotalRow1']

# Library open hours
library_hours = {
      "Monday":   {"open": 8, "close": 20},
      "Tuesday":  {"open": 8, "close": 20},
      "Wednesday":{"open": 8, "close": 20},
      "Thursday": {"open": 8, "close": 20},
      "Friday":   {"open": 8, "close": 18},
      "Saturday": {"open": 9, "close": 18},
      "Sunday":   {"open": 9, "close": 18}
    }


def convert24(str1):
    # Given a time as '[H]H:MM [A|P]M' return the hour as an integer in the range {0-23}
    # capture the hours portion of the string
    hour=int(str1.split(':')[0])

    # Checking if last two elements of time
    # is AM and first two elements are 12
    if str1[-2:] == "AM" and hour == 12:
        return 0
    # return AM hours
    elif str1[-2:] == "AM":
        return hour

    # Checking if last two elements of time
    # is PM and first two elements are 12
    elif str1[-2:] == "PM" and hour == 12:
        return hour
    else:
        # add 12 to hours
        return hour + 12

# Open and Parse the xml file

try:
    # extract data from a known location and filename
    obj = untangle.parse(filename_secrets.self_check_input_hourly)
except  Exception:
    raise("Unable to parse input file")

# create output file & write header row
with open(filename_secrets.self_check_output_hourly, 'w') as output_file:
    csvwriter = csv.writer(output_file, dialect='excel')
    csvwriter.writerow(csv_header)

    # process each row and write to CSV

    # iterate on date
    for date_row in range(0, len(obj.Report.Tablix1.EventDateTimePaging_Collection.EventDateTimePaging)):
        csv_output = ['null']*len(csv_header) # initialize the output list
        # get the date
        csv_output[0] = obj.Report.Tablix1.EventDateTimePaging_Collection.EventDateTimePaging[date_row]['txtDateHeader']
        # extract the day of the week
        dayofweek=csv_output[0].split(',')[0]
        # iterate on hour
        for  hour_row in range(0, len(obj.Report.Tablix1.EventDateTimePaging_Collection.EventDateTimePaging[date_row].EventDateTime_Collection.EventDateTime)):
            # extract the hour
            csv_output[1] = hour = obj.Report.Tablix1.EventDateTimePaging_Collection.EventDateTimePaging[date_row].EventDateTime_Collection.EventDateTime[hour_row]['tbDateToggle']
            # only output to csv only during library open hours
            if convert24(hour) >= library_hours[dayofweek]['open'] and convert24(hour) <= library_hours[dayofweek]['close']:
            #iterate on self-check stations
                for station_row in range(2, len(obj.Report.Tablix1.EventDateTimePaging_Collection.EventDateTimePaging[date_row].EventDateTime_Collection.EventDateTime[hour_row].LocationFullName_Collection.LocationFullName.Details_Collection.Details)):
                    # extract each element and place in csv output row
                    for element in range(0, len(output_fields)):
                         field = output_fields[element]
                         csv_output[element+2] = obj.Report.Tablix1.EventDateTimePaging_Collection.EventDateTimePaging[date_row].EventDateTime_Collection.EventDateTime[hour_row].LocationFullName_Collection.LocationFullName.Details_Collection.Details[station_row][field]
                    csvwriter.writerow(csv_output)
output_file.close()




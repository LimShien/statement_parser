# loop in directory to search for CSV file, and combine 
# for revolut statement -> filter only transaction
# return a CSV file with four column[Date, Transaction, Value, Source]
import csv
from datetime import datetime 

input_file = "./data/revolut-statement.csv"
transaction = []
with open(input_file, "r") as file:
  mycsv = csv.reader(file)
  for line in mycsv:
    transaction.append(line)

filtered_transaction = (t for t in transaction if t[0] in ("TRANSFER","CARD_PAYMENT"))
result_transaction = [["Date", "Transaction", "Value", "Currency"]]
for t in filtered_transaction:
  date = datetime.strptime(t[2], "%Y-%m-%d %H:%M:%S").strftime("%d %b")
  value = -float(t[5])
  transaction = t[4]
  currency = t[7]
  result_transaction.append([date,transaction,value, currency])

for t in result_transaction:
  print(t)
  
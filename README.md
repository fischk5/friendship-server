# Friendship Server  
  
A simple Flask server for a friend who needs to pay taxes.  
  
Two endpoints:  
`POST /transactions`  
- Expects a csv file with transaction data  
  
`GET /report`  
- Returns the expenses, gross revenue, and net revenue associated with the transactions  
  
Server runs on port `5000`.

## Prerequisites  
  
- Python 3.10 or higher  
- pip 23.0.1 or higher    
  
## Quick Start  
  
**To setup the server**  
Run the following commands from your machine to start the server:  
  
```bash
git clone repo
cd repo
sh run_server.sh
```  
  
**Using the service with test data**  
From the project directory, run the following command to submit test data to the service:  
`curl -X POST http://localhost:5000/transactions -H "Content-Type: multipart/form-data" -F "file=@test.csv"`  
  
Then, to review the results:  
`curl -X GET http://localhost:5000/report`  
  
Response (prettified):  
```json  
{
    "expenses": 72.93,
    "gross-revenue": 325.0,
    "net-revenue": 252.07
}
```  
  
**Using the service with production data**  
Make a `POST` request to `http://localhost:5000/transactions` with a CSV file attached as `form-data`. Format the CSV as follows:  
- No headers  
- Ordered columns for data, transaction type, transaction value, and an associated description  
- Comments must begin with a `#` character  
  
Example format:  
```
2020-07-01, Expense, 18.77, Fuel
2020-07-04, Income, 40.00, 347 Woodrow
2020-07-06, Income, 35.00, 219 Pleasant
# new spark plugs I think
2020-07-12, Expense, 27.50, Repairs
```  
  
To review the results:  
`curl -X GET http://localhost:5000/report`  
  
Response (prettified):  
```json  
{
    "expenses": 72.93,
    "gross-revenue": 325.0,
    "net-revenue": 252.07
}
```  
  
*Note: submitting new data to the /transactions endpoint will overwrite any existing transaction data*  
  
  
## Design  
  
Friendship Server receives a CSV file, stores it locally on the server (`data.csv`), and processes it into a json report for expenses, gross revenue, and net revenue (`report.json`).  
  
Data processing occurs asynchronously, and is available at the `/report` endpoint when ready.
  
## Assumptions  
  
- The only comment character in the CSV file is `#`  
- CSV file will never include a header  
- CSV file is always composed of 4 columns representing `Date`, `Type`, `Value`, and `Description`  
- The API is consuming a normal CSV file requiring zero validation
  
Example Data:  
  
```
2020-07-01, Expense, 18.77, Gas
# this is a comment and does not contribute to the data
2020-07-04, Income, 40.00, 347 Woodrow
2020-07-06, Income, 35.00, 219 Pleasant
2020-07-12, Expense, 49.50, Repairs
```  
  
## Future Improvements  
  
- Add file security and type checking to the CSV values  
- More robust API method handling for failures, required file formats, edge cases  
- Add event-based processing  
- Handle the race condition between POST and GET, if the report.json file is not ready  
- Backend the server with a database (SQL)  
- Improve threading reliability and stability  
- Build a more robust file naming convention (not needed if a database id value is available)  
- Add unit tests to the `ExpensesProcesser` class  
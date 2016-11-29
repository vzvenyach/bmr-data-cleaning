README

## Setup

Clone the repository. To set up, the original data is stored in the `BMR` folder. To run the script, you'll need an API key from [api.data.gov](https://api.data.gov/). The only external dependencies should be [pandas](pandas.pydata.org) and [requests](http://docs.python-requests.org/en/master/).

## Running `clear_bmr.py`

To run the program for each file, run `python3 clean_bmr.py [FILENAME]`. This then calls the `clean_bmr` function. That function takes the filename, goes through each line of the BMR file, and returns a *cleaned* BMR file and saves that new file to the `results` folder.

The majority of the work is actually done by the `cleaned_code` function. The `cleaned_code` function takes a row of BMR data and returns the corresponding cleaned Food Code. To do so, the function does the following:

1. Take the Food Code from the BMR data row
2. Removes the letter at the end
3. Checks the length of the stripped food code.
    a. If the food code is between 1 and 5 digits, we check the Canadian Food Name Code file and return the matched CountryCode from the Canadian file. If there is no corresponding code, we return `CHECK UPDATED`.
    b. If the Food Code is 6 digits or more, or is blank, search USDA SR and Branded Database for the closest match based on the text of the food description.
        * To do this, we first check a SQL database (if one doesn't exist, the program creates one) to see if the food description text is already found. If it is, it returns the corresponding food code.
        * If the database does not already have the food description text, the program makes a query to the `USDA SR and Branded Database` Application Programming Interface. The top match is then saved to the database and the food code is returned. If there is no match in the Database, the program returns "UNKNOWN".

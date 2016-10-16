import pandas as pd
from lib.cleaned_code import cleaned_code

def clean_bmr(file):
    """
    clean_bmr: takes in BMR file name. Returns cleaned BMRFILE.
    """

    # Loads the BMR data from the Excel File
    bmr = pd.read_excel(file)

    # Replaces blank spaces in the file with the word "NONE".
    bmr = bmr.fillna("NONE")

    # Get the Canadian Food Name Codes from the FOOD NAME.csv file
    food_name = pd.read_csv("data/FOOD NAME.csv", encoding='latin1')

    # Goes through row by row, and cleans the data using the cleanedCode function. Stores result in new "cleaned_code" column in BMR data.
    # bmr["cleaned_code"] = bmr.apply(lambda x: cleaned_code(x, food_name), axis=1)

    # Goes through row by row, and cleans the data using the cleanedCode function. Stores result in new "cleaned_code" column in BMR data.
    bmr = bmr.merge(bmr.apply(lambda x: cleaned_code(x, food_name), axis=1), left_index=True, right_index=True)

    return bmr

if __name__ == "__main__":
    import sys

    # Get the BMR File from the input. Defaults to BMR0002.xls because Tracy is starting with BMR0002
    try:
        BMRFILE = sys.argv[1]
    except:
        BMRFILE = "BMR0002.xls"

    # Clean the BMRFILE0002.xls to transform the food codes in BMRFILE and adds a new cleaned_code column.
    bmr = clean_bmr("BMR/" + BMRFILE)

    # Save the cleaned BMRFILE to the results folder.
    bmr.to_csv("results/CLEANED_" + BMRFILE + ".csv")

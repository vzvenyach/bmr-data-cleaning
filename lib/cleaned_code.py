import re
import pandas as pd
from .get_code_from_usda_api import get_code_from_usda_api

def cleaned_code(row, food_name):
    """
    cleaned_code: takes the row of BMR data, returns the cleaned Food Code.
    """

    # Take the Food Code from the BMR data row
    food_id = row["Food_ID"]

    # Removes the letter at the end
    stripped_food_id = re.sub('[a-zA-Z]','', str(food_id))

    # Checks the length of the stripped food code.
    if len(stripped_food_id) < 5 and len(stripped_food_id) > 1:

        # Checks to see if the food code is in the Canadian Food Name Code file
        if int(stripped_food_id) in food_name["FoodID"].values:

            # If it is, return the matched CountryCode
            result = food_name[food_name["FoodID"] == int(stripped_food_id)]
            cleaned_code = result.CountryCode.values[0]
            description = result.FoodDescription.values[0]
            try:
                return pd.Series({"cleaned_code": '{0:05d}'.format(int(cleaned_code)), "description": description})
            except:
                return pd.Series({"cleaned_code": "CHECK UPDATED", "description": description})
        # If it's here, then the Canadian UPDATE file needs to be checked for the code
        else:
            return pd.Series({"cleaned_code": "CHECK UPDATED", "description": row["Food_Item"]})

    # If the Food Code is 6 digits or more, or is blank, search USDA SR and Branded Database for the closest match based on the text of the food description
    elif len(stripped_food_id) > 5 or len(stripped_food_id) < 1:
        print("Getting %s, %s from USDA API" % (stripped_food_id, row["Food_Item"]))

        # Access the get_code_from_usda_api function
        res = get_code_from_usda_api(row["Food_Item"])
        return pd.Series({"cleaned_code": res[0], "description": res[1]})

    return pd.Series({"cleaned_code": '{0:05d}'.format(int(stripped_food_id)), "description": row["Food_Item"]})

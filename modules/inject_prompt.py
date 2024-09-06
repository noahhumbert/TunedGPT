# Takes the data that is returned from the prompt_handler and injects it into a database
# Input is the user logged in and data from prompt_handler
# Output is a just a return to show it completed

# Imports
import csv

# Setup Database
promptsdb = ".\\databases\\prompts.csv"

# Inject the prompt
def inject_prompt(user, organization, data):
    # Create a New Data list to combine the user with Data
    new_data = []
    new_data.append(user)
    new_data.append(organization)
    for piece in data:
        new_data.append(piece)

    # Remote the commas from the response to keep the whole thing inside one column
    new_data[4] = new_data[4].replace(",", "").replace("\n", "").replace("#", "").replace('#', '')
    new_data[5] = new_data[5].replace(",", "").replace("\n", "").replace("#", "").replace('#', '')

    # Write to the .csv file
    with open(promptsdb, mode='a', newline= '') as file:
        writer = csv.writer(file)
        writer.writerow(new_data)
        file.close()

    return True
# Edits the styles of the organization
# Takes the organization, image_link, primary_color, secondary_color, and text_color as inputs
# Outputs a True if it completed successfully

# Imports
import csv

def style_edits(organization, image_link, primary_color, secondary_color, text_color):
    # Grab the Database
    database = []
    with open('.\\databases\\orgstyles.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            database.append(row)

        file.close()

    # Update Row
    new_values = [image_link, primary_color, secondary_color, text_color]
    for i, row in enumerate(database):
        if row[0] == organization:
            # Update the row with new values (excluding the organization name itself)
            database[i] = [organization] + new_values
            break

    # Write to the file
    with open('.\\databases\\orgstyles.csv', mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(database)
        file.close()

    return True
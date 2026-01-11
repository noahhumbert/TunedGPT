This project is currently in rebuild mode

To add a new feature in settings

Push new column to DB with default value
ALTER TABLE [SETTINGS TABLE NAME]
ADD COLUMN [SETTING NAME] VARCHAR(7) NOT NULL DEFAULT [DEFAULT COLOR HEX];

Add it into the default styles dictionary with the default value for new initialized settings rows

Add it to settings.html calling out the same name as you used in the DB for the column

Edit custom.css to add the attribute and tie it to the variable

Go up to the root of chat.html and add the variable and pull it from the styles dict similar to the others
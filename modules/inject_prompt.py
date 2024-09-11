# Takes the data that is returned from the prompt_handler and injects it into a database
# Input is the user logged in and data from prompt_handler
# Output is a just a return to show it completed

# Imports
from supabase import create_client, Client

url: str = "https://cwopkvreemqzoorgalsq.supabase.co/"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3b3BrdnJlZW1xem9vcmdhbHNxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyNTkzNjk4MCwiZXhwIjoyMDQxNTEyOTgwfQ.zeQP7mgnuo4AWgbDJ4mV6yGGtNrczqtlXaV1q7QG3EE"
supabase: Client = create_client(url, key)

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

    injected_data = {
        "email": new_data[0],
        "organization": new_data[1],
        "date": str(new_data[2]),
        "time": str(new_data[3]),
        "question": new_data[4],
        "response": new_data[5],
        "stop_reason": new_data[6],
        "tokens": new_data[7]
    }

    insert_response = supabase.from_("prompts").insert(injected_data).execute()

    return injected_data
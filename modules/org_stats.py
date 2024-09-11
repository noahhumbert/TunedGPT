# This will make updates to the orgstats database to keep track of tokens, messages, and $$$ owed.
# It will take the inputted data is input
# It will output nothing

# Imports
from supabase import Client, create_client

# Setup Database
url: str = "https://cwopkvreemqzoorgalsq.supabase.co/"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3b3BrdnJlZW1xem9vcmdhbHNxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyNTkzNjk4MCwiZXhwIjoyMDQxNTEyOTgwfQ.zeQP7mgnuo4AWgbDJ4mV6yGGtNrczqtlXaV1q7QG3EE"
supabase: Client = create_client(url, key)

def calculate_cost(tokens, images):
    cost_per_token = float(0.000002)
    cost_per_image = float(0.5)

    return (cost_per_token * tokens) + (cost_per_image * images)

def update_stats(injected_data):
    # Check for organization in database
    response = supabase.from_("orgstats").select("*").eq("organization", injected_data['organization']).execute()
    data = response.data
    data = data[0]

    if injected_data["tokens"] == "image":
        data['images'] += 1
        data['images-this-period'] += 1
    else:
        data['messages-total'] += 1
        data['messages-this-period'] += 1
        data['tokens-this-period'] = data['tokens-this-period'] + injected_data['tokens']
        data['tokens-total'] = data['tokens-total'] + injected_data['tokens']

    data['payment-this-period'] = calculate_cost(data['tokens-this-period'], data['images-this-period'])

    new_data = {
        "organization": data['organization'],
        "tokens-this-period": data['tokens-this-period'],
        "tokens-total": data['tokens-total'],
        "messages-this-period": data['messages-this-period'],
        "messages-total": data['messages-total'],
        "payment-this-period": data['payment-this-period'],
        "total-payed": data['total-payed'],
        "images": data['images'],
        "images-this-period": data['images-this-period']
    }

    update_response = supabase.from_("orgstats").update(new_data).eq("organization", data['organization']).execute()
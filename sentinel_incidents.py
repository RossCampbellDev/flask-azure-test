import requests, json

api_string = "https://management.azure.com/subscriptions/351a12b6-0416-40e1-ae18-c0e6fb0334c8/resourceGroups/networkwatcherrg/providers/Microsoft.OperationalInsights/workspaces/sentineltest/providers/Microsoft.SecurityInsights/incidents?api-version=2021-04-01"

response = json.loads(requests.request('GET', api_string).text)

print(response)

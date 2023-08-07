import requests, json


url = "https://api.opensea.io/api/v1/collection/boredapeyachtclub"

response = requests.request("GET", url)
a = json.dumps(response.json(), indent=4)
print(a)

# import requests

# url = "https://api.opensea.io/api/v1/asset/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/1/"

# response = requests.request("GET", url)

# print(response.text)

# url = "https://api.opensea.io/api/v1/collections?offset=0&limit=300"

# headers = {"Accept": "application/json"}

# response = requests.request("GET", url, headers=headers)

# print(response.text)
# 5AJqCETCc8HyMSaxWtSFmgqCKRNR5UrLPIKkB2bZ3I2jzGbEdInGKRnct7USAXQ3
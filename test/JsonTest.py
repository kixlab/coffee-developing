import urllib.request
import json

teststr = '''
{'query': 'Sugar', 'topScoringIntent':
{'intent': 'set_field', 'score': 0.459747642},
'intents': [{'intent': 'set_field', 'score': 0.459747642},
{'intent': 'query_field', 'score': 0.0576428734},
{'intent': 'None', 'score': 0.0481121652},
{'intent': 'change_tempature', 'score': 0.00647813035},
{'intent': 'coffee_service', 'score': 0.00320557854},
{'intent': 'query_tempature', 'score': 0.000132509289}],
'entities': []}
'''
teststr = teststr.replace('\n',' ').strip()
encres = json.JSONEncoder().encode(teststr)

print(encres)


'''
link = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/b17f3e2d-8222-45c1-a51e-300d12dead2d?subscription-key=99632d6d302c405f8ff27c28ffc7d8d7&staging=true&verbose=true&timezoneOffset=0&q="
query = input("QUERY : ")
f = urllib.request.urlopen(link + query)
myfile = f.read()
resultJson = json.loads(myfile)
print(resultJson)

print(json.JSONDecoder.raw_decode(resultJson))
'''

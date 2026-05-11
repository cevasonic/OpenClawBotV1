import requests
import os

API_KEY = "v2.q7eyXHFzT_Lr1YGzQxRIFA50CvegggHCdbojQf5zfoBqxaJe59-OaBGXkxRJw70jN2nsvRpDvPPKFEyMncX0Gn31JT8VNIkN_WV_RdJcId8d4Jg0F1KrfTp1"
headers = {"Authorization": f"Bearer {API_KEY}"}

ROOT_ID = "C64D3600679F709F!32557"
url = f"https://gateway.maton.ai/one-drive/v1.0/drive/items/{ROOT_ID}/children"
print(f"Testing {url}...")
try:
    r = requests.get(url, headers=headers)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:500]}")
except Exception as e:
    print(f"Error: {e}")

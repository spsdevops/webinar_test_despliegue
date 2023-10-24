import requests
import base64
import json
import pprint
from jose import jwk
from jose.utils import base64url_decode

openid_domain = "token.actions.githubusercontent.com"
token_jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImVCWl9jbjNzWFlBZDBjaDRUSEJLSElnT3dPRSIsImtpZCI6Ijc4MTY3RjcyN0RFQzVEODAxREQxQzg3ODRDNzA0QTFDODgwRUMwRTEifQ.eyJqdGkiOiI2NDlhNGVjMC1lYTM5LTRiMGQtYmJkMi03Mjg0YmEzNWU1MWMiLCJzdWIiOiJyZXBvOnNwc2Rldm9wcy93ZWJpbmFyX3Rlc3RfZGVzcGxpZWd1ZTplbnZpcm9ubWVudDpkZXZlbG9wIiwiYXVkIjoiY2ljZC5zcHMiLCJyZWYiOiJyZWZzL2hlYWRzL21haW4iLCJzaGEiOiJmZGJiZmU0ZGUzZDQ1YTEzMWRlOWY5YTcyZWFjY2FhYWE5YWRiYzVhIiwicmVwb3NpdG9yeSI6InNwc2Rldm9wcy93ZWJpbmFyX3Rlc3RfZGVzcGxpZWd1ZSIsInJlcG9zaXRvcnlfb3duZXIiOiJzcHNkZXZvcHMiLCJyZXBvc2l0b3J5X293bmVyX2lkIjoiOTcyNTQ5MDciLCJydW5faWQiOiI1NzIwMDExMzg1IiwicnVuX251bWJlciI6IjMwIiwicnVuX2F0dGVtcHQiOiIyIiwicmVwb3NpdG9yeV92aXNpYmlsaXR5IjoicHVibGljIiwicmVwb3NpdG9yeV9pZCI6IjY1Mjg1MDc2MyIsImFjdG9yX2lkIjoiMTI3NzkwNjE4IiwiYWN0b3IiOiJKb3N1ZUNydXpCYXJyYWdhbiIsIndvcmtmbG93IjoiMSDwn5qAIERldiIsImhlYWRfcmVmIjoiIiwiYmFzZV9yZWYiOiIiLCJldmVudF9uYW1lIjoicHVzaCIsInJlZl9wcm90ZWN0ZWQiOiJmYWxzZSIsInJlZl90eXBlIjoiYnJhbmNoIiwid29ya2Zsb3dfcmVmIjoic3BzZGV2b3BzL3dlYmluYXJfdGVzdF9kZXNwbGllZ3VlLy5naXRodWIvd29ya2Zsb3dzL3B1c2gtbWFudWFsX21haW4ueW1sQHJlZnMvaGVhZHMvbWFpbiIsIndvcmtmbG93X3NoYSI6ImZkYmJmZTRkZTNkNDVhMTMxZGU5ZjlhNzJlYWNjYWFhYTlhZGJjNWEiLCJlbnZpcm9ubWVudCI6ImRldmVsb3AiLCJlbnZpcm9ubWVudF9ub2RlX2lkIjoiRU5fa3dET0p1bTJTODVCazJZRiIsImpvYl93b3JrZmxvd19yZWYiOiJzcHNkZXZvcHMvd2ViaW5hcl90ZXN0X2Rlc3BsaWVndWUvLmdpdGh1Yi93b3JrZmxvd3MvcmV1c2FibGVfZGVwbG95LnltbEByZWZzL2hlYWRzL21haW4iLCJqb2Jfd29ya2Zsb3dfc2hhIjoiZmRiYmZlNGRlM2Q0NWExMzFkZTlmOWE3MmVhY2NhYWFhOWFkYmM1YSIsInJ1bm5lcl9lbnZpcm9ubWVudCI6ImdpdGh1Yi1ob3N0ZWQiLCJpc3MiOiJodHRwczovL3Rva2VuLmFjdGlvbnMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwibmJmIjoxNjkwODQyMDE3LCJleHAiOjE2OTA4NDI5MTcsImlhdCI6MTY5MDg0MjYxN30.voFseMMwh6gHEk9cpB7O4qPckKmQZGvTDrXXFtXwil18rRaFKgy2240CynUE8Z_zmIV9BBdklx-P8LlZURki4VVFDp9CUYF9r4q2eLTBbICy6bCOEerP_OSdPr-kk35RJ8E7KBfgKXsjjIFlHDiw23X6J7u9Ny5POTuDvhoFjq86a8Fs-KGZGwcfEAPOUv_nTFZY0AMKbXhLmurCnYuAO_4-6ZFu4ukhN_TYvRjjbMYWAMwOsIHMVmtE3XKZtnTVQq4Q-nrzEjWjYe5ZkTdUQDDcRSSWtXw370Jf_yRWnRqXHCYvNhAKoaQycyiI-pYu89ifWEuFv13nE0rrBNxmdg"

def lambda_handler(event, context):
  print(event)
  print("\n")
  print(context)
  # Endpoints OIDC Configuración
  openid_configuration = "https://" + openid_domain + "/.well-known/openid-configuration"
  
  openid_configuration = requests.get(openid_configuration)
  
  JSON = openid_configuration.json()
  
  # Endpoint OIDC llaves públicas
  #print(JSON['jwks_uri'])
  JWKS = requests.get(JSON['jwks_uri'])
  JWKS_JSON = JWKS.json()['keys']
  #print(JWKS_JSON)
  
  # Separar token
  token_separado = token_jwt.split(".")
  #print(len(token_separado))
  header = token_separado[0]
  payload = token_separado[1]
  firma = token_separado[2]
  
  #print(header)
  #header_bytes = header.encode('utf-8')
  header_texto = base64.urlsafe_b64decode(header + "==")
  #print(str(header_texto, "utf-8"))
  header_dict = json.loads(str(header_texto, "utf-8"))
  alg = header_dict['alg']
  kid = header_dict['kid']
  #print(header_dict)
  
  llave_publica = ''
  
  for objeto in JWKS_JSON:
    if objeto.get('kid') == kid:
      llave_publica = objeto
      break
    else:
      print("no coincide nada")
      
  hmac_key = llave_publica
  #import base64 f
  #base64_bytes = base64_message.encode('ascii')
  #message_bytes = base64.b64decode(base64_bytes)
  #message = message_bytes.decode('ascii')
  print(hmac_key)
  key = jwk.construct(hmac_key)
  #decoded_sig = base64url_decode(encoded_sig)
  
  return print(key.verify(f"{header}.{payload}".encode("utf-8"), base64url_decode(firma.encode("utf-8"))))

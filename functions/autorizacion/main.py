import requests
import base64
import json
import pprint
from jose import jwk
from jose.utils import base64url_decode

openid_domain = "token.actions.githubusercontent.com"

def lambda_handler(event, context):
  print(event)
  print("\n")
  print(context)
  token_event = json.loads(event)
  token_jwt = token_event['headers']['authorization']
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
      hmac_key = llave_publica
      print(hmac_key)
      key = jwk.construct(hmac_key)
      return {"isAuthorized": key.verify(f"{header}.{payload}".encode("utf-8"), base64url_decode(firma.encode("utf-8")))}
    else:
      print(f"no coincide: {objeto}")
  
  return {"isAuthorized": False}
      
      
      
  
  #import base64 f
  #base64_bytes = base64_message.encode('ascii')
  #message_bytes = base64.b64decode(base64_bytes)
  #message = message_bytes.decode('ascii')
  
  #decoded_sig = base64url_decode(encoded_sig)
  
  

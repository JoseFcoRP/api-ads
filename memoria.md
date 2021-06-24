# Cognito
## Pasos
 - ir al grupo de usuarios y crear uno con usuario user@mail.com y contraseña user01
 - indicar el client_id y el pool_id en el fichero de examples/auth.json
 - ejecutar `aws cognito-idp admin-initiate-auth --cli-input-json file://examples/auth.json` y copiar la sesión de la respuesta.
 - se cambia la contraseña: `aws cognito-idp admin-respond-to-auth-challenge --user-pool-id {pool_id} --client-id {client_id} --challenge-name NEW_PASSWORD_REQUIRED --challenge-responses NEW_PASSWORD=user01,USERNAME=user@mail.com --session {sesion}`
 - para conseguir tokens ejecuta `aws cognito-idp admin-initiate-auth --cli-input-json file://auth.json`


# Plugin
Se ha incorporado el pluggin `serverless-python-requirements` para instalar las dependencia de python

# setup
 - tener awscli instalado y configurado
 - tener serverless en versión 2.46.0
 - tener instalado jq
 - instalar pluggins: `bash install_plugins.sh`
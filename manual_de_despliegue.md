# Prerequisitos
 - tener awscli instalado y configurado
 - tener serverless en versión 2.46.0
 - tener instalado jq
 - instalar pluggins: `bash install_plugins.sh`

# Despliegue
 En la ruta base del directorio ejecutar:
 `serverless deploy`

# Cognito
Se debe acceder al pool de usuarios de cognito a traves de la consola de AWS y crear los usuarios, estos requieren de un email y una contraseña para identificarse.

Para obtener un token de sesión de un usuario se debe ejecutar el script `get_token.sh` con la información del pool de usuarios, el cliente de autenticación, email y contraseña del usuario, de la siguiente forma:

`bash get_token.sh <pool_id> <client_id> <user_mail> <user_pwd>`

Este comando imprime el token del usuario para acceder a la aplicación.
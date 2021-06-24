if [ "$#" -ne 4 ]; then
    echo """Usage:
    bash get_token.sh UserPoolId UserPoolClientId User Password
    """
    exit 1
fi

POOL=$1
CLIENT=$2
USER=$3
PASS=$4 

REQUEST=`aws cognito-idp admin-initiate-auth --user-pool-id $POOL --client-id $CLIENT --auth-flow ADMIN_NO_SRP_AUTH --auth-parameters USERNAME=$USER,PASSWORD=$PASS`
SESION=`echo $REQUEST | jq -r .Session`
TOKEN=`echo $REQUEST | jq -r .AuthenticationResult.IdToken`
if [ $SESION == 'null' ]
then
    echo $TOKEN
else
    aws cognito-idp admin-respond-to-auth-challenge --user-pool-id $POOL --client-id $CLIENT --challenge-name NEW_PASSWORD_REQUIRED --challenge-responses NEW_PASSWORD=$PASS,USERNAME=$USER --session $SESION > /dev/null 2>&1
    TOKEN=`aws cognito-idp admin-initiate-auth --user-pool-id $POOL --client-id $CLIENT --auth-flow ADMIN_NO_SRP_AUTH --auth-parameters USERNAME=$USER,PASSWORD=$PASS | jq -r .AuthenticationResult.IdToken`
    echo $TOKEN
fi
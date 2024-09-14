import jwt from 'jsonwebtoken';

const secretKey = 'mi-clave-secreta'; // Usa la misma clave secreta que en la función de login

export const handler = async (event) => {
    console.log("Token recibido: ", event.authorizationToken);
    const token = event.authorizationToken.replace('Bearer ', '');

    try {
        // Decodificar el token JWT usando la clave secreta
        const decoded = jwt.verify(token, secretKey);
        console.log("Token decodificado: ", decoded);

        // Si el token es válido, permitir el acceso
        return generatePolicy(decoded.username, 'Allow', event.methodArn);
    } catch (err) {
        console.log("Error al verificar el token: ", err);
        // Si el token no es válido, denegar el acceso
        return generatePolicy('user', 'Deny', event.methodArn);
    }
};

// Función para generar la política de acceso
const generatePolicy = (principalId, effect, resource) => {
    const authResponse = {};
    authResponse.principalId = principalId;

    if (effect && resource) {
        const policyDocument = {
            Version: '2012-10-17',
            Statement: [{
                Action: 'execute-api:Invoke',
                Effect: effect,
                Resource: resource
            }]
        };
        authResponse.policyDocument = policyDocument;
    }

    return authResponse;
};

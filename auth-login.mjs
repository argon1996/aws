import jwt from 'jsonwebtoken'; // Importar el paquete jsonwebtoken

const secretKey = 'mi-clave-secreta'; // Cambia esta clave secreta

export const handler = async (event) => {
    // Asegúrate de manejar las solicitudes OPTIONS (preflight)
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            body: JSON.stringify({}),
        };
    }

    const { username, password } = JSON.parse(event.body);

    // Simular validación de credenciales (en producción, debes usar una base de datos o un servicio de autenticación)
    if (username === 'admin' && password === '1234') {
        // Generar un token JWT
        const token = jwt.sign({ username: 'admin' }, secretKey, { expiresIn: '1h' });

        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*', // Asegúrate de configurar correctamente el origen
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            body: JSON.stringify({
                message: 'Inicio de sesión exitoso',
                token: token
            }),
        };
    } else {
        return {
            statusCode: 401,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            body: JSON.stringify({
                message: 'Credenciales incorrectas'
            }),
        };
    }
};

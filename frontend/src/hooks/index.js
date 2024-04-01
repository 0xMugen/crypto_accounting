// src/hooks.js
import cookie from 'cookie';
import fetch from 'node-fetch';

export async function handle({ request, resolve }) {
    const cookies = cookie.parse(request.headers.cookie || '');
    request.locals.user = cookies.user;

    const response = await resolve(request);

    return {
        ...response,
        headers: {
            ...response.headers,
            'Set-Cookie': `user=${request.locals.user || ''}; Path=/; HttpOnly`
        }
    };
}

export async function getSession(request) {
    return {
        user: request.locals.user
    };
}

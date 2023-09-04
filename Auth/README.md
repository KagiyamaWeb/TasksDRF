# Authentication and Authorization:

## Creating JWT Token

The project uses rest_framework_simplejwt for auth:

* [JWT Endpoints](https://djoser.readthedocs.io/en/latest/jwt_endpoints.html)


* POST /auth/jwt/create to create token:
```json
{
        "username": "username",
        "password": "password",
}
```

* POST /auth/jwt/refresh to refresh token
# 🔐 Microservicio de Autenticación

Microservicio encargado de la gestión segura de autenticación utilizando JWT y Refresh Tokens. Averiguar est

---

## 📋 Especificación Técnica

### Tecnologías Principales

| Componente       | Tecnología             |
|------------------|-----------------------|
| **Lenguaje**     | Java 17               |
| **Framework**    | Spring Boot 3.2       |
| **Seguridad**    | Spring Security + JWT |
| **Base de Datos**| PostgreSQL            |
| **Tokens**       | JWT Library           |

---

## 🌐 Endpoints

### 1. Login

- **Endpoint:** `POST /auth/login`
- **Propósito:** Autenticar usuarios y generar tokens de acceso y refresh. Se debe consultar al microservicio de Usuarios para obtener el rol y crear el token correspondiente.

**Request:**
```json
{
  "email": "usuario@escuela.edu.pe",
  "password": "contraseña123"
}
```

**Response:**
```json
{
  "email": "usuario@escuela.edu.pe",
  "token": "jwt_token",
  "rol": "Student"
}
```

---

### 2. Validar Token

- **Endpoint:** `POST /auth/validate`
- **Propósito:** Validar el token de acceso. Si es válido, retorna el estado de autenticación y el email.

**Request:**
```json
{
  "email": "usuario@escuela.edu.pe",
  "rol": "Student"
}
```

**Response:**
```json
{
  "autenticado": true,
  "email": "usuario@escuela.edu.pe"
}
```

---

### 3. Logout

- **Endpoint:** `POST /auth/logout`
- **Propósito:** Invalidar el token de acceso y refresh. Se recomienda eliminar el refresh token del almacenamiento.

**Request:**
```json
{
  "email": "usuario@escuela.edu.pe",
  "token": "jwt_token",
  "rol": "Student"
}
```

**Response:**
```json
{
  "mensaje": "Sesión cerrada correctamente"
}
```

---

## ⚠️ Notas

- Verifica la configuración de CORS para permitir solicitudes desde los orígenes necesarios.
- Asegúrate de manejar los refresh tokens de forma segura.
- El microservicio de Usuarios debe ser consultado para obtener el rol del usuario durante el login.

---
# 👥 Microservicio de Usuarios y Salón

## 📖 Descripción

Microservicio encargado de la gestión de usuarios (profesores, alumnos, administradores) y la administración de salones.

---

## 🗂️ Entidades

### `User`
- `id` (UUID)
- `username` (String, único)
- `password_hash` (String)
- `role` (Enum: "teacher" | "student" | "admin")
- `created_at` (Timestamp)

### `Alumno`
- Hereda de `User`
- `seccion` (String)
- `dni` (String, único)

### `Profesor`
- Hereda de `User`
- (Agregar campos específicos si es necesario)

### `Admin`
- Hereda de `User`
- (Agregar campos específicos si es necesario)

### `Salon`
- `id` (UUID)
- `seccion` (String)
- `grado` (String)
- `turno` (String)
- `profesor_id` (UUID)

**Relaciones:**
- Un salón tiene muchos alumnos y un alumno solo está en un salón.
- Un profesor puede estar en muchos salones.

---

## 🌐 Endpoints

| Método | Ruta                    | Descripción                                 |
|--------|-------------------------|---------------------------------------------|
| POST   | /auth/register          | Registro general de usuarios                |
| POST   | /profesor/register      | Registrar profesor                          |
| POST   | /alumno/register        | Registrar alumno individualmente            |
| POST   | /admin/register         | Registrar administrador                     |
| GET    | /user/profile           | Obtener perfil del usuario autenticado      |
| POST   | /alumno/register-bulk   | Registrar alumnos por archivo CSV/Excel     |
| GET    | /alumnos/seccion/{id}   | Obtener todos los alumnos de una sección    |
| DELETE | /seccion/{id}           | Eliminar una sección                        |
| GET    | /salones/{profesor_id}  | Listar todos los salones de un profesor     |
| POST   | /salon                  | Crear un nuevo salón                        |
| PUT    | /salon/{id}             | Actualizar información de un salón          |
| DELETE | /salon/{id}             | Eliminar un salón                           |

---

### Ejemplos de Requests y Responses

#### Registrar Alumno

**POST /alumno/register**

**Request:**
```json
{
  "username": "alumno1",
  "password": "contraseña123",
  "dni": "12345678",
  "seccion": "A",
  "role": "student"
}
```

**Response:**
```json
{
  "id": "uuid-generado",
  "username": "alumno1",
  "seccion": "A",
  "role": "student",
  "created_at": "2024-05-29T12:00:00Z"
}
```

---

#### Obtener Alumnos de una Sección

**GET /alumnos/seccion/{id}**

**Response:**
```json
[
  {
    "id": "uuid-alumno1",
    "username": "alumno1",
    "dni": "12345678",
    "seccion": "A"
  },
  {
    "id": "uuid-alumno2",
    "username": "alumno2",
    "dni": "87654321",
    "seccion": "A"
  }
]
```

---

#### Registrar Alumnos por Archivo

**POST /alumno/register-bulk**

**Request:**  
Archivo CSV/Excel adjunto con los datos de los alumnos.

**Response:**
```json
{
  "mensaje": "Alumnos registrados correctamente",
  "total_registrados": 25
}
```

---

#### Eliminar una Sección

**DELETE /seccion/{id}**

**Response:**
```json
{
  "mensaje": "Sección eliminada correctamente"
}
```

---

## ⚙️ Tecnologías

- Java 17 o Python 3.x (según preferencia del equipo)
- Spring Boot / Django / FastAPI
- PostgreSQL

---

## 📝 Notas

- Manejo adecuado de errores y códigos de estado HTTP.
- Validación de datos en cada endpoint.
- Seguridad y autenticación recomendadas para todas las rutas sensibles.
- Documentar los endpoints con Swagger/OpenAPI si es posible.
- Agregar mas endpoinds segun su criterio revisar el readme principal

---
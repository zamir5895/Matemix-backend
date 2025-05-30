# 📊 Microservicio de Estadísticas y Recomendaciones

## 📖 Descripción

Microservicio encargado de analizar el progreso académico de cada estudiante, generar reportes de avance y brindar consejos personalizados sobre cómo mejorar su desempeño. Utiliza IA para sugerencias inteligentes y recomendaciones adaptadas a cada alumno.

---



## 🗂️ Entidades

### StudentProgress
- `id` (UUID)
- `alumno_id` (UUID)
- `ejercicios_resueltos` (Integer)
- `correctos` (Integer)
- `incorrectos` (Integer)
- `porcentaje_acierto` (Float)
- `temas_destacados` (Array<String>)
- `temas_a_mejorar` (Array<String>)
- `fecha_actualizacion` (Timestamp)

### StudentAdvice
- `id` (UUID)
- `alumno_id` (UUID)
- `consejo` (String)
- `fecha_generado` (Timestamp)

### ClassroomReport
- `id` (UUID)
- `salon_id` (UUID)
- `fecha_generado` (Timestamp)
- `resumen_general` (String)
- `progreso_estudiantes` (Array<StudentProgress>)
- `consejos_generales` (Array<String>)

---

## 🌐 Endpoints

| Método | Ruta                                  | Descripción                                                        |
|--------|---------------------------------------|--------------------------------------------------------------------|
| GET    | /progress/alumno/{alumno_id}          | Obtener avance y progreso detallado de un alumno                   |
| GET    | /advice/alumno/{alumno_id}            | Obtener consejos personalizados para un alumno                     |
| POST   | /advice/alumno/{alumno_id}            | Generar (o regenerar) consejos personalizados vía IA               |
| GET    | /report/salon/{salon_id}              | Obtener reporte de avance de todos los estudiantes de un salón     |
| POST   | /report/salon/{salon_id}/generate     | Generar y guardar reporte de avance para un salón                  |
| GET    | /health                              | Endpoint de salud del microservicio                                |

---

## 📝 Ejemplos de Requests y Responses

### Obtener Progreso de un Alumno

**GET /progress/alumno/{alumno_id}**
```json
{
  "alumno_id": "uuid-alumno",
  "ejercicios_resueltos": 50,
  "correctos": 40,
  "incorrectos": 10,
  "porcentaje_acierto": 80.0,
  "temas_destacados": ["Suma", "Resta"],
  "temas_a_mejorar": ["Multiplicación", "División"],
  "fecha_actualizacion": "2024-05-29T12:00:00Z"
}
```

---

### Obtener Consejos Personalizados

**GET /advice/alumno/{alumno_id}**
```json
{
  "alumno_id": "uuid-alumno",
  "consejo": "Te recomendamos repasar ejercicios de multiplicación y división. Intenta practicar con problemas de dificultad media para mejorar tu precisión.",
  "fecha_generado": "2024-05-29T12:00:00Z"
}
```

---

### Generar Consejos vía IA

**POST /advice/alumno/{alumno_id}**
```json
{
  "temas_a_mejorar": ["Multiplicación", "División"],
  "porcentaje_acierto": 80.0
}
```
**Response:**
```json
{
  "consejo": "Para mejorar en multiplicación y división, dedica 15 minutos diarios a practicar problemas variados. Utiliza recursos visuales y juegos interactivos para reforzar estos conceptos."
}
```

---

### Reporte de Avance de un Salón

**GET /report/salon/{salon_id}**
```json
{
  "salon_id": "id_salon",
  "fecha_generado": "2024-05-29T12:00:00Z",
  "resumen_general": "El salón muestra un avance promedio del 78%. La mayoría destaca en sumas y restas, pero debe reforzar multiplicación.",
  "progreso_estudiantes": [
    {
      "alumno_id": "uuid-alumno1",
      "ejercicios_resueltos": 50,
      "correctos": 40,
      "porcentaje_acierto": 80.0
    },
    {
      "alumno_id": "uuid-alumno2",
      "ejercicios_resueltos": 45,
      "correctos": 35,
      "porcentaje_acierto": 77.8
    }
  ],
  "consejos_generales": [
    "Dedicar más tiempo a ejercicios de multiplicación.",
    "Fomentar la participación en clase con juegos matemáticos."
  ]
}
```

---

## 📝 Notas

- Los consejos se generan automáticamente usando IA, considerando el desempeño y los temas a mejorar de cada alumno.
- Los reportes pueden ser exportados a PDF o visualizados en el frontend.
- Se recomienda proteger los endpoints con autenticación y roles.

---

## ⚙️ Tecnologías

- **Lenguaje:** Python 3.x
- **Framework:** Fast API
- **Base de Datos:** MongoDB
- **IA:** OpenAI API u otro modelo de lenguaje para generación de consejos

---

## 🚀 Ejecución

1. Clona el repositorio.
2. Instala dependencias:  
   `pip install -r requirements.txt`
3. Configura las variables de entorno para la base de datos y la API de IA.
4. Usar fast api y python para correr todo
5. usa requirments.txt y documentar todo

---

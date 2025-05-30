# 🎓 ContentForProfessor Microservicio

## 📝 Descripción

Microservicio diseñado para asistir a profesores en la preparación de clases, búsqueda de recursos educativos, generación de descripciones y procesamiento de materiales didácticos. Integra IA para automatizar tareas y mejorar la experiencia docente.

---

## 🗂️ Entidades

### `VideoRecomendado`
- `id` (UUID)
- `titulo` (String)
- `url` (String)
- `subtema_id` (UUID)
- `descripcion` (String)
- `fecha_busqueda` (Timestamp)



## 🌐 Endpoints

| Método | Ruta                                         | Descripción                                                        |
|--------|----------------------------------------------|--------------------------------------------------------------------|
| GET    | /youtube/search/subtema/{subtema_id}         | Buscar videos en YouTube relacionados a un subtema.                |
| POST   | /youtube/prompt                              | Generar prompt para búsqueda en YouTube a partir de un subtema.    |
| GET    | /temas/{tema_id}/subtemas                    | Generar/listar subtemas dado un tema.                              |
| POST   | /temas/{tema_id}/descripcion                 | Generar descripción automática de un tema.                         |
| POST   | /subtemas/{subtema_id}/descripcion           | Generar descripción automática de un subtema.                      |
| POST   | /pdf/parse                                   | Parsear PDF, devolver ejercicios en JSON y clasificarlos por dificultad. |
| POST   | /pdf/ejercicios/save                         | Guardar ejercicios modificados extraídos de un PDF.                |
| GET    | /pdf/parse/result/{id}                       | Obtener resultado del parseo de un PDF por ID.                     |
| GET    | /videos/recomendados/subtema/{subtema_id}    | Listar videos recomendados para un subtema.                        |
| POST   | /videos/recomendados                         | Guardar video recomendado manualmente.                             |
| PUT    | /temas/{tema_id}                            | Actualizar información de un tema.                                 |
| DELETE | /temas/{tema_id}                            | Eliminar un tema.                                                  |
| PUT    | /subtemas/{subtema_id}                      | Actualizar informacion del video de youtube.                              |
| GET    | /health                                     | Endpoint de salud del servicio.                                    |

---

### Ejemplos de Requests y Responses

#### Buscar Videos en YouTube por Subtema

**GET /youtube/search/subtema/{subtema_id}**

**Response:**
```json
[
  {
    "id": "uuid-video",
    "titulo": "Introducción a Derivadas",
    "url": "https://youtube.com/...",
    "descripcion": "Video explicativo sobre derivadas.",
    "subtema_id": "uuid-subtema"
  }
]
```

---

#### Generar Prompt para YouTube

**POST /youtube/prompt**
```json
{
  "subtema": "Integrales definidas"
}
```
**Response:**
```json
{
  "prompt": "Videos educativos sobre integrales definidas para secundaria"
}
```

---

#### Parsear PDF y Clasificar Ejercicios

**POST /pdf/parse**  
Archivo PDF adjunto.

**Response:**
```json
{
  "id": "uuid-parse-result",
  "ejercicios": [
    {
      "pregunta": "¿Cuánto es 2+2?",
      "opciones": ["2", "3", "4", "5"],
      "respuesta_correcta": "4",
      "dificultad": "facil"
    }
  ]
}
```

---

#### Guardar Ejercicios Modificados del PDF

**POST /pdf/ejercicios/save**
```json
{
  "parse_result_id": "uuid-parse-result",
  "ejercicios": [
    {
      "pregunta": "¿Cuánto es 2+2?",
      "opciones": ["2", "3", "4", "5"],
      "respuesta_correcta": "4",
      "dificultad": "facil"
    }
  ]
}
```
**Response:**
```json
{
  "mensaje": "Ejercicios guardados correctamente en MongoDB"
}
```

---

## ⚙️ Tecnologías

- Python 3.x + FastAPI
- MongoDB
- Integración con API de YouTube y OpenAI

---

## 📝 Notas

- Todos los endpoints que modifican datos requieren autenticación.
- Los ejercicios extraídos de PDF se almacenan en MongoDB.
- Se recomienda documentar los endpoints con Swagger/OpenAPI.
- El microservicio puede integrarse con otros servicios para enriquecer la experiencia docente.

---
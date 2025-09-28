# Proyecto Inmobiliario

Plataforma web para la **gestión de arriendos de propiedades** que conecta arrendadores con arrendatarios. Permite publicar inmuebles, gestionar solicitudes y administrar el ciclo completo de arriendo de manera centralizada.

---

## 🚀 Características principales

* **Registro y autenticación de usuarios**: permite crear cuentas de arrendadores y arrendatarios.
* **Formularios personalizados de registro**: no requieren username; el sistema genera automáticamente un username que luego puede ser actualizado en la sección de perfil junto con otros datos.
* **Formulario de login personalizado**: se realiza usando el correo electrónico en lugar del username.
* **Publicación y gestión de propiedades inmobiliarias**: solo los arrendadores pueden publicar y administrar sus inmuebles.

  * Al crear una propiedad se utiliza un formulario que requiere los datos del inmueble y la carga de imágenes y documentos que acrediten el dominio de la propiedad.
* **Visualización del catálogo de propiedades**: los arrendatarios pueden explorar todas las propiedades disponibles y enviar solicitudes, mientras que los arrendadores pueden revisar sus propiedades y el estado de arriendo.
* **Sistema de solicitudes de arriendo**:

  * El arrendatario puede enviar solicitudes de arriendo.
  * El arrendador puede aceptar o rechazar solicitudes.
  * Al enviar una solicitud, se debe llenar un formulario y adjuntar documentos que acrediten solvencia económica (contrato de trabajo, liquidaciones de sueldo, historial de cotizaciones, etc.).
* **Disponibilidad de inmuebles**: solo se muestran propiedades con el campo `Arrendado=False`. Cuando se aprueba una solicitud de arriendo, este campo se actualiza a `True` y la propiedad deja de mostrarse en la plataforma.
* **Panel de administración y perfiles**:

  * Ambos tipos de usuarios (arrendatario y arrendador) tienen su propio panel de perfil para actualizar datos personales.
  * Funcionalidades exclusivas según tipo de usuario:

    * El arrendatario puede revisar las solicitudes que ha realizado y su estado.
    * El arrendador puede gestionar sus inmuebles y revisar las solicitudes recibidas.

---

## 🛠️ Tecnologías utilizadas

* **Backend:** Django (Python)
* **Base de datos:** PostgreSQL
* **Visualizacion y administración DB:** PGAdmin
* **Frontend:** Bootstrap, Jinja2, HTML, CSS, JS
* **Contenedores:** Docker & Docker Compose
* **Control de versiones:** Git & GitHub

---

## 📂 Estructura del proyecto

```
proyecto-inmobiliario/
├── backend/
│   ├── dockerfile
│   ├── manage.py
│   ├── proyecto/        # Configuración principal de Django
│   ├── portal/          # App para gestión de inmuebles y solicitudes
│   ├── users/           # App para gestión de usuarios y perfiles
│   ├── templates/       # Plantillas HTML
│   ├── static/          # Archivos estáticos (CSS, JS, imágenes)
│   └── requirements.txt # Dependencias del backend
├── docker-compose.yml   # Orquestación con Docker
└── README.md            # Documentación
```

---

## ⚙️ Instalación y configuración

La forma recomendada de correr este proyecto es mediante **Docker Compose**. No es necesario crear entornos virtuales manualmente.

### 1. Clonar repositorio

```bash
git clone https://github.com/raul-1601/proyecto-inmobiliario.git
cd proyecto-inmobiliario
```

### 2. Configurar archivos `.env`

Debes crear **dos archivos `.env`** en ubicaciones distintas:

📌 En la raíz del proyecto (`.env` para `docker-compose.yml`):

```env
POSTGRES_DB=nombre_base
POSTGRES_USER=usuario
POSTGRES_PASSWORD=contraseña
PGADMIN_DEFAULT_EMAIL=correo@ejemplo.com
PGADMIN_DEFAULT_PASSWORD=contraseña_pgadmin
```

📌 Dentro de `backend/proyecto/.env` (para configuración de Django):

```env
# Genera tu SECRET_KEY aquí: https://djecrety.ir/
SECRET_KEY=tu_clave_secreta
DEBUG=True
```

> ⚠️ Reemplaza los valores con los que prefieras. La `SECRET_KEY` debe ser única y secreta.

### 3. Levantar contenedores

```bash
docker-compose up --build
```

El proyecto quedará disponible en `http://localhost:8000`.

---

## 📖 Uso de la aplicación

1. Crear cuenta como arrendador o arrendatario.
2. Publicar o buscar propiedades.
3. Enviar y gestionar solicitudes de arriendo.
4. Hacer seguimiento de inmuebles arrendados.

---

## 🔮 Mejoras futuras

* Mejoras en la interfaz visual.
* Generación y firma de contratos digitales.
* Notificaciones automáticas por email.
* Gestión avanzada de solicitudes duplicadas.
* Actualización automática de inmuebles disponibles según contratos.
* Dashboard con métricas y reportes.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Para colaborar:

1. Haz un fork del proyecto.
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`).
3. Haz commit de tus cambios (`git commit -m 'Agrega nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

---

## 📜 Licencia

Este proyecto está bajo la licencia **MIT**. Puedes usarlo, modificarlo y distribuirlo libremente, siempre mencionando al autor original.

---

## 👨‍💻 Autor

* Desarrollado por **Raúl Ignacio Ramírez Sanhueza**
* Repositorio secundario: [raul-1601](https://github.com/raul-1601)
* Perfil principal: [raul240sx](https://github.com/raul240sx)

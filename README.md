# Blog
Este es un proyecto de blog personal desarrollado con Python y el framework Django. Permite a los usuarios registrarse, crear perfiles, escribir y gestionar posts y cuenta con un panel de administración para la gestión de contenido.

## Características Principales

* **Autenticación de Usuarios:**
    * Registro de nuevos usuarios (solicitando nombre de usuario, email y contraseña).
    * Inicio de sesión (Login) y Cierre de sesión (Logout).
    * Sistema de mensajería de Django para notificaciones (ej. registro exitoso, error de login).
* **Perfiles de Usuario:**
    * Cada usuario tiene un perfil asociado.
    * Visualización del perfil con datos como: nombre, apellido, email, avatar, biografía, sitio web, fecha de nacimiento.
    * Edición del perfil por parte del usuario propietario.
    * Funcionalidad para cambiar la contraseña.
* **Gestión de Posts (Páginas del Blog):**
    * **Modelo `Post`:**
        * Campos: Título (CharField), Slug (CharField), Autor (ForeignKey a User), Resumen Corto (RichTextUploadingField - CKEditor), Contenido Principal (RichTextUploadingField - CKEditor), Imagen Destacada (ImageField), Fecha de Publicación (DateTimeField), Fecha de Creación (DateTimeField), Última Actualización (DateTimeField), Estado (Borrador/Publicado), Meta Descripción (CharField SEO), Palabras Clave (CharField SEO).
    * **CRUD de Posts:**
        * **Crear Posts:** Los usuarios autenticados pueden crear nuevos posts a través de un formulario que incluye un editor de texto enriquecido (CKEditor) para el contenido y la posibilidad de subir una imagen destacada.
        * **Leer Posts (Listado y Detalle):**
            * Vista de listado de posts (`/pages/`) que muestra todos los posts publicados, con paginación y un campo de búsqueda.
            * Si no hay posts o la búsqueda no arroja resultados, se muestra un mensaje informativo.
            * Vista de detalle para cada post (`/pages/<slug>/`) accesible al hacer clic en "Leer más" o en el título.
        * **Actualizar Posts:** Solo el autor del post (o un administrador) puede editar sus propios posts.
        * **Eliminar Posts:** Solo el autor del post (o un administrador) puede eliminar sus posts, con una página de confirmación.
    * **Manejo de Errores:** Si se intenta acceder a un post que no existe o no está publicado (y el usuario no tiene permisos para verlo), se muestra una página de error 404 personalizada.
* **Navegación y Páginas Estáticas:**
    * **Barra de Navegación (Navbar):** Implementada en la plantilla base (`base.html`) con enlaces a Inicio, Páginas (Blog), Acerca de Mí, y opciones de usuario (Perfil, Login/Logout, Registro) según el estado de autenticación.
    * **Página de Inicio (`/`):** Muestra una bienvenida y los posts más recientes.
    * **Página "Acerca de Mí" (`/about/`):** Página con información sobre el dueño del blog.
* **Panel de Administración de Django (`/admin/`):**
    * Registro de los modelos `Profile` (de la app `accounts`) y `Post` (de la app `blog_app`) para su gestión a través del panel de administración.
* **Diseño y Estructura:**
    * Uso de **herencia de plantillas** con una `base.html` principal.
    * Estilos básicos con Bootstrap y un archivo `custom_styles.css`.
    * Manejo de archivos estáticos y de medios (imágenes subidas por usuarios).
* **Buenas Prácticas de Desarrollo:**
    * Organización del proyecto en aplicaciones (`accounts` para usuarios, `blog_app` para el blog).
    * Uso de **Vistas Basadas en Clases (CBV)** (ej. `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`, `TemplateView`).
    * Uso de **Mixins en CBV** (ej. `LoginRequiredMixin`, `AuthorRequiredMixin` personalizado para control de permisos).
    * Uso de **Decoradores en vistas basadas en funciones** (ej. `@login_required` donde aplique).
    * Formularios de Django para validación y renderizado de campos.
    * Manejo de subida de imágenes para avatares de perfil y posts.
    * Generación automática de `slugs` para los posts.

## Estructura del Proyecto

```
blog_django_project/
├── manage.py
├── blog/                   # Configuración del proyecto
├── accounts/               # App para usuarios y perfiles
├── blog_app/               # App para posts del blog
├── static/                 # Archivos estáticos globales
├── media/                  # Archivos subidos por usuarios
├── templates/              # Plantillas globales
├── .gitignore
└── requirements.txt
```

## Requisitos Previos

* Python (versión 3.8 o superior recomendada)
* pip (gestor de paquetes de Python)
* Git (opcional, para control de versiones)

## Configuración e Instalación

1.  **Clonar el Repositorio (si aplica):**
    ```bash
    git clone https://github.com/Schimizzi/blog_xa_coder.git
    cd blog_libreria
    ```

2.  **Crear y Activar un Entorno Virtual (Recomendado):**
    ```bash
    python -m venv .blog_libreria
    # En Windows:
    #  .\.blog_libreria\Scripts\activate
    ```
    **Si la ejecución de scripts está deshabilitada en tu sistema:**
    ```PowerShell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    ```

3.  **Instalar Dependencias:**
    Asegúrate de tener el archivo `requirements.txt` con las siguientes dependencias (o las versiones que hayas usado):
    ```
    Django>=3.2,<4.3
    Pillow>=9.0.0
    django-ckeditor>=6.0.0
    ```
    Luego, instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar la Base de Datos:**
    El proyecto está configurado para usar SQLite por defecto. La base de datos (`db.sqlite3`) se creará automáticamente. Este archivo está incluido en `.gitignore` y no debe subirse al repositorio.

5.  **Aplicar Migraciones:**
    ```bash
    python manage.py makemigrations accounts blog_app
    python manage.py migrate
    ```

6.  **Crear un Superusuario (Administrador):**
    Esto te permitirá acceder al panel de administración de Django.
    ```bash
    python manage.py createsuperuser
    ```
    Sigue las instrucciones para crear un nombre de usuario, email y contraseña.

7.  **Recolectar Archivos Estáticos (Para Producción):**
    En desarrollo, Django sirve los archivos estáticos automáticamente si `DEBUG=True`. Para producción, necesitarías ejecutar:
    ```bash
    # python manage.py collectstatic # (Asegúrate que STATIC_ROOT esté configurado en settings.py)
    ```
    Por ahora, para desarrollo, esto no es estrictamente necesario.

8.  **Ejecutar el Servidor de Desarrollo:**
    ```bash
    python manage.py runserver
    ```
    La aplicación estará disponible en `http://127.0.0.1:8000/`.
    El panel de administración estará en `http://127.0.0.1:8000/admin/`.

## Uso

* **Navegación General:** Utiliza la barra de navegación para acceder a las secciones de Inicio, Páginas (Blog) y Acerca de Mí.
* **Usuarios:**
    * Regístrate para crear una cuenta.
    * Inicia sesión para acceder a funcionalidades como crear posts y editar tu perfil.
    * Visita tu perfil para ver y actualizar tu información.
* **Posts del Blog:**
    * Los usuarios autenticados pueden crear nuevos posts desde el enlace en la barra de navegación o desde la lista de posts.
    * Los posts se pueden editar o eliminar por sus autores.
    * Utiliza el campo de búsqueda en la sección "Páginas (Blog)" para encontrar posts específicos.
* **Panel de Administración:**
    * Accede a `/admin/` e inicia sesión con tus credenciales de superusuario.
    * Desde aquí puedes gestionar usuarios, perfiles y posts de forma avanzada.

## Archivos Importantes

* `.gitignore`: Especifica los archivos y directorios que deben ser ignorados por Git (ej. `__pycache__`, `db.sqlite3`, `media/`).
* `requirements.txt`: Lista las dependencias de Python del proyecto.
* `settings.py`: Contiene la configuración principal del proyecto Django, incluyendo `INSTALLED_APPS`, `DATABASES`, `STATIC_URL`, `MEDIA_URL`, y configuraciones de CKEditor.
* `media/`: Directorio donde se almacenan los archivos subidos por los usuarios (imágenes de posts, avatares). **Importante:** Este directorio está en `.gitignore` y su contenido no se versiona. En un entorno de producción, se recomienda usar un servicio de almacenamiento de archivos externo (como AWS S3, Google Cloud Storage, etc.).

## Consideraciones Adicionales

* **Seguridad:** Para un entorno de producción, asegúrate de cambiar `DEBUG = False` en `settings.py`, configurar `ALLOWED_HOSTS`, y usar una `SECRET_KEY` fuerte y única.
* **Imágenes por Defecto:** El sistema utiliza imágenes placeholder (ej. para avatares por defecto). Asegúrate de que las rutas a estas imágenes (ej. `media/avatars/default_avatar.png`) sean correctas y que los archivos existan.

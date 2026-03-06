# Business Workflow Manager

Aplicacion web interna construida con Django para centralizar operaciones de una pyme:

- clientes
- trabajos/pedidos
- estados y prioridades
- fechas limite
- notas operativas
- resumen en dashboard

## Stack

- Python
- Django
- SQLite (desarrollo)
- Bootstrap 5 + HTML/CSS

## Funcionalidades

- Autenticacion (`login/logout`) con vistas protegidas.
- Dashboard con metricas clave:
  - total de clientes
  - total de trabajos
  - trabajos pendientes
  - trabajos completados
  - vencimientos proximos
  - distribucion por estado
- CRUD completo de clientes.
- CRUD completo de trabajos/pedidos/tareas.
- Filtros y busqueda en trabajos por:
  - texto
  - estado
  - prioridad
  - cliente
- Exportacion de clientes y trabajos a CSV.
- Paginacion en listados.
- Mensajes de exito/error para feedback de acciones.
- Django admin para gestion rapida.

## Estructura

```text
business-web-app/
  config/
  core/
  clients/
  jobs/
  users/
  templates/
  static/
```

## Puesta en marcha

1. Crear entorno virtual.
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Aplicar migraciones:

```bash
python manage.py migrate
```

4. Crear superusuario:

```bash
python manage.py createsuperuser
```

5. Ejecutar servidor:

```bash
python manage.py runserver
```

6. Ejecutar tests:

```bash
python manage.py test
```

## Credenciales y acceso

- Login: `/users/login/`
- Dashboard: `/dashboard/`
- Admin: `/admin/`

## Notas

- Proyecto pensado como base profesional para portfolio y evolucion real en negocio.
- Para produccion, configurar variables de entorno (`DJANGO_SECRET_KEY`, hosts permitidos, DB, etc).

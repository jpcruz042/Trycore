# Base de datos

PostgreSQL 16 se ejecuta mediante Docker Compose.

## Inicialización

El script `init/001_create_schema.sql` se ejecuta automáticamente la primera vez que se crea el volumen de PostgreSQL.

Para iniciar:

```powershell
Copy-Item .env.example .env
docker compose up -d postgres
```

Para reiniciar completamente la base de datos:

```powershell
docker compose down -v
docker compose up -d postgres
```

La advertencia anterior elimina todos los datos persistidos.

Conexión local disponible en `localhost:5433`.

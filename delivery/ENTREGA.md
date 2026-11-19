# Lista de entrega

Incluya en el envío:

1. `Trycore-EVM-Entrega.zip`.
2. `Trycore-EVM-Entrega.zip.sha256` para verificar integridad.
3. El video explicativo máximo de diez minutos.

## Contenido del paquete

- PostgreSQL inicializado mediante Docker Compose.
- Backend FastAPI con endpoints CRUD y cálculos EVM.
- Frontend Angular moderno.
- Datos de demostración con proyecto y tres actividades.
- Pruebas unitarias e integración.
- README con instrucciones de instalación y ejecución.
- AI_PROCESS.md con prompts y decisiones técnicas.

## Verificación antes de enviar

```powershell
Get-FileHash .\Trycore-EVM-Entrega.zip -Algorithm SHA256
```

El resultado debe coincidir con el archivo `Trycore-EVM-Entrega.zip.sha256`.

## Inicio rápido del proyecto recibido

```powershell
Copy-Item .env.example .env
docker compose down -v
docker compose up -d --build
```

Luego abra:

- Frontend: http://localhost:4200
- Swagger: http://localhost:8001/docs

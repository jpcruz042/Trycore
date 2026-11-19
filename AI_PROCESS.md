# AI Process

Este archivo documentará el proceso completo de desarrollo asistido por IA.

## Estado inicial

- Fecha: 18 de noviembre de 2026.
- Herramientas de IA: GitHub Copilot.
- Objetivo actual: levantar la base de datos PostgreSQL y preparar la estructura inicial del proyecto.

## Prompts enviados en orden cronológico

### 1

`Lee y analisa el documento alojado en la carpeta raiz que tenemos abierta llamada Trycore. Como observaras tenemos que realizar una pequeña aplicación web para administrar proyectos y sus respectivos tiempos de desarrollo e indicadores de valor. Ahora bien, quiero establecer una arquitectura que ya tengo en mente. La base de datos la vamos a crear con Postgresql con un contenedor de Docker. Ya tenemos instalado esto en el PC. Para el back usaremos Python y la libreria FastAPI y por ultimo para el front usaremos Angular por facilidad Analisa el texto antes de emepzar con la creación de todo`

### 2

`Perfecto, iniciemos entonces. Propongo crear primero la base de datos. Realiza los procedimientos necesarios para crear el contenedor, las tablas necesarias y las carpetas y archivos obligatorios para que le proyecto funcione`

## Decisiones técnicas iniciales

- Usar PostgreSQL 16 dentro de Docker para garantizar un entorno reproducible.
- Usar `NUMERIC(14, 2)` para dinero y `NUMERIC(5, 2)` para porcentajes, evitando cálculos con valores de punto flotante.
- Exponer PostgreSQL en `localhost:5433` porque el puerto `5432` ya está ocupado por otro contenedor local.
- Usar UUID como identificador para evitar revelar secuencias numéricas y facilitar integración futura.
- Separar proyectos y actividades con eliminación en cascada.

## Pendientes obligatorios

- Herramientas utilizadas y justificación de su elección.
- Prompts enviados, copiados textualmente y en orden cronológico.
- Aprendizaje y validación de fórmulas EVM.
- Dos decisiones que no siguieron la recomendación de la IA.
- Verificación de los cálculos con ejemplos conocidos.
- Una decisión de arquitectura independiente.
- Reflexión honesta sobre cambios que haría al repetir el ejercicio.

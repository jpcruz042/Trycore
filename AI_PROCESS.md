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

### 3

`Perfecto, ahora necesitamos crear el contenedor para el back. Antes de iniciar con la creación de la API y los EndPoint necesitamos crear el contenedor del back`

### 4

`Perfecto, ahora crea los endpoint necesarios para todas las transacciones que requiere el proceso. Despues de crearlas realizar peticiones para probar cada una de las trnasacciones creadas`

### 5

`Excelente, ahora implementemos el front para poder interactuar con todo. Quiero un diseñor ligero pero contemporaneo, algo amigable y con colores profesionales y agradables`

### 6

`Vale, organiza todo para que quede listo para entregar el proyecto. Creo que vamos a tener que dejar por fuera el tema de Github por temas de tiempo pero todo lo demas lo podemos entregar. Realizar las configuraciones faltantes para comprimir el proyecto y enviarlo. No olvides adecuar el README de acuerdo con lo requerido para probar la aplicación`

## Herramientas utilizadas

- GitHub Copilot se utilizó dentro de VS Code para analizar el documento, generar estructura, modificar archivos y ejecutar validaciones.
- Docker Desktop y Docker Compose se utilizaron para levantar PostgreSQL, FastAPI y Angular.
- PostgreSQL se utilizó para validar el esquema real y las restricciones.
- PowerShell se utilizó para ejecutar servicios, pruebas HTTP y generar el paquete de entrega.
- Pytest se utilizó para validar los cálculos EVM y el contrato HTTP.

## Aprendizaje y validación de EVM

Aprendí EVM comparando las fórmulas del documento con ejemplos calculados antes de implementar el código:

- PV = porcentaje planificado × BAC.
- EV = porcentaje real × BAC.
- CV = EV − AC.
- SV = EV − PV.
- CPI = EV / AC.
- SPI = EV / PV.
- EAC = BAC / CPI.
- VAC = BAC − EAC.

Una prueba manual fue BAC = 10.000.000, progreso planificado y real = 50%, y AC = 6.000.000:

- PV = 5.000.000.
- EV = 5.000.000.
- CV = -1.000.000.
- SV = 0.
- CPI = 0.8333.
- SPI = 1.
- EAC = 12.000.000.
- VAC = -2.000.000.

Esta prueba confirmó que el proyecto puede estar dentro del cronograma pero sobre presupuesto.

Antes de considerar correcta la implementación, ejecuté pruebas unitarias para AC cero, PV cero, avance real cero, ausencia de actividades y consolidación de varias actividades. Los índices se dejaron como nulos cuando la división no tiene sentido.

## Decisiones que no seguí exactamente como sugirió la IA

1. PostgreSQL habría podido usar el puerto estándar 5432, pero adopté 5433 porque ese puerto ya estaba ocupado por otro contenedor local. Esta decisión evitó cambiar o detener servicios ajenos.
2. La IA sugirió usar el CPI redondeado para calcular EAC. Preferí conservar el CPI exacto internamente y redondearlo solamente para mostrarlo, evitando que el valor visual introdujera un error adicional en el pronóstico.

## Decisión independiente de arquitectura

Separé el backend en controladores, esquemas, modelos, persistencia y servicio EVM. La decisión fue independiente: mantener la lógica de cálculo fuera de los endpoints facilita leerla, probarla y reutilizarla.

## Reflexión

Si repitiera el ejercicio, empezaría por crear pruebas EVM antes de los endpoints. También automatizaría más pronto la integración completa y registraría cada decisión técnica mientras se trabaja, en lugar de completar algunos registros al final.

## Decisiones técnicas iniciales

- Usar PostgreSQL 16 dentro de Docker para garantizar un entorno reproducible.
- Usar `NUMERIC(14, 2)` para dinero y `NUMERIC(5, 2)` para porcentajes, evitando cálculos con valores de punto flotante.
- Exponer PostgreSQL en `localhost:5433` porque el puerto `5432` ya está ocupado por otro contenedor local.
- Exponer el backend en `localhost:8001` porque el puerto `8000` ya está ocupado por otro contenedor local.
- Usar UUID como identificador para evitar revelar secuencias numéricas y facilitar integración futura.
- Separar proyectos y actividades con eliminación en cascada.

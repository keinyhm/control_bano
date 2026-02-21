#  Módulo Odoo -- Control de uso del baño

##  Asignatura

Sistemas de Gestión Empresarial

##  Autora

Keiny Herrera Martínez

------------------------------------------------------------------------

## Descripción del proyecto

Este proyecto consiste en el desarrollo de un módulo personalizado para
Odoo 17 denominado **control_bano**, cuyo objetivo es digitalizar y
gestionar el registro de salidas del alumnado al baño dentro de un
centro educativo.

El módulo permite:

-   Registrar nombre del alumno.
-   Clasificar por etapa, curso, grupo e itinerario.
-   Controlar fecha y hora de salida y vuelta.
-   Gestionar estados (Borrador → En curso → Finalizada / Cancelada).
-   Bloquear edición tras finalización.
-   Generar estadísticas gráficas por duración.
-   Importar registros mediante archivo CSV.
-   Generar informes PDF.
-   Ejecutar acciones de servidor para finalizar registros masivamente.

------------------------------------------------------------------------

## Arquitectura del módulo

El módulo sigue la estructura estándar recomendada por Odoo:

-   **manifest**.py
-   models/
-   views/
-   security/
-   reports/

Incluye: - Modelo principal: control_bano.visit - Vistas tree, form y
search - Vista gráfica y pivot - Informe PDF - Acción de servidor
personalizada

------------------------------------------------------------------------

## Pruebas funcionales

Se realizaron pruebas estructuradas que verifican:

-   Creación y edición de registros.
-   Transición correcta de estados.
-   Bloqueo de edición tras finalización.
-   Funcionamiento de filtros y búsquedas.
-   Generación de estadísticas.
-   Integración mediante CSV.
-   Generación de informe PDF.
-   Acción de servidor funcional.

Todas las pruebas resultaron correctas sin errores críticos.

------------------------------------------------------------------------

## Metodología

El desarrollo se realizó siguiendo un enfoque incremental basado en
metodología tipo Kanban.

Fases principales:

1.  Diseño del modelo de datos.
2.  Implementación de vistas.
3.  Desarrollo del flujo de estados.
4.  Creación del dashboard.
5.  Integración e informes.
6.  Acciones de servidor.
7.  Documentación y control de versiones.

El seguimiento se realizó mediante tablero Kanban en Trello.

------------------------------------------------------------------------

## Control de versiones

Se utilizó Git como sistema de control de versiones, registrando commits
progresivos que documentan mejoras, correcciones e implementación de
nuevas funcionalidades.

------------------------------------------------------------------------

## Demostración funcional

Se incluye un vídeo demostrativo donde se prueba el funcionamiento
completo del módulo en Odoo 17:

-   Creación de registros.
-   Flujo completo de estados.
-   Estadísticas.
-   Importación CSV.
-   Generación de informe PDF.
-   Acción de servidor.

------------------------------------------------------------------------

## Estado del proyecto

✔ Módulo funcional\
✔ Sin errores críticos\
✔ Documentación técnica incluida\
✔ Testing formal realizado\
✔ Integración externa implementada

------------------------------------------------------------------------

Este proyecto demuestra la aplicación práctica de desarrollo modular en
Odoo 17, integrando arquitectura, ORM, interfaces, integración externa y
control de versiones.

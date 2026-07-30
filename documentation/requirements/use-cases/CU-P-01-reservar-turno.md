<a id="indice"></a>

# CU-P-01 — Reservar Turno

## Índice

- [1. Información General](#1-información-general)
- [2. Descripción](#2-descripción)
- [3. Evento Desencadenante](#3-evento-desencadenante)
- [4. Precondiciones](#4-precondiciones)
- [5. Suposiciones](#5-suposiciones)
- [6. Flujo Principal](#6-flujo-principal)
- [7. Reglas de Negocio](#7-reglas-de-negocio)
- [8. Postcondiciones](#8-postcondiciones)
- [9. Cuestiones Pendientes](#9-cuestiones-pendientes)
- [10. Escenarios Alternativos](#10-escenarios-alternativos)

---

<a id="1-información-general"></a>

# 1. Información General

| Campo | Descripción |
|-------|-------------|
| **Nombre** | Reservar Turno |
| **ID** | CU-P-01 |
| **Actor Principal** | Paciente |
| **Actores Secundarios** | Sistema, Doctores |
| **Tipo de Evento** | Normal |

---

<a id="2-descripción"></a>

# 2. Descripción

Permite que un paciente autenticado reserve una cita médica (`Appointment`) seleccionando un profesional (`Doctor`), una fecha y un horario disponible dentro de la agenda publicada por dicho profesional.

Durante el proceso, el sistema:

- Valida la disponibilidad del turno en tiempo real.
- Garantiza la exclusividad del horario, evitando reservas duplicadas.
- Registra la cita con estado **Programada**.
- Vincula automáticamente la cita al paciente o a una persona a su cargo.
- Envía una notificación de confirmación por correo electrónico.

---

<a id="3-evento-desencadenante"></a>

# 3. Evento Desencadenante

Desde la pantalla **Agendar cita**, el paciente:

1. Selecciona un profesional (o filtra por especialidad u obra social).
2. Elige una fecha.
3. Selecciona un horario disponible.
4. Indica si la reserva es para sí mismo o para una persona a su cargo.
5. Presiona **Confirmar reserva**.

---

<a id="4-precondiciones"></a>

# 4. Precondiciones

Para realizar una reserva deben cumplirse las siguientes condiciones:

- El paciente tiene una sesión iniciada.
- El paciente posee un perfil completo con sus datos de contacto.
- Si reserva para un tercero, la persona a cargo está registrada y vinculada al paciente.
- El profesional se encuentra activo y habilitado para recibir turnos.
- El profesional posee disponibilidad publicada para la fecha seleccionada.
- Existe al menos un horario disponible.
- La fecha solicitada es igual o posterior a la fecha actual.

---

<a id="5-suposiciones"></a>

# 5. Suposiciones

Se asume que:

- La agenda del profesional se administra mediante plantillas semanales y excepciones.
- Los horarios disponibles se calculan dinámicamente.
- El envío del correo electrónico es asíncrono y no bloquea la operación.
- El paciente puede reservar para sí mismo o para una persona a su cargo.
- El sistema valida que un beneficiario no posea turnos superpuestos.

---

<a id="6-flujo-principal"></a>

# 6. Flujo Principal

| Paso | Actor | Acción |
|------|-------|--------|
| 1 | Paciente | Selecciona el profesional, la fecha, el horario y el beneficiario. Luego presiona Reservar. |
| 2 | Sistema | Verifica que exista una sesión activa y que el usuario tenga el rol Paciente. |
| 3 | Sistema | Recupera el perfil del paciente. |
| 4 | Sistema | Si corresponde, valida que la persona a cargo exista y esté vinculada al paciente. |
| 5 | Sistema | Verifica que el profesional esté activo. |
| 6 | Sistema | Valida la fecha y el horario seleccionados. |
| 7 | Sistema | Comprueba que el horario continúe disponible. |
| 8 | Sistema | Crea la cita con estado **Programada**. |
| 9 | Sistema | Persiste la información mediante una transacción atómica. |
| 10 | Sistema | Dispara el evento de notificación de confirmación por correo electrónico. |

---

<a id="7-reglas-de-negocio"></a>

# 7. Reglas de Negocio

| Código | Regla |
|--------|-------|
| RN-P01-01 | Un horario (profesional + fecha + hora) admite como máximo una cita activa. |
| RN-P01-02 | Los turnos tienen una duración fija de 30 minutos. |
| RN-P01-05 | Toda cita se crea con estado Programada. |
| RN-P01-07 | El correo de confirmación debe incluir la información mínima de la cita. |
| RN-P01-08 | Un paciente no puede agendar dos citas en el mismo horario y fecha con diferentes doctores. |
| RN-P01-09 | Un paciente puede tener como máximo 5 citas programadas simultáneamente. |

---

<a id="8-postcondiciones"></a>

# 8. Postcondiciones

Al finalizar exitosamente el caso de uso:

- Existe una cita persistida con estado **Programada**.
- La cita queda vinculada al paciente y al profesional.
- El horario reservado deja de estar disponible.
- La cita aparece en **Mis Turnos** del paciente.
- La cita se visualiza en la agenda del profesional.
- Se envía o encola el correo electrónico de confirmación.

---

<a id="9-cuestiones-pendientes"></a>

# 9. Cuestiones Pendientes

- Implementar una confirmación obligatoria por correo electrónico para reducir ausencias.
- Definir una antelación mínima para reservar (ejemplo: 24 horas).
- Definir una antelación mínima para cancelar (ejemplo: 24 horas).

---

<a id="10-escenarios-alternativos"></a>

# 10. Escenarios Alternativos

---

# CU-P-01-EA1 — Límite de citas alcanzado

## Objetivo

Describe el comportamiento cuando el paciente alcanzó el máximo permitido de citas programadas.

## Punto de extensión

Se extiende antes del **Paso 8** del flujo principal.

## Flujo Alternativo

| Paso | Actor | Acción |
|------|-------|--------|
| A1 | Sistema | Consulta la cantidad de citas programadas del paciente. |
| A2 | Sistema | Determina que el paciente posee cinco citas activas. |
| A3 | Sistema | Cancela el proceso de reserva. |
| A4 | Sistema | Informa que se alcanzó el límite máximo de citas permitidas. |
| A5 | Sistema | Sugiere cancelar o reprogramar una cita existente antes de realizar una nueva reserva. |

### Reglas involucradas

- RN-P01-09

### Postcondición

- No se registra la nueva cita.

---

# CU-P-01-EA2 — Error del servicio de correo

## Objetivo

Describe el comportamiento cuando la cita fue creada correctamente pero el servicio encargado del envío del correo electrónico falla.

## Punto de extensión

Se extiende desde el **Paso 10** del flujo principal.

## Flujo de Excepción

| Paso | Actor | Acción |
|------|-------|--------|
| E1 | Sistema | Crea y confirma la cita exitosamente. |
| E2 | Sistema | Intenta enviar el correo de confirmación. |
| E3 | Sistema | El servicio de correo devuelve un error o no responde. |
| E4 | Sistema | Registra el incidente en el log de eventos. |
| E5 | Sistema | Encola nuevamente el envío del correo para un reintento automático. |
| E6 | Sistema | Finaliza la operación informando que la reserva fue realizada correctamente. |

### Reglas involucradas

- RN-P01-07

### Postcondición

- La cita permanece registrada con estado **Programada**.
- El horario queda reservado.
- El paciente puede visualizar la cita en **Mis Turnos**.
- El correo queda pendiente de reenvío sin afectar la reserva.

---
---

# CU-P-01-A03 — Superposición de turnos existentes

## Objetivo

Describe el comportamiento cuando el sistema detecta que el paciente o beneficiario seleccionado ya posee un turno reservado en la misma fecha y horario con otro profesional.

## Punto de extensión

Se extiende durante el **Paso 7** del flujo principal, luego de verificar la disponibilidad del horario seleccionado.

## Flujo Alternativo

| Paso | Actor | Acción |
|------|-------|--------|
| A1 | Sistema | Consulta los turnos activos del paciente o beneficiario seleccionado. |
| A2 | Sistema | Detecta que existe una cita programada para la misma fecha y horario con otro profesional. |
| A3 | Sistema | Rechaza la solicitud de reserva para evitar la superposición de turnos. |
| A4 | Sistema | Informa al paciente que ya posee un turno asignado en ese horario. |
| A5 | Sistema | Muestra información del turno existente para que el paciente pueda revisarlo. |

## Reglas involucradas

- RN-P01-08

## Postcondición

- No se registra la nueva cita.
- El turno existente permanece sin modificaciones.
- El horario seleccionado queda disponible para otros pacientes.
[↑ Volver al índice](#indice)


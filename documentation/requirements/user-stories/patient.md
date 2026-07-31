<a id="indice"></a>

# Historias de Usuario

## Índice

- [1. Introducción](#introduccion)
- [2. Actor: Paciente](#actor-paciente)
  - [HU-P-01 – Reservar turno](#hu-p-01)
  - [HU-P-02 – Consultar turnos reservados](#hu-p-02)
  - [HU-P-03 – Cancelar turno reservado](#hu-p-03)
  - [HU-P-04 – Gestionar personas a cargo](#hu-p-04)
  - [HU-P-05 – Consultar profesionales disponibles](#hu-p-05)
  - [HU-P-06 – Reservar turno](#hu-p-06)


---

<a id="introduccion"></a>

# 1. Introducción

El presente documento describe las **historias de usuario** asociadas al actor **Paciente**, detallando las funcionalidades principales que el sistema debe proporcionar desde la perspectiva del usuario final.

Cada historia de usuario incluye su descripción funcional, prioridad, estado y relación con el caso de uso correspondiente.

---

<a id="actor-paciente"></a>

# 2. Actor: Paciente

El paciente representa al usuario principal del sistema encargado de gestionar sus turnos médicos, consultar profesionales disponibles y administrar personas a su cargo.

---

<a id="hu-p-01"></a>

## HU-P-01 – Reservar turno

### Descripción

Como **paciente**, quiero **reservar un turno con un profesional de la salud**, para **obtener atención médica en una fecha y horario disponibles**.

### Información

| Atributo | Valor |
|----------|-------|
| **Identificador** | HU-P-01 |
| **Actor Principal** | Paciente |
| **Caso de Uso Asociado** | CU-P-01 |

### Criterios de aceptación

- El paciente debe estar autenticado en el sistema.
- Debe poder seleccionar un profesional disponible.
- Debe poder elegir una fecha y horario disponible.
- El sistema debe evitar reservas duplicadas.
- Debe enviarse una confirmación de la reserva.

[↑ Volver al índice](#indice)

---

<a id="hu-p-02"></a>

## HU-P-02 – Consultar turnos reservados

### Descripción

Como **paciente**, quiero **consultar mis turnos reservados**, para **conocer mis próximas citas médicas y organizar mi agenda personal**.

### Información

| Atributo | Valor |
|----------|-------|
| **Identificador** | HU-P-02 |
| **Actor Principal** | Paciente |
| **Caso de Uso Asociado** | CU-P-02 |

### Criterios de aceptación

- El paciente debe visualizar sus turnos activos.
- Debe mostrarse la fecha y horario del turno.
- Debe visualizarse el profesional asignado.
- Debe indicarse el estado actual de la cita.

[↑ Volver al índice](#indice)

---

<a id="hu-p-03"></a>

## HU-P-03 – Cancelar Turno

### Descripción

Como **paciente**, quiero **cancelar un turno**, para **liberar el horario cuando no pueda asistir a la consulta médica**.

### Información

| Atributo | Valor |
|----------|-------|
| **Identificador** | HU-P-03 |
| **Actor Principal** | Paciente |
| **Caso de Uso Asociado** | CU-P-03 |

### Criterios de aceptación

- El paciente debe poder seleccionar un turno previamente reservado.
- El sistema debe solicitar confirmación antes de cancelar.
- El turno debe cambiar su estado correctamente.
- El horario debe quedar disponible nuevamente.

[↑ Volver al índice](#indice)

---

<a id="hu-p-04"></a>

## HU-P-04 – Gestionar personas a cargo

### Descripción

Como **paciente**, quiero **gestionar las personas a mi cargo**, para **solicitar turnos médicos en representación de otra persona**.

### Información

| Atributo | Valor |
|----------|-------|
| **Identificador** | HU-P-04 |
| **Actor Principal** | Paciente |
| **Caso de Uso Asociado** | CU-P-04 |
### Criterios de aceptación

- El paciente debe poder registrar personas a cargo.
- Debe poder consultar la información registrada.
- Debe poder seleccionar una persona a cargo al reservar un turno.
- El sistema debe vincular correctamente la cita.

[↑ Volver al índice](#indice)

---

<a id="hu-p-05"></a>

## HU-P-05 – Consultar profesionales disponibles

### Descripción

Como **paciente**, quiero **consultar los profesionales disponibles**, para **seleccionar el especialista adecuado para mi atención médica**.

### Información

| Atributo | Valor |
|----------|-------|
| **Identificador** | HU-P-05 |
| **Actor Principal** | Paciente |
| **Caso de Uso Asociado** | CU-P-05 |

### Criterios de aceptación

- El paciente debe poder visualizar profesionales disponibles.
- Debe poder filtrar profesionales según especialidad.
- Debe visualizar información relevante del profesional.
- Debe poder iniciar la reserva de un turno.

[↑ Volver al índice](#indice)

---
<a id="hu-p-06"></a>

## HU-P-06 – Autenticarse

### Descripción

Como **paciente**, quiero **iniciar sesión en el sistema**, para **gestionar mis turnos médicos de forma segura**.

### Información

| Atributo | Valor |
|----------|-------|
| **Identificador** | HU-P-01 |
| **Actor Principal** | Paciente |
| **Caso de Uso Asociado** | CU-P-01 |

### Criterios de aceptación

- El paciente debe ingresar sus credenciales de acceso.
- El sistema debe validar el correo electrónico y la contraseña ingresados.
- Si las credenciales son correctas, el sistema debe permitir el acceso.
- Si las credenciales son incorrectas, el sistema debe informar el error correspondiente.
- El sistema debe mantener la sesión del paciente de forma segura.

[↑ Volver al índice](#indice)
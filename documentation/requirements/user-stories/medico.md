<a id="indice"></a>

# Historias de Usuario

## Índice

- [1. Introducción](#introduccion)
- [2. Actor: Médico](#actor-medico)
  - [HU-M-01 – Autenticarse](#hu-m-01)
  - [HU-M-02 – Gestionar perfil profesional](#hu-m-02)
  - [HU-M-03 – Consultar historia clínica](#hu-m-03)
  - [HU-M-04 – Gestionar estado del turno](#hu-m-04)
  - [HU-M-05 – Consultar agenda](#hu-m-05)
  - [HU-M-06 – Atender paciente](#hu-m-06)
  - [HU-M-07 – Registrar evolución clínica](#hu-m-07)


---

<a id="introduccion"></a>

# 1. Introducción

El presente documento describe las **historias de usuario** asociadas al actor **Médico**, detallando las funcionalidades principales que el sistema debe proporcionar desde la perspectiva del profesional de la salud.

Cada historia de usuario incluye su descripción funcional, prioridad, estado y relación con el caso de uso correspondiente.

---

<a id="actor-medico"></a>

# 2. Actor: Médico

El médico representa al profesional de la salud del sistema encargado de gestionar sus turnos asignados, administrar su disponibilidad, registrar la evolución clínica de sus pacientes y consultar sus historiales clínicos.

---

<a id="hu-m-01"></a>

## HU-M-01 – Autenticarse

### Descripción

Como **médico**, quiero **iniciar sesión en el sistema**, para **gestionar mis turnos y pacientes de forma segura**.

### Información

| Atributo | Valor |
|----------|-------|
| **Identificador** | HU-M-01 |
| **Actor Principal** | Médico |
| **Caso de Uso Asociado** | CU-M-01 |

### Criterios de aceptación

- El médico debe ingresar su correo electrónico registrado.
- El sistema debe enviar un código OTP al correo indicado.
- El médico debe poder ingresar el código OTP recibido.
- Si el código es correcto, el sistema debe permitir el acceso.
- Si el código es incorrecto o expiró, el sistema debe informar el error correspondiente.
- El sistema debe mantener la sesión del médico de forma segura.

[↑ Volver al índice](#indice)

---

<a id="hu-m-02"></a>

## HU-M-02 – Gestionar perfil profesional

### Descripción

Como **médico**, quiero **gestionar mi perfil profesional**, para **mantener actualizada mi información personal y profesional**.

### Información

| Atributo | Valor |
|----------|-------|
| **Identificador** | HU-M-02 |
| **Actor Principal** | Médico |
| **Caso de Uso Asociado** | CU-M-02 |

### Criterios de aceptación

- El médico debe poder consultar su perfil.
- Debe poder modificar la información permitida.
- El sistema debe validar los datos ingresados.
- El sistema debe impedir modificar el perfil de otro profesional.
- El acceso requiere autenticación.

[↑ Volver al índice](#indice)

<a id="hu-m-03"></a>

## HU-M-03 – Consultar historia clínica

### Descripción

Como **médico**, quiero **consultar la historia clínica de un paciente**, para **conocer sus antecedentes y evoluciones antes o durante la atención**.

### Información

| Atributo | Valor |
|----------|-------|
| **Identificador** | HU-M-03 |
| **Actor Principal** | Médico |
| **Caso de Uso Asociado** | CU-M-03 |

### Criterios de aceptación

- El médico debe autenticarse.
- Debe seleccionar un paciente.
- El sistema debe mostrar la historia clínica del paciente seleccionado.
- Deben visualizarse las evoluciones clínicas registradas.
- El sistema solo debe permitir acceder a pacientes autorizados para el profesional.

[↑ Volver al índice](#indice)


<a id="hu-m-04"></a>

## HU-M-04 – Gestionar estado del turno

### Descripción

Como **médico**, quiero **gestionar el estado de un turno**, para **reflejar correctamente el progreso o resultado de la atención médica**.

### Información

| Atributo | Valor |
|----------|-------|
| **Identificador** | HU-M-04 |
| **Actor Principal** | Médico |
| **Caso de Uso Asociado** | CU-M-04 |

### Criterios de aceptación

- El médico debe poder iniciar la atención de un turno programado.
- Debe poder cancelar un turno cuando corresponda.
- Debe poder registrar la inasistencia del paciente.
- Debe poder finalizar una atención iniciada.
- El sistema debe validar las transiciones de estado permitidas.
- Cancelar un turno **no libera automáticamente el horario**.
- Registrar una inasistencia **no libera automáticamente el horario**.

[↑ Volver al índice](#indice)

<a id="hu-m-05"></a>

## HU-M-05 – Consultar agenda

### Descripción

Como **médico**, quiero **consultar mi agenda**, para **visualizar los turnos programados y organizar mi jornada laboral**.

### Información

| Atributo | Valor |
|----------|-------|
| **Identificador** | HU-M-05 |
| **Actor Principal** | Médico |
| **Caso de Uso Asociado** | CU-M-05 |

### Criterios de aceptación

- El médico debe visualizar únicamente sus turnos.
- Deben mostrarse fecha, horario y paciente.
- Debe visualizarse el estado de cada turno.
- Debe poder filtrar por fecha.
- El acceso requiere autenticación.

[↑ Volver al índice](#indice)


<a id="hu-m-06"></a>

## HU-M-06 – Atender paciente

### Descripción

Como **médico**, quiero **atender a un paciente durante un turno**, para **realizar la consulta médica y completar el proceso de atención**.

### Información

| Atributo | Valor |
|----------|-------|
| **Identificador** | HU-M-06 |
| **Actor Principal** | Médico |
| **Caso de Uso Asociado** | CU-M-06 |

### Criterios de aceptación

- El médico debe iniciar la atención desde un turno válido.
- El sistema debe mostrar la información del paciente.
- Durante la atención el médico puede consultar la historia clínica.
- Durante la atención el médico puede registrar una evolución clínica.
- Al finalizar, el turno debe quedar en estado completado.

[↑ Volver al índice](#indice)

<a id="hu-m-07"></a>

## HU-M-07 – Registrar evolución clínica

### Descripción

Como **médico**, quiero **registrar la evolución clínica durante la atención de mi paciente**, para **documentar la consulta realizada**.

### Información

| Atributo | Valor |
|----------|-------|
| **Identificador** | HU-M-07 |
| **Actor Principal** | Médico |
| **Caso de Uso Asociado** | CU-M-07 (Extensión de Atender Paciente) |

### Criterios de aceptación

- La evolución solo puede registrarse durante una atención.
- Debe poder registrarse motivo de consulta.
- Debe poder registrarse diagnóstico.
- Debe poder registrarse tratamiento.
- Debe poder agregarse observaciones.
- La evolución debe quedar asociada al turno atendido.
- No debe agregar historia clínica de otro doctor.
- No debe poder ver historia clínica de otro doctor.

[↑ Volver al índice](#indice)
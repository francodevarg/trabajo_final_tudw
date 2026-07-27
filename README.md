# Trabajo Final TUDW

> Trabajo Final 
> Tecnicatura Universitaria en Desarrollo Web  
> **Desarrollado por:** Franco Narvaez

## 📋 Descripción

Este proyecto corresponde al trabajo final de la Carrera **Tecnicatura Universitaria en Desarrollo Web** del Año 2026. 

La aplicación desarrollada es un **Sistema de Gestión de Turnos para una Clinica**, cuyo objetivo es facilitar la organización y administración de citas entre los pacientes y los profesionales de la medicina.

## 📚 Documentación

La documentación del proyecto se encuentra organizada en los siguientes archivos:

- 📖 [**PROJECT.md**](https://github.com/francodevarg/trabajo_final_tudw/blob/master/documentation/PROJECT.md): descripción de la arquitectura, organización del proyecto, componentes y funcionamiento interno.
- 🚀 [**DEPLOY.md**](https://github.com/francodevarg/trabajo_final_tudw/blob/master/documentation/DEPLOY.md): guía de instalación, configuración del entorno, despliegue con Docker y comandos útiles.

## 🏗️ Arquitectura
La aplicación está compuesta por una arquitectura distribuida conformada por:

- 🖥️ **Frontend de pacientes:** interfaz destinada a la gestión de turnos por parte de los pacientes, permitiendo consultar disponibilidad y solicitar citas. (https://github.com/francodevarg/trabajo_final_tudw_frontend)
- 🧑‍⚕️ **Frontend administrativo/profesional:** interfaz orientada a la administración de la clínica y gestión de profesionales, horarios y turnos. (https://github.com/francodevarg/trabajo_final_tudw_frontend_admin)
- ⚙️ **Backend Django:** API y lógica de negocio central del sistema. Se encarga de la autenticación, validaciones, gestión de usuarios, turnos y comunicación con la base de datos.
- 🐘 **PostgreSQL:** base de datos relacional utilizada para almacenar la información del sistema.

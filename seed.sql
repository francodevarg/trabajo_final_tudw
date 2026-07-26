-- ============================================================
-- SEED SQL - Datos de negocio
-- Solo datos de negocio. Auth (grupos, usuarios, permisos)
-- se maneja desde seed_auth.py
-- ============================================================

-- ============================================================
-- 1. LIMPIEZA (orden inverso de dependencias)
-- ============================================================

TRUNCATE TABLE evolutions_evolution CASCADE;
TRUNCATE TABLE appointments_appointment CASCADE;
TRUNCATE TABLE patients_patientuser CASCADE;
TRUNCATE TABLE patients_patient CASCADE;
TRUNCATE TABLE doctor_availability CASCADE;
TRUNCATE TABLE doctor_doctor_insurances CASCADE;
TRUNCATE TABLE doctor_doctor CASCADE;
TRUNCATE TABLE doctor_insurance CASCADE;
TRUNCATE TABLE doctor_specialty CASCADE;

-- Resetear secuencias
ALTER SEQUENCE doctor_specialty_id_seq RESTART WITH 1;
ALTER SEQUENCE doctor_insurance_id_seq RESTART WITH 1;
ALTER SEQUENCE doctor_doctor_id_seq RESTART WITH 1;
ALTER SEQUENCE doctor_availability_id_seq RESTART WITH 1;
ALTER SEQUENCE patients_patient_id_seq RESTART WITH 1;
ALTER SEQUENCE patients_patientuser_id_seq RESTART WITH 1;
ALTER SEQUENCE appointments_appointment_id_seq RESTART WITH 1;
ALTER SEQUENCE evolutions_evolution_id_seq RESTART WITH 1;

-- ============================================================
-- 2. ESPECIALIDADES (doctor_specialty)
-- ============================================================

INSERT INTO doctor_specialty (id, name, slug) VALUES
(1, 'Cardiología', 'cardiologia'),
(2, 'Pediatría', 'pediatria'),
(3, 'Dermatología', 'dermatologia'),
(4, 'Traumatología', 'traumatologia'),
(5, 'Clínica Médica', 'clinica-medica');

-- ============================================================
-- 3. OBRAS SOCIALES (doctor_insurance)
-- ============================================================

INSERT INTO doctor_insurance (id, name, slug) VALUES
(1, 'OSDE', 'osde'),
(2, 'Swiss Medical', 'swiss-medical'),
(3, 'Galeno', 'galeno'),
(4, 'Medife', 'medife');

-- ============================================================
-- 4. DOCTORES (doctor_doctor)
-- user_id 2-11, specialty_id 1-5 (rotando)
-- ============================================================

INSERT INTO doctor_doctor (id, user_id, specialty_id, license_number, phone, description, consultation_fee, is_active, created_at, updated_at, appointment_duration) VALUES
(1, 2, 1, 'MP-12345', '+54 11 5555-1001', 'Cardiólogo con 20 años de experiencia. Especialista en arritmias y insuficiencia cardíaca.', 15000.00, TRUE, '2026-07-26 10:00:00-03', '2026-07-26 10:00:00-03', 30),
(2, 3, 2, 'MP-23456', '+54 11 5555-1002', 'Pediatra certificada. Atención integral del niño y adolescente.', 12000.00, TRUE, '2026-07-26 10:00:00-03', '2026-07-26 10:00:00-03', 30),
(3, 4, 3, 'MP-34567', '+54 11 5555-1003', 'Dermatólogo. Especialista en dermatología estética y oncológica.', 13000.00, TRUE, '2026-07-26 10:00:00-03', '2026-07-26 10:00:00-03', 30),
(4, 5, 4, 'MP-45678', '+54 11 5555-1004', 'Traumatólogo y ortopedista. Cirugía artroscópica y deportiva.', 14000.00, TRUE, '2026-07-26 10:00:00-03', '2026-07-26 10:00:00-03', 30),
(5, 6, 5, 'MP-56789', '+54 11 5555-1005', 'Clínico general. Atención primaria y medicina preventiva.', 10000.00, TRUE, '2026-07-26 10:00:00-03', '2026-07-26 10:00:00-03', 30),
(6, 7, 1, 'MP-67890', '+54 11 5555-1006', 'Cardióloga intervencionista. Cateterismos y stents coronarios.', 18000.00, TRUE, '2026-07-26 10:00:00-03', '2026-07-26 10:00:00-03', 45),
(7, 8, 2, 'MP-78901', '+54 11 5555-1007', 'Pediatra neonatólogo. Cuidados intensivos neonatales.', 15000.00, TRUE, '2026-07-26 10:00:00-03', '2026-07-26 10:00:00-03', 30),
(8, 9, 3, 'MP-89012', '+54 11 5555-1008', 'Dermatóloga. Especialista en acné, psoriasis y alergias cutáneas.', 12000.00, TRUE, '2026-07-26 10:00:00-03', '2026-07-26 10:00:00-03', 30),
(9, 10, 4, 'MP-90123', '+54 11 5555-1009', 'Traumatólogo. Especialista en columna vertebral y cirugía mínimamente invasiva.', 16000.00, TRUE, '2026-07-26 10:00:00-03', '2026-07-26 10:00:00-03', 45),
(10, 11, 5, 'MP-01234', '+54 11 5555-1010', 'Clínica médica. Diagnóstico y tratamiento de enfermedades complejas.', 11000.00, TRUE, '2026-07-26 10:00:00-03', '2026-07-26 10:00:00-03', 30);

-- ============================================================
-- 5. OBRAS SOCIALES POR DOCTOR (doctor_doctor_insurances)
-- ============================================================

INSERT INTO doctor_doctor_insurances (id, doctor_id, insurance_id) VALUES
-- Dr. Martínez (Cardiología) - OSDE, Swiss Medical
(1, 1, 1),
(2, 1, 2),
-- Dra. López (Pediatría) - OSDE, Galeno
(3, 2, 1),
(4, 2, 3),
-- Dr. García (Dermatología) - Swiss Medical
(5, 3, 2),
-- Dra. Rodríguez (Traumatología) - OSDE, Medife
(6, 4, 1),
(7, 4, 4),
-- Dr. Sánchez (Clínica) - Galeno, Medife
(8, 5, 3),
(9, 5, 4),
-- Dra. Fernández (Cardiología) - OSDE, Swiss Medical, Galeno
(10, 6, 1),
(11, 6, 2),
(12, 6, 3),
-- Dr. Torres (Pediatría) - Medife
(13, 7, 4),
-- Dra. Díaz (Dermatología) - OSDE
(14, 8, 1),
-- Dr. Ruiz (Traumatología) - Swiss Medical, Galeno
(15, 9, 2),
(16, 9, 3),
-- Dra. Morales (Clínica) - OSDE, Medife
(17, 10, 1),
(18, 10, 4);

-- ============================================================
-- 6. DISPONIBILIDADES (doctor_availability)
-- day_of_week: 0=Lunes, 1=Martes, 2=Miércoles, 3=Jueves, 4=Viernes
-- ============================================================

INSERT INTO doctor_availability (id, doctor_id, day_of_week, start_time, end_time) VALUES
-- Dr. Martínez (Cardiología) - Lunes a Viernes mañana
(1, 1, 0, '08:00:00', '12:00:00'),
(2, 1, 1, '08:00:00', '12:00:00'),
(3, 1, 2, '08:00:00', '12:00:00'),
(4, 1, 3, '08:00:00', '12:00:00'),
(5, 1, 4, '08:00:00', '12:00:00'),
-- Dra. López (Pediatría) - Lunes a Viernes tarde
(6, 2, 0, '14:00:00', '18:00:00'),
(7, 2, 1, '14:00:00', '18:00:00'),
(8, 2, 2, '14:00:00', '18:00:00'),
(9, 2, 3, '14:00:00', '18:00:00'),
(10, 2, 4, '14:00:00', '18:00:00'),
-- Dr. García (Dermatología) - Lunes, Miércoles, Viernes mañana
(11, 3, 0, '09:00:00', '13:00:00'),
(12, 3, 2, '09:00:00', '13:00:00'),
(13, 3, 4, '09:00:00', '13:00:00'),
-- Dra. Rodríguez (Traumatología) - Martes y Jueves mañana, Lunes tarde
(14, 4, 0, '14:00:00', '18:00:00'),
(15, 4, 1, '08:00:00', '12:00:00'),
(16, 4, 3, '08:00:00', '12:00:00'),
-- Dr. Sánchez (Clínica) - Lunes a Viernes mañana
(17, 5, 0, '07:00:00', '12:00:00'),
(18, 5, 1, '07:00:00', '12:00:00'),
(19, 5, 2, '07:00:00', '12:00:00'),
(20, 5, 3, '07:00:00', '12:00:00'),
(21, 5, 4, '07:00:00', '12:00:00'),
-- Dra. Fernández (Cardiología) - Martes y Jueves tarde
(22, 6, 1, '14:00:00', '18:30:00'),
(23, 6, 3, '14:00:00', '18:30:00'),
-- Dr. Torres (Pediatría) - Lunes a Viernes mañana
(24, 7, 0, '08:00:00', '12:00:00'),
(25, 7, 1, '08:00:00', '12:00:00'),
(26, 7, 2, '08:00:00', '12:00:00'),
(27, 7, 3, '08:00:00', '12:00:00'),
(28, 7, 4, '08:00:00', '12:00:00'),
-- Dra. Díaz (Dermatología) - Miércoles y Viernes tarde
(29, 8, 2, '14:00:00', '18:00:00'),
(30, 8, 4, '14:00:00', '18:00:00'),
-- Dr. Ruiz (Traumatología) - Lunes a Viernes mañana
(31, 9, 0, '08:00:00', '12:30:00'),
(32, 9, 1, '08:00:00', '12:30:00'),
(33, 9, 2, '08:00:00', '12:30:00'),
(34, 9, 3, '08:00:00', '12:30:00'),
(35, 9, 4, '08:00:00', '12:30:00'),
-- Dra. Morales (Clínica) - Martes y Jueves tarde
(36, 10, 1, '14:00:00', '18:00:00'),
(37, 10, 3, '14:00:00', '18:00:00');

-- ============================================================
-- 7. PACIENTES (patients_patient)
-- ============================================================

INSERT INTO patients_patient (id, first_name, last_name, date_of_birth, dni, sex, created_at, updated_at) VALUES
(1, 'Juan', 'Pérez', '1990-04-15', 30123456, 'M', '2026-07-26 10:00:00-03', '2026-07-26 10:00:00-03'),
(2, 'María', 'González', '1988-08-22', 32567890, 'F', '2026-07-26 10:00:00-03', '2026-07-26 10:00:00-03'),
(3, 'Lucas', 'Hernández', '1995-12-10', 35901234, 'M', '2026-07-26 10:00:00-03', '2026-07-26 10:00:00-03'),
(4, 'Valentina', 'López', '1992-06-18', 34678901, 'F', '2026-07-26 10:00:00-03', '2026-07-26 10:00:00-03'),
(5, 'Mateo', 'Ramírez', '1985-03-25', 28901234, 'M', '2026-07-26 10:00:00-03', '2026-07-26 10:00:00-03'),
(6, 'Camila', 'Pérez', '2018-05-10', 54123456, 'F', '2026-07-26 10:00:00-03', '2026-07-26 10:00:00-03'),
(7, 'Tomás', 'González', '2020-09-25', 55678901, 'M', '2026-07-26 10:00:00-03', '2026-07-26 10:00:00-03');

-- ============================================================
-- 8. VÍNCULOS PACIENTE-USUARIO (patients_patientuser)
-- ============================================================

INSERT INTO patients_patientuser (id, user_id, patient_id, is_primary, role, created_at) VALUES
-- patient1 (user_id=12) → Patient1 (primary) + Patient6 (non-primary)
(1, 12, 1, TRUE, 'self', '2026-07-26 10:00:00-03'),
(2, 12, 6, FALSE, 'parent', '2026-07-26 10:00:00-03'),
-- patient2 (user_id=13) → Patient2 (primary) + Patient7 (non-primary)
(3, 13, 2, TRUE, 'self', '2026-07-26 10:00:00-03'),
(4, 13, 7, FALSE, 'parent', '2026-07-26 10:00:00-03'),
-- patient3 (user_id=14) → Patient3 (primary)
(5, 14, 3, TRUE, 'self', '2026-07-26 10:00:00-03'),
-- patient4 (user_id=15) → Patient4 (primary)
(6, 15, 4, TRUE, 'self', '2026-07-26 10:00:00-03'),
-- patient5 (user_id=16) → Patient5 (primary)
(7, 16, 5, TRUE, 'self', '2026-07-26 10:00:00-03');

-- ============================================================
-- 9. TURNOS (appointments_appointment)
-- Fechas en julio 2026 (ya pasaron)
-- ============================================================

INSERT INTO appointments_appointment (id, date, time, status, notes, doctor_id, patient_id, user_id, created_at, updated_at) VALUES
-- Turnos completados (julio - ya pasaron → tienen evolución)
(1, '2026-07-02', '09:00:00', 'completed', 'Control cardiológico anual. Paciente asintomático.', 1, 1, 12, '2026-06-28 11:00:00-03', '2026-07-02 09:30:00-03'),
(2, '2026-07-04', '14:30:00', 'completed', 'Consulta pediátrica de rutina. Niño sano.', 2, 7, 13, '2026-06-29 11:00:00-03', '2026-07-04 15:00:00-03'),
(3, '2026-07-07', '10:00:00', 'completed', 'Revisión de manchas en piel. Sin hallazgos preocupantes.', 3, 4, 15, '2026-07-01 11:00:00-03', '2026-07-07 10:30:00-03'),
(4, '2026-07-09', '08:30:00', 'completed', 'Dolor lumbar. Se indica radiografía.', 4, 3, 14, '2026-07-02 11:00:00-03', '2026-07-09 09:00:00-03'),
(5, '2026-07-11', '07:30:00', 'completed', 'Control presión arterial. Ajuste de medicación.', 5, 5, 16, '2026-07-04 11:00:00-03', '2026-07-11 08:00:00-03'),
(6, '2026-07-14', '09:00:00', 'completed', 'Seguimiento cardiológico post-tratamiento.', 1, 2, 13, '2026-07-07 11:00:00-03', '2026-07-14 09:30:00-03'),
(8, '2026-07-21', '10:30:00', 'completed', 'Primera consulta dermatológica.', 8, 1, 12, '2026-07-14 11:00:00-03', '2026-07-21 11:00:00-03'),
-- Turnos cancelados (julio - no llevan evolución)
(7, '2026-07-16', '15:00:00', 'cancelled', 'Paciente canceló por motivos personales.', 2, 6, 12, '2026-07-09 11:00:00-03', '2026-07-15 16:00:00-03'),
(11, '2026-07-23', '11:00:00', 'cancelled', 'Doctor no disponible. Se reprogramó.', 6, 2, 13, '2026-07-16 11:00:00-03', '2026-07-22 10:00:00-03'),
-- Turnos programados (agosto - futuro, no llevan evolución)
(9, '2026-08-05', '08:00:00', 'scheduled', 'Control de evolución de lesión en rodilla.', 9, 3, 14, '2026-07-26 11:00:00-03', '2026-07-26 11:00:00-03'),
(10, '2026-08-12', '14:00:00', 'scheduled', 'Consulta clínica general. Chequeo anual.', 10, 4, 15, '2026-07-26 11:00:00-03', '2026-07-26 11:00:00-03');

-- ============================================================
-- 10. EVOLUCIONES (evolutions_evolution)
-- Solo para turnos completed en julio (ya pasaron)
-- ============================================================

INSERT INTO evolutions_evolution (id, appointment_id, reason, diagnosis, treatment, notes, created_at) VALUES
(1, 1, 'Control cardiológico anual de rutina.',
 'Paciente asintomático. Sin alteraciones significativas en ECG de reposo.',
 'Se mantiene tratamiento actual con Enalapril 10mg/día. Control en 6 meses.',
 'Paciente colaborador. Se recomienda dieta baja en sodio y ejercicio moderado.',
 '2026-07-02 09:30:00-03'),
(2, 2, 'Consulta pediátrica de rutina. Niño de 6 años.',
 'Paciente sano. Desarrollo psicomotor adecuado para la edad.',
 'Vacunación pendiente: refuerzo de DPT. Se programa para próximo control.',
 'Peso y talla en percentil 50. Sin observaciones.',
 '2026-07-04 15:00:00-03'),
(3, 3, 'Revisión de manchas pigmentadas en dorso.',
 'Queratosis seborreicas benignas. Sin signos de malignidad.',
 'No requiere tratamiento. Se recomienda protección solar.',
 'Se fotografían lesiones para seguimiento.',
 '2026-07-07 10:30:00-03'),
(4, 4, 'Dolor lumbar bajo de 2 semanas de evolución.',
 'Contractura muscular lumbar. Descartada patología ósea.',
 'Diclofenaco 50mg c/12hs por 7 días. Kinesiología 2 sesiones/semana.',
 'Se indica reposo relativo y evitación de esfuerzos pesados.',
 '2026-07-09 09:00:00-03'),
(5, 5, 'Control de presión arterial. Hipertensión diagnosticada hace 2 años.',
 'HTA esencial controlada. PA 130/85 mmHg.',
 'Se ajusta medicación: Losartán 50mg/día (dosis anterior insuficiente).',
 'Paciente refiere buena adhesión al tratamiento. Se cita para control en 1 mes.',
 '2026-07-11 08:00:00-03'),
(6, 6, 'Seguimiento cardiológico post-tratamiento de arritmia.',
 'Ritmo sinusal regular. Sin episodios de taquicardia en el último mes.',
 'Se reduce dosis de Bisoprolol a 2.5mg/día. Próximo control en 3 meses.',
 'Paciente refiere mejoría sintomática. tolera bien la actividad física.',
 '2026-07-14 09:30:00-03'),
(7, 8, 'Primera consulta dermatológica. Lesión en antebrazo derecho.',
 'Dermatitis de contacto. Se descarta patología maligna.',
 'Crema con hidrocortisona 1% por 14 días. Evitar contacto con irritantes.',
 'Se recomienda seguimiento en 30 días si no hay mejoría.',
 '2026-07-21 11:00:00-03');

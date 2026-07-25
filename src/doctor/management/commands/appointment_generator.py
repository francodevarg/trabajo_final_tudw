"""Generador determinista de turnos para la clínica."""
import random
from datetime import date, time, timedelta
from typing import Iterable, List

from django.utils import timezone

from doctor.models import Availability, Doctor

from appointments.models import Appointment

from patients.models import Patient



class AppointmentGenerator:
    """Genera turnos respetando disponibilidad, sin superposiciones.

    El generador es determinista: usa ``random.seed(42)`` para garantizar
    resultados reproducibles entre ejecuciones.
    """

    def __init__(self) -> None:
        self.today: date = timezone.localdate()
        self.appointments: List[Appointment] = []
        self.doctor_schedule: dict[int, dict[date, set[time]]] = {}

    def generate(
        self,
        doctors: Iterable[Doctor],
        patients: Iterable[Patient],
        appointments_per_doctor: int = 20,
        months: int = 2,
    ) -> List[Appointment]:
        """Genera turnos para los médicos indicados.

        Args:
            doctors: Médicos sobre los que generar turnos.
            patients: Pacientes candidatos.
            appointments_per_doctor: Turnos objetivo por médico.
            months: Ventana de meses hacia adelante.

        Returns:
            Lista de instancias de Appointment (aún no persistidas).
        """
        random.seed(42)

        patients_list = [p for p in patients if p.user_id is not None]
        if not patients_list:
            return []

        end_date = self.today + timedelta(days=months * 30)

        for doctor in doctors:
            self._generate_doctor_appointments(
                doctor=doctor,
                patients=patients_list,
                count=appointments_per_doctor,
                end_date=end_date,
            )

        return self.appointments

    def _generate_doctor_appointments(
        self,
        doctor: Doctor,
        patients: List[Patient],
        count: int,
        end_date: date,
    ) -> None:
        """Genera los turnos de un médico específico."""
        availabilities = list(doctor.availabilities.all())
        if not availabilities:
            return

        attempts = 0
        max_attempts = count * 20

        while len(self._get_doctor_appointments(doctor)) < count and attempts < max_attempts:
            attempts += 1

            appointment_date = self._generate_random_date(self.today, end_date)
            appointment_time = self._generate_random_time(
                doctor, appointment_date, availabilities
            )

            if appointment_time is None:
                continue

            patient = random.choice(patients)
            status = self._determine_status(appointment_date)

            appointment = Appointment(
                doctor=doctor,
                patient=patient,
                user=patient.user,
                date=appointment_date,
                time=appointment_time,
                status=status,
            )

            self.appointments.append(appointment)
            self._register_appointment(doctor, appointment_date, appointment_time)

    def _get_doctor_appointments(self, doctor: Doctor) -> List[Appointment]:
        """Obtiene los turnos ya generados para un médico."""
        return [apt for apt in self.appointments if apt.doctor_id == doctor.id]

    def _generate_random_date(self, start_date: date, end_date: date) -> date:
        """Genera una fecha aleatoria dentro del rango indicado."""
        delta = (end_date - start_date).days
        return start_date + timedelta(days=random.randint(0, delta))

    def _generate_random_time(
        self,
        doctor: Doctor,
        appointment_date: date,
        availabilities: List[Availability],
    ) -> time | None:
        """Genera un horario libre dentro de la disponibilidad del médico."""
        day_of_week = appointment_date.weekday()

        available_slots = [
            avail for avail in availabilities if avail.day_of_week == day_of_week
        ]
        if not available_slots:
            return None

        availability = random.choice(available_slots)
        start_minutes = availability.start_time.hour * 60 + availability.start_time.minute
        end_minutes = availability.end_time.hour * 60 + availability.end_time.minute

        possible_slots: List[time] = []
        current_minutes = start_minutes

        while current_minutes + 30 <= end_minutes:
            slot_time = time(current_minutes // 60, current_minutes % 60)
            if self._is_slot_available(doctor, appointment_date, slot_time):
                possible_slots.append(slot_time)
            current_minutes += 30

        if not possible_slots:
            return None

        return random.choice(possible_slots)

    def _is_slot_available(
        self, doctor: Doctor, appointment_date: date, slot_time: time
    ) -> bool:
        """Verifica si un horario está libre para un médico."""
        doctor_id = doctor.id
        schedule = self.doctor_schedule.get(doctor_id)
        if schedule is None:
            return True
        booked_times = schedule.get(appointment_date)
        if booked_times is None:
            return True
        return slot_time not in booked_times

    def _register_appointment(
        self, doctor: Doctor, appointment_date: date, appointment_time: time
    ) -> None:
        """Registra el horario ocupado para evitar superposiciones."""
        doctor_id = doctor.id
        schedule = self.doctor_schedule.setdefault(doctor_id, {})
        booked_times = schedule.setdefault(appointment_date, set())
        booked_times.add(appointment_time)

    def _determine_status(self, appointment_date: date) -> str:
        """Determina el estado del turno según la fecha.

        Distribución:
            - Pasados: 90% completed, 10% cancelled.
            - Futuros: 55% scheduled, 25% completed, 10% cancelled, 10% no_show.
        """
        is_past = appointment_date < self.today

        if is_past:
            return random.choices(
                ["completed", "cancelled"],
                weights=[90, 10],
                k=1,
            )[0]

        return random.choices(
            ["scheduled", "completed", "cancelled", "no_show"],
            weights=[80, 0, 10, 10],
            k=1,
        )[0]

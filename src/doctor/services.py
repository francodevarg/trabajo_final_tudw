from datetime import date, datetime, timedelta, time as time_type
from collections import defaultdict
from typing import Optional

from django.utils import timezone

from doctor.models import Doctor
from appointments.models import Appointment


class SlotService:
    MAX_DAYS_AHEAD = 90

    @staticmethod
    def _generate_time_strings(
        start_time: time_type,
        end_time: time_type,
        duration: int,
    ) -> list[str]:
        base = date(2000, 1, 1)
        current = datetime.combine(base, start_time)
        end = datetime.combine(base, end_time)
        delta = timedelta(minutes=duration)
        result: list[str] = []
        while current + delta <= end:
            result.append(current.strftime("%H:%M"))
            current += delta
        return result

    @staticmethod
    def get_available_slots(
        doctor: Doctor,
        target_date: date,
    ) -> list[dict]:
        availabilities = list(
            doctor.availabilities.filter(day_of_week=target_date.weekday())
        )
        if not availabilities:
            return []

        appointment_times = set(
            doctor.appointments.filter(date=target_date).values_list("time", flat=True)
        )
        appointment_times_str = {t.strftime("%H:%M") for t in appointment_times}

        now = timezone.localtime().time() if target_date == timezone.localdate() else None

        duration = doctor.appointment_duration
        base_dt = date(2000, 1, 1)
        slots: list[dict] = []
        for availability in availabilities:
            current_dt = datetime.combine(base_dt, availability.start_time)
            end_dt = datetime.combine(base_dt, availability.end_time)
            delta = timedelta(minutes=duration)
            while current_dt + delta <= end_dt:
                time_str = current_dt.strftime("%H:%M")
                slot_time = current_dt.time()
                if now is None or slot_time > now:
                    slots.append(
                        {"time": time_str, "available": time_str not in appointment_times_str}
                    )
                current_dt += delta
        return slots

    @staticmethod
    def get_next_available_slot(doctor: Doctor) -> Optional[dict]:
        today = timezone.localdate()
        max_date = today + timedelta(days=SlotService.MAX_DAYS_AHEAD)

        availabilities = list(doctor.availabilities.all())
        if not availabilities:
            return None

        appointments_by_date: dict[date, set[str]] = defaultdict(set)
        qs = Appointment.objects.filter(
            doctor=doctor,
            date__gte=today,
            date__lte=max_date,
        ).values("date", "time")
        for a in qs:
            appointments_by_date[a["date"]].add(a["time"].strftime("%H:%M"))

        duration = doctor.appointment_duration
        now = timezone.localtime().time()
        base_dt = date(2000, 1, 1)

        for day_offset in range(SlotService.MAX_DAYS_AHEAD):
            target_date = today + timedelta(days=day_offset)
            day_availabilities = [
                a for a in availabilities if a.day_of_week == target_date.weekday()
            ]
            if not day_availabilities:
                continue

            booked = appointments_by_date.get(target_date, set())
            is_today = target_date == today

            for availability in day_availabilities:
                current_dt = datetime.combine(base_dt, availability.start_time)
                end_dt = datetime.combine(base_dt, availability.end_time)
                delta = timedelta(minutes=duration)

                while current_dt + delta <= end_dt:
                    time_str = current_dt.strftime("%H:%M")
                    slot_time = current_dt.time()
                    if time_str not in booked and (not is_today or slot_time > now):
                        return {
                            "date": target_date.isoformat(),
                            "time": time_str,
                        }
                    current_dt += delta

        return None

# Copyright (c) 2023, Jinal and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from appointments_app.appointments_app.doctype.appointment_queue.appointment_queue import create_queues_for_today


class TestAppointmentQueue(FrappeTestCase):
	def test_create_queues_for_today(self):
		doctor = frappe.get_doc({"doctype": "Doctor", "first_name": "Test Doctor", "speciality": "Pediatrician"}).insert()
		clinic = frappe.get_doc({"doctype": "Clinic", "name": "Test Clinic", "doctor": doctor.name, "contact_number": "+918523694128", "is_published": True}).insert()
		shift = frappe.get_doc({"doctype": "Schedule Shift", "start_time": "9:00:00", "end_time": "15:00:00", "clinic": clinic.name}).insert()

		self.assertEqual(frappe.db.count("Appointment Queue"), 0)
  
		create_queues_for_today()
  
		self.assertEqual(frappe.db.count("Appointment Queue"), 1)
  
		queue = frappe.get_doc("Appointment Queue", {"clinic": clinic.name, "shift": shift.name, "date": frappe.utils.today()})
		self.assertTrue(queue)
  
	def tearDown(self):
		frappe.db.rollback()
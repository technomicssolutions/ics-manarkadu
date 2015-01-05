from django.db import models
from college.models import Course
from admission.models import Student

CHOICES = (
	('Incoming', 'Incoming'),
	('Outgoing', 'Outgoing'),
)

class Letter(models.Model):

	letter_type = models.CharField('Letter Type',null=True, blank=True, max_length=200, choices=CHOICES)
	date = models.DateField('Date',null=True, blank=True)
	to_address = models.CharField('To Address',null=True, blank=True, max_length=200) 
	from_address = models.CharField('From Address',null=True, blank=True, max_length=200)

	def __unicode__(self):
		return self.letter_type + str('') + self.from_address


class Certificate(models.Model):

	certificate_name = models.CharField('Certificate Name',null=True, blank=True, max_length=200)
	date = models.DateField('Date',null=True, blank=True)
	student = models.ForeignKey(Student)
	course = models.ForeignKey(Course)
	issued_authority = models.CharField('Issued Authority',null=True, blank=True, max_length=200)

	def __unicode__(self):
		return self.certificate_name + str('') + self.student.student_name		
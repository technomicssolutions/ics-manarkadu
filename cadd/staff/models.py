from django.db import models
from django.contrib.auth.models import User

ROLE = (
	('teacher', 'Teacher'),
	('staff', 'Staff'),
)
class Permission(models.Model):

	attendance_module = models.BooleanField('Attendance Permission', default=False)
	student_module = models.BooleanField('Student Permission', default=False)
	master_module = models.BooleanField('Master Permission', default=False)
	fees_module = models.BooleanField('Fees Permission', default=False)
	register_module = models.BooleanField('Register Permission', default=False)
	expense_module = models.BooleanField('Expense Permission', default=False)
	
	class Meta:
		verbose_name_plural = 'Permission'

class Staff(models.Model):
	user = models.ForeignKey(User, null=True, blank=True)
	permission = models.ForeignKey(Permission, null=True, blank=True)

	dob = models.DateField('Date of Birth',null=True, blank=True)
	address= models.TextField('Staff Address',null=True, blank=True, max_length=200)
	mobile_number= models.CharField('Mobile Number',null=True, blank=True, max_length=200)
	land_number= models.CharField('Land Number',null=True, blank=True, max_length=200)
	
	blood_group = models.CharField('Blood Group',null=True, blank=True, max_length=200)
	doj = models.DateField('Date of Join',null=True, blank=True)
	qualifications = models.TextField('Qualifications',null=True, blank=True, max_length=200)
	experience = models.CharField('Experiance',null=True, blank=True, max_length=200)
	photo = models.ImageField(upload_to = "uploads/photos/", null=True, blank=True)
	
	role = models.CharField('Role',null=True, blank=True, max_length=200, choices=ROLE)

	def __unicode__(self):
		return (self.user.first_name + str(' ') + self.user.last_name)

	class Meta:
		verbose_name = 'Staff'
		verbose_name_plural = 'Staff'






from django.db import models

class Software(models.Model):
	name = models.CharField('Software Name', null=True, blank=True, max_length=200, unique=True)
	
	def __unicode__(self):
		return (self.name)

class Course(models.Model):
	name = models.CharField('Course Name', null=True, blank=True, max_length=200, unique=True)
	software = models.ManyToManyField(Software)
	amount = models.DecimalField('Amount', null=True, blank=True, decimal_places=2, max_digits=10)
	duration = models.DecimalField('Duration', null=True, blank=True, decimal_places=2, max_digits=10)
	duration_unit = models.CharField('Duration Unit', null=True, blank=True, max_length=200)

	def __unicode__(self):
		return (self.name)

class Batch(models.Model):
	name = models.CharField('Batch Name', null=True, blank=True, max_length=200)
	software = models.ForeignKey(Software)
	start_time = models.TimeField('Start Time', null=True, blank=True)
	end_time = models.TimeField('End Time', null=True, blank=True)
	no_of_students = models.IntegerField('No of Students', default=0, null=True,blank=True)
	allowed_students = models.IntegerField('Allowed No of Students', default=0, null=True, blank=True)

	def __unicode__(self):
		return (self.name + ' ' + str(self.start_time) + '-' + str(self.end_time))

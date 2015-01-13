
from django.db import models
from college.models import Course, Batch


class Installment(models.Model):

	due_date = models.DateField('Due Date', null=True, blank=True)
	amount = models.DecimalField('Amount',max_digits=14, decimal_places=2, default=0)
	fine_amount = models.DecimalField('Fine Amount',max_digits=14, decimal_places=2, default=0)
	
	def __unicode__(self):

		return str(self.amount)
	
	class Meta:

		verbose_name_plural = 'Installment'

		
class FollowUp(models.Model):

	follow_up_date = models.DateField('Next follow up date',null=True, blank=True)
	remarks_for_follow_up_date =   models.TextField('Remark for Next follow up date',null=True, blank=True)


class Enquiry(models.Model):

	mode = models.CharField('Enquiry Mode', null=True, blank=True, max_length=200)
	student_name = models.CharField('Student Name', null=True, blank=True, max_length=200)
	address = address= models.TextField('Student Address',null=True, blank=True)
	mobile_number= models.CharField('Mobile Number',null=True, blank=True, max_length=200)
	email = models.CharField('Email',null=True, blank=True, max_length=200)
	details_about_clients_enquiry =  models.TextField('Details ', null=True, blank=True)
	educational_qualification = models.CharField('Educational Qualification', null=True, blank=True, max_length=200)
	land_mark = models.CharField('Nearest land mark',null=True, blank=True, max_length=200)
	course = models.ForeignKey(Course,null=True, blank=True)
	remarks = models.TextField('Remark',null=True, blank=True)
	auto_generated_num = models.CharField('Auto generated number',null=True, blank=True, max_length=200)
	discount = models.IntegerField('Discount', default=0, null=True, blank=True)
	saved_date = models.DateField('Saved Date',null=True, blank=True)
	is_admitted = models.BooleanField('Is Admitted',default=False)
	follow_up = models.ManyToManyField(FollowUp, null=True, blank=True)
	def __unicode__(self):
		return str(self.student_name)

	class Meta:
		verbose_name = 'Enquiry'
		verbose_name_plural = 'Enquiry'


class Student(models.Model):

	enquiry = models.ForeignKey(Enquiry, null=True, blank=True)

	student_name = models.CharField('Student Name', null=True, blank=True, max_length=200)
	roll_number = models.CharField('Roll Number', null=True, blank=True, max_length=200)
	unique_id = models.CharField('Unique ID', null=True, blank=True, max_length=200)
	cadd_registration_no = models.CharField('Cadd Registration No', null=True, blank=True, max_length=200)
	address = models.CharField('Student Address', null=True, blank=True, max_length=200 )
	course = models.ForeignKey(Course, null=True, blank=True)
	batches = models.ManyToManyField(Batch, null=True, blank=True)
	dob = models.DateField('Date of Birth',null=True, blank=True)
	mobile_number= models.CharField('Mobile Number',null=True, blank=True, max_length=200)
	email = models.CharField('Email',null=True, blank=True, max_length=200)
	blood_group = models.CharField('Blood Group',null=True, blank=True, max_length=200)
	doj = models.DateField('Date of Join',null=True, blank=True)
	photo = models.ImageField(upload_to = "uploads/photos/", null=True, blank=True)
	qualifications = models.TextField('Qualifications', null=True, blank=True)
	certificates_submitted = models.CharField('Certificates',null=True, blank=True, max_length=200)
	id_proofs_submitted = models.CharField('Id Proofs',null=True, blank=True, max_length=200)
	guardian_name = models.CharField('Guardian Name',null=True, blank=True, max_length=200)
	relationship = models.CharField('Relationship',null=True, blank=True, max_length=200)
	guardian_mobile_number= models.CharField('Guardian Mobile Number',null=True, blank=True, max_length=200)
	is_rolled = models.BooleanField('Is Rolled',default=False)
	fees = models.DecimalField('Fees', max_digits=14, decimal_places=2, default=0)
	balance = models.DecimalField('Balance', max_digits=14, decimal_places=2, default=0)
	discount = models.DecimalField('Discount', max_digits=14, decimal_places=2, default=0)
	no_installments = models.IntegerField('No of Installments', default=0)
	installments = models.ManyToManyField(Installment, null=True, blank=True)


	def __unicode__(self):
		return str(self.student_name)
		
	class Meta:
		verbose_name = 'Student'
		verbose_name_plural = 'Student'



from django.db import models
from college.models import Batch, Course
from admission.models import Student, Installment

class FeesPaymentInstallment(models.Model):
	student = models.ForeignKey(Student, null=True, blank=True)
	total_amount = models.DecimalField('Total Amount', max_digits=14, decimal_places=2, default=0)
	next_fees_payment_installment = models.ForeignKey('self', null=True, blank=True)
	installment = models.ForeignKey(Installment, null=True, blank=True)
	paid_amount = models.DecimalField('Paid Amount', max_digits=14, decimal_places=2, default=0)
	installment_amount = models.DecimalField('Installment Amount', max_digits=14, decimal_places=2, default=0)
	installment_fine = models.DecimalField('Installment Fine Amount', max_digits=14, decimal_places=2, default=0)
	fee_waiver_amount = models.DecimalField('Fee Waiver Amount', max_digits=14, decimal_places=2, default=0)
	receipt_no = models.CharField('Receipt No',max_length=200,null=True, blank=True)
	paid_date = models.DateField('Paid Date', null=True, blank=True)
	paid_fine_amount = models.DecimalField('Fine Amount', max_digits=14, decimal_places=2, default=0)

	def __unicode__(self):

		return str(self.total_amount)

	class Meta:

		verbose_name_plural = 'Fees Payment Installment'


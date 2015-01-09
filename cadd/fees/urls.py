from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from fees.views import FeesPaymentSave, ListOutStandingFees, GetOutStandingFeesDetails, PrintOutstandingFeesReport, FeepaymentReport,\
 UnRollStudent, RollStudent, AccountStatement, ReceiptNo

urlpatterns = patterns('',
	
	url(r'^fees_payment/$',login_required(FeesPaymentSave.as_view()), name='fees_payment'),
	
	url(r'^list_outstanding_fees/$',login_required(ListOutStandingFees.as_view()), name='list_outstanding_fees'),
	url(r'^get_outstanding_fees_details/$',login_required(GetOutStandingFeesDetails.as_view()), name='get_outstanding_fees_details'),
	
	url(r'^print_outstanding_fees_details/$', login_required(PrintOutstandingFeesReport.as_view()), name='print_outstanding_fees_details'),
	url(r'^fees_payment_report/$', login_required(FeepaymentReport.as_view()), name='fees_payment_report'),
	url(r'^unroll_students/$',login_required(UnRollStudent.as_view()), name='unroll_students'),
	url(r'^roll_students/$',login_required(RollStudent.as_view()), name='roll_students'),
	url(r'^account_statement/$',login_required(AccountStatement.as_view()), name='account_statement'),
	url(r'^receipt_no/$',login_required(ReceiptNo.as_view()), name='receipt_no'),
)
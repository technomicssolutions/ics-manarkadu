
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.conf import settings

from admission.views import GetStudent,AddStudent,ListStudent,ViewStudentDetails,EditStudentDetails,\
DeleteStudentDetails, EnquiryView, SearchEnquiry, EnquiryDetails, StudentAdmission, EnquiryReport, \
StudentSearch, GetInstallmentDetails,AllEnquiries, DeleteEnquiry, AdmissionReport, FollowUpReport, \
EnquiryToAdmission, AdmissionCardView

urlpatterns = patterns('',
	url(r'^get_student/(?P<course_id>\d+)/$',login_required(GetStudent.as_view()), name="get_student"),
	url(r'^add_student/$',login_required(AddStudent.as_view()), name='add_student'),
	# # url(r'^edit_student/$', Editstudent.as_view(), name='edit_student'),
	url(r'^list_student/$',login_required(ListStudent.as_view()), name='list_student'),
	url(r'^view_student_details/(?P<student_id>\d+)/$',login_required(ViewStudentDetails.as_view()), name="view_student_details"),
	url(r'^edit_student_details/(?P<student_id>\d+)/$',login_required(EditStudentDetails.as_view()), name="edit_student_details"),
	url(r'^delete_student_details/(?P<student_id>\d+)/$',login_required(DeleteStudentDetails.as_view()), name="delete_student_details"),
	

	url(r'^enquiry/$',login_required(EnquiryView.as_view()), name='enquiry'),
	url(r'^enquiry_details/$',login_required(EnquiryDetails.as_view()), name='enquiry_details'),
	url(r'^all_enquiries/$',login_required(AllEnquiries.as_view()), name='all_enquiries'),
	url(r'^delete_enquiry/(?P<enquiry_id>\d+)/$',login_required(DeleteEnquiry.as_view()), name="delete_enquiry"),
	url(r'^enquiry_search/$',login_required(SearchEnquiry.as_view()), name='enquiry_search'),
	
	url(r'^student_admission/$', login_required(StudentAdmission.as_view()), name='student_admission'),
	url(r'^enquiry_report/$',login_required(EnquiryReport.as_view()), name='enquiry_report'),
	url(r'^admission_report/$',login_required(AdmissionReport.as_view()), name='admission_report'),
	url(r'^search_student/$',login_required(StudentSearch.as_view()), name='search_student'),
	url(r'^get_installment_details/$', login_required(GetInstallmentDetails.as_view()), name='get_installment_details'),
	url(r'^follow_up_details/$', login_required(FollowUpReport.as_view()), name='follow_up_details'),
	url(r'^enquiry_to_admission/$', login_required(EnquiryToAdmission.as_view()), name='enquiry_to_admission'),
	url(r'^admission_card/$', login_required(AdmissionCardView.as_view()), name='admission_card'),
	
)
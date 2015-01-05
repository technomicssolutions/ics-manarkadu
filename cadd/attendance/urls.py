from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from attendance.views import AddAttendance, AttendanceDetails, BatchStudents, JobCard, AttendanceReport, TopicsCovered

urlpatterns = patterns('',
	url(r'^batch_students/(?P<batch_id>\d+)/$',login_required (BatchStudents.as_view()), name="batch_students"),
	url(r'^job_card/$',login_required(JobCard.as_view()), name='job_card'),
	url(r'^add_attendance/$',login_required(AddAttendance.as_view()), name='add_attendance'),
	url(r'^attendance_details/$',login_required(AttendanceDetails.as_view()), name='attendance_details'),

	url(r'^attendance_report/$',login_required(AttendanceReport.as_view()), name='attendance_report'),
	url(r'^topics_covered/$',login_required(TopicsCovered.as_view()), name='topics_covered'),
)
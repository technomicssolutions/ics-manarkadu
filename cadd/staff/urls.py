from django.conf.urls import patterns, include, url

from django.conf import settings
from django.contrib.auth.decorators import login_required

from staff.views import AddStaff, ListStaff, DeleteStaffDetails, IsUsernameExists, PermissionSetting, SearchStaff

urlpatterns = patterns('',
	url(r'^add_staff/$', login_required (AddStaff.as_view()), name='add_staff'),
	url(r'^staffs/$',login_required( ListStaff.as_view()), name='staffs'),
	url(r'^delete_staff_details/(?P<staff_id>\d+)/$',login_required( DeleteStaffDetails.as_view()), name="delete_staff_details"),
	url(r'^search_staff/$',login_required( SearchStaff.as_view()), name='serach_staff'),

	url(r'^is_username_exists/$', login_required(IsUsernameExists.as_view()), name='is_username_exists'), 
	url(r'^permissions/$', login_required(PermissionSetting.as_view()), name='permissions'),
)
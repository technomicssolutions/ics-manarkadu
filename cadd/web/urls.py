from django.conf.urls import patterns, include, url

from django.conf import settings
from django.contrib.auth.decorators import login_required

from web.views import Home, ResetPassword, Login, Logout, Letters, DeleteLetter, Certificates, \
	AddCertificate, DeleteCertificate, LetterList

urlpatterns = patterns('',
	
	url(r'^$', Home.as_view(), name='home'),
	url(r'login/$',  Login.as_view(), name='login'),
    url(r'logout/$', Logout.as_view(), name='logout'),

	url(r'letters/$', Letters.as_view(), name='letters'),    
	url(r'^delete_letter/(?P<letter_id>\d+)/$',login_required(DeleteLetter.as_view()), name='delete_letter'),
	url(r'^letter_list/$', login_required(LetterList.as_view()), name="letter_list"),

	url(r'add_certificate/$', AddCertificate.as_view(), name='add_certificate'),    
	url(r'certificate/$', Certificates.as_view(), name='certificate'), 
	url(r'^delete_certificate/(?P<certificate_id>\d+)/$',login_required (DeleteCertificate.as_view()), name='delete_certificate'),
	
    
    url(r'^reset_password/(?P<user_id>\d+)/$', login_required(ResetPassword.as_view()), name="reset_password"),
	
)
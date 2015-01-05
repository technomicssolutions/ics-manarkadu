from django.contrib import admin
from fees.models import *

admin.site.register(FeesPayment)
admin.site.register(FeesPaymentInstallment)
admin.site.register(FeesPaid)

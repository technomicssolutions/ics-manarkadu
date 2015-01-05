from django.core.management.base import BaseCommand
import datetime
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.conf import settings

from admission.models import Student, Enquiry, Installment, FollowUp
from fees.models import FeesPayment
text_content = 'This is an Important Message'
from_email = settings.DEFAULT_FROM_EMAIL
follow_up_mail_id = settings.FOLLOW_UP_MAIL_ID

class Command(BaseCommand):
    help = "Create initial test user and pre-requisite data"

    def handle(self, *args, **options):

        date = datetime.datetime.now()
        current_date = date.date()
        # Reminder about the next follow up
        try:
            follow_ups = FollowUp.objects.filter(follow_up_date__year=current_date.year, follow_up_date__month=current_date.month, follow_up_date__day=current_date.day)
            follow_up_list = []
            for follow_up in follow_ups:
                enquiries = follow_up.enquiry_set.filter(is_admitted=False)
                for enquiry in enquiries:
                    follow_up_list.append({
                        'name': enquiry.student_name,
                        'enquiry_no': enquiry.auto_generated_num,
                        'date': enquiry.saved_date.strftime('%d/%m/%Y'),
                        'mobile': enquiry.mobile_number,
                        'email': enquiry.email,
                    })
            subject = "Today's Follow Ups"
            
            # for enquiry in current_follow_ups:
                
            ctx = {
                'enquiries': follow_up_list,
            }
            html_content = render_to_string('email/follow_up_reminder.html', ctx)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [follow_up_mail_id])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid Header Found')
        except Exception as ex:
            print str(ex)

        # Reminder about the Fees collection, 2 days before the due date of the installment

        try:
            students = Student.objects.all()
            for student in students:
                i = 0
                is_not_paid = False
                ctx_installments = []
                for installment in student.installments.all():
                    try:
                        fees_payment = FeesPayment.objects.get(student__id=student.id)
                        fees_payment_installments = fees_payment.payment_installment.filter(installment=installment)
                        if fees_payment_installments.count() > 0:
                            if fees_payment_installments[0].installment_amount < installment.amount:
                                is_not_paid = True
                                ctx_installments.append({
                                    'amount':installment.amount,
                                    'due_date': installment.due_date.strftime('%d/%m/%Y'),
                                    'fine': installment.fine_amount,
                                    'name':'installment'+str(i + 1),
                                })
                        elif fees_payment_installments.count() == 0:
                            diff = (installment.due_date - current_date).days
                            if current_date >= installment.due_date or diff <= 2:
                                is_not_paid = True
                                ctx_installments.append({
                                    'amount':installment.amount,
                                    'due_date': installment.due_date.strftime('%d/%m/%Y'),
                                    'fine': installment.fine_amount,
                                    'name':'installment'+str(i + 1),
                                })
                    except Exception as ex:
                        diff = (installment.due_date - current_date).days
                        if current_date >= installment.due_date or diff <= 2:
                            is_not_paid = True
                            ctx_installments.append({
                                'amount':installment.amount,
                                'due_date': installment.due_date.strftime('%d/%m/%Y'),
                                'fine_amount': installment.fine_amount,
                                'name':'installment'+str(i + 1),
                            })
                    i = i + 1
                if is_not_paid:
                    subject = "Fees Payment Reminder"
                    ctx = {
                        'payment': {
                            'installments': ctx_installments,
                            'student_name': student.student_name,
                        },
                    }
                    html_content = render_to_string('email/fees_payment_reminder.html', ctx)
                    if student.email != 'undefined':
                        send_email_id = student.email
                    else:
                        if student.enquiry:
                            send_email_id = student.enquiry.email
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [send_email_id])
                    msg.attach_alternative(html_content, "text/html")
                    try:
                        msg.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid Header Found')
                    
        except Exception as ex:
            print str(ex), 'except'






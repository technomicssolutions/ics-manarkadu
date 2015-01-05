
import simplejson
import ast
import datetime as dt

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4

from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from fees.models import *
from datetime import datetime

style = [
    ('FONTSIZE', (0,0), (-1, -1), 12),
    ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
]

para_style = ParagraphStyle('fancy')
para_style.fontSize = 12
para_style.fontName = 'Helvetica'

class FeesPaymentSave(View):

    def get(self, request, *args, **kwargs):
        current_date = dt.datetime.now().date()
        context = {
            
           'current_date': current_date.strftime('%d/%m/%Y'),

        }
        return render(request, 'fees_payment.html',context)

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            status_code = 200 
            try:
                fees_payment_details = ast.literal_eval(request.POST['fees_payment'])
                student = Student.objects.get(id=fees_payment_details['student'])
                if student.is_rolled:
                    student.is_rolled = False
                fees_payment, created = FeesPayment.objects.get_or_create(student=student)
                installment = Installment.objects.get(id=fees_payment_details['installment_id'])
                fee_payment_installment, installment_created = FeesPaymentInstallment.objects.get_or_create(installment=installment, student=student)
                fee_payment_installment.installment_amount = installment.amount
                
                if installment_created:
                    fee_payment_installment.paid_amount = fees_payment_details['paid_amount']
                    fee_payment_installment.installment_fine = fees_payment_details['paid_fine_amount']
                    fee_payment_installment.fee_waiver_amount = fees_payment_details['fee_waiver']
                else:
                    fee_payment_installment.paid_amount = float(fee_payment_installment.paid_amount) + float(fees_payment_details['paid_amount'])
                    fee_payment_installment.installment_fine = float(fee_payment_installment.installment_fine) + float(fees_payment_details['paid_fine_amount'])
                    fee_payment_installment.fee_waiver_amount = float(fee_payment_installment.fee_waiver_amount)  + float(fees_payment_details['fee_waiver'])
                # fee_payment_installment.paid_date = datetime.strptime(fees_payment_details['paid_date'], '%d/%m/%Y')
                fee_payment_installment.total_amount = fees_payment_details['total_amount']
                fee_payment_installment.save()
                fees_paid = FeesPaid()
                fees_paid.paid_date = datetime.strptime(fees_payment_details['paid_date'], '%d/%m/%Y')
                fees_paid.fees_payment_installment = fee_payment_installment
                fees_paid.paid_amount = fees_payment_details['paid_amount']
                #fees_paid.fee_waiver_amount = fees_payment_details['fee_waiver']
                fees_paid.paid_fine_amount = fees_payment_details['paid_fine_amount']
                fees_paid.save()
                fees_payment.payment_installment.add(fee_payment_installment)
                res = {
                    'result': 'ok',
                }
            except Exception as Ex:
                res = {
                    'result': 'error: '+str(Ex),
                    'message': 'Already Paid',
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")

class ListOutStandingFees(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'list_outstanding_fees.html',{})

class GetOutStandingFeesDetails(View):

    def get(self, request, *args, **kwargs):

        current_date = datetime.now().date()
        status = 200
        if request.is_ajax():
            student_id = request.GET.get('student_id', '')
            course = request.GET.get('course','')
            fees_details = []
            if student_id:
                student = Student.objects.get(id=student_id)
                i = 0
                is_not_paid = False
                ctx_installments = []
                for installment in student.installments.all():
                    try:
                        fees_payment = FeesPayment.objects.get(student__id=student_id)
                        fees_payment_installments = fees_payment.payment_installment.filter(installment=installment)
                        if current_date >= installment.due_date:
                            if (float(fees_payment_installments[0].paid_amount) + float(fees_payment_installments[0].fee_waiver_amount)) < installment.amount:
                                if fees_payment_installments[0].paid_amount < installment.amount:
                                    is_not_paid = True
                                    ctx_installments.append({
                                        'id': installment.id,
                                        'amount':installment.amount,
                                        'due_date': installment.due_date.strftime('%d/%m/%Y'),
                                        'fine_amount': installment.fine_amount,
                                        'name':'installment'+str(i + 1),
                                        'paid_installment_amount': fees_payment_installments[0].paid_amount,
                                        'balance': float(installment.amount) - (float(fees_payment_installments[0].paid_amount) + float(fees_payment_installments[0].fee_waiver_amount)),
                                    })
                        elif fees_payment_installments.count() == 0:
                            if current_date >= installment.due_date:
                                is_not_paid = True
                                ctx_installments.append({
                                    'id': installment.id,
                                    'amount':installment.amount,
                                    'due_date': installment.due_date.strftime('%d/%m/%Y'),
                                    'fine_amount': installment.fine_amount,
                                    'name':'installment'+str(i + 1),
                                    'paid_installment_amount': 0,
                                    'balance': float(installment.amount),
                                })
                    except Exception as ex:
                        if current_date >= installment.due_date:
                            is_not_paid = True
                            ctx_installments.append({
                                'id': installment.id,
                                'amount':installment.amount,
                                'due_date': installment.due_date.strftime('%d/%m/%Y'),
                                'fine_amount': installment.fine_amount,
                                'name':'installment'+str(i + 1),
                                'paid_installment_amount': 0,
                                'balance': float(installment.amount),
                            })
                    i = i + 1
                if is_not_paid:
                    fees_details.append({
                        'no_installments': student.no_installments,
                        'installments': ctx_installments,
                        'student_name': student.student_name,
                        'roll_no': student.roll_number,
                    })
                res = {
                    'result':'ok',
                    'fees_details': fees_details,
                    'student_name': student.student_name,
                    'roll_no': student.roll_number,
                }
            elif course:
                students = Student.objects.filter(course__id=course)
                student_details = []
                for student in students:
                    i = 0
                    is_not_paid = False
                    ctx_installments = []
                    for installment in student.installments.all():
                        try:
                            fees_payment = FeesPayment.objects.get(student__id=student.id)
                            fees_payment_installments = fees_payment.payment_installment.filter(installment=installment)
                            if fees_payment_installments.count() > 0:
                                if current_date >= installment.due_date:
                                    if (float(fees_payment_installments[0].paid_amount) + float(fees_payment_installments[0].fee_waiver_amount)) < installment.amount:
                                        is_not_paid = True
                                        ctx_installments.append({
                                            'id': installment.id,
                                            'amount':installment.amount,
                                            'due_date': installment.due_date.strftime('%d/%m/%Y'),
                                            'fine_amount': installment.fine_amount,
                                            'name':'installment'+str(i + 1),
                                            'paid_installment_amount': fees_payment_installments[0].paid_amount,
                                            'balance': float(installment.amount) - (float(fees_payment_installments[0].paid_amount) + float(fees_payment_installments[0].fee_waiver_amount)),
                                        })
                            elif fees_payment_installments.count() == 0:
                                if current_date >= installment.due_date:
                                    is_not_paid = True
                                    ctx_installments.append({
                                        'id': installment.id,
                                        'amount':installment.amount,
                                        'due_date': installment.due_date.strftime('%d/%m/%Y'),
                                        'fine_amount': installment.fine_amount,
                                        'name':'installment'+str(i + 1),
                                        'paid_installment_amount': 0,
                                        'balance': float(installment.amount),
                                    })
                        except Exception as ex:
                            if current_date >= installment.due_date:
                                is_not_paid = True
                                ctx_installments.append({
                                    'id': installment.id,
                                    'amount':installment.amount,
                                    'due_date': installment.due_date.strftime('%d/%m/%Y'),
                                    'fine_amount': installment.fine_amount,
                                    'name':'installment'+str(i + 1),
                                    'paid_installment_amount': 0,
                                    'balance': float(installment.amount),
                                })
                        i = i + 1
                    if is_not_paid :
                        student_details.append({
                            'no_installments': student.no_installments,
                            'installments': ctx_installments,
                            'student_id' : student.id,
                            'student_name': student.student_name,
                            'is_rolled': 'true' if student.is_rolled else 'false',
                            'roll_no': student.roll_number,
                        })
                fees_details.append({
                    'student_details': student_details,
                })

                res = {
                    'result':'ok',
                    'fees_details': fees_details,
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class PrintOutstandingFeesReport(View):

    def get(self, request, *args, **kwargs):

        response = HttpResponse(content_type='application/pdf')
        p = SimpleDocTemplate(response, pagesize=A4)
        current_date = datetime.now().date()
        elements = []
        try:  
            student = Student.objects.get(id=request.GET.get('student', ''))
        except:
            return render(request, 'list_outstanding_fees.html', {})
        d = [['Outstanding fees details - '+ student.student_name]]
        t = Table(d, colWidths=(450), rowHeights=25, style=style)
        t.setStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                    ('FONTSIZE', (0,0), (-1,-1), 17),
                    ])   
        elements.append(t)
        elements.append(Spacer(4, 5))
        data_list = []
        i = 0
        is_not_paid = False
        for installment in student.installments.all():
            try:
                fees_payment = FeesPayment.objects.get(student__id=student.id)
                fees_payment_installments = fees_payment.payment_installment.filter(installment=installment)
                if fees_payment_installments.count() > 0:
                    if current_date >= installment.due_date:
                        if (float(fees_payment_installments[0].paid_amount) + float(fees_payment_installments[0].fee_waiver_amount)) < installment.amount:
                                is_not_paid = True
                                data_list.append({
                                    'id': installment.id,
                                    'amount':installment.amount,
                                    'due_date': installment.due_date.strftime('%d/%m/%Y'),
                                    'fine_amount': installment.fine_amount,
                                    'name':'installment'+str(i + 1),
                                    'paid_installment_amount': fees_payment_installments[0].paid_amount,
                                    'balance': float(installment.amount) - (float(fees_payment_installments[0].paid_amount) + float(fees_payment_installments[0].fee_waiver_amount)),
                                })
                elif fees_payment_installments.count() == 0:
                    if current_date >= installment.due_date:
                        is_not_paid = True
                        data_list.append({
                            'id': installment.id,
                            'amount':installment.amount,
                            'due_date': installment.due_date.strftime('%d/%m/%Y'),
                            'fine_amount': installment.fine_amount,
                            'name':'installment'+str(i + 1),
                            'paid_installment_amount': 0,
                            'balance': float(installment.amount),
                        })
            except Exception as ex:
                if current_date >= installment.due_date:
                    is_not_paid = True
                    data_list.append({
                        'id': installment.id,
                        'amount':installment.amount,
                        'due_date': installment.due_date.strftime('%d/%m/%Y'),
                        'fine_amount': installment.fine_amount,
                        'name':'installment'+str(i + 1),
                        'paid_installment_amount': 0,
                        'balance': float(installment.amount),
                    })
            i = i + 1
        d = []
        d.append(['Name', 'Amount', 'Due Date', 'Fine', 'Paid', 'Balance'])
        if is_not_paid:
            for data in data_list:
                d.append([data['name'], data['amount'], data['due_date'], data['fine_amount'], data['paid_installment_amount'], data['balance']])
        table = Table(d, colWidths=(100, 100, 75, 100, 100,100),  style=style)
        table.setStyle([('ALIGN',(0,-1),(0,-1),'LEFT'),
                    ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                    ('FONTNAME', (0, -1), (-1,-1), 'Helvetica'),
                    ])
        elements.append(table)
        p.build(elements)        
        return response

class FeepaymentReport(View):

    def get(self, request, *args, **kwargs):
        date = datetime.now().date()
        report_type = request.GET.get('report_type')
        if report_type == 'course_wise' :
            course =  request.GET.get('course')
            students = Student.objects.filter(course=course)
            response = HttpResponse(content_type='application/pdf')
            p = SimpleDocTemplate(response, pagesize=A4)
            elements = []        
            d = [['FeesPayment Report']]

            t = Table(d, colWidths=(450), rowHeights=25, style=style)
            t.setStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('FONTSIZE', (0,0), (0,0), 20),
                        ('FONTSIZE', (1,0), (-1,-1), 17),
                        ])   
            elements.append(t)
            elements.append(Spacer(4, 5))
            data = []
            data.append(['Student' , 'Installment','Installment Amount','Paid date','Paid Amount'])
            for student in students:
                try:
                    fees_payment = FeesPayment.objects.get(student=student)
                    if fees_payment.payment_installment.count > 0 :
                        for fee_payment_installment in fees_payment.payment_installment.all().order_by('-id'):
                            for payment in fee_payment_installment.feespaid_set.all():
                                data.append([Paragraph(student.student_name, para_style), 'Installment' +str(fee_payment_installment.installment.id), fee_payment_installment.total_amount,payment.paid_date.strftime('%d/%m/%Y'), payment.paid_amount])
                except Exception as ex:
                    print str(ex)
            table = Table(data, colWidths=(100, 100, 150,100,100),  style=style)
            table.setStyle([('ALIGN',(0,-1),(0,-1),'LEFT'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('BACKGROUND',(0, 0),(-1,-1),colors.white),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ('FONTNAME', (0, -1), (-1,-1), 'Helvetica'),
                        ])   
            elements.append(table)  
            p.build(elements)      
            return response
        elif report_type == 'student_wise':
            student_id = request.GET.get('student_id')
            student = Student.objects.get(id=student_id)
            response = HttpResponse(content_type='application/pdf')
            p = SimpleDocTemplate(response, pagesize=A4)
            elements = []        
            d = [['FeesPayment Report']]
            t = Table(d, colWidths=(450), rowHeights=25, style=style)
            t.setStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('FONTSIZE', (0,0), (0,0), 20),
                        ('FONTSIZE', (1,0), (-1,-1), 17),
                        ])   
            elements.append(t)
            elements.append(Spacer(4, 5))
            d = [['Student: '+student.student_name], ['Course: '+student.course.name]]
            t = Table(d, colWidths=(450), style=style)
            t.setStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('FONTSIZE', (0,0), (-1,-1), 12),
                        ])   
            elements.append(t)
            elements.append(Spacer(4, 5))
            try:
                fees_payment = FeesPayment.objects.get(student=student)
                data = []
                data.append(['Installment' ,'Installment Amount','Paid date','Paid Amount'])
                if fees_payment.payment_installment.count > 0 :
                    for fee_payment_installment in fees_payment.payment_installment.all().order_by('-id'):
                        for payment in fee_payment_installment.feespaid_set.all():
                            data.append(['Installment'+str(fee_payment_installment.installment.id), fee_payment_installment.total_amount,payment.paid_date.strftime('%d/%m/%Y'),payment.paid_amount])
                table = Table(data, colWidths=(100,150,100,100),  style=style)
                table.setStyle([('ALIGN',(0,-1),(0,-1),'LEFT'),
                            ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                            ('BACKGROUND',(0, 0),(-1,-1),colors.white),
                            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                            ('FONTNAME', (0, -1), (-1,-1), 'Helvetica'),
                        ])   
                elements.append(table)
            except Exception as ex:
                print str(ex) 
            p.build(elements)        
            return response 
        elif report_type == 'date_wise':
            date = request.GET.get('date', '')
            date = datetime.strptime(date, '%d/%m/%Y')
            response = HttpResponse(content_type='application/pdf')
            p = SimpleDocTemplate(response, pagesize=A4)
            elements = []        
            d = [['FeesPayment Report']]

            t = Table(d, colWidths=(450), rowHeights=25, style=style)
            t.setStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('FONTSIZE', (0,0), (0,0), 20),
                        ('FONTSIZE', (1,0), (-1,-1), 17),
                        ])   
            elements.append(t)
            elements.append(Spacer(4, 5))
            data = []
            data.append(['Student' , 'Installment','Installment Amount','Paid date','Paid Amount'])
            
            try:
                fee_paids = FeesPaid.objects.filter(paid_date=date)
                print fee_paids
                for fee_payed in fee_paids:
                    print fee_payed.fees_payment_installment.id
                    fees_payment_installment = FeesPaymentInstallment.objects.get(id=fee_payed.fees_payment_installment.id)
                    # print fees_payment_installment
                    data.append([Paragraph(fees_payment_installment.student.student_name, para_style), 'Installment' +str(fees_payment_installment.installment.id), fees_payment_installment.total_amount,fee_payed.paid_date.strftime('%d/%m/%Y'), fee_payed.paid_amount])
            except Exception as ex:
                print str(ex)
            table = Table(data, colWidths=(100, 100, 150,100,100),  style=style)
            table.setStyle([('ALIGN',(0,-1),(0,-1),'LEFT'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('BACKGROUND',(0, 0),(-1,-1),colors.white),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ('FONTNAME', (0, -1), (-1,-1), 'Helvetica'),
                        ])   
            elements.append(table)  
            p.build(elements)      
            return response      
        else:
            return render(request, 'fee_collected_report.html',{})            

class UnRollStudent(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            student_id = request.GET.get('student_id','')
            try:
                student = Student.objects.get(id=student_id)
                student.is_rolled = True
                student.save()
                res = {
                    'result': 'ok',
                }
                status = 200
                response = simplejson.dumps(res)
                return HttpResponse(response, status=status, mimetype='application/json')
            except:
                res = {
                    'result': 'error',
                }
                status = 200
                response = simplejson.dumps(res)
                return HttpResponse(response, status=status, mimetype='application/json')
        return render(request, 'unroll_students.html',{})  

class RollStudent(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            student_id = request.GET.get('student_id','')
            try:
                student = Student.objects.get(id=student_id)
                student.is_rolled = False
                student.save()
                res = {
                    'result': 'ok',
                }
                status = 200
                response = simplejson.dumps(res)
                return HttpResponse(response, status=status, mimetype='application/json')
            except:
                res = {
                    'result': 'error',
                }
                status = 200
                response = simplejson.dumps(res)
                return HttpResponse(response, status=status, mimetype='application/json')
        return render(request, 'unroll_students.html',{})  

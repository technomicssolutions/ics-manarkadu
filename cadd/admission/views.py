
import simplejson
import ast
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics

from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from admission.models import Student, Enquiry, Installment, FollowUp
from college.models import Course, Batch
from datetime import datetime
from fees.models import FeesPayment

style = [
    ('FONTSIZE', (0,0), (-1, -1), 12),
    ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
]

para_style = ParagraphStyle('fancy')
para_style.fontSize = 12
para_style.fontName = 'Helvetica'

class AddStudent(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                course = Course.objects.get(id = request.POST['course'])
                enquiry = None
                if request.POST.get('enquiry', ''):
                    if request.POST.get('enquiry', '') != 'undefined':
                        enquiry = Enquiry.objects.get(id=request.POST['enquiry'])

                student, created = Student.objects.get_or_create(roll_number = request.POST['roll_number'], course=course)
                if not created:
                    res = {
                        'result': 'error',
                        'message': 'Student with this roll no already existing'
                    }
                else:
                    try:
                        batches = request.POST['batch'].split(',')
                        for batch in batches:
                            batch_obj = Batch.objects.get(id = batch)
                            if batch_obj.no_of_students == None:
                                batch_obj.no_of_students = 1
                            else:
                                batch_obj.no_of_students = batch_obj.no_of_students + 1
                            batch_obj.save()
                            student.batches.add(batch_obj)
                        student.student_name = request.POST['student_name']
                        if enquiry is not None:
                            student.enquiry = enquiry
                            enquiry.is_admitted = True;
                            enquiry.save()
                        student.roll_number = request.POST['roll_number']
                        student.address = request.POST['address']
                        if request.POST['qualifications'] != 'undefined':
                            student.qualifications = request.POST['qualifications']
                        student.course=course
                        student.batch=batch
                        student.dob = datetime.strptime(request.POST['dob'], '%d/%m/%Y')
                        student.address = request.POST['address']
                        student.mobile_number = request.POST['mobile_number']
                        if request.POST['email'] != 'undefined':
                            student.email = request.POST['email']
                        student.blood_group = request.POST['blood_group']
                        student.doj = datetime.strptime(request.POST['doj'], '%d/%m/%Y')
                        student.photo = request.FILES.get('photo_img', '')                       
                        student.certificates_submitted = request.POST['certificates_submitted']
                        student.id_proofs_submitted = request.POST['id_proofs_submitted']
                        student.guardian_name = request.POST['guardian_name']
                        student.relationship = request.POST['relationship']
                        student.guardian_mobile_number = request.POST['guardian_mobile_number']
                        student.fees = request.POST['fees'] 
                        student.balance = request.POST['fees']
                        student.discount = request.POST['discount']          
                        student.no_installments = request.POST['no_installments']
                        installments = ast.literal_eval(request.POST['installments'])
                        for installment in installments:
                            installmet = Installment()
                            installmet.amount = installment['amount']
                            if installment.get('fine', ''):
                                installmet.fine_amount = installment['fine']
                            installmet.due_date = datetime.strptime(installment['due_date'], '%d/%m/%Y')
                            installmet.save()
                            student.installments.add(installmet)
                            student.save()
                    except Exception as ex:
                        res = {
                            'result': 'error',
                            'message': str(ex)
                        }
                    student.save()
                    res = {
                        'result': 'ok',
                    }                     
            except Exception as ex:
                res = {
                    'result': 'error',
                    'message': str(ex)
                }
            status_code = 200 
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")
        return render(request, 'list_student.html', {})

class ListStudent(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get('batch_id', ''):
            batch = Batch.objects.get(id=request.GET.get('batch_id', ''))
            students = batch.student_set.all()
        else:
            students = Student.objects.all().order_by('roll_number')  
        if request.is_ajax():
            student_list = []
            for student in students:
                student_list.append({
                    'id': student.id,
                    'name': student.student_name,
                    'roll_number': student.roll_number,
                })            
            response = simplejson.dumps({
                'result': 'Ok',
                'students': student_list
            })
            return HttpResponse(response, status = 200, mimetype="application/json")
        ctx = {
            'students': students
        }
        return render(request, 'list_student.html',ctx)



class GetStudent(View):

    def get(self, request, *args, **kwargs):
        course_id = kwargs['course_id']
        if request.is_ajax():
            try:
                students = Student.objects.filter(course__id=course_id)
                student_list = []
                for student in students:
                    student_list.append({
                        'student': student.student_name,
                        'id' : student.id,
                        'fees': student.fees,
                    })
                res = {
                    'result': 'ok',
                    'students': student_list,
                }
            except Exception as ex:
                res = {
                    'result': 'error: '+ str(ex),
                }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class ViewStudentDetails(View):  

    def get(self, request, *args, **kwargs):
        
        student_id = kwargs['student_id']
        ctx_student_data = []
        if request.is_ajax():
            try:
                student = Student.objects.get(id = student_id)
                ctx_student_data.append({
                'student_name': student.student_name if student.student_name else '',
                'roll_number': student.roll_number if student.roll_number else '',
                'dob': student.dob.strftime('%d/%m/%Y') if student.dob else '',
                'address': student.address if student.address else '',
                'course': student.course.id if student.course else '',
                'batch' :student.batch.id if student.batch else '',
                'mobile_number': student.mobile_number if student.mobile_number else '',
                'email': student.email if student.email else '',
                'blood_group': student.blood_group if student.blood_group else '',
                'doj': student.doj.strftime('%d/%m/%Y') if student.doj else '',
                'photo': student.photo.name if student.photo.name else '',
                'certificates_submitted': student.certificates_submitted if student.certificates_submitted else '',
                'id_proofs_submitted': student.id_proofs_submitted if student.id_proofs_submitted else '',
        
                'guardian_name': student.guardian_name if student.guardian_name else '',
                
                'relationship': student.relationship if student.relationship else '',
                'guardian_mobile_number': student.guardian_mobile_number if student.guardian_mobile_number else '',
                })
                res = {
                    'result': 'ok',
                    'student': ctx_student_data,
                }
            except Exception as ex:
                res = {
                    'result': 'error: ' + str(ex),
                    'student': ctx_student_data,
                }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class EditStudentDetails(View):
   
    def get(self, request, *args, **kwargs):
        
        student_id = kwargs['student_id']
        context = {
            'student_id': student_id,
        }
        ctx_student_data = []
        batch_details = []
        installment_list = []
        student = Student.objects.get(id=student_id)
        if request.is_ajax():
            for batch in student.batches.all():
                batch_details.append({
                    'id': batch.id,
                    'name': batch.name,
                })
            installments = student.installments.all()
            for installment in installments:
                installment_list.append({
                    'id': installment.id,
                    'amount': installment.amount,
                    'due_date': installment.due_date.strftime('%d/%m/%Y'),
                    'fine': installment.fine_amount if installment.fine_amount else '',
                    'due_date_id': installment.id,
                })
            ctx_student_data.append({
                'student_id': student.id,
                'student_name': student.student_name if student.student_name else '',
                'roll_number': student.roll_number if student.roll_number else '',
                'unique_id': student.unique_id if student.unique_id else '',
                'cadd_registration_no': student.cadd_registration_no if student.cadd_registration_no else '',
                'dob': student.dob.strftime('%d/%m/%Y') if student.dob else '',
                'address': student.address if student.address else '',
                'course': student.course.id if student.course else '',
                'batches' : batch_details,
                'mobile_number': student.mobile_number if student.mobile_number else '',
                'email': student.email if student.email else '',
                'blood_group': student.blood_group if student.blood_group else '',
                'doj': student.doj.strftime('%d/%m/%Y') if student.doj else '',
                'photo': student.photo.name if student.photo.name else '',
                'qualifications': student.qualifications if student.qualifications else '',
                'certificates_submitted': student.certificates_submitted if student.certificates_submitted else '',
                'id_proofs_submitted': student.id_proofs_submitted if student.id_proofs_submitted else '',
                'guardian_name': student.guardian_name if student.guardian_name else '',
                'relationship': student.relationship if student.relationship else '',
                'guardian_mobile_number': student.guardian_mobile_number if student.guardian_mobile_number else '',
                'fees': student.course.amount if student.course else '',
                'fees_after_discount' : student.fees if student else '',
                'discount': student.discount if student.discount else '',
                'no_installments': student.no_installments if student.no_installments else '',
                'installments': installment_list,
                })
            res = {
                'result': 'ok',
                'student': ctx_student_data,
            }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        return render(request, 'edit_student_details.html',context)

    def post(self, request, *args, **kwargs):

        student_data = ast.literal_eval(request.POST['student'])
        student_id = student_data['student_id']
        student = Student.objects.get(id = student_id)
        try:
            student.student_name = student_data['student_name']
            student.roll_number = student_data['roll_number']
            student.address = student_data['address']
            course = Course.objects.get(id = student_data['course'])
            student.course=course
            student.batches.clear()
            batches = student_data['batch']
            for batch in batches:
                batch_obj = Batch.objects.get(id = batch)
                if batch_obj.no_of_students == None:
                    batch_obj.no_of_students = 1
                else:
                    batch_obj.no_of_students = batch_obj.no_of_students + 1
                batch_obj.save()
                student.batches.add(batch_obj)
            student.dob = datetime.strptime(student_data['dob'], '%d/%m/%Y')
            student.address = student_data['address']
            student.mobile_number = student_data['mobile_number']
            student.cadd_registration_no = student_data['cadd_registration_no']
            student.email = student_data['email']
            student.blood_group = student_data['blood_group']
            student.doj = datetime.strptime(student_data['doj'], '%d/%m/%Y')
            if request.FILES.get('photo_img', ''):
                student.photo = request.FILES.get('photo_img', '')                       
            student.certificates_submitted = student_data['certificates_submitted']
            student.id_proofs_submitted = student_data['id_proofs_submitted']
            student.guardian_name = student_data['guardian_name']
            student.relationship = student_data['relationship']
            student.guardian_mobile_number = student_data['guardian_mobile_number']
            student.fees = student_data['fees_after_discount']
            student.balance = student_data['fees_after_discount']
            if student_data['discount']:
                student.discount = student_data['discount']
            student.no_installments = student_data['no_installments']
            installments = student_data['installments']
            for installment in installments:
                try:
                    installment_obj = Installment.objects.get(id=installment['id'])
                except:
                    installment_obj = Installment()
                installment_obj.amount = installment['amount']
                installment_obj.due_date = datetime.strptime(installment['due_date'], '%d/%m/%Y')
                if installment.get('fine', ''):
                    installment_obj.fine_amount = installment['fine']
                installment_obj.save()
                student.installments.add(installment_obj)
                student.save()
            student.save()
            res = {
                'result': 'ok',
            }
            status = 200
        except Exception as Ex:
            print str(Ex)
            res = {
                'result': 'error',
                'message': str(Ex)
            }
            status = 500
        response = simplejson.dumps(res)
        return HttpResponse(response, status=status, mimetype='application/json')

class DeleteStudentDetails(View):
    def get(self, request, *args, **kwargs):
        student_id = kwargs['student_id']       
        student = Student.objects.filter(id=student_id)                          
        student.delete()
        return HttpResponseRedirect(reverse('list_student'))

class EnquiryView(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            res = {
                'result': 'ok',
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'enquiry.html', {})

    def post(self, request, *args, **kwargs):

        
        if request.is_ajax():
            enquiry_details = ast.literal_eval(request.POST['enquiry'])
            if enquiry_details:
                enquiry = Enquiry()
                enquiry.mode = enquiry_details['mode']
                enquiry.student_name = enquiry_details['student_name']
                enquiry.address = enquiry_details['address']
                enquiry.mobile_number = enquiry_details['mobile_number']
                enquiry.email = enquiry_details['email']
                enquiry.details_about_clients_enquiry = enquiry_details['details_about_clients_enquiry']
                enquiry.educational_qualification = enquiry_details['educational_qualification']
                enquiry.land_mark = enquiry_details['land_mark']
                if enquiry_details['course'] != '':
                    course = Course.objects.get(id=enquiry_details['course'])
                    enquiry.course = course
                enquiry.remarks = enquiry_details['remarks']
                enquiry.save()
                follow_up_details = enquiry_details['follow_up']
                for follow_up in follow_up_details:
                    follow_up_obj = FollowUp()
                    follow_up_obj.follow_up_date = datetime.strptime(follow_up['follow_up_date'], '%d/%m/%Y')
                    follow_up_obj.remarks_for_follow_up_date = follow_up['remarks_for_follow_up_date']
                    follow_up_obj.save()
                    enquiry.follow_up.add(follow_up_obj)
                if enquiry_details['discount'] == '':
                    enquiry.discount = 0
                else:
                    enquiry.discount = enquiry_details['discount']
                enquiry.saved_date = datetime.strptime(enquiry_details['date'], '%d/%m/%Y')
                enquiry.save()
                enquiry.auto_generated_num = 'ENQ' + str(Enquiry.objects.latest('id').id)
                enquiry.save()
            res = {
                'result': 'ok',
                
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')

class EnquiryDetails(View):

    def get(self, request, *args, **kwargs): 
        if request.is_ajax():
            enquiry_list = []
            enquiry_num = request.GET.get('enquiry_num', '')
            enquiry_id = request.GET.get('enquiry_id', '')
            try:
                if enquiry_num :
                    enquiry = Enquiry.objects.get(auto_generated_num=enquiry_num)
                    enquiry_list.append({
                        'id': enquiry.id,
                        'student_name': enquiry.student_name,
                        'address': enquiry.address,
                        'mobile_number' : enquiry.mobile_number,
                        'email' : enquiry.email,
                        'details_about_clients_enquiry' : enquiry.details_about_clients_enquiry,
                        'educational_qualification': enquiry.educational_qualification,
                        'land_mark': enquiry.land_mark,
                        'course' : enquiry.course.id,
                        'remarks': enquiry.remarks,
                        'saved_date':enquiry.saved_date.strftime('%d/%m/%Y') if enquiry.saved_date else '',
                        
                        'discount': enquiry.discount,
                        'auto_generated_num': enquiry.auto_generated_num,
                    })
                elif enquiry_id :
                    enquiry = Enquiry.objects.get(id=enquiry_id)
                    enquiry_list.append({
                        'id': enquiry.id,
                        'student_name': enquiry.student_name,
                        'address': enquiry.address,
                        'mobile_number' : enquiry.mobile_number,
                        'email' : enquiry.email,
                        'details_about_clients_enquiry' : enquiry.details_about_clients_enquiry,
                        'educational_qualification': enquiry.educational_qualification,
                        'land_mark': enquiry.land_mark,
                        'course' : enquiry.course.name,
                        'remarks': enquiry.remarks,
                        'saved_date':enquiry.saved_date.strftime('%d/%m/%Y') if enquiry.saved_date else '',
                        'discount': enquiry.discount,
                        'auto_generated_num': enquiry.auto_generated_num,
                    })
            except Exception as ex:
                enquiry_list = []
            
            response = simplejson.dumps({
                'enquiry': enquiry_list,
            })    
            return HttpResponse(response, status=200, mimetype='application/json')

class AllEnquiries(View):
    def get(self, request, *args, **kwargs): 
        if request.is_ajax():
            enquiry_list = []
            enquiries = Enquiry.objects.all()
            for enquiry in enquiries:
                follow_up_details = []
                if not enquiry.is_admitted:
                    for follow_up in enquiry.follow_up.all():
                        follow_up_details.append({
                            'date': follow_up.follow_up_date.strftime('%d/%m/%Y'),
                            'remark': follow_up.remarks_for_follow_up_date
                        })
                    enquiry_list.append({
                        'id': enquiry.id,
                        'student_name': enquiry.student_name,
                        'address': enquiry.address,
                        'mobile_number' : enquiry.mobile_number,
                        'email' : enquiry.email,
                        'details_about_clients_enquiry' : enquiry.details_about_clients_enquiry,
                        'educational_qualification': enquiry.educational_qualification,
                        'land_mark': enquiry.land_mark,
                        'saved_date':enquiry.saved_date.strftime('%d/%m/%Y') if enquiry.saved_date else '',
                        'course' : enquiry.course.id,
                        'course_name':enquiry.course.name,
                        'remarks': enquiry.remarks,
                        'follow_ups': follow_up_details,
                        'discount': enquiry.discount,
                        'auto_generated_num': enquiry.auto_generated_num,
                    })
            response = simplejson.dumps({
                'enquiry': enquiry_list,
            })    
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'enquiry_list.html', {})

class DeleteEnquiry(View):
    def get(self, request, *args, **kwargs):
        enquiry_id = kwargs['enquiry_id']       
        enquiry = Enquiry.objects.filter(id=enquiry_id) 
        if not enquiry.is_admitted:
            enquiry.delete()
        return HttpResponseRedirect(reverse('all_enquiries'))
            
class SearchEnquiry(View):

    def get(self, request, *args, **kwargs):
        student_name = request.GET.get('student_name', '')
        enquiries = []
        q_list = []
        if student_name :
            enquiries = Enquiry.objects.filter(student_name__icontains=student_name,is_admitted=False)
            count = enquiries.count()
        else :
            enquiries = []
            count = 0
        enquiry_list = []
        for enquiry in enquiries:
            if not enquiry.is_admitted:
                enquiry_list.append({
                    'student_name': enquiry.student_name,
                    'address': enquiry.address,
                    'mobile_number' : enquiry.mobile_number,
                    'email' : enquiry.email,
                    'details_about_clients_enquiry' : enquiry.details_about_clients_enquiry,
                    'educational_qualification': enquiry.educational_qualification,
                    'land_mark': enquiry.land_mark,
                    'course' : enquiry.course.name,
                    'remarks': enquiry.remarks,
                    'discount': enquiry.discount,
                    'auto_generated_num': enquiry.auto_generated_num,
                    })
        if request.is_ajax():
            response = simplejson.dumps({
                'enquiries': enquiry_list,
                'count': count,
            })    
            return HttpResponse(response, status=200, mimetype='application/json')
        
class StudentAdmission(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'admission_details.html', {})

class EnquiryReport(View):

    def get(self, request, *args, **kwargs):
        
        date = datetime.now().date()
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if not start_date: 
            return render(request, 'enquiry_report.html', {})
        elif not end_date:
            return render(request, 'enquiry_report.html', {}) 
        else:
            start_date = datetime.strptime(start_date, '%d/%m/%Y')
            end_date = datetime.strptime(end_date, '%d/%m/%Y')
        try:
            enquiries = Enquiry.objects.filter( saved_date__gte=start_date,saved_date__lte=end_date).order_by('saved_date')
        except Exception as ex:
            res = {
                    'result': 'error',
                }
        if enquiries:
            if request.is_ajax():
                enquiry_list = []
                for enquiry in enquiries:
                    follow_up_details = []
                    for follow_up in enquiry.follow_up.all():
                        follow_up_details.append({
                            'date': follow_up.follow_up_date.strftime('%d/%m/%Y'),
                            'remark': follow_up.remarks_for_follow_up_date
                        })
                    enquiry_list.append({
                        'student_name': enquiry.student_name,
                        'address': enquiry.address,
                        'mobile_number' : enquiry.mobile_number,
                        'email' : enquiry.email,
                        'details_about_clients_enquiry' : enquiry.details_about_clients_enquiry,
                        'educational_qualification': enquiry.educational_qualification,
                        'land_mark': enquiry.land_mark,
                        'course' : enquiry.course.name,
                        'remarks': enquiry.remarks,
                        'follow_ups': follow_up_details,
                        'discount': enquiry.discount,
                        'auto_generated_num': enquiry.auto_generated_num,
                        'saved_date':enquiry.saved_date.strftime('%d/%m/%Y') if enquiry.saved_date else '',
                    })
                res = {
                        'result': 'ok',
                        'enquiries': enquiry_list,
                    }
                response = simplejson.dumps(res)
                return HttpResponse(response, status=200, mimetype='application/json')

        if request.GET.get('report_type',''):
            if enquiries:
                response = HttpResponse(content_type='application/pdf')
                p = SimpleDocTemplate(response, pagesize=A4)
                elements = []        
                d = [['Enquiry Report as at '+date.strftime('%d %B %Y')]]
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
                data_list = []
                data.append(['Date','Enquiry Number','Name','Course'])
                for enquiry in enquiries:
                    data.append([enquiry.saved_date.strftime('%d/%m/%Y') ,enquiry.auto_generated_num,Paragraph(enquiry.student_name,para_style), Paragraph(enquiry.course.name,para_style)])
                table = Table(data, colWidths=(100,100,100,100),  style=style)
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
                return render(request, 'enquiry_report.html',{'message':'No enquiries founds'})
        else:
            return render(request, 'enquiry_report.html',{})

class AdmissionReport(View):

    def get(self, request, *args, **kwargs):
        
        date = datetime.now().date()
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if not start_date: 
            return render(request, 'admission_report.html', {})
        elif not end_date:
            return render(request, 'admission_report.html', {}) 
        else:
            start_date = datetime.strptime(start_date, '%d/%m/%Y')
            end_date = datetime.strptime(end_date, '%d/%m/%Y')
        try:
            admissions = Student.objects.filter( doj__gte=start_date,doj__lte=end_date).order_by('doj')
        except Exception as ex:
            res = {
                    'result': 'error',
                }
        if admissions:
            if request.is_ajax():
                admission_list = []
                batch_list = []
                for admission in admissions:
                    batch_list = []
                    if admission.batches.all().count() > 0: 
                        for batch in admission.batches.all().order_by('-id'):
                            batch_list.append(batch.name)
                       
                    admission_list.append({
                        'student_name': admission.student_name,
                        'course' : admission.course.name,
                        'batch' : batch_list,
                        'saved_date': admission.doj.strftime('%d/%m/%Y') if admission.doj else '',
                    })
                res = {
                        'result': 'ok',
                        'admissions': admission_list,
                    }
                response = simplejson.dumps(res)
                return HttpResponse(response, status=200, mimetype='application/json')
        if request.GET.get('report_type',''):
            if admissions:
                response = HttpResponse(content_type='application/pdf')
                p = SimpleDocTemplate(response, pagesize=A4)
                elements = []        
                d = [['Admission Report as at '+date.strftime('%d %B %Y')]]
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
                data_list = []
                batches_name = ''
                data.append(['Date of Admission','Name','Course','Batches'])
                for admission in admissions:
                    if admission.batches.all().count() > 0:
                        for batch in admission.batches.all().order_by('-id'):
                            batches_name = batches_name + batch.name + ','
                    data.append([admission.doj.strftime('%d/%m/%Y') ,Paragraph(admission.student_name,para_style),Paragraph(admission.course.name,para_style),Paragraph(batches_name,para_style)])
                table = Table(data, colWidths=(100,100,100,100),  style=style)
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
                return render(request, 'admission_report.html',{'message':'No admissions founds'})
        else:
            return render(request, 'admission_report.html',{})

class StudentSearch(View):

    def get(self, request, *args, **kwargs):

        if request.is_ajax():
            students_list = []
            student_name = request.GET.get('name')
            if request.GET.get('batch'):
                batch_id = request.GET.get('batch')
                batch = Batch.objects.get(id=batch_id)
                students = batch.student_set.filter(student_name__istartswith=student_name)
                for student in students:
                    students_list.append({
                        'id': student.id,
                        'name': student.student_name,
                        'roll_number': student.roll_number,
                    })
            elif request.GET.get('course'):
                course_id = request.GET.get('course')
                course = Course.objects.get(id=course_id)
                students = Student.objects.filter(course=course, student_name__istartswith=student_name)
                for student in students:
                    students_list.append({
                        'id': student.id,
                        'name': student.student_name,
                        'roll_number': student.roll_number,
                    })
            elif student_name:
                students = Student.objects.filter(student_name__istartswith=student_name)
                for student in students:
                    students_list.append({
                        'id': student.id,
                        'name': student.student_name,
                        'roll_number': student.roll_number,
                    })
            res = {
                    'result': 'ok',
                    'students': students_list,
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')

class GetInstallmentDetails(View):

    def get(self, request, *args, **kwargs):

        student = Student.objects.get(id=request.GET.get('student', ''))
        ctx_installments = []
        i = 0
        total_amount_paid = 0
        for installment in student.installments.all():
            try:
                fees_payment = FeesPayment.objects.get(student__id=student.id)
                fees_payment_installments = fees_payment.payment_installment.filter(installment=installment)
                if fees_payment_installments.count() > 0:
                    total_amount_paid = float(total_amount_paid) + float(fees_payment_installments[0].paid_amount) + float(fees_payment_installments[0].fee_waiver_amount)
                    if (float(fees_payment_installments[0].paid_amount) + float(fees_payment_installments[0].fee_waiver_amount)) < installment.amount:
                        ctx_installments.append({
                            'id': installment.id,
                            'amount':installment.amount,
                            'due_date': installment.due_date.strftime('%d/%m/%Y'),
                            'fine_amount': installment.fine_amount,
                            'name':'installment'+str(i + 1),
                            'paid_installment_amount': float(fees_payment_installments[0].paid_amount) + float(fees_payment_installments[0].fee_waiver_amount),
                            'balance': float(installment.amount) - float(fees_payment_installments[0].paid_amount),
                        })
                elif fees_payment_installments.count() == 0:
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
        for installment in ctx_installments:
            installment.update({
                'total_amount_paid': total_amount_paid,
                'course_balance': float(student.fees) - float(total_amount_paid),
            })
        res = {
            'result': 'ok',
            'installments': ctx_installments,
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

class FollowUpReport(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            enquiry_list = []
            enquiries = []
            current_date = datetime.now().date()
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            if start_date and end_date:
                start_date = datetime.strptime(start_date, '%d/%m/%Y')
                end_date = datetime.strptime(end_date, '%d/%m/%Y')
                follow_ups = FollowUp.objects.filter(follow_up_date__gte=start_date,follow_up_date__lte=end_date).order_by('follow_up_date')
                enquiry_list = []
                for follow_up in follow_ups:
                    try:
                        enquiry = follow_up.enquiry_set.get(is_admitted=False)
                        follow_up_details = []
                        for follow_up in enquiry.follow_up.all():
                            follow_up_details.append({
                                'date': follow_up.follow_up_date.strftime('%d/%m/%Y'),
                                'remark': follow_up.remarks_for_follow_up_date
                            })
                        enquiry_list.append({
                            'id': enquiry.id,
                            'student_name': enquiry.student_name,
                            'address': enquiry.address,
                            'mobile_number' : enquiry.mobile_number,
                            'email' : enquiry.email,
                            'details_about_clients_enquiry' : enquiry.details_about_clients_enquiry,
                            'educational_qualification': enquiry.educational_qualification,
                            'land_mark': enquiry.land_mark,
                            'saved_date':enquiry.saved_date.strftime('%d/%m/%Y') if enquiry.saved_date else '',
                            'course' : enquiry.course.id,
                            'course_name':enquiry.course.name,
                            'remarks': enquiry.remarks,
                            'follow_ups': follow_up_details,
                            'discount': enquiry.discount,
                            'auto_generated_num': enquiry.auto_generated_num,
                        })
                    except Exception as ex:
                        pass
            else:
                try:
                    follow_ups = FollowUp.objects.filter(follow_up_date__year=current_date.year, follow_up_date__month=current_date.month, follow_up_date__day=current_date.day)
                    enquiry_list = []
                    for follow_up in follow_ups:
                        enquiry = follow_up.enquiry_set.get(is_admitted=False)
                        follow_up_details = []
                        for follow_up in enquiry.follow_up.all():
                            follow_up_details.append({
                                'date': follow_up.follow_up_date.strftime('%d/%m/%Y'),
                                'remark': follow_up.remarks_for_follow_up_date
                            })
                        enquiry_list.append({
                            'id': enquiry.id,
                            'student_name': enquiry.student_name,
                            'address': enquiry.address,
                            'mobile_number' : enquiry.mobile_number,
                            'email' : enquiry.email,
                            'details_about_clients_enquiry' : enquiry.details_about_clients_enquiry,
                            'educational_qualification': enquiry.educational_qualification,
                            'land_mark': enquiry.land_mark,
                            'saved_date':enquiry.saved_date.strftime('%d/%m/%Y') if enquiry.saved_date else '',
                            'course' : enquiry.course.id,
                            'course_name':enquiry.course.name,
                            'remarks': enquiry.remarks,
                            'follow_ups': follow_up_details,
                            'discount': enquiry.discount,
                            'auto_generated_num': enquiry.auto_generated_num,
                        })
                except Exception as ex:
                    print str(ex)
            response = simplejson.dumps({
                'enquiries': enquiry_list,
            })    
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'follow_up_report.html', {})

class EnquiryToAdmission(View):

    def get(self, request, *args, **kwargs):
        enquiry_to_admission_completed = request.GET.get('completed')
        enquiry_to_admission_incompleted = request.GET.get('incompleted')
        if request.GET.get('start_date') and request.GET.get('end_date'):
            start_date = datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
            end_date = datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y')
        if enquiry_to_admission_completed:
            enquiries = Enquiry.objects.filter(is_admitted=True,saved_date__gte=start_date,saved_date__lte=end_date).order_by('saved_date')
        elif enquiry_to_admission_incompleted:
            enquiries = Enquiry.objects.filter(is_admitted=False,saved_date__gte=start_date,saved_date__lte=end_date).order_by('saved_date')
        if request.is_ajax():
            enquiry_list = []
            if enquiries:
                for enquiry in enquiries:
                    follow_up_details = []
                    for follow_up in enquiry.follow_up.all():
                        follow_up_details.append({
                            'date': follow_up.follow_up_date.strftime('%d/%m/%Y'),
                            'remark': follow_up.remarks_for_follow_up_date
                        })
                    enquiry_list.append({
                        'id': enquiry.id,
                        'student_name': enquiry.student_name,
                        'address': enquiry.address,
                        'mobile_number' : enquiry.mobile_number,
                        'email' : enquiry.email,
                        'details_about_clients_enquiry' : enquiry.details_about_clients_enquiry,
                        'educational_qualification': enquiry.educational_qualification,
                        'land_mark': enquiry.land_mark,
                        'saved_date':enquiry.saved_date.strftime('%d/%m/%Y') if enquiry.saved_date else '',
                        'course' : enquiry.course.id,
                        'course_name':enquiry.course.name,
                        'remarks': enquiry.remarks,
                        'follow_ups': follow_up_details,
                        'discount': enquiry.discount,
                        'auto_generated_num': enquiry.auto_generated_num,
                    })
                response = simplejson.dumps({
                    'enquiries': enquiry_list,
                }) 
            else:
               response = simplejson.dumps({
                'enquiries': [],
                'message': 'No enquiries found'
            }) 
            return HttpResponse(response, status=200, mimetype='application/json')
        else:
            if request.GET.get('start_date') and request.GET.get('end_date'):
                response = HttpResponse(content_type='application/pdf')
                p = SimpleDocTemplate(response, pagesize=A4)
                elements = []       
                if enquiry_to_admission_completed:
                    d = [[' Report Of Enquiries Converted To Admission']]
                elif enquiry_to_admission_incompleted:
                    d = [[' Report Of Enquiries That Are Not Converted To Admission']]
                t = Table(d, colWidths=(450), rowHeights=25, style=style)
                t.setStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                            ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                            ('FONTSIZE', (0,0), (0,0), 20),
                            ('FONTSIZE', (1,0), (-1,-1), 17),
                            ])   
                elements.append(t)
                elements.append(Spacer(4, 5))
                if enquiry_to_admission_completed:
                    enquiries = Enquiry.objects.filter(is_admitted=True,saved_date__gte=start_date,saved_date__lte=end_date).order_by('saved_date')
                elif enquiry_to_admission_incompleted:
                    enquiries = Enquiry.objects.filter(is_admitted=False,saved_date__gte=start_date,saved_date__lte=end_date).order_by('saved_date')
                data = []
                data.append(['Date','Enquiry Number','Name','Course'])
                if enquiries:
                    for enquiry in enquiries:
                        data.append([enquiry.saved_date.strftime('%d/%m/%Y') ,enquiry.auto_generated_num,Paragraph(enquiry.student_name,para_style), Paragraph(enquiry.course.name,para_style)])
                table = Table(data, colWidths=(100,100,100,100),  style=style)
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
        return render(request, 'enquiry_to_admission.html', {})

class AdmissionCardView(View):

    def get(self, request, *args, **kwargs):
        student_id = request.GET.get('student_id', '')
        if student_id :
            student = Student.objects.get(id=student_id)
            response = HttpResponse(content_type='application/pdf')
            current_date = datetime.now()
            p = canvas.Canvas(response, pagesize=(1000, 1250))
            y = 1150
            time = str(student.batches.all()[0].start_time.strftime("%-I:%M%P")) + ' to ' + str(student.batches.all()[0].end_time.strftime("%-I:%M%P"))
            p.setFont("Helvetica", 24)
            p.drawCentredString(500, y - 60, 'Admission Card')
            p.setFont("Helvetica", 14)
            p.drawString(150, y-100 , 'Date...................')
            p.drawString(150, y-150, 'Course..........................')
            p.drawString(300, y-150,'Duration...........................')
            p.drawString(150, y-200, 'Name Of Candidate..............................................')
            p.drawString(150, y-250, 'Time....................................' )
            p.drawString(150, y-300, 'Total Fee.....................')
            p.drawString(150, y-350, 'Discount if any.......................')
            p.drawString(150, y-400, 'Course Starting date......................')
            p.drawString(150, y-450, 'No of Installments.................')
            p.drawString(200, y-97 , current_date.strftime('%d/%m/%Y') )
            p.drawString(200, y-147, student.course.name)
            p.drawString(360, y-147, str(student.course.duration if student.course else '') + str(student.course.duration_unit if student.course else ''))
            p.drawString(350, y-197, student.student_name)
            p.drawString(200, y-247, time)
            p.drawString(210, y-297, str(student.fees))
            p.drawString(300, y-347, str(student.discount))
            p.drawString(300, y-397, student.doj.strftime('%d/%m/%Y') )
            p.drawString(300, y-447, str(student.no_installments))
            p.save()
            return response
        return render(request, 'admission_card.html', {})

    


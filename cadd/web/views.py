import simplejson
import ast
from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4

from django.views.generic.base import View
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from web.models import Letter, Certificate
from admission.models import Student
from college.models import Course

style = [
    ('FONTSIZE', (0,0), (-1, -1), 12),
    ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
]

para_style = ParagraphStyle('fancy')
para_style.fontSize = 12
para_style.fontName = 'Helvetica'


style = [
    ('FONTSIZE', (0,0), (-1, -1), 12),
    ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
]

para_style = ParagraphStyle('fancy')
para_style.fontSize = 12
para_style.fontName = 'Helvetica'

class Home(View):
    def get(self, request, *args, **kwargs):
        
        return render(request, 'home.html',{})# Create your views here.


class Letters(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            letters_list = []
            letters = Letter.objects.all()
            for letter in letters:
                letters_list.append({
                    'id': letter.id,
                    'date': letter.date.strftime('%d/%m/%Y'),
                    'from': letter.from_address,
                    'to': letter.to_address,
                    'type': letter.letter_type,
                })
            res = {
                'letters' : letters_list,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype="application/json")
        return render(request, 'letter.html',{})
    
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            letter_details = ast.literal_eval(request.POST['letter_details'])
            try:
                if letter_details.get('id'):
                    letter = Letter.objects.get(id=letter_details['id'])
                else:
                    letter = Letter()
                letter.letter_type = letter_details['type']
                letter.date = datetime.strptime(letter_details['date'], '%d/%m/%Y')
                letter.from_address = letter_details['from']
                letter.to_address = letter_details['to']
                letter.save()
                res = {
                    'result': 'ok',
                    }
            except Exception as ex:
                res = {
                    'result': 'error',
                    'message': 'Failed',
                }
            status_code = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")

class Certificates(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            start_date = datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
            end_date = datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y')
            certificate_list = []
            certificates = Certificate.objects.filter(date__gte=start_date, date__lte=end_date).order_by('date')
            for certificate in certificates:
                certificate_list.append({
                    'id': certificate.id,
                    'name': certificate.certificate_name,
                    'date': certificate.date.strftime('%d/%m/%Y'),
                    'student': certificate.student.student_name,
                    'course': certificate.course.name,
                    'issued_authority': certificate.issued_authority,
                })
            res = {
                'certificates': certificate_list,
            }
            status_code = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")
        elif request.GET.get('report_type'):
                start_date = datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
                end_date = datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y')
                certificates = Certificate.objects.filter(date__gte=start_date, date__lte=end_date).order_by('date')
                response = HttpResponse(content_type='application/pdf')
                p = SimpleDocTemplate(response, pagesize=A4)
                elements = []        
                d = [['Certificate Register from '+ str(start_date.strftime('%d/%m/%Y')) +' to ' + str(end_date.strftime('%d/%m/%Y'))]]
                t = Table(d, colWidths=(450), rowHeights=35, style=style)
                t.setStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                            ('TEXTCOLOR',(0,0),(-1,-1),colors.HexColor('#699AB7')),
                            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                            ('BACKGROUND',(0, 0),(-1,-1),colors.HexColor('#EEEEEE')),
                            ('FONTSIZE', (0,0), (0,0), 16),
                            ('FONTSIZE', (1,0), (-1,-1), 15),
                            ])   
                elements.append(t)
                elements.append(Spacer(4, 5))
                count = 0
                d = []
                d.append(['SL No', 'DATE', Paragraph('CERTIFICATE NAME', para_style), 'ISSUED TO', Paragraph('ISSUED AUTHORITY', para_style), Paragraph('COURSE WHICH THAT STUDENT ADMITTED TO', para_style)])
                for certificate in certificates:
                    count = count + 1
                    d.append([count, certificate.date.strftime('%d/%m/%Y'), Paragraph(certificate.certificate_name, para_style), Paragraph(certificate.student.student_name, para_style), Paragraph(certificate.issued_authority, para_style), Paragraph(certificate.course.name, para_style)])
                table = Table(d, colWidths=(50, 75, 100, 100, 100,100),  style=style)
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
        return render(request, 'certificates.html',{})


class AddCertificate(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'add_certificate.html',{})

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            certificate_details = ast.literal_eval(request.POST['certificate_details'])
            try:
                certificate = Certificate()
                certificate.certificate_name = certificate_details['name']
                certificate.date = datetime.strptime(certificate_details['date'], '%d/%m/%Y')
                student = Student.objects.get(id=certificate_details['student'])
                certificate.student = student
                course = Course.objects.get(id=certificate_details['course'])
                certificate.course = course
                certificate.issued_authority = certificate_details['issued_authority']
                certificate.save()
                res = {
                    'result': 'ok',
                    }
            except Exception as ex:
                res = {
                    'result': 'error',
                    'message': 'Failed',
                }
            status_code = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")


class DeleteCertificate(View):
    def get(self,request,*args,**kwargs):
        certificate_id = kwargs['certificate_id']
        certificate = Certificate.objects.get(id=certificate_id)
        certificate.delete()
        return render(request, 'certificates.html', {})

class DeleteLetter(View):
    def get(self,request,*args,**kwargs):
        letter_id = kwargs['letter_id']
        letter = Letter.objects.get(id=letter_id)
        letter.delete()
        return HttpResponseRedirect(reverse('letters'))


class Login(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        return render(request,'home.html',{})

    def post(self,request,*args,**kwargs):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user and user.is_active:
            login(request, user)
        else:
            context = {
                'message' : 'Username or password is incorrect'
            }
            return render(request, 'home.html',context)
        context = {
         'Success_message': 'Welcome '+request.POST['username']
        }
        return HttpResponseRedirect(reverse('home'))

class Logout(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('home'))

class ResetPassword(View):

    def get(self, request, *args, **kwargs):

        user = User.objects.get(id=kwargs['user_id'])
        context = {
            'user_id': user.id
        }
        return render(request, 'reset_password.html', context)

    def post(self, request, *args, **kwargs):

        context = {}
        user = User.objects.get(id=kwargs['user_id'])
        if request.POST['password'] != request.POST['confirm_password']:
            context = {
                'user_id': user.id,
                'message': 'Password is not matched with Confirm Password',
            }
            return render(request, 'reset_password.html', context)
        if len(request.POST['password']) > 0 and not request.POST['password'].isspace():
            user.set_password(request.POST['password'])
        user.save()
        if user == request.user:
            logout(request)
            return HttpResponseRedirect(reverse('home'))  
        else:
            user_type = user.userprofile_set.all()[0].user_type 
            return HttpResponseRedirect(reverse('users', kwargs={'user_type': user_type}))

class LetterList(View):

    def get(self, request, *args, **kwargs):

        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        letter_type = request.GET.get('letter_type', '')
        letters = Letter.objects.filter(date__gte=datetime.strptime(start_date, '%d/%m/%Y'), date__lte=datetime.strptime(end_date, '%d/%m/%Y'), letter_type=letter_type)
        letter_list = []
        if request.is_ajax():
            for letter in letters:
                letter_list.append({
                    'id': letter.id,
                    'date': letter.date.strftime('%d/%m/%Y'),
                    'to': letter.to_address,
                    'from': letter.from_address,
                    'type': letter.letter_type,
                })
            res = {
                'result': 'ok',
                'letters': letter_list,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        else:
            response = HttpResponse(content_type='application/pdf')
            p = SimpleDocTemplate(response, pagesize=A4)
            elements = []        
            d = [['Letter '+letter_type +' Register Report -     '+start_date+' - ' + end_date]]
            t = Table(d, colWidths=(450), rowHeights=25, style=style)
            t.setStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('FONTSIZE', (0,0), (-1,-1), 17),
                        ])   
            elements.append(t)
            elements.append(Spacer(4, 5))
            data = []
            if letter_type == 'Incoming':
                data.append([ 'SL #','DATE','FROM ADDRESS','LETTER BY WHO INSIDE THE OFFICE'])
            else:
                data.append([ 'SL #','DATE','TO ADDRESS','TO WHO INSIDE THE OFFICE'])
            i = 1
            for letter in letters:
                if letter_type == 'Incoming':
                    data.append([i , letter.date.strftime('%d/%m/%Y'), Paragraph(letter.from_address,para_style), Paragraph(letter.to_address,para_style)])
                else:
                    data.append([i , letter.date.strftime('%d/%m/%Y'), Paragraph(letter.to_address,para_style), Paragraph(letter.from_address,para_style)])
                i = i + 1
            table = Table(data, colWidths=(40,100,150,250),  style=style)
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


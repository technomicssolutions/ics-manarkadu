import sys
import simplejson
import ast
import pytz

from datetime import datetime
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect

from college.models import Software, Course, Batch
from admission.models import Student

utc=pytz.UTC

class Softwares(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            software_list = []
            softwares = Software.objects.all()
            for software in softwares:
                software_list.append({
                    'id': software.id,
                    'name': software.name,
                    })
            res = {
                'softwares': software_list,
            }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        return render(request, 'list_softwares.html', {})

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            software_details = ast.literal_eval(request.POST['software_details'])
            try:
                if software_details.get('id'):
                    software = Software.objects.get(id=software_details['id'])
                else:
                    software = Software()
                software.name = software_details['name']
                software.save()
                res = {
                    'result': 'ok',
                    }
            except Exception as ex:
                res = {
                    'result': 'error',
                    'message': 'Software Already Exists',
                }
            status_code = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")


class DeleteSoftware(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                software = Software.objects.get(id=kwargs['software_id'])
                if software.course_set.all().count() > 0 or software.batch_set.all().count() > 0:
                    res = {
                        'result': 'ok',
                        'message': 'This software is currently being used, So cannot delete.'
                    }
                else:
                    name = software.name
                    software.delete()
                    res = {
                        'result': 'ok',
                        'message': name + ' Deleted Successfully',
                    }
            except:
                res = {
                    'result': 'error',
                    'message': 'failed',
                }

            status_code = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")


class Courses(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            course_list = []
            software_list = []
            courses = Course.objects.all()
            for course in courses:
                softwares = course.software.all()
                for software in softwares:
                    software_list.append({
                        'id': software.id,
                        'name': software.name,
                    })
                course_list.append({
                    'id': course.id,
                    'name': course.name,
                    'duration': course.duration,
                    'duration_unit': course.duration_unit,
                    'amount': course.amount,
                    'softwares': software_list,
                    'course_name': course.name + str(' - ') +str(course.duration) + ' ' + str(course.duration_unit)
                })
                software_list = []
            res = {
                'courses': course_list,
            }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        return render(request, 'list_courses.html', {})        

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            course_details = ast.literal_eval(request.POST['course_details'])
            try:
                if course_details.get('id'):
                    course = Course.objects.get(id=course_details['id'])
                else:
                    course = Course()
                course.name = course_details['name']
                course.amount = course_details['amount']
                course.duration = course_details['duration']
                course.duration_unit = course_details['duration_unit']
                course.save()
                if course.software:
                    course.software.clear()
                softwares = course_details['softwares']
                for software_id in softwares:
                    software = Software.objects.get(id=software_id)
                    course.software.add(software)
                course.save()
                res = {
                    'result': 'ok',
                    }
            except Exception as ex:
                res = {
                    'result': 'error',
                    'message': 'Course Already Exists',
                }
            status_code = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")


class DeleteCourse(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                course = Course.objects.get(id=kwargs['course_id'])
                name = course.name
                course.delete()
                res = {
                    'result': 'ok',
                    'message': name + ' Deleted Successfully',
                }
            except:
                res = {
                    'result': 'error',
                    'message': 'failed',
                }

            status_code = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")

class CourseDetails(View):
    def get(self, request, *args, **kwargs):

        courses = Course.objects.all()
        course_list = []
        ctx_software = []
        
        for course in courses:
            course_name = course.name + str(course.duration) + str(course.duration_unit)
            course_list.append({
                'software':course.software.name,
                'duration':course.duration,
                'duration_unit':course.duration_unit,                                       
                'course_name': course_name,
                'id': course.id
            })
            if course.software.all().count() > 0: 
                for software in course.software.all().order_by('-id'):
                    ctx_software.append({
                        'software': software.name,
                    })
            course_list.append({
                'software': ctx_software
                })
        res = {
            'result': 'ok',
            'courses': course_list,
        }            
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

class Batches(View):
    
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            batches = Batch.objects.all()
            batch_list = []
            for batch in batches:
                batch_name = batch.name + ' - '+ str(batch.start_time.strftime('%I:%M%p')) + ' to ' + str(batch.end_time.strftime('%I:%M%p'))
                batch_list.append({
                    'software':batch.software.name,
                    'software_id': batch.software.id,
                    'start':batch.start_time.strftime('%I:%M%p'),
                    'end':batch.end_time.strftime('%I:%M%p'),
                    'allowed_students':batch.allowed_students,                                        
                    'batch_name': batch_name,
                    'id': batch.id,
                    'name': batch.name,
                })
            res = {
                'result': 'ok',
                'batches': batch_list,
            }            
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'batch.html',{})

    def post(self, request, *args, **kwargs):
        status_code = 200
        if request.is_ajax():
            try:
                batch_details = ast.literal_eval(request.POST['batch'])
                software = Software.objects.get(id = batch_details['software_id'])
                if batch_details.get('id'):
                    batch = Batch.objects.get(id=batch_details['id'])
                else:
                    batch = Batch()
                batch.name = batch_details['name']
                batch.software = software
                batch.start_time = utc.localize(datetime.strptime(batch_details['start'], '%I:%M%p'))
                batch.end_time = utc.localize(datetime.strptime(batch_details['end'], '%I:%M%p'))
                batch.allowed_students = batch_details['allowed_students']
                batch.save()
                res = {
                    'result': 'ok',
                    'message': 'Batch /Added Successfully',
                }  
            except Exception as ex:
                res = {
                    'result': 'error',
                    'message': 'Batch Already Exists',
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")


class DeleteBatch(View):
    def get(self, request, *args, **kwargs):

        batch_id = kwargs['batch_id']       
        batch = Batch.objects.filter(id=batch_id)                          
        batch.delete()
        return HttpResponseRedirect(reverse('batches'))

class FreeBatchDetails(View):

    def get(self, request, *args, **kwargs):

        if request.is_ajax():
            batches = Batch.objects.all()
            batch_list = []
            for batch in batches:
                if batch.allowed_students != batch.no_of_students:
                    batch_name = batch.name + ' - '+ str(batch.start_time.strftime('%H:%M%p')) + ' to ' + str(batch.end_time.strftime('%H:%M%p'))
                    batch_list.append({
                        'software':batch.software.name,
                        'software_id': batch.software.id,
                        'start':batch.start_time.strftime('%H:%M%p'),
                        'end':batch.end_time.strftime('%H:%M%p'),
                        'allowed_students':batch.allowed_students,                                        
                        'name': batch.name,
                        'batch_name': batch_name,
                        'id': batch.id
                    })
            res = {
                'result': 'ok',
                'batches': batch_list,
            }            
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')


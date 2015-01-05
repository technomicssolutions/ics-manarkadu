
import simplejson
import ast
from datetime import datetime

from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from staff.models import Staff, Permission

class AddStaff(View):    
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            staff_details = ast.literal_eval(request.POST['staff'])
            if staff_details.get('id', ''):
                staff = Staff.objects.get(id=staff_details['id'])
                user = staff.user
            else:
                try:
                    user = User.objects.get(username=staff_details['username'])
                    res = {
                        'result': 'error',
                        'message': 'Username already exists',
                    }
                except Exception as ex:
                    user = User.objects.create(username=staff_details['username'])
                    user.set_password(staff_details['password'])
                    user.is_staff = True
                    user.save()
                    staff = Staff.objects.create(user=user)
            user.first_name = staff_details['first_name']
            user.last_name = staff_details['last_name']
            user.email = staff_details['email']
            user.save()
            staff.dob = datetime.strptime(staff_details['dob'], '%d/%m/%Y')
            staff.address = staff_details['address']
            staff.mobile_number = staff_details['mobile_number']
            staff.land_number = staff_details['land_number']                
            staff.blood_group = staff_details['blood_group']
            staff.doj = datetime.strptime(staff_details['doj'], '%d/%m/%Y')
            staff.qualifications = staff_details['qualifications']
            staff.photo = request.FILES.get('photo_img', '')
            staff.experience = staff_details['experience']
            staff.role = staff_details['role']
            staff.save()
            permission_details = {
                'attendance_module': 'true' if staff.permission and staff.permission.attendance_module  else 'false',
                'student_module': 'true' if staff.permission and staff.permission.student_module else 'false',
                'master_module': 'true' if staff.permission and staff.permission.master_module else 'false',
                'fees_module': 'true' if staff.permission and staff.permission.fees_module else 'false',
                'register_module': 'true' if staff.permission and staff.permission.register_module else 'false',
                'expense_module': 'true' if staff.permission and staff.permission.expense_module else 'false',
            }
            res = {
                'result': 'ok',
                'staff': {
                    'id': staff.id,
                    'first_name': staff.user.first_name,
                    'last_name': staff.user.last_name,
                    'username': staff.user.username,
                    'dob': staff.dob.strftime('%d/%m/%Y'),
                    'address': staff.address,
                    'mobile_number' : staff.mobile_number,
                    'land_number' : staff.land_number,
                    'email': staff.user.email,
                    'blood_group': staff.blood_group,
                    'doj': staff.doj.strftime('%d/%m/%Y'),
                    'qualifications': staff.qualifications,
                    'role': staff.role,
                    'experience': staff.experience,
                    'photo': staff.photo.name,
                    'permission': permission_details,
                }
            }  
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype="application/json")

class ListStaff(View):

    def get(self, request, *args, **kwargs):
        
        staffs = Staff.objects.all()
        if request.GET.get('staff_name', ''):
            staffs = Staff.objects.filter(user__first_name__istartswith=request.GET.get('staff_name', ''))
        if request.is_ajax():
            staff_list = []
            for staff in staffs:
                permission_details = {}
                permission_details = {
                    'attendance_module': 'true' if staff.permission and staff.permission.attendance_module  else 'false',
                    'student_module': 'true' if staff.permission and staff.permission.student_module else 'false',
                    'master_module': 'true' if staff.permission and staff.permission.master_module else 'false',
                    'fees_module': 'true' if staff.permission and staff.permission.fees_module else 'false',
                    'register_module': 'true' if staff.permission and staff.permission.register_module else 'false',
                    'expense_module': 'true' if staff.permission and staff.permission.expense_module else 'false',
                }
                staff_list.append({
                    'id': staff.id,
                    'first_name': staff.user.first_name,
                    'last_name': staff.user.last_name,
                    'username': staff.user.username,
                    'dob': staff.dob.strftime('%d/%m/%Y'),
                    'address': staff.address,
                    'mobile_number' : staff.mobile_number,
                    'land_number' : staff.land_number,
                    'email': staff.user.email,
                    'blood_group': staff.blood_group,
                    'doj': staff.doj.strftime('%d/%m/%Y'),
                    'qualifications': staff.qualifications,
                    'role': staff.role,
                    'experience': staff.experience,
                    'photo': staff.photo.name,
                    'permission': permission_details,
                })
            res = {
                'result': 'Ok',
                'staffs': staff_list
            }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        return render(request, 'list_staff.html',{})

class DeleteStaffDetails(View):
    def get(self, request, *args, **kwargs):

        staff_id = kwargs['staff_id']       
        staff = Staff.objects.filter(id=staff_id)                          
        staff.delete()
        return HttpResponseRedirect(reverse('staffs'))

class IsUsernameExists(View):

    def get(self, request, *args, **kwargs):

        if request.is_ajax():
            status = 200
            username = request.GET.get('username', '')
            try:
                user = User.objects.get(username=username)
                res = {
                    'result': 'error',
                    'message': 'Username already existing',
                }
            except Exception as ex:
                res = {
                    'result': 'ok',
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class PermissionSetting(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'permission_setting.html', {})

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            permission_details = ast.literal_eval(request.POST['permission_details'])
            staff = Staff.objects.get(id=permission_details['staff'])
            if staff.permission:
                permission = staff.permission
            else:
                permission = Permission()
            if permission_details['attendance_module'] == 'true':
                permission.attendance_module = True
            else:
                permission.attendance_module = False
            if permission_details['student_module'] == 'true':
                permission.student_module = True
            else:
                permission.student_module = False
            if permission_details['master_module'] == 'true':
                permission.master_module = True
            else:
                permission.master_module = False
            if permission_details['fees_module'] == 'true':
                permission.fees_module = True
            else:
                permission.fees_module = False
            if permission_details['register_module'] == 'true':
                permission.register_module = True
            else:
                permission.register_module = False
            if permission_details['expense_module'] == 'true':
                permission.expense_module = True
            else:
                permission.expense_module = False
            permission.save()
            staff.permission = permission
            staff.save()
            res = {
                'result': 'ok',
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')


class SearchStaff(View):

    def get(self, request, *args, **kwargs):
        staff_name = request.GET.get('name')
        staffs = Staff.objects.filter(user__first_name__istartswith=staff_name)
        staff_list = []
        for staff in staffs:
            staff_list.append({
                'id': staff.user.id,
                'name': staff.user.first_name + " " + staff.user.last_name,
            })
        res = {
            'staffs': staff_list,
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')
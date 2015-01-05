
import ast
import simplejson
import datetime as dt
from datetime import datetime
import math

from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4

from django.db.models import Max
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from expense.models import Expense, ExpenseHead

style = [
    ('FONTSIZE', (0,0), (-1, -1), 12),
    ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
]

para_style = ParagraphStyle('fancy')
para_style.fontSize = 12
para_style.fontName = 'Helvetica'

class AddExpenseHead(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'add_expense_head.html', {})

    def post(self, request, *args, **kwargs):

        post_dict = request.POST
        status = 200
        try:
            if len(post_dict['head_name']) > 0 and not post_dict['head_name'].isspace():
                expense_head, created = ExpenseHead.objects.get_or_create(expense_head = post_dict['head_name'])
                if created:
                    context = {
                        'message' : 'Added successfully',
                    }
                    res = {
                        'result': 'ok',
                        'head_id': expense_head.id,
                    }
                else:
                    context = {
                        'message' : 'This Head name is Already Existing',
                    }
                    res = {
                        'result': 'error',
                        'message': 'This Head name is Already Existing',
                    }
            else:
                context = {
                    'message' : 'Head name Cannot be null',
                }
        except Exception as ex:
            context = {
                'message' : post_dict['head_name']+' is already existing',
            }
            res = {
                'result': 'error',
                'message': post_dict['head_name']+' is already existing',
            }
        if request.is_ajax():
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        return render(request, 'add_expense_head.html', context)

class ExpenseHeadList(View):

    def get(self, request, *args, **kwargs):

        ctx_expense_head = []
        status_code = 200
        expense_heads = ExpenseHead.objects.all()
        if len(expense_heads) > 0:
            for head in expense_heads:
                ctx_expense_head.append({
                    'head_name': head.expense_head,
                    'id': head.id, 
                })
        res = {
            'result': 'ok',
            'expense_heads':ctx_expense_head
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=status_code, mimetype="application/json")

class ExpenseList(View):

    def get(self, request, *args, **kwargs):
        expenses = Expense.objects.all()
        if request.is_ajax():
            ctx_expenses = []
            status_code = 200
            if len(expenses) > 0:
                for expense in expenses:
                    ctx_expenses.append({
                        'expense_head_id': expense.expense_head.id if expense.expense_head else '',
	                    'id': expense.id, 
	                    'date': expense.date.strftime('%d/%m/%Y'),
	                    'voucher_no': expense.voucher_no,
	                    'amount': expense.amount,
	                    'payment_mode': expense.payment_mode,
	                    'branch': expense.branch,
	                    'bank_name': expense.bank_name,
	                    'cheque_no': expense.cheque_no,
	                    'cheque_date': expense.cheque_date.strftime('%d/%m/%Y') if expense.cheque_date else '',
	                    'narration': expense.narration,
	                    'expense_head': expense.expense_head.expense_head if expense.expense_head else '',
                    })
            res = {
                'result': 'ok',
                'expenses': ctx_expenses
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status_code, mimetype="application/json")
        return render(request, 'expense_list.html', {'expenses': expenses})

class EditExpense(View):

    def get(self, request, *args, **kwargs):
        expense = Expense.objects.get(id=request.GET['expense_id'])
        if request.is_ajax():
            ctx_expense = []
            status_code = 200
            if expense:
                ctx_expense.append({
                    'expense_head_id': expense.expense_head.id if expense.expense_head else '',
                    'id': expense.id, 
                    'date': expense.date.strftime('%d/%m/%Y'),
                    'voucher_no': expense.voucher_no,
                    'amount': expense.amount,
                    'payment_mode': expense.payment_mode,
                    'branch': expense.branch,
                    'bank_name': expense.bank_name,
                    'cheque_no': expense.cheque_no,
                    'cheque_date': expense.cheque_date.strftime('%d/%m/%Y') if expense.cheque_date else '',
                    'narration': expense.narration,
                })
            res = {
                'result': 'ok',
                'expense': ctx_expense
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status_code, mimetype="application/json")
        return render(request, 'edit_expense.html', {'expense': expense})
    
    def post(self, request, *args, **kwargs):

        expense_details = ast.literal_eval(request.POST['expense'])
        status = 200
        expense = Expense.objects.get(id=expense_details['id'])
        try:
            expense.voucher_no = expense_details['voucher_no']
            expense.date = datetime.strptime(expense_details['date'], '%d/%m/%Y')
            expense.payment_mode = expense_details['payment_mode']
            expense.narration = expense_details['narration']
            if expense.payment_mode == 'cheque':
                expense.cheque_no = expense_details['cheque_no']
                if expense_details['cheque_date']:
                    expense.cheque_date = datetime.strptime(expense_details['cheque_date'], '%d/%m/%Y')
                expense.bank_name = expense_details['bank_name']
                expense.branch = expense_details['branch']
            else:
                expense.cheque_date = None
                expense.bank_name = ''
                expense.branch = ''
                expense.cheque_no = ''
            expense_head = ExpenseHead.objects.get(id=expense_details['expense_head_id'])
            expense.expense_head = expense_head
            expense.amount = expense_details['amount']
            expense.save()
            res = {
                'result': 'ok',
            }
        except Exception as ex:
            res = {
                'result': 'error',
                'message': 'Voucher No already existing'
            }
        response = simplejson.dumps(res)

        return HttpResponse(response, status=status, mimetype='application/json')

class Expenses(View):

    def get(self, request, *args, **kwargs):

        current_date = dt.datetime.now().date()
        expenses = Expense.objects.all().count()
        if int(expenses) > 0:
            latest_expense = Expense.objects.latest('id')
            voucher_no = int(latest_expense.voucher_no) + 1
        else:
            voucher_no = 1
        context = {
            'current_date': current_date.strftime('%d/%m/%Y'),
            'voucher_no': voucher_no,
        }
        
        return render(request, 'expense.html', context)

    def post(self, request, *args, **kwargs):

        post_dict = ast.literal_eval(request.POST['expense'])
        try:
            expense = Expense.objects.get(voucher_no=post_dict['voucher_no'])
            res = {
                'result': 'error',
                'message': 'Voucher No already Existing'
            }
        except Exception as ex:
            expense = Expense.objects.create(created_by=request.user, voucher_no=post_dict['voucher_no'])
            expense.expense_head = ExpenseHead.objects.get(id = post_dict['expense_head_id'])
            expense.date = datetime.strptime(post_dict['date'], '%d/%m/%Y')
            expense.amount = post_dict['amount']
            expense.payment_mode = post_dict['payment_mode']
            expense.narration = post_dict['narration']
            if post_dict['payment_mode'] == 'cheque':
                expense.cheque_no = post_dict['cheque_no']
                expense.cheque_date = datetime.strptime(post_dict['cheque_date'], '%d/%m/%Y')
                expense.bank_name = post_dict['bank_name']
                expense.branch = post_dict['branch']
            expense.save()
            res = {
                'result': 'ok'
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype="application/json")

class ExpenseReport(View):

    def get(self, request, *args, **kwargs):

        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        if start_date and end_date:
            expenses = Expense.objects.filter(date__gte=datetime.strptime(start_date, '%d/%m/%Y'), date__lte=datetime.strptime(end_date, '%d/%m/%Y'))
            response = HttpResponse(content_type='application/pdf')
            p = SimpleDocTemplate(response, pagesize=A4)
            elements = []
            d = [['Expense Report - '+ start_date + ' - ' + end_date]]
            t = Table(d, colWidths=(450), rowHeights=25, style=style)
            t.setStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('FONTSIZE', (0,0), (-1,-1), 17),
                        ])   
            elements.append(t)
            elements.append(Spacer(4, 5))
            data = []
            data.append(['Date', 'Expense Head', 'Voucher No', 'Amount'])
            for expense in expenses:
                data.append([expense.date.strftime('%d/%m/%Y'), Paragraph(expense.expense_head.expense_head, para_style), expense.voucher_no, expense.amount ])
            table = Table(data, colWidths=(70, 150, 75, 100),  style=style)
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
        else:
            return render(request, 'expense_report.html', {})
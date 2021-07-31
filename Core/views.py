from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import *
from Invoices.models import *
from Calendar.models import *
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from datetime import date
import datetime


# Create your views here.
@login_required(login_url='Auth:login')
def index(request):
    return render(request, 'base.html')


class Index(LoginRequiredMixin, TemplateView):
    login_url = '/auth/login/'
    template_name = 'Core/index.html'

    def get_context_data(self, **kwargs):
        today = date.today()
        if today.month < 10:
            m = '0' + str(today.month)
        else:
            m = str(today.month)

        if today.day < 10 :
            day = '0'+ str(today.day)
        else:
            day = str(today.day)

        start_date = '01-' + m + '-' + str(today.year)
        current_date = day + '-' + m + '-' + str(today.year)
        xx = datetime.datetime.strptime(start_date, "%d-%m-%Y")
        xxx = datetime.datetime.strptime(current_date, "%d-%m-%Y")
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['opened_invoices'] = Invoice.objects.filter(saved=False, deleted=False)
        context['private_tasks'] = Task.objects.filter(employee=self.request.user, deleted=False, task_type=1)
        context['public_tasks'] = Task.objects.filter(deleted=False, task_type=2)

        context['today_sales'] = Invoice.objects.filter(saved=True, deleted=False, invoice_type=1, date__date = xxx).aggregate(total=Sum('after_discount'))
        context['today_expenses'] = Invoice.objects.filter(saved=True, deleted=False, invoice_type=11, date__date = xxx).aggregate(total=Sum('treasury_out'))
        context['new_customers'] = Customer.objects.filter(added_at__month=now().month).count()
        context['today_calls'] = CustomerCall.objects.filter(added_at__date=now().date()).count()
        context['sales'] = Invoice.objects.filter(saved=True, deleted=False, invoice_type=1, date__gte = xx)

        return context
           

class ChangeLog(TemplateView):
    template_name = 'Core/change_log.html'


def fix(request):
    for x in Invoice.objects.filter(invoice_type__in=[1, 2, 3, 4]):
        x.calculate_profit()
    return redirect('Core:index')


def update(request):
    invoices = Invoice.objects.all()
    from_branch = [1, 2, 3, 6, 7]
    to_branch = [4, 5]
    to_treasury = [1, 2, 3, 6, 7]
    from_treasury = [4, 5]
    for x in invoices.filter(invoice_type__in=from_branch):
        if x.creator:
            x.from_branch = x.creator.default_branch
            x.save()
    for x in invoices.filter(invoice_type__in=to_branch):
        if x.creator:
            x.to_branch = x.creator.default_branch
            x.save()
    for x in invoices.filter(invoice_type__in=from_treasury):
        if x.creator:
            x.from_treasury = x.creator.default_treasury
            x.save()
    for x in invoices.filter(invoice_type__in=to_treasury):
        if x.creator:
            x.to_treasury = x.creator.default_treasury
            x.save()
    context = {
        'title': 'تم التحديث بنجاح',
    }
    return render(request, 'base.html', context)

from django.shortcuts import render, HttpResponse
from django.views.generic import *
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
import xlwt


# Create your views here.
class PartnerList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Partners.access_partner_menu'
    model = Partner
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('phone'):
            queryset = queryset.filter(phone__icontains=self.request.GET.get('phone'))
        return queryset


class PartnerTrashList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Partners.access_partner_menu'
    model = Partner
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('phone'):
            queryset = queryset.filter(phone__icontains=self.request.GET.get('phone'))
        return queryset


class PartnerCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'Partners.add_partner'
    model = Partner
    form_class = PartnerForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Partner:PartnerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة شريك'
        context['action_url'] = reverse_lazy('Partners:PartnerCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class PartnerUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Partners.edit_partner'
    model = Partner
    form_class = PartnerForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Partners:PartnerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل شريك: ' + str(self.object)
        context['action_url'] = reverse_lazy('Partners:PartnerUpdate', kwargs={'pk': self.object.id})
        return context


class PartnerDelete(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Partners.delete_partner'
    model = Partner
    form_class = PartnerDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Partners:PartnerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف شريك: ' + str(self.object)
        context['action_url'] = reverse_lazy('Partners:PartnerDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

def PartnerXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Partner.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Partner') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم','رقم الهاتف','الرصيد الإفتتاحي']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows = Partner.objects.filter(deleted=False).values_list('id', 'name', 'phone', 'initial_balance')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response
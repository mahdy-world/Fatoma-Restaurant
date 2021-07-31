from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render , HttpResponse
from django.views.generic import *
from django.urls import reverse_lazy
from .models import *
from .forms import *
import xlwt


# Create your views here.
class BranchList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Branches.access_branch_menu'
    model = Branch
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(type=self.request.GET.get('type'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('address'):
            queryset = queryset.filter(address__icontains=self.request.GET.get('address'))
        if self.request.GET.get('phone'):
            queryset = queryset.filter(phone__icontains=self.request.GET.get('phone'))
        return queryset


class BranchTrashList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Branches.access_branch_menu'
    model = Branch
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(type=self.request.GET.get('type'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('address'):
            queryset = queryset.filter(address__icontains=self.request.GET.get('address'))
        if self.request.GET.get('phone'):
            queryset = queryset.filter(phone__icontains=self.request.GET.get('phone'))
        return queryset


class BranchCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'Branches.add_branch'
    model = Branch
    form_class = BranchForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Branches:BranchList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة فرع'
        context['action_url'] = reverse_lazy('Branches:BranchCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class BranchUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Branches.edit_branch'
    model = Branch
    form_class = BranchForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Branches:BranchList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل فرع: ' + str(self.object)
        context['action_url'] = reverse_lazy('Branches:BranchUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class BranchDelete(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Branches.delete_branch'
    model = Branch
    form_class = BranchDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Branches:BranchList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف فرع: ' + str(self.object)
        context['action_url'] = reverse_lazy('Branches:BranchDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
    
def BranchXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Branch.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Branch') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم', 'النوع','العنوان','رقم الهاتف']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows = Branch.objects.filter(deleted=False).values_list('id', 'name', 'type', 'address','phone')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response

class TreasuryList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Branches.access_treasury_menu'
    model = Treasury
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(type=self.request.GET.get('type'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('no'):
            queryset = queryset.filter(no__icontains=self.request.GET.get('no'))
        return queryset


class TreasuryTrashList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Branches.access_treasury_menu'
    model = Treasury
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(type=self.request.GET.get('type'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('no'):
            queryset = queryset.filter(no__icontains=self.request.GET.get('no'))
        return queryset


class TreasuryCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'Branches.add_treasury'
    model = Treasury
    form_class = TreasuryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Branches:TreasuryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة خزينة'
        context['action_url'] = reverse_lazy('Branches:TreasuryCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class TreasuryUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Branches.edit_treasury'
    model = Treasury
    form_class = TreasuryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Branches:TreasuryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل خزينة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Branches:TreasuryUpdate', kwargs={'pk': self.object.id})
        return context
    
    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class TreasuryDelete(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Branches.delete_treasury'
    model = Treasury
    form_class = TreasuryDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Branches:TreasuryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف خزينة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Branches:TreasuryDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

def TreasuryXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Treasury.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Treasury') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم', 'النوع','رقم الحساب','الرصيد الإفتتاحي']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows = Treasury.objects.filter(deleted=False).values_list('id', 'name', 'type', 'no','initial_balance')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response

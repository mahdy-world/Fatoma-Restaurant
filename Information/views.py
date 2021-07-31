from django.contrib import messages
from django.http import response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import *
from .models import *
from .forms import *
from django.urls import reverse_lazy
import xlwt

# Create your views here.
class InformationList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Information.view_informations_list'
    model = Information
    paginate_by = 100

    def get_queryset(self):
        employee = Employee.objects.get(user = self.request.user)
        # categories = InformationCategory.objects.filter(employee__name = employee.name , deleted = False)
        if self.request.user.is_superuser:
            queryset = self.model.objects.filter( deleted=False)
        else:
            queryset = self.model.objects.filter(employee__name = employee.name  , deleted=False)
        
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('title'):
            queryset = queryset.filter(title=self.request.GET.get('title'))
        return queryset

class InformationCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Information
    form_class = InformationForm
    permission_required = 'Information.add_information'
    template_name = 'Core/form_template1.html'
    success_url = reverse_lazy('Information:InformationList')
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة معلومة جديدة'
        context['action_url'] = reverse_lazy('Information:InformationCreate')
        return context
    
    def form_valid(self, form):
        object = form.save(commit = False)
        object.createdBy = self.request.user
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class InformationUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Information
    form_class = InformationForm
    template_name = 'Core/form_template1.html'
    success_url = reverse_lazy('Information:InformationList')
    permission_required = 'Information.edit_information'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل المعلومة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Information:InformationUpdate', kwargs={'pk': self.kwargs['pk']})
        return context
    
    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class InformationCard(LoginRequiredMixin, PermissionRequiredMixin , DetailView):
    login_url = '/auth/login/'
    permission_required = 'Information.view_information'
    model = Information

def DeleteInformation(request, pk):
    if not request.user.has_perm('Information.delete_information'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
    info = Information.objects.get(id=pk)
    info.delete()
    messages.add_message(request, messages.SUCCESS ,'تم الحذف بنجاح')
    return redirect('Information:InformationList')

def InformationXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Information.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Information') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الموظفين', 'العنوان']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows = InformationCategory.objects.filter(deleted= False).values_list('id','title', 'employee__name')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response 

class InformationCategoryList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Information.view_informations_category_list'
    model = InformationCategory
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('name'):
            queryset = queryset.filter(name=self.request.GET.get('name'))
        return queryset

class InformationCategoryCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = InformationCategory
    form_class = InformationCategoryForm
    permission_required = 'Information.add_information_category'
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Information:InformationCategoryList')
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة معلومة جديدة'
        context['action_url'] = reverse_lazy('Information:InformationCategoryCreate')
        return context
    
    def form_valid(self, form):
        object = form.save(commit = False)
        object.createdBy = self.request.user
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class InformationCategoryUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = InformationCategory
    form_class = InformationCategoryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Information:InformationCategoryList')
    permission_required = 'Information.edit_information_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل تصنيف المعلومة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Information:InformationCategoryUpdate', kwargs={'pk': self.kwargs['pk']})
        return context
    
    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

def DeleteCategoryInformation(request, pk):
    if not request.user.has_perm('Information.delete_information_category'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
    info = InformationCategory.objects.get(id=pk)
    info.delete()
    messages.add_message(request, messages.SUCCESS ,'تم الحذف بنجاح')
    return redirect('Information:InformationCategoryList')

def InformationCategoryXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=InformationCategory.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Information Category') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم', 'الموظفين']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows = InformationCategory.objects.filter(deleted= False).values_list('id','name', 'employee__name')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response 
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import *
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
import xlwt

# Create your views here.
class EmployeeDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    login_url = '/auth/login/'
    permission_required = 'HR.view_employee_data'
    model = Employee


class EmployeeList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'HR.view_employee'
    model = Employee
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('phone'):
            queryset = queryset.filter(phone__icontains=self.request.GET.get('phone'))
        if self.request.GET.get('address'):
            queryset = queryset.filter(address__icontains=self.request.GET.get('address'))
        if self.request.GET.get('job_title'):
            queryset = queryset.filter(job_title__name__icontains=self.request.GET.get('job_title'))
        return queryset


class EmployeeCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'HR.add_employee'
    model = Employee
    form_class = EmployeeForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('HR:EmployeeList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة موظف'
        context['action_url'] = reverse_lazy('HR:EmployeeCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class EmployeeUpdate(LoginRequiredMixin, PermissionRequiredMixin,  UpdateView):
    login_url = '/auth/login/'
    permission_required = 'HR.edit_employee'
    model = Employee
    form_class = EmployeeForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('HR:EmployeeList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل موظف: ' + str(self.object)
        context['action_url'] = reverse_lazy('HR:EmployeeUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class EmployeeDelete(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'HR.delete_employee'
    model = Employee
    form_class = EmployeeDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('HR:EmployeeList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف موظف: ' + str(self.object)
        context['action_url'] = reverse_lazy('HR:EmployeeDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
    
def EmployeeXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Employee.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Employee') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم','الهاتف','العنوان','تاريخ الميلاد','البريد الإلكتروني','المؤهل','نوع تحقيق الشخصية','رقم تحقيق الشخصية','جهةإصدار تحقيق الشخصية','انتهاء تحقيق الشخصية',
    'المسمى الوظيفي','الراتب','الحافز','تاريخ التأمين','تاريخ الإنتهاء','تكلفة التأمينات','الرقم على جهاز البصمة','تارييخ التعيين','تاريخ انتهاء العقد','الديانة',
    'موقف التجنيد','الحالة الإجتماعية','رصيد الأجازات','ايام الأجازة الاسبوعية','ايام الأجازة الشهرية','ايام الأجازة السنوية']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows =  Employee.objects.filter(deleted= False).values_list('id', 'name', 'phone', 'address', 'birthday', 'email', 'qualification', 'id_type', 'national_id', 'id_issued_from',
    'settlement_end_date', 'job_title', 'salary', 'over', 'insurance_start', 'insurance_end', 'insurance_cost', 'finger_print_id', 'start_date', 'end_date', 'religion',
    'military_state', 'relationship', 'rest_credit', 'weekly_rest_days', 'monthly_rest_days', 'yearly_rest_days')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response


class JobTitleList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'HR.view_job_title'
    model = JobTitle
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('description'):
            queryset = queryset.filter(description__icontains=self.request.GET.get('description'))
        if self.request.GET.get('available_job'):
            queryset = queryset.filter(available_job=self.request.GET.get('available_job'))
        return queryset


class JobTitleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'HR.add_job_title'
    model = JobTitle
    form_class = JobTitleForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('HR:JobTitleList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة موظف'
        context['action_url'] = reverse_lazy('HR:JobTitleCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class JobTitleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'HR.edit_job_title'
    model = JobTitle
    form_class = JobTitleForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('HR:JobTitleList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل موظف: ' + str(self.object)
        context['action_url'] = reverse_lazy('HR:JobTitleUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class JobTitleDelete(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'HR.delete_job_title'
    model = JobTitle
    form_class = JobTitleDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('HR:JobTitleList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف موظف: ' + str(self.object)
        context['action_url'] = reverse_lazy('HR:JobTitleDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

def JobTitleXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=JobTitle.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('JobTitle') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم', 'المهام الوظيفية','هل توجد وظائف متاحة ؟']
    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows =  JobTitle.objects.filter(deleted= False).values_list('id', 'name', 'description','available_job')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response

class UploadFile(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'HR.add_employee_file'
    model = EmployeeFile
    form_class = EmployeeFileForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('HR:EmployeeList')

    def form_valid(self, form):
        """
        Overridden to add the ipsum relation to the `Lorem` instance.
        """
        employee = get_object_or_404(Employee, id=self.kwargs['pk'])
        form.instance.employee = employee
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'رفع ملف موظف: ' + str(get_object_or_404(Employee, id=self.kwargs['pk']))
        print(self.kwargs['pk'])
        context['action_url'] = reverse_lazy('HR:UploadFile', kwargs={'pk': self.kwargs['pk']})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class ViewFile(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = EmployeeFile


class UserCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'HR.add_employee_user'
    model = User
    form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة حساب لموظف: ' + str(get_object_or_404(Employee, id=self.kwargs['pk']))
        print(self.kwargs['pk'])
        context['action_url'] = reverse_lazy('HR:UploadFile', kwargs={'pk': self.kwargs['pk']})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

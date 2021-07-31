from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import *
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
import xlwt

# Create your views here.
class ProjectStatusList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Projects.access_project_status_menu'
    model = ProjectStatus
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class ProjectStatusTrashList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Projects.access_project_status_menu'
    model = ProjectStatus
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class ProjectStatusCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'Projects.add_project_status'
    model = ProjectStatus
    form_class = ProjectStatusForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Projects:ProjectStatusList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة حالة المشروعات'
        context['action_url'] = reverse_lazy('Projects:ProjectStatusCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class ProjectStatusUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Projects.edit_project_status'
    model = ProjectStatus
    form_class = ProjectStatusForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Projects:ProjectStatusList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل حالة المشروعات: ' + str(self.object)
        context['action_url'] = reverse_lazy('Projects:ProjectStatusUpdate', kwargs={'pk': self.object.id})
        return context
    
    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class ProjectStatusDelete(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Projects.delete_project_status'
    model = ProjectStatus
    form_class = ProjectStatusDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Projects:ProjectStatusList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف حالة المشروعات: ' + str(self.object)
        context['action_url'] = reverse_lazy('Projects:ProjectStatusDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

def ProjectStatusXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Project Status.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Project Status') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows =  ProjectStatus.objects.filter(deleted= False).values_list('id', 'name')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response

class ProjectList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Projects.access_project_menu'
    model = Project
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('phone'):
            queryset = queryset.filter(customer__name__icontains=self.request.GET.get('customer'))
        return queryset


class ProjectTrashList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Projects.access_project_menu'
    model = Project
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('phone'):
            queryset = queryset.filter(customer__name__icontains=self.request.GET.get('customer'))
        return queryset


class ProjectCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'Projects.add_project'
    model = Project
    form_class = ProjectForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Project:ProjectList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة مشروع'
        context['action_url'] = reverse_lazy('Projects:ProjectCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        self.object = form.save()
        respose = ProjectResponse()
        respose.date = self.object.start_date
        respose.user = self.request.user
        respose.type = 7
        respose.project = self.object
        respose.comment = 'تم بدء المشروع'
        respose.comment += '\n'
        respose.comment += 'حالة المشروع: ' + self.object.status.name
        respose.save()
        return redirect('Projects:ProjectView', self.object.id)


class ProjectUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Projects.edit_project'
    model = Project
    form_class = ProjectForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Projects:ProjectList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مشروع: ' + str(self.object)
        context['action_url'] = reverse_lazy('Projects:ProjectUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class ProjectDelete(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Projects.delete_project'
    model = Project
    form_class = ProjectStatusDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Projects:ProjectList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف مشروع: ' + str(self.object)
        context['action_url'] = reverse_lazy('Projects:ProjectDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class ProjectView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    login_url = '/auth/login/'
    permission_required = 'Projects.view_project'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مشروع: ' + str(self.object)
        return context

def ProjectXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Projects.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Projects') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم', 'العميل', 'تاريخ البداية', 'تاريخ النهاية' , 'نسبة الإنجاز', 'حالة المشروع', 'رقم فاتورة المشروع','نوع الفاتورة']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows =  Project.objects.filter(deleted= False).values_list('id', 'name', 'client', 'start_date', 'end_date', 'complete_percent', 'status' , 'invoices', 'invoices__invoice_type')
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response

def change_project_status(request, pk):
    project = get_object_or_404(Project, id=pk)
    form = ChangeProjectStatusForm(request.POST or None, instance=project)
    if form.is_valid():
        response = ProjectResponse()
        response.project = project
        response.user = request.user
        response.type = 7
        response.save()
        new = form.save(commit=False)
        new.save()
        response.comment = '''
        تم تغيير حالة المشروع إلي : ''' + project.status.name + ''' ونسبة الإنجاز إلي ''' + str(project.complete_percent) + '''%'''
        response.save()
        return redirect('Projects:ProjectView', project.id)
    context = {
        'form': form,
        'title': 'تغيير حالة المشروع: ' + project.name,
    }
    return render(request, 'Core/form_template.html', context)


def customer_call(request, pk):
    project = get_object_or_404(Project, id=pk)
    form = CallForm(request.POST or None)
    if form.is_valid():
        response = form.save()
        response.type = 6
        response.visible_to_customer = True
        response.project = project
        response.save()
        return redirect('')

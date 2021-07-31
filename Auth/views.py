from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import *
from django.contrib.auth import get_user_model
from .forms import *
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from HR.models import Employee
from Website.models import WebsiteSetting


# Create your views here.
def login_user(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form,
    }
    if form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Core:index')
        else:
            error = 'برجاء إدخال اسم المستخدم وكلمة السر'
            context.update({'error': error})
            return render(request, 'Auth/login.html', context)
    return render(request, 'Auth/login.html', context)


class Login(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                #self.mail_notify(request)
                return redirect('Core:index')
            else:
                error = 'تم إيقاف الحساب الخاص بك'
                return render(request, 'Auth/login.html', context={'error': error})
        else:
                error = 'برجاء التأكد من اسم المستخدم وكلمة السر'
                return render(request, 'Auth/login.html', context={'error': error})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('Core:index')
        return render(request, 'Auth/login.html')

    def mail_notify(self, request):
        send_mail(
            'Subject here',
            'Here is the message.',
            'noreply@daftre.com',
            ['ahmed.elkhayyat@onlink4it.com'],
            fail_silently=False,
        )


class Logout(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('Auth:login')


def permissions(request, pk):
    user = User.objects.get(id=pk)
    form = PermissionsForm(request.POST or None, instance=user)
    title = 'تعديل صلاحيات الموظف ' + user.__str__()
    action_url = reverse_lazy('Auth:permissions', kwargs={'pk': user.id})
    if form.is_valid():
        obj = form.save()
        return redirect('Core:index')
    context = {
        'form': form,
        'title': title,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'تم تغيير كلمة المرور بنجاح!')
            return redirect('Core:index')
        else:
            messages.error(request, 'برجاء إصلاح الأخطاء الاتية')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Core/form_template.html', {
        'form': form,
        'title': 'تغيير كلمة المرور',
        'action_url': reverse_lazy('Auth:change_password'),
    })


def login_as(request, pk):
    user = User.objects.get(id=pk)
    login(request, user)
    return redirect('Core:index')


class PasswordReset(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = User
    form_class = PasswordResetForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('HR:EmployeeList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إعادة ضبط كلمة المرور للمستخدم: ' + str(self.object)
        context['action_url'] = reverse_lazy('Auth:PasswordReset', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.set_password(form.cleaned_data['password'])
        obj.save()
        return redirect('HR:EmployeeList')


def account_setting(request):
    form = AccountSettingForm(request.POST, instance=request.user)
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        return redirect('Core:index')
    return render(request, 'Core/form_template.html', {
        'form': form,
        'title': 'إعدادات الحساب',
        'action_url': reverse_lazy('Auth:account_setting'),
    })


def create_user_for_employee(request, pk):
    employee = get_object_or_404(Employee, id=pk)
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.email = employee.email
        user.first_name = employee.name
        user.is_staff = True
        user.save()
        employee.user = user
        employee.save()
        return redirect(request.POST.get('url'))
    context = {
        'title': 'إضافة حساب علي البرنامج للموظف',
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)


class UserLogin(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(request.POST.get('url'))
            else:
                error = 'تم إيقاف الحساب الخاص بك'
                return render(request, 'Auth/login.html', context={'error': error})
        else:
                error = 'برجاء التأكد من اسم المستخدم وكلمة السر'
                return render(request, 'Core/form_template.html', context={'error': error})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('Website:HomePage')
        return render(request, 'Auth/website_login.html', self.get_context_data())

    def get_context_data(self, **kwargs):
        context = {}
        setting = WebsiteSetting.objects.get_or_create(id=1)
        setting = WebsiteSetting.objects.get(id=1)
        context.update({'setting': setting})
        return context


class RegisterUser(CreateView):
    model = get_user_model()
    form_class = RegisterForm
    template_name = 'Core/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "تسجيل حساب جديد"
        return context


class UserLogout(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('Website:HomePage')

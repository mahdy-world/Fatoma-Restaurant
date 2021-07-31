from django.shortcuts import render, redirect
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from Auth.models import User
from Branches.models import Branch, Treasury
from Customers.models import Customer
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def setup(request):
    try:
        title = 'تعديل ترخيص برنامج أون بيزنس'
        user = User.objects.get(id=1)
        object = ModulesSetting.objects.all().first()
        if request.user.id == 1:
            form = SetupForm(request.POST or None, instance=object)
            if form.is_valid():
                object = form.save(commit=False)
                object.save()
                return redirect('Core:index')
        else:
            title = 'عفواً لا تمتلك صلاحية الدخول لهذه الصفحة برجاء الإتصال بالدعم الفني 01066440666'
            form = ''
    except ObjectDoesNotExist:
        title = 'مرحباً بك في برنامج أون بيزنس'
        try:
            user = User.objects.get(id=1)
        except ObjectDoesNotExist:
            superuser = User()
            superuser.username = 'amk'
            superuser.email = '2beordie@gmail.com'
            superuser.set_password('0nl1nk4it')
            superuser.is_superuser = True
            superuser.is_staff = True
            superuser.first_name = 'Ahmed'
            superuser.last_name = 'El-Khayyat'
            superuser.save()
            login(request, superuser)
        customer = Customer()
        customer.name = 'عميل نقدي'
        customer.save()
        branch = Branch()
        branch.name = 'الفرع الافتراضي'
        branch.type = 1
        branch.save()
        treasury = Treasury()
        treasury.name = 'الخزينة الافتراضية'
        treasury.type = 1
        treasury.save()
        setting = ModulesSetting()
        setting.save()
        form = SetupForm(request.POST or None, instance=setting)
        if form.is_valid():
            object = form.save(commit=False)
            object.save()
            return redirect('Core:index')
        context = {
            'form': form,
            'title': title,
        }
        return render(request, 'Setting/setup.html', context)
    context = {
        'form': form,
        'title': title,
    }
    return render(request, 'Core/form_template.html', context)

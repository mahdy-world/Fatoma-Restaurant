from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect ,HttpResponse
from django.views.generic import *
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from rest_framework import generics
from django.db.models import Q
from .serializers import CustomerSerializer
from django.contrib import messages
from Products.models import Product, ProductPrices
import xlwt


# Create your views here.
class CategoryList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Customers.access_customer_category_menu'
    model = Category
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset




class CategoryTrashList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Customers.access_customer_category_menu'
    model = Category
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class CategoryCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'Customers.add_customer_category'
    model = Category
    form_class = CategoryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:CategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة شريحة عملاء'
        context['action_url'] = reverse_lazy('Customers:CategoryCreate')
        return context
    
    def add_to_all_product(self):
        for x in Product.objects.all():
            product_price = ProductPrices()
            product_price.product = x
            product_price.customer_segment = Category.objects.get(name=self.object.name)
            product_price.price = x.sell_price
            product_price.discount = '0'
            product_price.new_price = x.sell_price
            product_price.save()
        return 'ok'
    
    def form_valid(self, form):
        self.object = form.save()
        self.add_to_all_product()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class CategoryUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Customers.edit_customer_category'
    model = Category
    form_class = CategoryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:CategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل شريحة عملاء: ' + str(self.object)
        context['action_url'] = reverse_lazy('Customers:CategoryUpdate', kwargs={'pk': self.object.id})
        return context


class CategoryDelete(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Customers.delete_customer_category'
    model = Category
    form_class = CategoryDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:CategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف شريحة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Customers:CategoryDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

def CategoryXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Customer Category.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Category') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows =  Category.objects.filter(deleted= False).values_list('id', 'name')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    print(work_sheet)
    work_book.save(response)
    return response

class CustomerList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Customers.access_customer_menu'
    model = Customer
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(type=self.request.GET.get('type'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('job'):
            queryset = queryset.filter(job__icontains=self.request.GET.get('job'))
        if self.request.GET.get('category'):
            queryset = queryset.filter(category=self.request.GET.get('category'))
        if self.request.GET.get('group'):
            queryset = queryset.filter(group=self.request.GET.get('group'))
        if self.request.GET.get('q'):
            queryset = queryset.filter(
                Q(name__icontains=self.request.GET.get('q')) |
                Q(facebook_account__icontains=self.request.GET.get('q'))
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = CustomerGroup.objects.filter(deleted = False)
        return context


class CustomerTrashList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Customers.access_customer_menu'
    model = Customer
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
        if self.request.GET.get('job'):
            queryset = queryset.filter(job__icontains=self.request.GET.get('job'))
        if self.request.GET.get('category'):
            queryset = queryset.filter(category=self.request.GET.get('category'))
        if self.request.GET.get('q'):
            queryset = queryset.filter(
                Q(name__icontains=self.request.GET.get('q')) |
                Q(phone__icontains=self.request.GET.get('q')) |
                Q(facebook_account__icontains=self.request.GET.get('q'))
            )
        return queryset


class CustomerCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'Customers.add_customer'
    model = Customer
    form_class = CustomerForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:CustomerList')

    def get_form(self, form_class=CustomerForm):
        form = super(CustomerCreate, self).get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(deleted = False)
        form.fields['group'].queryset = CustomerGroup.objects.filter(deleted = False)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة عميل / مورد'
        context['action_url'] = reverse_lazy('Customers:CustomerCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class CustomerUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Customers.edit_customer'
    model = Customer
    form_class = CustomerEditForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:CustomerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل عميل / مورد: ' + str(self.object)
        context['action_url'] = reverse_lazy('Customers:CustomerUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class CustomerDelete(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Customers.delete_customer'
    model = Customer
    form_class = CustomerDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:CustomerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف عميل / مورد: ' + str(self.object)
        context['action_url'] = reverse_lazy('Customers:CustomerDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

def CustomerXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Customers.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Customers') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#','الاسم' , 'حساب الفيس بوك' , 'الوظيفة' , 'الشريحة', 'التصنيف',  'الرصيد الافتتاحي', 'السماح بالبيع الآجل', 'الحد الإتماني', 'اضيف بواسطة','اضيف بتاريخ']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows =  Customer.objects.filter(deleted= False).values_list('id', 'name', 'facebook_account', 'job', 'category__name', 'group__name', 'initial_balance', 'allow_negative_balance',
    'max_negative_balance', 'added_by__username', 'added_at')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response

class CallReasonList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Customers.access_call_reason_menu'
    model = CallReason
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class CallReasonTrashList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Customers.access_call_reason_menu'
    model = CallReason
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class CallReasonCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'Customers.add_call_reason'
    model = CallReason
    form_class = CallReasonForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('customersCallReasonList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة سبب مكالمة'
        context['action_url'] = reverse_lazy('customersCallReasonCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class CallReasonUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Customers.edit_call_reason'
    model = CallReason
    form_class = CallReasonForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('customersCallReasonList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل سبب المكالمة: ' + str(self.object)
        context['action_url'] = reverse_lazy('customersCallReasonUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class CallReasonDelete(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Customers.delete_call_reason'
    model = CallReason
    form_class = CallReasonDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('customers:CallReasonList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف سبب المكالمة: ' + str(self.object)
        context['action_url'] = reverse_lazy('customers:CallReasonDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

def CallReasonXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Call Reason.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Call Reason') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows =  CallReason.objects.filter(deleted= False).values_list('id', 'name')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response


class CustomerDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    login_url = '/auth/login/'
    permission_required = 'Customers.view_customer'
    model = Customer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address'] = Address.objects.filter(customer=self.kwargs['pk'])
        context['phone'] = Phone.objects.filter(customer=self.kwargs['pk'])
        return context


class CustomerInvoices(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Customer
    template_name = 'Customers/customer_invoices.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('type'):
            context['invoices'] = self.object.invoice_set.filter(deleted=False,
                                                                 invoice_type=self.request.GET.get('type'))
        else:
            context['invoices'] = self.object.invoice_set.filter(deleted=False)
        return context


class CustomerCalls(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Customer
    template_name = 'Customers/customer_calls.html'


class CustomerAPIList(generics.ListCreateAPIView):
    queryset = Customer.objects.filter(deleted=False)
    serializer_class = CustomerSerializer


class CustomerAPIDetail(generics.RetrieveUpdateAPIView):
    queryset = Customer.objects.filter(deleted=False)
    serializer_class = CustomerSerializer


def add_call(request, pk):
    if not request.user.has_perm('Customers.add_customer_call'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
    customer = get_object_or_404(Customer, id=pk)
    form = CustomerCallForm(request.POST or None)
    if form.is_valid():
        call = form.save(commit=False)
        call.customer = customer
        call.added_by = request.user
        call.save()
        history = CustomerHistory()
        history.customer = customer
        history.added_by = request.user
        history.history_type = 2
        history.call = call
        history.save()
        return redirect(request.POST.get('url'))
    context = {
        'form': form,
        'title': 'إضافة مكالمة',
    }
    return render(request, 'Core/form_template.html', context)


class CallDetail(LoginRequiredMixin, DetailView):
    model = CustomerCall
    login_url = '/auth/login/'
    
class AddressCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'Customers.add_address'
    model = Address
    form_class = AddressForm
    template_name = 'Core/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضاف عنوان عميل / مورد'
        context['action_url'] = reverse_lazy('Customers:AddressCreate')
        return context

    def form_valid(self, form):
        c = Customer.objects.get(id = self.kwargs['pk'])
        object = form.save(commit=False)
        object.customer = c
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Customers:CustomerDetail', kwargs={'pk': self.kwargs['pk']})

class AddressUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Customers.edit_address'
    model = Address
    form_class = AddressForm
    template_name = 'Core/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل عنوان عميل / مورد' 
        context['action_url'] = reverse_lazy('AddressUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

def AddressDelete(request, pk):
    if not request.user.has_perm('Customers.delete_address'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    address = Address.objects.get(id=pk)
    customerId = address.customer.id
    address.delete()
    return redirect('Customers:CustomerDetail', pk=customerId)


class GroupList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Customers.access_customer_rating_menu'
    model = CustomerGroup
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset

class GroupTrashList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Customers.access_customer_rating_menu'
    model = CustomerGroup
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset

class GroupCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'Customers.add_customer_rating'
    model = CustomerGroup
    form_class = GroupForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:GroupList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة تصنيف عملاء'
        context['action_url'] = reverse_lazy('Customers:GroupCreate')
        return context


class GroupUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Customers.edit_customer_rating'
    model = CustomerGroup
    form_class = GroupForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:GroupList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل تصنيف عملاء: ' + str(self.object)
        context['action_url'] = reverse_lazy('Customers:GroupUpdate', kwargs={'pk': self.object.id})
        return context

class GroupDelete(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Customers.delete_customer_rating'
    model = CustomerGroup
    form_class = GroupDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:GroupList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف تصنيف عملاء: ' + str(self.object)
        context['action_url'] = reverse_lazy('Customers:GroupDelete', kwargs={'pk': self.object.id})
        return context

def GroupXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=CustomerGroups.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Groups') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows =  CustomerGroup.objects.filter(deleted= False).values_list('id', 'name')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response


class PhoneCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'Customers.add_customer_phone'
    model = Phone
    form_class = PhoneForm
    template_name = 'Core/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضاف رقم عميل / مورد'
        context['action_url'] = reverse_lazy('Customers:PhoneCreate')
        return context

    def form_valid(self, form):
        c = Customer.objects.get(id = self.kwargs['pk'])
        object = form.save(commit=False)
        object.customer = c
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Customers:CustomerDetail', kwargs={'pk': self.kwargs['pk']})

class PhoneUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Customers.edit_customer_phone'
    model = Phone
    form_class = PhoneForm
    template_name = 'Core/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل رقم عميل / مورد' 
        context['action_url'] = reverse_lazy('AddressUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

def PhoneDelete(request, pk):
    if not request.user.has_perm('Customers.delete_customer_phone'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    phone = Phone.objects.get(id=pk)
    customerId = phone.customer.id
    phone.delete()
    return redirect('Customers:CustomerDetail', pk=customerId)
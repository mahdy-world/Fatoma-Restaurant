from collections import Counter
from django.core.exceptions import PermissionDenied
from django.db.models.aggregates import Count, Sum
from django.db.models.fields import FloatField
from django.forms.widgets import NumberInput
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import HttpResponse, JsonResponse
from django.views.generic import *
from django.urls import reverse_lazy
from xlwt import ExcelFormula
from .models import *
from .forms import *
from datetime import date
from Products.models import Product , MainCategory , SubCategory, GroupedProduct
from Invoices.models import Invoice , InvoiceItem
from Customers.models import Address , Customer, Phone
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
import datetime
from Invoices.views import get_invoice_base_setting
from Customers.forms import CustomerForm , AddressForm, AddressForm1
import xlwt

################## POS ##################
def get_pos_base_setting():
    try:
        setting = PosBaseSetting.objects.get(id=1)
    except:
        setting = PosBaseSetting()
        setting.save()
    return setting

def pos_setting(request):
    if not request.user.has_perm('POS.edit_pos_setting'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.POST.get('HTTP_REFERER'))

    setting = get_pos_base_setting()
    form = PosSettingForm(request.POST or None, request.FILES or None, instance=setting)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()

        return redirect(request.POST.get('url'))
    context = {
        'title': 'إعدادات نقاط البيع',
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)

class POSList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'POS.view_pos'
    model = POS
    paginate_by = 100
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('POS.view_pos'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية للدخول')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return super(POSList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        employee = Employee.objects.get(user = self.request.user)
        if self.request.user.is_superuser:
            queryset = self.model.objects.filter(deleted=False)
        else:
            queryset = self.model.objects.filter(employees__name=employee.name, deleted=False)

        if self.request.GET.get('name'):
            queryset = queryset.filter(name=self.request.GET.get('name'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(type=self.request.GET.get('type'))
        if self.request.GET.get('warehouse'):
            queryset = queryset.filter(warehouse__icontains=self.request.GET.get('warehouse'))
        if self.request.GET.get('employees'):
            queryset = queryset.filter(employees__icontains=self.request.GET.get('employees'))
        if self.request.GET.get('createdBy'):
            queryset = queryset.filter(createdBy__icontains=self.request.GET.get('createdBy'))
        return queryset

class POSTrashList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'POS.view_pos'
    model = POS
    paginate_by = 100

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('POS.view_pos'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية للدخول')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return super(POSTrashList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('name'):
            queryset = queryset.filter(id=self.request.GET.get('name'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(date__icontains=self.request.GET.get('type'))
        if self.request.GET.get('warehouse'):
            queryset = queryset.filter(start_time__icontains=self.request.GET.get('warehouse'))
        if self.request.GET.get('employees'):
            queryset = queryset.filter(end_time__icontains=self.request.GET.get('employees'))
        if self.request.GET.get('createdBy'):
            queryset = queryset.filter(employee__icontains=self.request.GET.get('createdBy'))
        return queryset

class POSCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = POS
    form_class = POSForm
    permission_required = 'POS.add_pos'
    template_name = 'Core/form_template1.html'
    success_url = reverse_lazy('POS:POSList')
        
    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات لإضافة نقطة بيع')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة نقطة بيع جديدة'
        context['action_url'] = reverse_lazy('POS:POSCreate')
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

class POSCard(LoginRequiredMixin, PermissionRequiredMixin , DetailView):
    login_url = '/auth/login/'
    model = POS
    permission_required = 'POS.view_pos_detail'

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات للدخول لبيانات نقطة البيع')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        open_tables_count = 0 
        floors = Floor.objects.filter(pos=self.object)
        for f in floors:
            open_tables_count += Table.objects.filter(floor = f , status=1).count()
        context = super().get_context_data(**kwargs)
        context['open_shifts'] = Shift.objects.filter(pos=self.object, status=2 , deleted = False)
        context['closed_shifts'] = Shift.objects.filter(pos=self.object, status=1, deleted = False)
        context['shifts'] = Shift.objects.filter(pos=self.object)
        context['floors'] = floors
        context['tables'] = Table.objects.all()
        context['open_tables_count']= open_tables_count
        context['action_url'] = reverse_lazy('POS:EmployeeCard', kwargs={'pk': self.object.id})
        return context

class POSUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = POS
    form_class = POSForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('POS:POSList')
    permission_required = 'POS.edit_pos'

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات لتعديل بيانات نقطة البيع')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل نقطة البيع: ' + str(self.object)
        context['action_url'] = reverse_lazy('POS:POSUpdate', kwargs={'pk': self.kwargs['pk']})
        return context
    
    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class POSDelete(LoginRequiredMixin, PermissionRequiredMixin , UpdateView):
    login_url = '/auth/login/'
    model = POS
    form_class = POSDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('POS:POSList')
    permission_required = 'POS.delete_pos'

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات لحذف نقطة البيع')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف نقطة البيع: ' + str(self.object)
        context['action_url'] = reverse_lazy('POS:POSDelete', kwargs={'pk': self.kwargs['pk']})
        return context
    
    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

def EnterPOS(request , id):
    if not request.user.has_perm('POS.enter_pos'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية للدخول')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    employee = Employee.objects.get(user = request.user)
    pos = POS.objects.get(id = id)
    shift = Shift.objects.filter(employee= employee , pos = pos, status=2, deleted=False).order_by('-id')
    if ( shift.count() > 0 ):
        order = Order.objects.filter(pos =pos , shift =shift[0], status=1, deleted=False).order_by('-id')
        if ( order.count() > 0 ):
            single_order = Order.objects.get(id = order[0].id)
            return redirect('POS:OrderUpdate', id=single_order.id)
        else:
            setting = get_pos_base_setting()
            if (setting.default_customer_in_sales != None):
                NewOrder = Order(pos= pos , shift=shift[0], customer= setting.default_customer_in_sales)
            else:
                NewOrder = Order(pos= pos , shift=shift[0])
            NewOrder.save()
            return redirect('POS:OrderUpdate', id=str(NewOrder.id))
    else:
        NewShift = Shift(employee= employee , pos = pos)
        NewShift.save()
        setting = get_pos_base_setting()
        if (setting.default_customer_in_sales != None):
            NewOrder = Order(pos= pos , shift=NewShift, customer= setting.default_customer_in_sales)
        else:
            NewOrder = Order(pos= pos , shift=NewShift)
        NewOrder.save()
        return redirect('POS:OrderUpdate', id=str(NewOrder.id))

def PosReport(request, id):
    single_pos = POS.objects.get(id = id)
    orders = Order.objects.filter(deleted=False, pos = single_pos.id , status = 2)
    customers = Customer.objects.filter(deleted=False).filter(id__in=[o.customer.id for o in orders ])
    orders_detail = orders.values_list('customer_id', 'customer__name', 'customer__category__name' , 'partner__name').annotate(number=Count('total'),value=Sum('total')).order_by()
    shifts = Shift.objects.filter(deleted = False, pos = single_pos.id)
    context = {
        'single_pos': single_pos,
        'customers': customers,
        'orders_detail': orders_detail,
        'shifts': shifts,
        'orders': orders,
    }
    return render(request, 'POS/pos_report.html', context)

def PosXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=InformationCategory.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('pos') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم', 'النوع' , 'المخزن' , 'الموظف' ,'أنشأت بواسطة' ,'من خزينة' ,'كلمة السر' , 'الدولة' , 'سعر توصيل الدولة','الإقليم', 'المحافظة', 'سعر توصيل المحافظة']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows =  POS.objects.filter(deleted= False).values_list('id', 'name', 'type', 'warehouse__name' , 'employees__name', 'createdBy__username' , 'from_treasury__name' , 'password',
    'country', 'country_delivery_cost', 'region', 'governorate', 'governorate_delivery_cost')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    print(work_sheet)
    work_book.save(response)
    return response

################## SHIFTS ##################
class ShiftCreate(LoginRequiredMixin, PermissionRequiredMixin , CreateView):
    login_url = '/auth/login/'
    model = Shift
    form_class = ShiftForm
    template_name = 'Core/form_template.html'
    permission_required = 'POS.add_shift'

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات لإضافة شيفت جديد')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة شيفت جديد'
        context['action_url'] = reverse_lazy('POS:ShiftCreate')
        return context
    
    def form_valid(self, form):
        object = form.save(commit = False)
        p = POS.objects.get(id=self.kwargs['pk'])
        object.pos = p
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class ShiftCard(LoginRequiredMixin, PermissionRequiredMixin , DetailView):
    login_url = '/auth/login/'
    permission_required = 'POS.view_shift'
    model = Shift

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات للدخول لبيانات الشيفت')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['open_orders'] = Order.objects.filter(shift=self.object , status='1', deleted=False)
        context['closed_orders'] = Order.objects.filter(shift=self.object , status='2', deleted=False)
        context['canceled_orders'] = Order.objects.filter(shift=self.object , status='3', deleted=False)
        context['floors'] = Floor.objects.filter(pos = self.object.pos )
        context['tables'] = Table.objects.all()
        context['action_url'] = reverse_lazy('POS:EmployeeCard', kwargs={'pk': self.object.id})
        return context

def EndShift(request, id):
    if not request.user.has_perm('POS.close_shift'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية لإغلاق الشيفت ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    shift = Shift.objects.get(id=id)

    if ( Order.objects.filter(shift = shift , status= 1 ).count()) > 0:
        messages.add_message(request, messages.ERROR , 'لا يمكن إنهاء الشيفت إلا بعد إغلاق كل الطلبات')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    invoice = Invoice.objects.create(invoice_type=23, creator=request.user, from_branch=shift.pos.warehouse , to_treasury = shift.pos.to_treasury )
    shift_orders = Order.objects.filter(shift = shift , status = 2)
    total = 0 
    for S_O in shift_orders:
        total += S_O.total
        products = Order_detail.objects.filter(order = S_O)
        for p in products:
            if p.product.product_type == 2 :
                small_products = GroupedProduct.objects.filter(grouped_item = p.product)
                for s_p in small_products:
                    if s_p.contain.refundable:
                        a_d = p.sub_total - p.dicount
                        quantity = p.quantity * s_p.quantity
                        iv_item = InvoiceItem.objects.create(invoice=invoice, item=s_p.contain , quantity=quantity, unit_price= p.price, total_price=p.sub_total, discount=p.dicount ,after_discount=a_d)
                        iv_item.save()
                        iv_item.calculate_profit()
            else:
                if p.product.refundable:
                    a_d = p.sub_total - p.dicount
                    iv_item = InvoiceItem.objects.create(invoice=invoice, item= p.product, quantity=p.quantity, unit_price= p.price, total_price=p.sub_total, discount=p.dicount ,after_discount=a_d)
                    iv_item.save()
                    iv_item.calculate_profit()
        
    shift.status = 1
    shift.invoice = invoice
    shift.end_time = datetime.datetime.now()
    shift.save()
    invoice.saved = True
    invoice.treasury_in = total
    invoice.overall = total
    invoice.save()
    invoice.calculate_profit()


    if request.is_ajax():
        return JsonResponse({})
    else:
        return redirect('POS:POSCard', pk=shift.pos.id)
    
def Report(request, id):
    all_products=[]
    q = []
    if not request.user.has_perm('POS.view_shift_report'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية لعرض تقارير الشيفت')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    money=0
    single_shift = Shift.objects.get(id = id)
    total_order_done = Order.objects.filter(shift = single_shift , status =2)
    ttotal = total_order_done.count()
    total_order_canceled = Order.objects.filter(shift = single_shift , status =3).count()
    open_orders= Order.objects.filter(shift = single_shift , status='1').count()
    for x in total_order_done:
        money = money +( x.total - x.discount_value)
        all_Order_detail = Order_detail.objects.filter(order=x)
        for o in all_Order_detail:
            if o.product.product_type == 2 :
                small_products = GroupedProduct.objects.filter(grouped_item = o.product)
                for s_p in small_products:
                    sub_product = s_p.contain
                    sub_quantity = o.quantity * s_p.quantity
                    if len(all_products) > 0 : 
                        number  = 0 
                        for a in range(len(all_products)):
                            if ( all_products[a] == sub_product):
                                q[a]= q[a] + sub_quantity
                                number = 1
                        if number == 0:
                            all_products.append(sub_product)
                            q.append(sub_quantity)
                    else:
                        all_products.append(sub_product)
                        q.append(sub_quantity)
            else:
                sub_product = o.product
                sub_quantity = o.quantity
                if len(all_products) > 0 :
                    number  = 0 
                    for a in range(len(all_products)):
                        if ( all_products[a] == sub_product):
                            q[a]= q[a] + sub_quantity
                            number = 1
                    if number == 0 :
                        all_products.append(sub_product)
                        q.append(sub_quantity)
                else:
                    all_products.append(sub_product)
                    q.append(sub_quantity)
    shift_products = zip(all_products,q)
    return render(request, 'POS/shifts_report.html', {'single_shift':single_shift, 'total_order_done':total_order_done, 'total_order_canceled':total_order_canceled, 
        'money':money,'open_orders':open_orders,'ttotal':ttotal, 'shift_products':shift_products })

class CreateShiftWithOrders(LoginRequiredMixin, PermissionRequiredMixin ,CreateView):
    login_url = '/auth/login/'
    model = Shift
    form_class = ShiftForm
    template_name = 'Core/form_template.html'
    permission_required = 'POS.add_shift'

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات لإضافة شيفت جديد')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' إضافة شيفت جديد وتحويل الطلبات المفتوحة إليه'
        context['action_url'] = reverse_lazy('POS:CreateShiftWithOrders', kwargs={'id': self.kwargs['pk']})
        return context
    
    def form_valid(self, form):
        object = form.save(commit = False)
        p = POS.objects.get(id=self.kwargs['pk'])
        object.pos = p
        object.save()

        open_orders = Order.objects.filter(shift= Shift.objects.get(id= self.kwargs['shiftId']) , status='1')
        for order in open_orders:
            order.shift = object
            order.save()
        EndShift(self.request, self.kwargs['shiftId'])
        return super().form_valid(form)

    def get_success_url(self):
        shift= Shift.objects.get(id= self.kwargs['shiftId'])
        return reverse_lazy('POS:POSCard', kwargs={'pk': shift.pos.id })

class ShiftDelete(LoginRequiredMixin, PermissionRequiredMixin , UpdateView):
    login_url = '/auth/login/'
    model = Shift
    form_class = ShiftDeleteForm
    template_name = 'Core/form_template.html'
    permission_required = 'POS.delete_shift'

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات لحذف الشيفت')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف الشيفت : ' + str(self.object)
        context['action_url'] = reverse_lazy('POS:ShiftDelete', kwargs={'pk': self.kwargs['pk']})
        return context

    def get_success_url(self):
        return reverse_lazy('POS:POSCard', kwargs={'pk': self.kwargs['POSId'] })

################## ORDER ##################
class OrderCreate(LoginRequiredMixin, PermissionRequiredMixin , CreateView):
    login_url = '/auth/login/'
    model = Order
    form_class = OrderForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('POS:ShiftCard')
    permission_required = 'POS.add_order'

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات لإضافة طلب')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة طلب جديد'
        context['action_url'] = reverse_lazy('POS:OrderCreate', kwargs={'pk': self.kwargs['pk']})
        return context
    
    def form_valid(self, form):
        object = form.save(commit = False)
        p = Shift.objects.get(id=self.kwargs['pk'])
        object.pos = p.pos
        object.shift = p
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

def OrderCreateByTabel(request, s_id , t_id):
    if not request.user.has_perm('POS.add_order'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية لإضافة طلب جديد')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    shift = Shift.objects.get(id = s_id)
    table = Table.objects.get(id = t_id)
    table.status = 2
    table.save()
    setting = get_pos_base_setting()
    if (setting.default_customer_in_sales != None):
        order = Order.objects.create(pos=shift.pos, shift= shift , floor= table.floor , table= table, customer= setting.default_customer_in_sales)
    else:
        order = Order.objects.create(pos=shift.pos, shift= shift , floor= table.floor , table= table)
    return redirect('POS:OrderUpdate', id=str(order.id))
    

def OrderUpdate(request , id):
    if not request.user.has_perm('POS.edit_order'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية  لتعديل الطلب')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    single_order = Order.objects.get(id = id)
    if str(single_order.status) == '1':
        all_products = Product.objects.all()
        MainCategories = MainCategory.objects.all()
        SubCategories = SubCategory.objects.all()
        open_orders= Order.objects.filter(shift=single_order.shift.id , status='1' , deleted =False )
        shiftInfo = Shift.objects.get(id = single_order.shift.id )
        floors = Floor.objects.filter(pos = single_order.pos )
        tables = Table.objects.all()
        customer_addresses = Address.objects.filter(customer= single_order.customer)
        all_phones = Phone.objects.all()
        all_customer = Customer.objects.all()
        partners = Partner.objects.all()
        context = {
            'all_products':all_products, 
            'single_order':single_order, 
            'MainCategories':MainCategories, 
            'SubCategories':SubCategories, 
            'open_orders':open_orders,  
            'shiftInfo':shiftInfo, 
            'customer_addresses':customer_addresses, 
            'floors':floors,    
            'tables':tables,
            'all_phones': all_phones,
            'all_customer':all_customer,
            'partners':partners,
        }
        return render(request,'POS/new_order.html', context)
    else:
        if not request.user.has_perm('POS.view_order_bill'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية للدخول لفاتورة الطلب ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        order_items = Order_detail.objects.filter(order = single_order)
        return render(request,'POS/bill.html',{'order':single_order, 'order_items':order_items})

def Orderdetail(request, id):
    single_order = Order.objects.get(id = id)
    products_names = []
    user_temporary_order = Order_detail.objects.filter(order = single_order)

    try:
        deliveryCost = float(single_order.address.country_delivery_cost) +  float(single_order.address.governorate_delivery_cost) + float(single_order.address.area_delivery_cost)
        f = single_order.total - single_order.discount_value + deliveryCost
    except:
        deliveryCost = 0
        f = single_order.total - single_order.discount_value + single_order.pos.service

    o_list = [single_order.taxes , f , single_order.discount_value , deliveryCost , single_order.pos.service ] 

    for x in user_temporary_order:
        products_names.append(x.product.name)
    return JsonResponse({"orders":list(user_temporary_order.values()),"products_names":products_names , 'o_list':o_list })

def AddOrderdetail(request ,o_id, id , q):
    if not request.user.has_perm('POS.add_order_detail'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية  لإضافة منتجات للطلب ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    product = Product.objects.get(id=id)
    order = Order.objects.get(id = o_id)
    taxes = 0.0

    try:
        if(str(product.tax.type) == '1'):
            taxes = float(product.tax.value) * float(q)
        else:
            taxes = float( product.tax.value * product.sell_price / 100)  * float(q)
    except:
        pass
    total_without = float(product.sell_price) * float(q)
    s_t = (float(product.sell_price) * float(q)) + float(taxes)

    try:
        repeated_item = Order_detail.objects.get(order = order , product= product)
        if repeated_item:
            repeated_item.quantity = float(repeated_item.quantity) + float(q)
            repeated_item.taxes = float(repeated_item.taxes) + float(taxes)
            repeated_item.total_wo_taxes = float(repeated_item.total_wo_taxes) + float(total_without)
            repeated_item.sub_total = float(repeated_item.sub_total) + float(s_t)
            repeated_item.save()
    except:
        T_O = Order_detail(order= order, product= product, quantity= q, price= product.sell_price, taxes= taxes, total_wo_taxes=total_without , sub_total = s_t)
        T_O.save()

    order.total = order.total + s_t
    order.taxes = order.taxes + taxes
    order.save()
    
    return JsonResponse({})

def SingleProduct(request, id):
    single_product = Product.objects.filter(id=id)
    if request.user.has_perm('POS.add_order_detail_returns'):
        perm = 1
    else:
        perm = 0
    return JsonResponse({"single_product":list(single_product.values()), "perm":perm})

def OrderTotalPrice(request):
    orderId = request.GET['orderId']
    total_tax = request.GET['total_tax']
    final_price = request.GET['final_price']
    single_order = Order.objects.get(id = orderId)
    single_order.total = final_price
    single_order.taxes = total_tax
    single_order.save()
    return JsonResponse({})

def CheckOut(request):
    if not request.user.has_perm('POS.close_order'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية لإغلاق الطلب ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    orderId = request.GET['orderId']
    total_tax = request.GET['total_tax']
    final_price = request.GET['final_price']
    paid = request.GET['paid']
    method = request.GET['method']
    single_order = Order.objects.get(id = orderId)
    single_order.total = final_price
    single_order.taxes = total_tax
    single_order.status = 2
    single_order.total_paid = paid
    single_order.payment_method = method
    try: 
        print(request.GET['partner_id'])
        partner = Partner.objects.get(id = int(request.GET['partner_id']))
        single_order.partner = partner
    except:
        single_order.partner = None


    if str(single_order.pos.type) == '3':
        try:
            single_order.delivery_cost = float(single_order.address.country_delivery_cost) +  float(single_order.address.governorate_delivery_cost)
        except:
            messages.add_message(request, messages.ERROR , 'يجب اختيار عنوان العميل')
            return JsonResponse({}) 
    if str(single_order.pos.type) == '1':
        try:
            t = Table.objects.get(id = single_order.table.id )
            t.status = 1
            t.save()
        except:
            messages.add_message(request, messages.ERROR , 'يجب اختيار الطابق والطاولة')
            return JsonResponse({})    
    single_order.save()
    return JsonResponse({})
    

def bill(request , id):
    if not request.user.has_perm('POS.view_order_bill'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية للدخول لفاتورة الطلب ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    order = Order.objects.get(id = id)
    order_items = Order_detail.objects.filter(order = order)
    return render(request,'POS/bill.html',{'order':order, 'order_items':order_items})

def addDiscount(request):
    if not request.user.has_perm('POS.add_order_discount'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية لإضافة خصم للطلب ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    single_order = Order.objects.get(id = request.GET['orderId'])
    single_order.discount_type = request.GET['percantageType']
    single_order.discount_value = request.GET['discountValue']
    single_order.save()
    return JsonResponse({})

class OrderCustomerUpdate(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'Core/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل العميل: '
        return context

    def form_valid(self, form):
        object = form.save(commit = False)
        object.address = None
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('POS:OrderUpdate', kwargs={'id': self.kwargs['pk']})

class CustomerAddressUpdate(UpdateView):
    model = Order
    template_name = 'Core/form_template.html'
    
    def get_success_url(self):
        return reverse_lazy('POS:OrderUpdate', kwargs={'id': self.kwargs['pk']})

    def get_form(self, form_class=CustomerAddressUpdateForm):
        customer = Customer.objects.get(id = self.object.customer.id )
        form = super(CustomerAddressUpdate, self).get_form(form_class)
        form.fields['address'].queryset = Address.objects.filter(customer=customer)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل عنوان العميل:'
        return context

def OrderCancel(request,id , shiftid):
    if not request.user.has_perm('POS.cancel_order'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    single_order = Order.objects.get(id = id)
    single_order.status = 3
    if single_order.pos.type == 1:
        table = Table.objects.get(id = single_order.table.id )
        table.status = 1 
        table.save()
    single_order.save()
    return redirect('POS:ShiftCard', pk=shiftid)

class OrderDelete(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Order
    form_class = OrderDeleteForm
    template_name = 'Core/form_template.html'
    permission_required = 'POS.delete_order'

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات لحذف الطلب')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف الطلب : ' + str(self.object)
        context['action_url'] = reverse_lazy('POS:OrderDelete', kwargs={'pk': self.kwargs['pk']})
        return context

    def get_success_url(self):
        return reverse_lazy('POS:ShiftCard', kwargs={'pk': self.object.shift.id })

def PrintSetting(request):
    if not request.user.has_perm('POS.edit_order_print'):
            messages.add_message(request, messages.ERROR , ' لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    try:
        setting = OrderPrintSetting.objects.get(id=1)
    except:
        setting = OrderPrintSetting()
        setting.save()
    form = OrderPrintForm(request.POST or None, request.FILES or None, instance=setting)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect(request.POST.get('url'))
    context = {
        'title': 'إعدادات طباعة الطلبات',
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)

def printInvoice(request, pk):
    order = Order.objects.get(id = pk)
    order_items = Order_detail.objects.filter(order = order)
    try:
        setting = OrderPrintSetting.objects.get(id=1)
    except:
        setting = OrderPrintSetting()
        setting.save()
    context = {
        'order': order,
        'order_items':order_items,
        'setting': setting,
    }
    return render(request, 'POS/Print/' + str(setting.size) + '.html', context)

class OrderFloorUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Order
    template_name = 'Core/form_template.html'
    permission_required = 'POS.edit_order_floor'

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات الكافية')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل الدور: '
        return context
    
    def get_form(self, form_class=OrderFloorForm):
        pos = POS.objects.get(id = self.object.pos.id )
        form = super(OrderFloorUpdate, self).get_form(form_class)
        form.fields['floor'].queryset = Floor.objects.filter(pos=pos)
        return form

    def form_valid(self, form):
        object = form.save(commit = False)
        if object.table != None:
            table = Table.objects.get(id = object.table.id)
            table.status = 1
            table.save()
        object.table = None
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('POS:OrderUpdate', kwargs={'id': self.kwargs['pk']})

class OrderTabelUpdate(LoginRequiredMixin, PermissionRequiredMixin , UpdateView):
    login_url = '/auth/login/'
    model = Order
    template_name = 'Core/form_template.html'
    permission_required = 'POS.edit_order_table'

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات الكافية')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل الطاولة: '
        return context
    
    def get_form(self, form_class=OrderTabelForm):
        floor = Floor.objects.get(id = self.object.floor.id )
        form = super(OrderTabelUpdate, self).get_form(form_class)
        form.fields['table'].queryset = Table.objects.filter(floor=floor, status=1)
        return form
    
    def form_valid(self, form):
        object = form.save(commit = False)
        table = Table.objects.get(id = object.table.id)
        table.status = 2
        table.save()
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('POS:OrderUpdate', kwargs={'id': self.kwargs['pk']})

def Delete_order_detail(request, id):
    if not request.user.has_perm('POS.delete_order_detail'):
            messages.add_message(request, messages.ERROR , ' لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    c = Order_detail.objects.get(id = id)
    order = Order.objects.get(id = c.order.id)
    order.taxes = order.taxes - c.taxes 
    order.total = order.total - c.sub_total
    order.save()
    c.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def ChangeOrderDetailQuantity(request):
    new_value = int(request.GET['new_value'])
    order_detail = Order_detail.objects.get(id = request.GET['product_id'])
    product = Product.objects.get(id=order_detail.product.id)
    order = Order.objects.get(id = order_detail.order.id )

    d = new_value - order_detail.quantity 
    
    if d > 0 : 
        order_detail.quantity = new_value
        taxes = 0.0
        try:
            if(str(product.tax.type) == '1'):
                taxes = float(product.tax.value) * d
            else:
                taxes = float( product.tax.value * product.sell_price / 100)  * d
        except:
            pass
        total_without = float(product.sell_price) * d
        s_t = (float(product.sell_price) * d) + float(taxes)

        order_detail.taxes = order_detail.taxes + taxes
        order_detail.total_wo_taxes = order_detail.total_wo_taxes + total_without
        order_detail.sub_total = order_detail.sub_total + s_t
        order_detail.save()

        order.total = order.total + s_t
        order.taxes = order.taxes + taxes
        order.save()
    elif d < 0 :
        order_detail.quantity = new_value
        taxes = 0.0

        try:
            if(str(product.tax.type) == '1'):
                taxes = float(product.tax.value) * d
            else:
                taxes = float( product.tax.value * product.sell_price / 100)  * d
        except:
            pass
        total_without = float(product.sell_price) * d
        s_t = (float(product.sell_price) * d) + float(taxes)

        order_detail.taxes = order_detail.taxes + taxes
        order_detail.total_wo_taxes = order_detail.total_wo_taxes + total_without
        order_detail.sub_total = order_detail.sub_total + s_t
        order_detail.save()

        order.total = order.total - s_t
        order.taxes = order.taxes - taxes
        order.save()
    else:
        pass
    return JsonResponse({})

####### old function #######
def add_customer_to_order(request, pk):
    if not request.user.has_perm('POS.edit_order_customer'):
        messages.error(request, 'لا تمتلك الصلاحيات الكافية لإضافة عميل \ مورد')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    order = get_object_or_404(Order, id=pk)
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        customer = form.save(commit=False)
        customer.save()
        order.customer = customer
        order.save()
        return redirect('POS:OrderUpdate', pk)
    context = {
        'title': 'إضافة عميل \ مورد',
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)
####### old function ####### 

def add_customer_to_order1(request, pk , c_pk ):
    if not request.user.has_perm('POS.edit_order_customer'):
        messages.error(request, 'لا تمتلك الصلاحيات الكافية لإضافة عميل \ مورد')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    order = get_object_or_404(Order, id=pk)
    customer = Customer.objects.get(id = c_pk)
    order.customer = customer
    order.address = None
    order.save()
    return redirect('POS:OrderUpdate', pk)

def add_customer_to_order_by_phone(request, pk , p_pk ):
    if not request.user.has_perm('POS.edit_order_customer'):
        messages.error(request, 'لا تمتلك الصلاحيات الكافية لإضافة عميل \ مورد')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    order = get_object_or_404(Order, id=pk)
    phone = Phone.objects.get(id = p_pk)
    order.customer = phone.customer
    order.address = None
    order.save()
    return redirect('POS:OrderUpdate', pk)


class AddOrderDeliveryEmployee(LoginRequiredMixin, PermissionRequiredMixin , UpdateView):
    login_url = '/auth/login/'
    model = Order
    form_class = OrderDeliveryEmployeeForm
    template_name = 'Core/form_template.html'
    permission_required = 'POS.edit_order_table'

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات الكافية')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'اسناد الطلب الى: '
        return context

    def get_success_url(self):
        return reverse_lazy('POS:OrderUpdate', kwargs={'id': self.kwargs['pk']})

class AddNewAddress(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'Customers.add_address'
    model = Address
    form_class = AddressForm1
    template_name = 'Core/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضاف عنوان للعميل'
        context['action_url'] = reverse_lazy('Customers:AddressCreate')
        return context

    def get_form(self, form_class=AddressForm1):
        order = Order.objects.get(id = self.kwargs['pk'])
        form = super(AddNewAddress, self).get_form(form_class)
        form.fields['country'].widget.attrs.update({'value': order.pos.country })
        form.fields['region'].widget.attrs.update({'value': order.pos.region })
        form.fields['governorate'].widget.attrs.update({'value': order.pos.governorate })
        return form
        
    def form_valid(self, form):
        order = Order.objects.get(id = self.kwargs['pk'])
        object = form.save(commit = False)
        object.customer = order.customer
        object.country_delivery_cost = order.pos.country_delivery_cost 
        object.governorate_delivery_cost = order.pos.governorate_delivery_cost 
        object.save()
        order.address = object
        order.save()
        return super().form_valid(form)

    def get_success_url(self):
        order = Order.objects.get(id = self.kwargs['pk'])
        return reverse_lazy('POS:OrderUpdate', kwargs={'id': order.id})
        
################## FLOOR ##################
class FloorCreate(LoginRequiredMixin, PermissionRequiredMixin , CreateView):
    login_url = '/auth/login/'
    model = Floor
    form_class = FloorForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('POS:POSCard')
    permission_required = 'POS.add_floor'

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات الكافية لإضافة طابق')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة دور جديد'
        context['action_url'] = reverse_lazy('POS:FloorCreate', kwargs={'pk': self.kwargs['pk']})
        return context
    
    def form_valid(self, form):
        object = form.save(commit = False)
        pos = POS.objects.get(id=self.kwargs['pk'])
        print(self.kwargs['pk'])
        object.pos = pos
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

def FloorDelete(request, pk):
    if not request.user.has_perm('POS.delete_floor'):
            messages.add_message(request, messages.ERROR , ' لا تمتلك الصلاحيات الكافية لحذف طابق')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    floor = Floor.objects.get(id=pk)
    POSId = floor.pos.id
    floor.delete()
    return redirect('POS:POSCard', pk=POSId)

################## FLOOR ##################

################## TABLE ##################
class TableCreate(LoginRequiredMixin, PermissionRequiredMixin , CreateView):
    login_url = '/auth/login/'
    model = Table
    form_class = TableForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('POS:POSCard')
    permission_required = 'POS.add_table'

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات الكافية لإضافة طاولة')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة طاولة جديدة'
        context['action_url'] = reverse_lazy('POS:TableCreate', kwargs={'pk': self.kwargs['pk']})
        return context
    
    def form_valid(self, form):
        object = form.save(commit = False)
        floor = Floor.objects.get(id=self.kwargs['pk'])
        print(self.kwargs['pk'])
        object.floor = floor
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

def TableDelete(request, pk):
    if not request.user.has_perm('POS.delete_table'):
            messages.add_message(request, messages.ERROR , ' لا تمتلك الصلاحيات الكافية لحذف الطاولة')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    table = Table.objects.get(id=pk)
    POSId = table.floor.pos.id
    table.delete()
    return redirect('POS:POSCard', pk=POSId)
################## TABLE ##################
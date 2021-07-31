from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import *
from django.urls import reverse_lazy
from .forms import *
from Customers.forms import CustomerForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
import xlwt


# Create your views here.
def get_invoice_base_setting():
    try:
        setting = InvoiceBaseSetting.objects.get(id=1)
    except:
        setting = InvoiceBaseSetting()
        setting.save()
    return setting

def get_invoices(request, invoice_type=None):
    if request.user.is_superuser:
        invoices = Invoice.objects.all()
        if invoice_type:
            invoices = invoices.filter(invoice_type=int(invoice_type))
    else:
        invoices = Invoice.objects.filter(creator=request.user, deleted=False)
        if invoice_type:
            invoices = invoices.filter(invoice_type=int(invoice_type))
    return invoices

def make_invoice(request, type):
    setting = get_invoice_base_setting()
    invoice = Invoice(invoice_type=type)
    if setting.default_customer_in_sales:
        if invoice.invoice_type == 1:
            invoice.customer = setting.default_customer_in_sales
    if type in [1, 2, 3, 6, 7]:
        invoice.from_branch = request.user.default_branch
        invoice.to_treasury = request.user.default_treasury
    if type in [4, 5]:
        invoice.to_branch = request.user.default_branch
        invoice.from_treasury = request.user.default_treasury
    invoice.save()
    return redirect('Invoices:show_invoice', invoice.id)

def show_invoice(request, pk):
    message = ''
    warning = []
    setting = get_invoice_base_setting()
    invoice = get_object_or_404(Invoice, id=pk)
    out_stock_invoices = [1, 2, 3, 6, 15]
    in_stock_invoices = [4, 5, 16]
    in_treasury_invoices = [1, 2, 3, 6, 12]
    out_treasury_invoices = [4, 5, 11]
    invoices = get_invoices(request, invoice.invoice_type).order_by('id')
    prev_invoice = invoices.filter(id__lt=invoice.id).last()
    next_invoice = invoices.filter(id__gt=invoice.id).first()
    opened_invoices = Invoice.objects.filter(saved=False, invoice_type=invoice.invoice_type, deleted=False)
    categories = Category.objects.filter(deleted=False)
    products = Product.objects.all()
    form = InvoiceItemForm(request.POST or None)
    form.fields['item'].queryset = Product.objects.filter(deleted=False)
    context = {
        'invoice': invoice,
        'opened_invoices': opened_invoices,
        'categories': categories,
        'products': products,
        'form': form,
        'prev_invoice': prev_invoice,
        'next_invoice': next_invoice,
        'out_stock_invoices': out_stock_invoices,
        'in_stock_invoices': in_stock_invoices,
        'in_treasury_invoices': in_treasury_invoices,
        'out_treasury_invoices': out_treasury_invoices,

    }
    if form.is_valid():
        item = form.save(commit=False)
        if invoice.from_branch or invoice.to_branch:
            if invoice.from_branch:
                item_stock = item.item.branch_stock(invoice.from_branch.id)
            if invoice.to_branch:
                item_stock = item.item.branch_stock(invoice.to_branch.id)
        else:
            item_stock = item.item.current_stock()
        if invoice.invoice_type in [1, 2, 6]:
            if not setting.sell_without_stock:
                if not item_stock - item.quantity >= 0:
                    message = 'عفواً لا يوجد رصيد كافٍ. الرصيد المتاح: ' + str(item_stock)
                    messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
                    return render(request, 'Invoices/OneByOne/invoice_detail.html', context)
            if setting.alert_on_critical_storage:
                if not item_stock - item.quantity > item.item.critical_stock:
                    message = 'المنتج: ' + item.item.name + ".وصل للرصيد الحرج."
                    messages.add_message(request, messages.WARNING, message)
            if setting.alert_on_min_cost_price:
                if item.unit_price <= item.item.cost_price:
                    warning = 'تنبيه: سعر البيع أقل من سعر التكلفة'
                    if request.user.has_perm('Invoices.access_purchase_invoice_menu'):
                        message = ' سعر التكلفة: ' + str(item.item.cost_price)
                    messages.add_message(request, messages.WARNING, message)
            if setting.alert_on_min_purchase_price:
                if item.unit_price <= item.item.purchase_price:
                    message = 'تنبيه: سعر البيع أقل من سعر الشراء'
                    if request.user.has_perm('Invoices.access_purchase_invoice_menu'):
                        message = ' سعر الشراء: ' + str(item.item.purchase_price)
                    messages.add_message(request, messages.WARNING, message)

        if invoice.invoice_type == 5:
            if setting.update_cost_profit_on_purchase:
                item.item.cost_price = item.unit_price
                item.item.save()

        item.invoice = invoice
        if invoice.invoice_type in [1, 2, 3, 4, 7]:
            if item.unit_price == 0.0:
                item.unit_price = item.item.sell_price
        elif invoice.invoice_type in [5, 6]:
            if item.unit_price == 0.0:
                item.unit_price = item.item.cost_price

        item.total_price = item.unit_price * item.quantity
        item.after_discount = item.total_price - item.discount
        item.save()
        item.calculate_profit()
        invoice.calculate()
        # return render(request, 'Invoices/OneByOne/invoice_detail.html', context)
        return redirect('Invoices:show_invoice', invoice.id)
    return render(request, 'Invoices/OneByOne/invoice_detail.html', context)

def save_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    setting = get_invoice_base_setting()
    if invoice.saved:
        return render(request, 'empty_base.html', context={'alert': 'هذه الفاتورة محفوظة بالفعل'})
    if not invoice.invoice_type in [15, 16, 17]:
        if not invoice.customer:
            return render(request, 'empty_base.html', context={'alert': 'يجب اختيار العميل/المورد قبل الحفظ'})
    if invoice.invoice_type in [1, 2, 4, 5, 6]:
        if not invoice.from_treasury and not invoice.to_treasury:
            return render(request, 'empty_base.html', context={'alert': 'يجب اختيار الخزينة قبل الحفظ'})
        if not invoice.from_branch and not invoice.to_branch:
            return render(request, 'empty_base.html', context={'alert': 'يجب اختيار الفرع قبل الحفظ'})

    invoice.calculate()
    invoice.creator = request.user
    action_url = reverse_lazy('Invoices:save_invoice', kwargs={'pk': invoice.id})
    invoice.save()
    if invoice.invoice_type in [1, 2, 3, 6]:
        form = SalesInvoiceForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type in [4, 5]:
        form = PurchaseInvoiceForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type in [15, 16]:
        form = PlusMinusForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type == 7:
        form = QuotationForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type == 17:
        form = StockTransferSaveForm(request.POST or None, instance=invoice)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.saved = True
        obj.save()
        invoice.save_invoice()
        if setting.update_cost_profit_on_purchase:
            invoice.update_cost_profit()
        return redirect('Invoices:show_invoice', invoice.id)
    context = {
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)

def unsave_invoice(request, pk):
    if not request.user.has_perm('Invoices.undo_save_invoice'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    invoice = get_object_or_404(Invoice, id=pk)
    invoice.calculate()
    invoice.creator = request.user
    invoice.save()
    action_url = reverse_lazy('Invoices:unsave_invoice', kwargs={'pk': invoice.id})
    form = InvoiceUnSaveForm(request.POST or None, instance=invoice)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect('Invoices:show_invoice', invoice.id)
    context = {
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)

def delete_invoice(request, pk):
    if not request.user.has_perm('Invoices.delete_invoice'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    invoice = get_object_or_404(Invoice, id=pk)
    invoice_type = invoice.invoice_type
    title = "حذف " + invoice.__str__()
    action_url = reverse_lazy('Invoices:delete_invoice', kwargs={'pk': invoice.id})
    form = InvoiceDeleteForm(request.POST or None, instance=invoice)
    if form.is_valid():
        form.save()
        return redirect('Invoices:show_opened_invoices', invoice_type)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)

def show_opened_invoices(request, type):
    opened_invoices = Invoice.objects.filter(saved=False, invoice_type=type, deleted=False)
    context = {
        'opened_invoices': opened_invoices,
        'type': type,
    }
    return render(request, 'Invoices/OneByOne/opened_invoices.html', context)

def delete_invoice_item(request, pk):
    item = get_object_or_404(InvoiceItem, id=pk)
    invoice = item.invoice
    item.delete()
    invoice.calculate()
    return redirect('Invoices:show_invoice', invoice.id)

def edit_invoice_item_price(request, pk):
    if not request.user.has_perm('Invoices.edit_item_unit_price'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    setting = get_invoice_base_setting()
    item = get_object_or_404(InvoiceItem, id=pk)
    invoice = item.invoice
    if invoice.from_branch or invoice.to_branch:
        if invoice.from_branch:
            item_stock = item.item.branch_stock(invoice.from_branch.id)
        if invoice.to_branch:
            item_stock = item.item.branch_stock(invoice.to_branch.id)
    else:
        item_stock = item.item.current_stock()
    form = InvoiceItemPriceUpdateForm(request.POST or None, instance=item)
    title = 'تعديل سعر ' + item.item.name
    action_url = reverse_lazy('Invoices:edit_invoice_item_price', kwargs={'pk': item.id})
    if form.is_valid():
        item = form.save(commit=False)
        if invoice.invoice_type in [1, 2, 6]:
            if setting.alert_on_min_cost_price:
                if item.unit_price <= item.item.cost_price:
                    message = 'تنبيه: سعر البيع أقل من سعر التكلفة'
                    if request.user.has_perm('Invoices.access_purchase_invoice_menu'):
                        message += ' سعر التكلفة: ' + str(item.item.cost_price)
                    messages.add_message(request, messages.WARNING, message)
            if setting.alert_on_min_purchase_price:
                if item.unit_price <= item.item.purchase_price:
                    message = 'تنبيه: سعر البيع أقل من سعر الشراء'
                    if request.user.has_perm('Invoices.access_purchase_invoice_menu'):
                        message += ' سعر الشراء: ' + str(item.item.purchase_price)
                    messages.add_message(request, messages.WARNING, message)

        item.calculate()
        return redirect('Invoices:show_invoice', item.invoice.id)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)

def edit_invoice_item_quantity(request, pk):
    item = get_object_or_404(InvoiceItem, id=pk)
    invoice = item.invoice
    setting = get_invoice_base_setting()
    if invoice.from_branch or invoice.to_branch:
        if invoice.from_branch:
            item_stock = item.item.branch_stock(invoice.from_branch.id)
        if invoice.to_branch:
            item_stock = item.item.branch_stock(invoice.to_branch.id)
    else:
        item_stock = item.item.current_stock()
    form = InvoiceItemQuantityUpdateForm(request.POST or None, instance=item)
    title = 'تعديل كمية ' + item.item.name
    action_url = reverse_lazy('Invoices:edit_invoice_item_quantity', kwargs={'pk': item.id})
    if form.is_valid():
        item = form.save(commit=False)
        if invoice.invoice_type in [1, 2, 6]:
            if not setting.sell_without_stock:
                if not item_stock - item.quantity >= 0:
                    message = 'عفواً لا يوجد رصيد كافٍ. الرصيد المتاح: ' + str(item_stock)
                    messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
                    return redirect('Invoices:show_invoice', item.invoice.id)
            if setting.alert_on_critical_storage:
                if not item_stock - item.quantity > item.item.critical_stock:
                    message = 'المنتج: ' + item.item.name + ".وصل للرصيد الحرج."
                    messages.add_message(request, messages.WARNING, message)
        form.save()
        item.calculate()
        return redirect('Invoices:show_invoice', item.invoice.id)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)

def edit_invoice_date(request, pk):
    if not request.user.has_perm('Invoices.edit_invoice_date'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    invoice = get_object_or_404(Invoice, id=pk)
    form = InvoiceDateForm(request.POST or None, instance=invoice)
    title = 'تعديل تاريخ فاتورة ' + invoice.__str__()
    action_url = reverse_lazy('Invoices:edit_invoice_date', kwargs={'pk': invoice.id})
    if form.is_valid():
        form.save()
        invoice.calculate()
        return redirect('Invoices:show_invoice', invoice.id)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)

def edit_invoice_item_discount(request, pk):
    if not request.user.has_perm('Invoices.item_discount'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    item = get_object_or_404(InvoiceItem, id=pk)
    form = InvoiceItemDiscountUpdateForm(request.POST or None, instance=item)
    title = 'تعديل خصم ' + item.item.name
    action_url = reverse_lazy('Invoices:edit_invoice_item_discount', kwargs={'pk': item.id})
    if form.is_valid():
        form.save()
        item.calculate()
        return redirect('Invoices:show_invoice', item.invoice.id)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)

def edit_invoice_discount(request, pk):
    if not request.user.has_perm('Invoices.invoice_discount'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    invoice = get_object_or_404(Invoice, id=pk)
    title = 'تعديل خصم فاتورة'
    action_url = reverse_lazy('Invoices:edit_invoice_discount', kwargs={'pk': invoice.id})
    form = InvoiceDiscountUpdateForm(request.POST or None, instance=invoice)
    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.save()
        invoice.calculate_after_discount()
        return redirect('Invoices:show_invoice', invoice.id)
    context = {
        'title': title,
        'action_url': action_url,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)

def edit_invoice_customer(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    title = 'العميل / مورد'
    action_url = reverse_lazy('Invoices:edit_invoice_customer', kwargs={'pk': invoice.id})
    form = InvoiceCustomerForm(request.POST or None, instance=invoice)
    form.fields['customer'].queryset = Customer.objects.filter(deleted=False)
    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.save()
        history = CustomerHistory()
        if invoice.invoice_type == 1:
            history.history_type = 4
        if invoice.invoice_type == 7:
            history.history_type = 3
        if invoice.invoice_type == 4:
            history.history_type = 5
        if invoice.invoice_type == 5:
            history.history_type = 6
        if invoice.invoice_type == 6:
            history.history_type = 7
        history.customer = invoice.customer
        history.invoice_id = invoice.id
        history.added_by = request.user
        history.save()
        return redirect('Invoices:show_invoice', invoice.id)
    context = {
        'title': title,
        'action_url': action_url,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)

def edit_invoice_branch(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    title = 'الفرع'
    action_url = reverse_lazy('Invoices:edit_invoice_branch', kwargs={'pk': invoice.id})
    if invoice.invoice_type in [1, 2, 3, 6, 7, 15]:
        form = InvoiceFromBranchForm(request.POST or None, instance=invoice)
    if invoice.invoice_type in [4, 5, 16]:
        form = InvoiceToBranchForm(request.POST or None, instance=invoice)
    if invoice.invoice_type == 17:
        form = BranchTransferForm(request.POST or None, instance=invoice)
    if not request.user.is_superuser:
        if invoice.invoice_type in [1, 2, 3, 6, 7]:
            form.fields['from_branch'].queryset = request.user.allowed_branches.all()
        if invoice.invoice_type in [4, 5]:
            form.fields['to_branch'].queryset = request.user.allowed_branches.all()
    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.save()
        return redirect('Invoices:show_invoice', invoice.id)
    context = {
        'title': title,
        'action_url': action_url,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)

def edit_invoice_treasury(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    title = 'الخزينة'
    action_url = reverse_lazy('Invoices:edit_invoice_treasury', kwargs={'pk': invoice.id})
    if invoice.invoice_type in [1, 2, 3, 6]:
        form = InvoiceToTreasuryForm(request.POST or None, instance=invoice)
    if invoice.invoice_type in [4, 5]:
        form = InvoiceFromTreasuryForm(request.POST or None, instance=invoice)
    if not request.user.is_superuser:
        if invoice.invoice_type in [1, 2, 3, 6]:
            form.fields['to_treasury'].queryset = request.user.allowed_treasuries.all()
        if invoice.invoice_type in [4, 5]:
            form.fields['from_treasury'].queryset = request.user.allowed_treasuries.all()
    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.save()
        return redirect('Invoices:show_invoice', invoice.id)
    context = {
        'title': title,
        'action_url': action_url,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)

def get_unit_price(request, invoice_id):
    product = get_object_or_404(Product, id=request.GET.get('product_id'))
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if invoice.invoice_type in [1, 2, 3, 4, 7]:
        try:
            price = ProductPrices.objects.get(product=product , customer_segment = invoice.customer.category)
            return HttpResponse(price.new_price)
        except:
            return HttpResponse(product.sell_price)
        
    if invoice.invoice_type in [5, 6]:
        return HttpResponse(product.purchase_price)

def expense_invoice(request):
    title = 'إذن صرف نقدية'
    form = ExpenseInvoiceForm(request.POST or None)
    if not request.user.is_superuser:
        form.fields['treasury'].querset = request.user.allowed_treasuries.all()
        if not request.user.has_perm('Invoices.edit_invoice_date'):
            form.fields['date'].disabled = True
    form.initial['treasury'] = request.user.default_treasury
    action_url = reverse_lazy('Invoices:expense_invoice')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.invoice_type = 11
        obj.creator = request.user
        obj.saved = True
        obj.save()
        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)

def edit_fast_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    title = 'تعديل ' + str(invoice)
    if invoice.invoice_type == 11:
        form = ExpenseInvoiceForm(request.POST or None, instance=invoice)
    if invoice.invoice_type == 12:
        form = IncomeInvoiceForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type == 13:
        form = CapitalIncomeForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type == 14:
        form = CapitalOutcomeForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type == 19:
        form = TreasuryTransferForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type == 24:
        form = DailyRestrictionsForm(request.POST or None, instance=invoice)
    if not request.user.is_superuser:
        form.fields['treasury'].querset = request.user.allowed_treasuries.all()
        if not request.user.has_perm('Invoices.edit_invoice_date'):
            form.fields['date'].disabled = True
    action_url = reverse_lazy('Invoices:edit_fast_invoice', kwargs={'pk': invoice.id})
    if form.is_valid():
        obj = form.save(commit=False)
        if invoice.invoice_type == 19:
            obj.treasury_out = form.cleaned_data['treasury_in']
        obj.saved = True
        obj.save()
        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)

def income_invoice(request):
    title = 'إذن قبض نقدية'
    form = IncomeInvoiceForm(request.POST or None)
    if not request.user.is_superuser:
        form.fields['treasury'].querset = request.user.allowed_treasuries.all()
        if not request.user.has_perm('Invoices.edit_invoice_date'):
            form.fields['date'].disabled = True
    form.initial['treasury'] = request.user.default_treasury
    action_url = reverse_lazy('Invoices:income_invoice')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.invoice_type = 12
        obj.creator = request.user
        obj.saved = True
        obj.save()
        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)

def get_last_invoice(request, type):
    invoices = get_invoices(request, int(type)).order_by('id')
    last_invoice = invoices.last()
    if last_invoice:
        return redirect('Invoices:show_invoice', last_invoice.id)
    else:
        return redirect('Invoices:show_opened_invoices', int(type))

def search_invoice(request):
    if not request.user.has_perm('Invoices.search_invoice'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية للبحث عن فاتورة')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    id = request.GET.get('invoice_id')
    invoice = get_object_or_404(Invoice, id=id)
    return redirect('Invoices:show_invoice', invoice.id)

def get_invoice_setting():
    try:
        setting = InvoiceSetting.objects.get(id=1)
    except:
        setting = InvoiceSetting()
        setting.save()
    return setting

def invoice_base_setting(request):
    if not request.user.has_perm('Invoices.edit_invoice_setting'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    setting = get_invoice_base_setting()
    form = BaseSettingForm(request.POST or None, request.FILES or None, instance=setting)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect(request.POST.get('url'))
    context = {
        'title': 'إعدادات الفواتير',
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)

def invoice_setting(request):
    if not request.user.has_perm('Invoices.edit_invoice_print_setting'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    setting = get_invoice_setting()
    form = SettingForm(request.POST or None, request.FILES or None, instance=setting)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect(request.POST.get('url'))
    context = {
        'title': 'إعدادات طباعة الفواتير',
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)

def print_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    setting = get_invoice_setting()
    context = {
        'invoice': invoice,
        'setting': setting,
    }
    return render(request, 'Invoices/Print/' + str(setting.size) + '.html', context)

def customer_income(request):
    title = 'إذن قبض سداد'
    form = CustomerIncomeForm(request.POST or None)
    if request.GET.get('customer'):
        customer = get_object_or_404(Customer, id=request.GET.get('customer'))
        form.initial['customer'] = customer
    if not request.user.is_superuser:
        form.fields['treasury'].querset = request.user.allowed_treasuries.all()
    form.initial['treasury'] = request.user.default_treasury
    action_url = reverse_lazy('Invoices:income_invoice')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.invoice_type = 21
        obj.creator = request.user
        obj.saved = True
        obj.save()
        obj.calculate()
        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)

def customer_outcome(request):
    title = 'إذن صرف سداد'
    form = CustomerOutcomeForm(request.POST or None)
    if request.GET.get('customer'):
        customer = get_object_or_404(Customer, id=request.GET.get('customer'))
        form.initial['customer'] = customer
    if not request.user.is_superuser:
        form.fields['treasury'].querset = request.user.allowed_treasuries.all()
    form.initial['treasury'] = request.user.default_treasury
    action_url = reverse_lazy('Invoices:income_invoice')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.invoice_type = 22
        obj.creator = request.user
        obj.saved = True
        obj.save()
        obj.calculate()
        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)

def capital_plus(request):
    if not request.user.has_perm('Invoices.add_capital'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    title = 'إضافة لرأس المال'
    form = CapitalIncomeForm(request.POST or None)
    if not request.user.is_superuser:
        form.fields['treasury'].querset = request.user.allowed_treasuries.all()
        if not request.user.has_perm('Invoices.edit_invoice_date'):
            form.fields['date'].disabled = True
    form.initial['treasury'] = request.user.default_treasury
    action_url = reverse_lazy('Invoices:income_invoice')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.invoice_type = 13
        obj.creator = request.user
        obj.saved = True
        obj.save()
        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)

def capital_minus(request):
    if not request.user.has_perm('Invoices.minus_capital'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    title = 'سحب من رأس المال'
    form = CapitalOutcomeForm(request.POST or None)
    if not request.user.is_superuser:
        form.fields['treasury'].querset = request.user.allowed_treasuries.all()
        if not request.user.has_perm('Invoices.edit_invoice_date'):
            form.fields['date'].disabled = True
    form.initial['treasury'] = request.user.default_treasury
    action_url = reverse_lazy('Invoices:income_invoice')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.invoice_type = 14
        obj.creator = request.user
        obj.saved = True
        obj.save()
        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)

def super_delete(request, pk):
    if not request.user.has_perm('Invoices.permanent_delete_invoices'):
            messages.add_message(request, messages.ERROR , 'لا تمتلك الصلاحيات الكافية')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    invoice = get_object_or_404(Invoice, id=pk)
    invoice_type = invoice.invoice_type
    invoices = get_invoices(request, invoice.invoice_type).order_by('id')
    prev_invoice = invoices.filter(id__lt=invoice.id).last()
    next_invoice = invoices.filter(id__gt=invoice.id).first()
    invoice.delete()
    if prev_invoice:
        return redirect(reverse_lazy('Invoices:show_invoice', kwargs={'pk': prev_invoice.id}))
    elif next_invoice:
        return redirect(reverse_lazy('Invoices:show_invoice', kwargs={'pk': prev_invoice.id}))
    else:
        return redirect(reverse_lazy('Invoices:get_last_invoice', kwargs={'type': invoice_type}))

def treasury_transfer(request):
    title = 'تحويل خزينة'
    form = TreasuryTransferForm(request.POST or None)
    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.invoice_type = 19
        invoice.treasury_out = form.cleaned_data['treasury_in']
        invoice.saved = True
        invoice.creator = request.user
        invoice.save()
        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)

def daily_restrictions(request):
    title = 'قيد يومي'
    form = DailyRestrictionsForm(request.POST or None)
    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.invoice_type = 24
        invoice.treasury_out = form.cleaned_data['treasury_in']
        invoice.saved = True
        invoice.creator = request.user
        invoice.save()
        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)

class SpendCategoryList(PermissionRequiredMixin, ListView):
    model = SpendCategory
    paginate_by = 100
    permission_required = 'Invoices.access_spend_category_menu'

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات الكافية')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset

class SpendCategoryTrashList(PermissionRequiredMixin, ListView):
    model = SpendCategory
    paginate_by = 100
    permission_required = 'Invoices.access_spend_category_menu'

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات الكافية')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset

class SpendCategoryCreate(PermissionRequiredMixin, CreateView):
    model = SpendCategory
    form_class = SpendCategoryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Invoices:SpendCategoryList')
    permission_required = 'Invoices.add_spend_category'

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات الكافية')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة تصنيف مصروفات'
        context['action_url'] = reverse_lazy('Invoices:SpendCategoryCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class SpendCategoryUpdate(PermissionRequiredMixin, UpdateView):
    model = SpendCategory
    form_class = SpendCategoryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Invoices:SpendCategoryList')
    permission_required = 'Invoices.edit_spend_category'

    def handle_no_permission(self):
        messages.error(self.request, 'لا تمتلك الصلاحيات الكافية')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل تصنيف مصروفات: ' + str(self.object)
        context['action_url'] = reverse_lazy('Invoices:SpendCategoryUpdate', kwargs={'pk': self.object.id})
        return context

class SpendCategoryDelete(PermissionRequiredMixin, UpdateView):
    model = SpendCategory
    form_class = SpendCategoryDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Invoices:SpendCategoryList')
    permission_required = 'Invoices.delete_spend_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف تصنيف مصروفات: ' + str(self.object)
        context['action_url'] = reverse_lazy('Invoices:SpendCategoryDelete', kwargs={'pk': self.object.id})
        return context

def add_customer_to_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        customer = form.save(commit=False)
        customer.save()
        invoice.customer = customer
        invoice.save()
        return redirect('Invoices:show_invoice', pk)
    context = {
        'title': 'إضافة عميل / مورد',
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)

def SpendCategoriesXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Spend Categories.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Spend Categories') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows = SpendCategory.objects.filter(deleted=False).values_list('id', 'name')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response
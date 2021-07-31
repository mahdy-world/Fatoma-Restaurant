from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .mybarcode import *
from .forms import *
from Invoices.models import Invoice


# Create your views here.
def barcode_generator(request, barcode):
    d = MyBarcodeDrawing(barcode)
    binaryStuff = d.asString('png')
    return HttpResponse(binaryStuff, 'image/png')


def view_barcode(request):
    barcode = request.GET.get('barcode')
    quantity = int(request.GET.get('quantity'))
    parameter1 = request.GET.get('par1')
    parameter2 = request.GET.get('par2')
    try:
        setting = BarcodeSetting.objects.get(id=1)
    except:
        setting = BarcodeSetting()
        setting.save()
    context = {
        'barcode': barcode,
        'quantity_range': range(quantity),
        'quantity': quantity,
        'parameter1': parameter1,
        'parameter2': parameter2,
        'setting': setting,
    }
    return render(request, 'Barcode/barcode.html', context)


def print_barcode(request):
    barcode = request.GET.get('barcode')
    quantity = int(request.GET.get('quantity'))
    parameter1 = request.GET.get('par1')
    parameter2 = request.GET.get('par2')
    try:
        setting = BarcodeSetting.objects.get(id=1)
    except:
        setting = BarcodeSetting()
        setting.save()
    context = {
        'barcode': barcode,
        'quantity_range': range(quantity),
        'quantity': quantity,
        'parameter1': parameter1,
        'parameter2': parameter2,
        'setting': setting,

    }
    return render(request, 'Barcode/print_barcode.html', context)


def get_barcode_setting():
    try:
        setting = BarcodeSetting.objects.get(id=1)
    except:
        setting = BarcodeSetting()
        setting.save()
    return setting


def barcode_setting(request):
    setting = get_barcode_setting()
    form = SettingForm(request.POST or None, instance=setting)
    if form.is_valid():
        setting = form.save(commit=False)
        setting.save()
        return redirect(request.POST.get('url'))
    context = {
        'form': form,
        'title': 'إعدادات الملصقات (باركود)'
    }
    return render(request, 'Core/form_template.html', context)


def print_barcode_for_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    setting = get_barcode_setting()
    context = {
        'invoice': invoice,
        'setting': setting,
    }
    return render(request, 'Barcode/invoice_barcode.html', context)



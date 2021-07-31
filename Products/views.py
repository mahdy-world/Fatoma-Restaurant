from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import *
from django.urls import reverse_lazy
from .models import *
from .forms import *
import xlwt


# Create your views here.
class MainCategoryList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Products.access_main_category_menu'
    model = MainCategory
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class MainCategoryTrashList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Products.access_main_category_menu'
    model = MainCategory
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class MainCategoryCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'Products.add_main_category'
    model = MainCategory
    form_class = MainCategoryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:MainCategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة مجموعة أصناف رئيسية'
        context['action_url'] = reverse_lazy('Products:MainCategoryCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class MainCategoryUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Products.edit_main_category'
    model = MainCategory
    form_class = MainCategoryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:MainCategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مجموعة أصناف رئيسية: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:MainCategoryUpdate', kwargs={'pk': self.object.id})
        return context


class MainCategoryDelete(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Products.delete_main_category'
    model = MainCategory
    form_class = MainCategoryDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:MainCategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مجموعة أصناف رئيسية: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:MainCategoryDelete', kwargs={'pk': self.object.id})
        return context
    
def MainCategoryXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Product Main Category.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Main Category') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows =  MainCategory.objects.filter(deleted= False).values_list('id', 'name')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response

class SubCategoryList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Products.access_sub_category_menu'
    model = SubCategory
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('main_category'):
            queryset = queryset.filter(main_category__name__icontains=self.request.GET.get('main_category'))
        return queryset


class SubCategoryTrashList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Products.access_sub_category_menu'
    model = SubCategory
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('main_category'):
            queryset = queryset.filter(main_category__name__icontains=self.request.GET.get('main_category'))
        return queryset


class SubCategoryCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'Products.add_sub_category'
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:SubCategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة مجموعة أصناف فرعية'
        context['action_url'] = reverse_lazy('Products:SubCategoryCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class SubCategoryUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Products.edit_sub_category'
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:SubCategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مجموعة أصناف فرعية: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:SubCategoryUpdate', kwargs={'pk': self.object.id})
        return context


class SubCategoryDelete(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Products.delete_sub_category'
    model = SubCategory
    form_class = SubCategoryDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:SubCategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مجموعة أصناف فرعية: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:SubCategoryDelete', kwargs={'pk': self.object.id})
        return context

def SubCategoryXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Product Sub Category.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Sub Category') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم' , 'المجموعة الرئيسية']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows =  SubCategory.objects.filter(deleted= False).values_list('id', 'name', 'main_category__name')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response    
    
class ManufactureList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Products.access_manufacture_menu'
    model = Manufacture
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class ManufactureTrashList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Products.access_manufacture_menu'
    model = Manufacture
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class ManufactureCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/auth/login/'
    permission_required = 'Products.add_manufacture'
    model = Manufacture
    form_class = ManufactureForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:ManufactureList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة شركة مصنعة'
        context['action_url'] = reverse_lazy('Products:ManufactureCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class ManufactureUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Products.edit_manufacture'
    model = Manufacture
    form_class = ManufactureForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:ManufactureList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل شركة مصنعة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:ManufactureUpdate', kwargs={'pk': self.object.id})
        return context


class ManufactureDelete(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Products.delete_manufacture'
    model = Manufacture
    form_class = ManufactureDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:ManufactureList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل شركة مصنعة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:ManufactureDelete', kwargs={'pk': self.object.id})
        return context

def ManufactureXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Manufacture.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Manufacture') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows =  Manufacture.objects.filter(deleted= False).values_list('id', 'name')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response

class BrandList(LoginRequiredMixin, PermissionRequiredMixin ,ListView):
    login_url = '/auth/login/'
    permission_required = 'Products.access_brand_menu'
    model = Brand
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class BrandTrashList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = '/auth/login/'
    permission_required = 'Products.access_brand_menu'
    model = Brand
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class BrandCreate(LoginRequiredMixin, PermissionRequiredMixin , CreateView):
    login_url = '/auth/login/'
    permission_required = 'Products.add_brand'
    model = Brand
    form_class = BrandForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:BrandList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة براند'
        context['action_url'] = reverse_lazy('Products:BrandCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class BrandUpdate(LoginRequiredMixin, PermissionRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Products.edit_brand'
    model = Brand
    form_class = BrandForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:BrandList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل براند: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:BrandUpdate', kwargs={'pk': self.object.id})
        return context


class BrandDelete(LoginRequiredMixin, PermissionRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Products.delete_brand'
    model = Brand
    form_class = BrandDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:BrandList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل براند: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:BrandDelete', kwargs={'pk': self.object.id})
        return context

def BrandXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Brand.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Brand') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows =  Brand.objects.filter(deleted= False).values_list('id', 'name')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response

class UnitList(LoginRequiredMixin, PermissionRequiredMixin ,ListView):
    login_url = '/auth/login/'
    permission_required = 'Products.access_unit_menu'
    model = Unit
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class UnitCreate(LoginRequiredMixin, PermissionRequiredMixin ,CreateView):
    login_url = '/auth/login/'
    permission_required = 'Products.add_unit'
    model = Unit
    form_class = UnitForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:UnitList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة وحدة'
        context['action_url'] = reverse_lazy('Products:UnitCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class UnitUpdate(LoginRequiredMixin, PermissionRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Products.edit_unit'
    model = Unit
    form_class = UnitForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:UnitList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل وحدة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:UnitUpdate', kwargs={'pk': self.object.id})
        return context


class UnitDelete(LoginRequiredMixin, PermissionRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Products.delete_unit'
    model = Unit
    form_class = UnitDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:UnitList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل وحدة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:UnitDelete', kwargs={'pk': self.object.id})
        return context


class ProductList(LoginRequiredMixin, PermissionRequiredMixin ,ListView):
    login_url = '/auth/login/'
    permission_required = 'Products.access_product_menu'
    model = Product
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('description'):
            queryset = queryset.filter(description__icontains=self.request.GET.get('description'))
        if self.request.GET.get('main_category'):
            queryset = queryset.filter(sub_category__main_category__name__icontains=self.request.GET.get('main_category'))
        if self.request.GET.get('sub_category'):
            queryset = queryset.filter(sub_category__name__icontains=self.request.GET.get('sub_category'))
        if self.request.GET.get('manufacture'):
            queryset = queryset.filter(manufacture__name__icontains=self.request.GET.get('manufacture'))
        if self.request.GET.get('brand'):
            queryset = queryset.filter(brand__name__icontains=self.request.GET.get('brand'))
        if self.request.GET.get('purchase_price'):
            queryset = queryset.filter(purchase_price=self.request.GET.get('purchase_price'))
        if self.request.GET.get('cost_price'):
            queryset = queryset.filter(cost_price=self.request.GET.get('cost_price'))
        if self.request.GET.get('sell_price'):
            queryset = queryset.filter(sell_price=self.request.GET.get('sell_price'))
        if self.request.GET.get('main_unit'):
            queryset = queryset.filter(main_unit__name__icontains=self.request.GET.get('main_unit'))
        if self.request.GET.get('sub_unit'):
            queryset = queryset.filter(sub_unit__name__icontains=self.request.GET.get('sub_unit'))
        if self.request.GET.get('sub_sub_unit'):
            queryset = queryset.filter(sub_sub_unit__name__icontains=self.request.GET.get('sub_sub_unit'))
        return queryset


class ProductCreate(LoginRequiredMixin, PermissionRequiredMixin ,CreateView):
    login_url = '/auth/login/'
    permission_required = 'Products.add_product'
    model = Product
    form_class = ProductForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:ProductList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة صنف'
        context['action_url'] = reverse_lazy('Products:ProductCreate')
        return context

    def form_valid(self, form):
        product = form.save()
        for x in Category.objects.filter(deleted=False):
            product_price = ProductPrices()
            product_price.product = product
            product_price.customer_segment = x
            product_price.price = product.sell_price
            product_price.discount = 0
            product_price.new_price = product.sell_price
            product_price.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class ProductUpdate(LoginRequiredMixin, PermissionRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Products.edit_product'
    model = Product
    form_class = ProductForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:ProductList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل صنف: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:ProductUpdate', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        product_item = get_object_or_404(Product, id=self.kwargs['pk'])
        if str(form.instance.sell_price) != str(product_item.sell_price):
            for m in ProductPrices.objects.filter(product=product_item):
                m.price = form.instance.sell_price
                m.calculate_after_discount()
                m.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class ProductDelete(LoginRequiredMixin, PermissionRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Products.delete_product'
    model = Product
    form_class = ProductDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:ProductList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف صنف: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:ProductDelete', kwargs={'pk': self.object.id})
        return context
    
    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class ProductCard(LoginRequiredMixin, PermissionRequiredMixin ,DetailView):
    login_url = '/auth/login/'
    permission_required = 'Products.access_product_detail'
    model = Product

def ProductXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Product.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Product') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'النوع', 'الاسم','وصف المنتج','المجموعة الرئيسية','المجموعة الفرعية','الجهة المصنعة','البراند','سعر الشراء','سعر التكلفة','سعر البيع','الوحدة الرئيسية','حد الصرف',
    'حد الطلب','الرصيد الحرج','الضريبة المضافة','آخر تحديث للسعر','منتج قابل للإستبدال']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows =  Product.objects.filter(deleted=False).values_list('id', 'product_type', 'name', 'description','sub_category__main_category__name','sub_category__name','manufacture__name','brand__name','purchase_price','cost_price',
    'sell_price','main_unit','max_sell','full_stock','critical_stock','tax__name','sell_price_last_update','refundable')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response

class GroupedProductCreate(LoginRequiredMixin, PermissionRequiredMixin ,CreateView):
    login_url = '/auth/login/'
    permission_required = 'Products.add_group_product'
    model = GroupedProduct
    template_name = 'Core/form_template.html'
    form_class = GroupedProductForm
    success_url = reverse_lazy('Products:ProductList')

    def form_valid(self, form):
        small_product = form.instance.contain
        grouped_item = get_object_or_404(Product, id=self.kwargs['pk'])
        form.instance.grouped_item = grouped_item
        if form.instance.unit ==  small_product.main_unit :
            return super().form_valid(form)
        else:
            if form.instance.unit == 1 or form.instance.unit == 2 or form.instance.unit == 3 :
                if form.instance.unit == 1 and small_product.main_unit == 2 or form.instance.unit == 2 and small_product.main_unit == 3:
                    form.instance.quantity = ( form.instance.quantity * 1000 )
                elif form.instance.unit == 1 and small_product.main_unit == 3 :
                    form.instance.quantity = ( form.instance.quantity * 1000000 )
                elif form.instance.unit == 3 and small_product.main_unit == 1 :
                    form.instance.quantity = ( form.instance.quantity / 1000000 )
                elif form.instance.unit == 2 and small_product.main_unit == 1 or form.instance.unit == 3 and small_product.main_unit == 2:
                    form.instance.quantity = ( form.instance.quantity / 1000 )
                else:
                    form.instance.unit = 0
                    form.instance.quantity =0 
                    return super().form_valid(form)
            elif form.instance.unit == 9 or form.instance.unit == 8 :
                if form.instance.unit == 9 and small_product.main_unit == 8:
                    form.instance.quantity = ( form.instance.quantity * 12 )
                elif form.instance.unit == 8 and small_product.main_unit == 9:
                    form.instance.quantity = ( form.instance.quantity / 12 )
                else:
                    form.instance.unit = 0
                    form.instance.quantity =0 
                    return super().form_valid(form)
            else:
                if form.instance.unit == 4 and small_product.main_unit == 5:
                    form.instance.quantity = ( form.instance.quantity * 1000000 )
                elif form.instance.unit == 4 and small_product.main_unit == 6 or form.instance.unit == 6 and small_product.main_unit == 5 or form.instance.unit == 6 and small_product.main_unit == 7:
                    form.instance.quantity = ( form.instance.quantity * 1000  )
                elif form.instance.unit == 4 and small_product.main_unit == 7:
                    form.instance.quantity = ( form.instance.quantity * 1000000  )
                elif form.instance.unit == 5 and small_product.main_unit == 4 or form.instance.unit == 7 and small_product.main_unit == 4:
                    form.instance.quantity = ( form.instance.quantity / 1000000  )
                elif form.instance.unit == 5 and small_product.main_unit == 6 or form.instance.unit == 6 and small_product.main_unit == 4 or form.instance.unit == 7 and small_product.main_unit == 6:
                    form.instance.quantity = ( form.instance.quantity / 1000   )
                elif form.instance.unit == 5 and small_product.main_unit == 7 or form.instance.unit == 7 and small_product.main_unit == 5:
                    return super().form_valid(form)
                else:
                    form.instance.unit = 0
                    form.instance.quantity =0 
                    return super().form_valid(form) 
            form.instance.unit = small_product.main_unit
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة مكون: '
        context['action_url'] = reverse_lazy('Products:GroupedProductCreate', kwargs={'pk': self.kwargs['pk']})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class GroupedProductUpdate(LoginRequiredMixin, PermissionRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Products.edit_group_product'
    model = GroupedProduct
    template_name = 'Core/form_template.html'
    form_class = GroupedProductForm
    success_url = reverse_lazy('Products:ProductList')

    def form_valid(self, form):
        small_product = form.instance.contain
        grouped_item = get_object_or_404(Product, id=self.object.grouped_item.id)
        form.instance.grouped_item = grouped_item
        if form.instance.unit ==  small_product.main_unit :
            return super().form_valid(form)
        else:
            if form.instance.unit == 1 or form.instance.unit == 2 or form.instance.unit == 3 :
                if form.instance.unit == 1 and small_product.main_unit == 2 or form.instance.unit == 2 and small_product.main_unit == 3:
                    form.instance.quantity = ( form.instance.quantity * 1000 )
                elif form.instance.unit == 1 and small_product.main_unit == 3 or form.instance.unit == 3 and small_product.main_unit == 1:
                    form.instance.quantity = ( form.instance.quantity / 1000000 )
                elif form.instance.unit == 2 and small_product.main_unit == 1 or form.instance.unit == 3 and small_product.main_unit == 2:
                    form.instance.quantity = ( form.instance.quantity / 1000 )
            elif form.instance.unit == 9 or form.instance.unit == 8 :
                if form.instance.unit == 9 and small_product.main_unit == 8:
                    form.instance.quantity = ( form.instance.quantity * 12 )
                elif form.instance.unit == 8 and small_product.main_unit == 9:
                    form.instance.quantity = ( form.instance.quantity / 1000000 )
            else:
                if form.instance.unit == 4 and small_product.main_unit == 5:
                    form.instance.quantity = ( form.instance.quantity * 1000000 )
                elif form.instance.unit == 4 and small_product.main_unit == 6 or form.instance.unit == 6 and small_product.main_unit == 5 or form.instance.unit == 6 and small_product.main_unit == 7:
                    form.instance.quantity = ( form.instance.quantity * 1000  )
                elif form.instance.unit == 4 and small_product.main_unit == 7:
                    form.instance.quantity = ( form.instance.quantity * 1000000  )
                elif form.instance.unit == 5 and small_product.main_unit == 4 or form.instance.unit == 7 and small_product.main_unit == 4:
                    form.instance.quantity = ( form.instance.quantity / 1000000  )
                elif form.instance.unit == 5 and small_product.main_unit == 6 or form.instance.unit == 6 and small_product.main_unit == 4 or form.instance.unit == 7 and small_product.main_unit == 6:
                    form.instance.quantity = ( form.instance.quantity / 1000   )
                elif form.instance.unit == 5 and small_product.main_unit == 7 or form.instance.unit == 7 and small_product.main_unit == 5:
                    return super().form_valid(form) 
            form.instance.unit = small_product.main_unit
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مكونات: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:GroupedProductUpdate', kwargs={'pk': self.kwargs['pk']})
        return context
    
    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

def GroupedProductDelete(requset, pk):
    x = GroupedProduct.objects.get(id = pk)
    x.delete()
    return redirect('/products/products/')
    
class ProductTrashList(LoginRequiredMixin, PermissionRequiredMixin ,ListView):
    login_url = '/auth/login/'
    permission_required = 'Products.access_product_menu'
    model = Product
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('description'):
            queryset = queryset.filter(description__icontains=self.request.GET.get('description'))
        if self.request.GET.get('main_category'):
            queryset = queryset.filter(sub_category__main_category__name__icontains=self.request.GET.get('main_category'))
        if self.request.GET.get('sub_category'):
            queryset = queryset.filter(sub_category__name__icontains=self.request.GET.get('sub_category'))
        if self.request.GET.get('manufacture'):
            queryset = queryset.filter(manufacture__name__icontains=self.request.GET.get('manufacture'))
        if self.request.GET.get('brand'):
            queryset = queryset.filter(brand__name__icontains=self.request.GET.get('brand'))
        if self.request.GET.get('purchase_price'):
            queryset = queryset.filter(purchase_price=self.request.GET.get('purchase_price'))
        if self.request.GET.get('cost_price'):
            queryset = queryset.filter(cost_price=self.request.GET.get('cost_price'))
        if self.request.GET.get('sell_price'):
            queryset = queryset.filter(sell_price=self.request.GET.get('sell_price'))
        if self.request.GET.get('main_unit'):
            queryset = queryset.filter(main_unit__name__icontains=self.request.GET.get('main_unit'))
        if self.request.GET.get('sub_unit'):
            queryset = queryset.filter(sub_unit__name__icontains=self.request.GET.get('sub_unit'))
        if self.request.GET.get('sub_sub_unit'):
            queryset = queryset.filter(sub_sub_unit__name__icontains=self.request.GET.get('sub_sub_unit'))
        return queryset

class TaxesList(LoginRequiredMixin, PermissionRequiredMixin ,ListView):
    login_url = '/auth/login/'
    permission_required = 'Products.access_tax_menu'
    model = Tax
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(id=self.request.GET.get('name'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('type'))
        if self.request.GET.get('value'):
            queryset = queryset.filter(description__icontains=self.request.GET.get('value'))
        return queryset

class TaxCreate(LoginRequiredMixin, PermissionRequiredMixin ,CreateView):
    login_url = '/auth/login/'
    permission_required = 'Products.add_tax'
    model = Tax
    form_class = TaxForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:TaxesList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة ضريبة'
        context['action_url'] = reverse_lazy('Products:TaxesList')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class TaxUpdate(LoginRequiredMixin, PermissionRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    permission_required = 'Products.edit_tax'
    model = Tax
    form_class = TaxForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:TaxesList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل بيانات الضريبة: ' + str(self.object.id)
        context['action_url'] = reverse_lazy('Products:TaxesList')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

def TaxDelete(request, id):
    instance = Tax.objects.get(id=id)
    instance.delete()
    return redirect('/products/taxes/')

def TaxXls(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Tax.xls' 
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    work_sheet = work_book.add_sheet('Tax') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'الاسم', 'النوع','القيمة']

    for col_num in range(len(columns)):
        work_sheet.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    rows =  Tax.objects.all().values_list('id', 'name', 'type', 'value')

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            work_sheet.write(row_num,col_num,str(row[col_num]),font_style)
    work_book.save(response)
    return response

class PricesProductUpdate(UpdateView):
    model = ProductPrices
    template_name = 'Core/form_template.html'
    form_class = PricesProductFormU

    def form_valid(self, form):
        x = form.save(commit=False)
        if x.opration == 1:
            x.new_price = x.price - (x.discount * x.price / 100)
        else:
            x.new_price = x.price + (x.discount * x.price / 100)
        x.save()

        return super(PricesProductUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل الشريحة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:PricesProductUpdate', kwargs={'pk': self.kwargs['pk']})
        return context

    def get_success_url(self):
        return reverse_lazy('Products:ProductCard', kwargs={'pk': self.kwargs['ppk']})
    


class PricesProductDelete(UpdateView):
    model = ProductPrices
    template_name = 'Core/confirm_delete.html'
    form_class = PricesProductFormD

    def form_valid(self, form):
        form.instance.deleted = 1
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف سعر شريحة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:PricesProductDelete', kwargs={'pk': self.kwargs['pk']})
        return context

    def get_success_url(self):
        return reverse_lazy('Products:ProductCard', kwargs={'pk': self.kwargs['ppk']})


class PricesProductStop(UpdateView):
    model = ProductPrices
    template_name = 'Core/confirm_stop.html'
    form_class = PricesProductFormS
    success_url = reverse_lazy('Products:ProductList')

    def form_valid(self, form):
        form.instance.inactive = 1
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعطيل سعر شريحة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:PricesProductStop', kwargs={'pk': self.kwargs['pk']})
        return context

    def get_success_url(self):
        return reverse_lazy('Products:ProductCard', kwargs={'pk': self.kwargs['ppk']})

class PricesProductActive(UpdateView):
    model = ProductPrices
    template_name = 'Core/confirm_active.html'
    form_class = PricesProductFormS
    success_url = reverse_lazy('Products:ProductList')

    def form_valid(self, form):
        form.instance.inactive = 0
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تفعيل سعر شريحة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:PricesProductActive', kwargs={'pk': self.kwargs['pk']})
        return context

    def get_success_url(self):
        return reverse_lazy('Products:ProductCard', kwargs={'pk': self.kwargs['ppk']})


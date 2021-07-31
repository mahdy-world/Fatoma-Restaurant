from django.urls import reverse_lazy
from django.urls import reverse_lazy
from django.views.generic import *
from Invoices.models import *
from .forms import *
from django.db.models import Q


# Create your views here.
class HomePage(TemplateView):
    template_name = 'Website/home1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = MainPage.objects.get_or_create(id=1)
        setting = MainPage.objects.get(id=1)
        context['setting'] = setting
        context['AboutItems'] = AboutItems.objects.all()
        context['StatisticsItems']= StatisticsItems.objects.all()
        context['ServiceItems']= ServiceItems.objects.all()
        context['ProductItems']= ProductItems.objects.all()
        context['TeamItems']= TeamItems.objects.all()
        return context


class HomePageUpdate(UpdateView):
    model = MainPage
    form_class = MainPageForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Website:HomePageUpdate', kwargs={'pk': 1})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل بيانات الموقع: ' + str(self.object.index_title)
        context['action_url'] = reverse_lazy('Website:HomePageUpdate', kwargs={'pk': 1})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


# class Home(TemplateView):
#     template_name = 'Website/homepage.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         setting = WebsiteSetting.objects.get_or_create(id=1)
#         setting = WebsiteSetting.objects.get(id=1)
#         context['setting'] = setting
#         homepage_slider = HomePageSlider.objects.all()
#         context['slides'] = homepage_slider
#         context['navbar_pages'] = Page.objects.filter(add_to_menu=True)
#         context['main_categories'] = MainCategory.objects.filter(deleted=False)
#         return context


class Shop(TemplateView):
    template_name = 'Website/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = WebsiteSetting.objects.get_or_create(id=1)
        setting = WebsiteSetting.objects.get(id=1)
        context['setting'] = setting
        context['main_categories'] = MainCategory.objects.filter(deleted=False)
        return context


class ProductView(DetailView):
    model = Product
    template_name = 'Website/ProductView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = WebsiteSetting.objects.get_or_create(id=1)
        setting = WebsiteSetting.objects.get(id=1)
        context['setting'] = setting
        context['main_categories'] = MainCategory.objects.filter(deleted=False)
        return context


class ProductList(ListView):
    model = Product
    template_name = 'Website/productList.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = WebsiteSetting.objects.get_or_create(id=1)
        setting = WebsiteSetting.objects.get(id=1)
        context['setting'] = setting
        context['main_categories'] = MainCategory.objects.filter(deleted=False)
        return context

    def get_queryset(self):
        queryset = Product.objects.filter(deleted=False)
        sub_category_id = self.kwargs['pk']
        queryset = queryset.filter(sub_category__id=sub_category_id)
        return queryset


class Search(ProductList):
    def get_queryset(self):
        queryset = Product.objects.filter(deleted=False)
        if self.request.GET.get('q'):
            s = self.request.GET.get('q')
            queryset = queryset.filter(
                Q(name__icontains=s) |
                Q(description__icontains=s) |
                Q(brand__name__icontains=s) |
                Q(manufacture__name__icontains=s) |
                Q(sub_category__name__icontains=s) |
                Q(sub_category__main_category__name__icontains=s)
            )
        if self.request.GET.get('sub_category'):
            queryset = queryset.filter(sub_category__id=self.request.GET.get('sub_category'))
        if self.request.GET.get('main_category'):
            queryset = queryset.filter(sub_category__main_category__id=self.request.GET.get('main_category'))
        if self.request.GET.get('brand'):
            queryset = queryset.filter(brand__id=self.request.GET.get('brand'))
        return queryset


def get_user_invoice(request):
    if request.user.invoice_set.filter(saved=False).count > 0:
        opened_invoice = request.user.invoice_set.filter(saved=False)[0]
    else:
        opened_invoice = Invoice()
        opened_invoice.creator = request.user
        opened_invoice.invoice_type = 3
        opened_invoice.save()
    return opened_invoice


class AddToCart(CreateView):
    model = InvoiceItem
    template_name = 'Website/form.html'
    form_class = AddToCartForm
    success_url = reverse_lazy('Website:Shop')

    def form_valid(self, form):
        product = Product.objects.get(id=self.request.GET.get('product'))
        invoice = get_user_invoice(self.request)
        item = form.save(commit=False)
        item.invoice = invoice
        item.product = product
        item.unit_price = product.sell_price
        item.total_price = item.unit_price * item.quantity
        item.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=self.request.GET.get('product'))
        context['title'] = 'إضافة' + str(product.name) + 'إلي سلة الشراء'
        setting = WebsiteSetting.objects.get_or_create(id=1)
        setting = WebsiteSetting.objects.get(id=1)
        context['setting'] = setting
        context['main_categories'] = MainCategory.objects.filter(deleted=False)
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class MyOrders(ListView):
    model = Invoice
    template_name = 'Website/my_orders.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = WebsiteSetting.objects.get_or_create(id=1)
        setting = WebsiteSetting.objects.get(id=1)
        context['setting'] = setting
        context['main_categories'] = MainCategory.objects.filter(deleted=False)
        return context

    def get_queryset(self):
        queryset = Invoice.objects.filter(creator=self.request.user, invoice_type=3)
        return queryset


class MyCart(TemplateView):
    template_name = 'Website/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = WebsiteSetting.objects.get_or_create(id=1)
        setting = WebsiteSetting.objects.get(id=1)
        context['setting'] = setting
        context['main_categories'] = MainCategory.objects.filter(deleted=False)
        context['object'] = get_user_invoice(self.request)
        return context



#######################################################################################

class AboutItemsList(ListView):

    model = AboutItems
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('title'):
            queryset = queryset.filter(title__icontains=self.request.GET.get('title'))
        if self.request.GET.get('description'):
            queryset = queryset.filter(description__icontains=self.request.GET.get('description'))
        return queryset

class AboutItemsCreate(CreateView):
    model = AboutItems
    form_class = AboutItemsForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Website:AboutItemsList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة عنصر جديد'
        context['action_url'] = reverse_lazy('Website:AboutItemsCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class AboutItemsUpdate(UpdateView):
    model = AboutItems
    form_class = AboutItemsForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Website:AboutItemsList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل : ' + str(self.object)
        context['action_url'] = reverse_lazy('Website:AboutItemsUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class AboutItemsDelete(DeleteView):
    model = AboutItems
    template_name = 'Core/confirm_delete.html'
    success_url = reverse_lazy('Website:AboutItemsList')

class StatisticsItemsList(ListView):

    model = StatisticsItems
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('title'):
            queryset = queryset.filter(title__icontains=self.request.GET.get('title'))
        if self.request.GET.get('number'):
            queryset = queryset.filter(number=self.request.GET.get('number'))
        return queryset

class StatisticsItemsCreate(CreateView):
    model = StatisticsItems
    form_class = StatisticsItemsForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Website:StatisticsItemsList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة إحصائية جديدة'
        context['action_url'] = reverse_lazy('Website:StatisticsItemsCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class StatisticsItemsUpdate(UpdateView):
    model = StatisticsItems
    form_class = StatisticsItemsForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Website:StatisticsItemsList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل : ' + str(self.object)
        context['action_url'] = reverse_lazy('Website:StatisticsItemsUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class StatisticsItemsDelete(DeleteView):
    model = StatisticsItems
    template_name = 'Core/confirm_delete.html'
    success_url = reverse_lazy('Website:StatisticsItemsList')


class ServiceItemsList(ListView):

    model = ServiceItems
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('title'):
            queryset = queryset.filter(title__icontains=self.request.GET.get('title'))
        if self.request.GET.get('description'):
            queryset = queryset.filter(description__icontains=self.request.GET.get('description'))
        return queryset

class ServiceItemsCreate(CreateView):
    model = ServiceItems
    form_class = ServiceItemsForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Website:ServiceItemsList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة خدمة جديدة'
        context['action_url'] = reverse_lazy('Website:ServiceItemsCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class ServiceItemsUpdate(UpdateView):
    model = ServiceItems
    form_class = ServiceItemsForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Website:ServiceItemsList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل : ' + str(self.object)
        context['action_url'] = reverse_lazy('Website:ServiceItemsUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class ServiceItemsDelete(DeleteView):
    model = ServiceItems
    template_name = 'Core/confirm_delete.html'
    success_url = reverse_lazy('Website:ServiceItemsList')

class ProductItemsList(ListView):

    model = ProductItems
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('title'):
            queryset = queryset.filter(title__icontains=self.request.GET.get('title'))
        return queryset

class ProductItemsCreate(CreateView):
    model = ProductItems
    form_class = ProductItemsForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Website:ProductItemsList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة منتج جديد'
        context['action_url'] = reverse_lazy('Website:ProductItemsCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class ProductItemsUpdate(UpdateView):
    model = ProductItems
    form_class = ProductItemsForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Website:ProductItemsList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل : ' + str(self.object)
        context['action_url'] = reverse_lazy('Website:ProductItemsUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class ProductItemsDelete(DeleteView):
    model = ProductItems
    template_name = 'Core/confirm_delete.html'
    success_url = reverse_lazy('Website:ProductItemsList')


class TeamItemsList(ListView):

    model = TeamItems
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset

class TeamItemsCreate(CreateView):
    model = TeamItems
    form_class = TeamItemsForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Website:TeamItemsList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة عضو جديد'
        context['action_url'] = reverse_lazy('Website:TeamItemsCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class TeamItemsUpdate(UpdateView):
    model = TeamItems
    form_class = TeamItemsForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Website:TeamItemsList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل : ' + str(self.object)
        context['action_url'] = reverse_lazy('Website:TeamItemsUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class TeamItemsDelete(DeleteView):
    model = TeamItems
    template_name = 'Core/confirm_delete.html'
    success_url = reverse_lazy('Website:TeamItemsList')
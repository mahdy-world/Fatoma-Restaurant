from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.shortcuts import render
from django.views.generic import *
from datetime import datetime
from django.db.models import Q

from .forms import *


# Create your views here.
class ReportsHome(LoginRequiredMixin, TemplateView):
    login_url = '/auth/login/'
    template_name = 'Reports/reports_home.html'


class InvoiceReport(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Invoice
    template_name = 'Reports/invoice_reports/invoice_report.html'
    form = InvoiceReportForm()

    def get_queryset(self):
        if not self.request.GET.get('submit'):
            queryset = Invoice.objects.filter(id=0)
        else:
            if not self.request.user.is_superuser:
                queryset = Invoice.objects.filter(deleted=False, saved=True,
                                                  branch__in=self.request.user.allowed_branches.all(),
                                                  treasury__in=self.request.user.allowed_treasuries.all())
            else:
                queryset = Invoice.objects.filter(deleted=False, saved=True)
        if self.request.GET.get('from_date'):
            queryset = queryset.filter(date__date__gte=self.request.GET.get('from_date'))
        if self.request.GET.get('to_date'):
            queryset = queryset.filter(date__date__lte=self.request.GET.get('to_date'))
        if self.request.GET.get('creator'):
            queryset = queryset.filter(creator__id=self.request.GET.get('creator'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(invoice_type=self.request.GET.get('type'))
        if self.request.GET.get('branch'):
            queryset = queryset.filter(
                Q(from_branch__id=self.request.GET.get('branch')) | Q(to_branch__id=self.request.GET.get('branch')))
        if self.request.GET.get('treasury'):
            queryset = queryset.filter(Q(from_treasury__id=self.request.GET.get('treasury')) | Q(
                to_branch__id=self.request.GET.get('treasury')))
        if self.request.GET.get('spend_category'):
            queryset = queryset.filter(spend_category__id=self.request.GET.get('spend_category'))
        if self.request.GET.get('customer'):
            queryset = queryset.filter(customer__id=self.request.GET.get('customer'))
        return queryset

    def get_summary(self):
        queryset = self.get_queryset()
        total = queryset.aggregate(total=Sum('overall'), count=Count('id'), total_in=Sum('treasury_in'),
                                   total_out=Sum('treasury_out'), cost_profit=Sum('cost_profit'),
                                   purchase_profit=Sum('purchase_profit'))
        return total

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_superuser:
            self.form.fields['treasury'].queryset = self.request.user.allowed_treasuries.all()
            self.form.fields['branch'].queryset = self.request.user.allowed_treasuries.all()
        context['form'] = self.form
        context['summary'] = self.get_summary()
        context['default_from'] = now().date().replace(day=1).isoformat()
        context['default_to'] = now().date().isoformat()
        context['treasuries'] = Treasury.objects.all()
        context['branches'] = Branch.objects.all()
        context['users'] = User.objects.all()
        return context


class ExpenseReport(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Invoice
    template_name = 'Reports/invoice_reports/invoice_report.html'
    form = ExpenseReportForm()

    def get_queryset(self):
        if not self.request.GET.get('submit'):
            queryset = Invoice.objects.filter(id=0)
        else:
            if not self.request.user.is_superuser:
                queryset = Invoice.objects.filter(Q(Q(from_branch__in=self.request.user.allowed_branches.all() | Q(
                    to_branch__in=self.request.user.allowed_branches.all())) &
                                                    Q(Q(
                                                        from_treasury__in=self.request.user.allowed_treasuries.all()) | Q(
                                                        to_treasuries__in=self.request.user.allowed_treasuries.all()))),
                                                  deleted=False, saved=True,
                                                  branch__in=self.request.user.allowed_branches.all())
            else:
                queryset = Invoice.objects.filter(deleted=False, saved=True)
        if self.request.GET.get('from_date'):
            queryset = queryset.filter(date__date__gte=self.request.GET.get('from_date'))
        if self.request.GET.get('to_date'):
            queryset = queryset.filter(date__date__lte=self.request.GET.get('to_date'))
        if self.request.GET.get('creator'):
            queryset = queryset.filter(creator__id=self.request.GET.get('creator'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(invoice_type=self.request.GET.get('type'))
        if self.request.GET.get('branch'):
            queryset = queryset.filter(branch__id=self.request.GET.get('branch'))
        if self.request.GET.get('treasury'):
            queryset = queryset.filter(Q(from_treasury__id=self.request.GET.get('treasury')) | Q(
                to_treasury__id=self.request.GET.get('treasury')))
        if self.request.GET.get('spend_category'):
            queryset = queryset.filter(spend_category__id=self.request.GET.get('spend_category'))
        if self.request.GET.get('customer'):
            queryset = queryset.filter(customer__id=self.request.GET.get('customer'))
        return queryset

    def get_summary(self):
        queryset = self.get_queryset()
        total = queryset.aggregate(total=Sum('overall'), count=Count('id'), total_in=Sum('treasury_in'),
                                   total_out=Sum('treasury_out'), cost_profit=Sum('cost_profit'),
                                   purchase_profit=Sum('purchase_profit'))
        return total

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_superuser:
            self.form.fields['treasury'].queryset = self.request.user.allowed_treasuries.all()
            self.form.fields['branch'].queryset = self.request.user.allowed_treasuries.all()
        context['form'] = self.form
        context['summary'] = self.get_summary()
        context['default_from'] = now().date().replace(day=1).isoformat()
        context['default_to'] = now().date().isoformat()
        context['treasuries'] = Treasury.objects.all()
        context['branches'] = Branch.objects.all()
        context['users'] = User.objects.all()
        return context


class TreasuryBalanceReport(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Treasury
    form = TreasuryBalanceReportForm()
    template_name = 'Reports/treasury_reports/treasury_balance_report.html'

    def get_queryset(self):
        if not self.request.GET.get('submit'):
            queryset = Treasury.objects.filter(id=0)
        else:
            if not self.request.user.is_superuser:
                queryset = self.request.user.allowed_treasuries.filter(deleted=False)
            else:
                queryset = Treasury.objects.filter(deleted=False)

            if self.request.GET.getlist('treasury'):
                queryset = queryset.filter(id__in=self.request.GET.getlist('treasury'))
        return queryset

    def get_summary(self):
        queryset = self.get_queryset()
        summary = 0
        for x in queryset:
            summary += x.balance()
        return summary

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_superuser:
            self.form.fields['treasury'].queryset = self.request.user.allowed_treasuries.all()
        context['form'] = self.form
        context['summary'] = self.get_summary()
        return context


class TreasuryTransactionReport(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Invoice
    form = TreasuryReportForm
    template_name = 'Reports/treasury_reports/treasury_transaction_report.html'

    def get_queryset(self):
        if not self.request.GET.get('submit'):
            queryset = Invoice.objects.filter(id=0)
        else:
            if self.request.user.is_superuser:
                queryset = Invoice.objects.filter(deleted=False, saved=True).exclude(invoice_type=7)
            else:
                queryset = Invoice.objects.filter(deleted=False, saved=True,
                                                  treasury__in=self.request.user.allowed_treasuries.all()).exclude(
                    invoice_type=7)
            if self.request.GET.get('from_date'):
                queryset = queryset.filter(date__date__gte=self.request.GET.get('from_date'))
            if self.request.GET.get('to_date'):
                queryset = queryset.filter(date__date__lte=self.request.GET.get('to_date'))
            if self.request.GET.get('treasury'):
                queryset = queryset.filter(
                    Q(from_treasury=self.request.GET.get('treasury')) | Q(to_treasury=self.request.GET.get('treasury')))
        return queryset

    def get_summary(self):
        queryset = self.get_queryset()
        if self.request.GET.get('treasury'):
            total = queryset.aggregate(total=(Sum('treasury_in') - Sum('treasury_out')), count=Count('id'),
                                       total_in=Sum('treasury_in'),
                                       total_out=Sum('treasury_out'))
            total_in = queryset.filter(to_treasury=self.request.GET.get('treasury')).aggregate(
                total_in=Sum('treasury_in'))
            total_out = queryset.filter(from_treasury=self.request.GET.get('treasury')).aggregate(
                total_out=Sum('treasury_out'))
            if total_in['total_in'] and total_out['total_out']:
                t = total_in['total_in'] - total_out['total_out']
                total = [total_in, total_out, t]
                return total
            elif total_in['total_in'] and not total_out['total_out']:
                t = total_in['total_in']
                total = [total_in, 0, t]
                return total
            elif not total_in['total_in'] and total_out['total_out']:
                t = 0 - total_out['total_out']
                total = [0, total_out, t]
                return total

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_superuser:
            self.form.fields['treasury'].queryset = self.request.user.allowed_treasuries.all()
        context['form'] = self.form
        context['summary'] = self.get_summary()
        if self.request.GET.get('treasury'):
            context['treasury_id'] = int(self.request.GET.get('treasury'))
        return context


def item_stock_report(request):
    form = ItemStockReportForm(request.GET or None)
    context = {'form': form}
    if form.is_valid():
        stock = {}
        if request.GET.get('item'):
            item = Product.objects.get(id=request.GET.get('item'))
        if request.GET.getlist('branch'):
            branches = request.GET.getlist('branch')
            for x in branches:
                branch = Branch.objects.get(id=x)
                stock.update({branch: item.branch_stock(x)})
        else:
            branches = Branch.objects.filter(deleted=False)
            for x in branches:
                stock.update({x: item.branch_stock(x.id)})
        total = item.current_stock()
        context.update({
            'stock': stock,
            'total': total,
            'item': item,
        })
    return render(request, 'Reports/stock_reports/item_stock_report.html', context)


def items_below_critical_stock(request):
    object_list = Product.objects.filter(deleted=False)
    context = {
        'object_list': object_list,
    }
    return render(request, 'Reports/stock_reports/items_below_critical_stock.html', context)


def items_below_order_stock(request):
    object_list = Product.objects.filter(deleted=False)
    context = {
        'object_list': object_list,
    }
    return render(request, 'Reports/stock_reports/items_below_order_stock.html', context)


def item_transactions_report(request):
    form = ItemTransactionReportForm(request.GET or None)
    context = {'form': form}
    if form.is_valid():
        if not request.GET.get('submit'):
            queryset = InvoiceItem.objects.filter(id=0)
        else:
            queryset = InvoiceItem.objects.filter(invoice__deleted=False, invoice__saved=True,
                                                  item__product_type__in=[1, 2])
            if request.GET.get('from_date'):
                queryset = queryset.filter(invoice__date__date__gte=request.GET.get('from_date'))
            if request.GET.get('to_date'):
                queryset = queryset.filter(invoice__date__date__lte=request.GET.get('to_date'))
            if request.GET.get('item'):
                queryset = queryset.filter(item__id=request.GET.get('item'))
            if request.GET.getlist('branch'):
                queryset = queryset.filter(Q(invoice__from_branch__id__in=request.GET.getlist('branch')) | Q(
                    invoice__to_branch__id__in=request.GET.getlist('branch')))
        sales = queryset.filter(invoice__invoice_type__in=[1, 2, 3,23]).aggregate(total=Sum('quantity'),
                                                                               value=Sum('after_discount'),
                                                                               purchase_profit=Sum('purchase_profit'),
                                                                               cost_profit=Sum('cost_profit'))
        purchases = queryset.filter(invoice__invoice_type=5).aggregate(total=Sum('quantity'),
                                                                       value=Sum('after_discount'),
                                                                       purchase_profit=Sum('purchase_profit'),
                                                                       cost_profit=Sum('cost_profit'))
        r_sales = queryset.filter(invoice__invoice_type=4).aggregate(total=Sum('quantity'), value=Sum('after_discount'),
                                                                     purchase_profit=Sum('purchase_profit'),
                                                                     cost_profit=Sum('cost_profit'))
        r_purchases = queryset.filter(invoice__invoice_type=6).aggregate(total=Sum('quantity'),
                                                                         value=Sum('after_discount'),
                                                                         purchase_profit=Sum('purchase_profit'),
                                                                         cost_profit=Sum('cost_profit'))
        minus = queryset.filter(invoice__invoice_type=15).aggregate(total=Sum('quantity'), value=Sum('after_discount'),
                                                                    purchase_profit=Sum('purchase_profit'),
                                                                    cost_profit=Sum('cost_profit'))
        plus = queryset.filter(invoice__invoice_type=16).aggregate(total=Sum('quantity'), value=Sum('after_discount'),
                                                                   purchase_profit=Sum('purchase_profit'),
                                                                   cost_profit=Sum('cost_profit'))
        context.update({
            'object_list': queryset,
            'sales': sales,
            'purchases': purchases,
            'r_sales': r_sales,
            'r_purchases': r_purchases,
            'minus': minus,
            'plus': plus,
        })
    return render(request, 'Reports/stock_reports/item_transactions_report.html', context)


def branch_stock_report(request):
    form = BranchStockReportForm(request.GET or None)
    context = {'form': form}
    if form.is_valid():
        stock = {}
        total = 0
        if request.GET.get('branch'):
            branch_id = request.GET.get('branch')
        else:
            branch_id = 0
        for product in Product.objects.filter(product_type__in=[1, 2]):
            if not product.branch_stock(branch_id) == 0:
                stock.update(
                    {product: [product.branch_stock(branch_id), product.cost_price * product.branch_stock(branch_id)]})
                total += product.cost_price * product.branch_stock(branch_id)
        context.update({'form': form, 'stock': stock, 'total': total})
    return render(request, 'Reports/stock_reports/branch_stock_report.html', context)


def not_sold_items_report(request):
    form = NotSoldItemsForm(request.GET or None)
    context = {'form': form}
    if form.is_valid():
        stock = {}
        total = 0
        if request.GET.get('branch'):
            branch_id = request.GET.get('branch')
        else:
            branch_id = 0
        for product in Product.objects.filter(product_type__in=[1, 2]):
            since_date = datetime.strptime(request.GET.get('date'), '%Y-%m-%d').date()
            if product.last_sell_date() < since_date and not product.branch_stock(branch_id) == 0:
                stock.update(
                    {product: [product.branch_stock(branch_id), product.cost_price * product.branch_stock(branch_id)]})
                total += product.cost_price * product.branch_stock(branch_id)
        context.update({'form': form, 'stock': stock, 'total': total})
    return render(request, 'Reports/stock_reports/not_sold_items.html', context)


class CustomerStatementReport(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Invoice
    form = CustomerStatementReportFrom()
    template_name = 'Reports/customer_reports/customer_statement.html'

    def get_queryset(self):
        if not self.request.GET.get('submit'):
            queryset = Invoice.objects.filter(id=0)
        else:
            queryset = Invoice.objects.filter(deleted=False, saved=True)
            if self.request.GET.get('from_date'):
                queryset = queryset.filter(date__date__gte=self.request.GET.get('from_date'))
            if self.request.GET.get('to_date'):
                queryset = queryset.filter(date__date__lte=self.request.GET.get('to_date'))
            if self.request.GET.get('customer'):
                queryset = queryset.filter(customer__id=self.request.GET.get('customer'))
        return queryset

    def get_summary(self):
        if self.request.GET.get('customer'):
            customer = Customer.objects.get(id=self.request.GET.get('customer'))

            queryset = self.get_queryset()
            total = queryset.aggregate(total=(Sum('customer_debit') - Sum('customer_credit')),
                                       total_debit=Sum('customer_debit'),
                                       total_credit=Sum('customer_credit'))
            total = {
                'total': customer.balance(),
                'total_debit': customer.total_debit(),
                'total_credit': customer.total_credit(),
            }

            return total

    def initial_balance(self):
        before_total = {'total_debit': 0, 'total_credit': 0}
        if self.request.GET.get('submit'):
            before_queryset = Invoice.objects.filter(deleted=False, saved=True,
                                                     date__date__lt=self.request.GET.get('from_date'))
            if self.request.GET.get('customer'):
                before_queryset = before_queryset.filter(customer__id=self.request.GET.get('customer'))
            before_total = before_queryset.aggregate(total=(Sum('customer_debit') - Sum('customer_credit')),
                                                     total_debit=Sum('customer_debit'),
                                                     total_credit=Sum('customer_credit'))
            before_total_debit = before_total['total_debit']
            before_total_credit = before_total['total_credit']
            customer = Customer.objects.get(id=self.request.GET.get('customer'))
            if customer.initial_balance > 0:
                if before_total_debit:
                    before_total['total_debit'] = before_total_debit + customer.initial_balance
                else:
                    before_total['total_debit'] = customer.initial_balance
            elif customer.initial_balance < 0:
                if before_total_debit:
                    before_total['total_credit'] = before_total_credit - customer.initial_balance
                else:
                    before_total['total_credit'] = 0 - customer.initial_balance
        return before_total

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['summary'] = self.get_summary()
        context['initial_balance'] = self.initial_balance()
        return context


class DebitorsReport(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Customer
    template_name = 'Reports/customer_reports/debitors_creditors_report.html'

    def get_queryset(self):
        queryset = Customer.objects.filter(deleted=False)
        debitors_id = [x.id for x in queryset if x.is_debitor()]
        queryset = queryset.filter(id__in=debitors_id)
        return queryset

    def get_summary(self):
        queryset = self.get_queryset()
        total = 0
        for x in queryset:
            total += x.balance()
        return total

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['summary'] = self.get_summary()
        context['title'] = 'الدائنون'
        return context


class CreditorsReport(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Customer
    template_name = 'Reports/customer_reports/debitors_creditors_report.html'

    def get_queryset(self):
        queryset = Customer.objects.filter(deleted=False)
        creditors_id = [x.id for x in queryset if x.is_creditor()]
        queryset = queryset.filter(id__in=creditors_id)
        return queryset

    def get_summary(self):
        queryset = self.get_queryset()
        total = 0
        for x in queryset:
            total += x.balance()
        return total

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['summary'] = self.get_summary()
        context['title'] = 'المدينون'
        return context


class ProfitReport(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Invoice
    form = ProfitReportForm()
    template_name = 'Reports/invoice_reports/invoice_report.html'

    def get_queryset(self):
        if not self.request.GET.get('submit'):
            queryset = Invoice.objects.filter(id=0)
        else:
            if not self.request.user.is_superuser:
                queryset = Invoice.objects.filter(deleted=False, saved=True,
                                                  branch__in=self.request.user.allowed_branches.all(),
                                                  treasury__in=self.request.user.allowed_treasuries.all())
            else:
                queryset = Invoice.objects.filter(deleted=False, saved=True)
        if self.request.GET.get('from_date'):
            queryset = queryset.filter(date__date__gte=self.request.GET.get('from_date'))
        if self.request.GET.get('to_date'):
            queryset = queryset.filter(date__date__lte=self.request.GET.get('to_date'))
        if self.request.GET.get('creator'):
            queryset = queryset.filter(creator__id=self.request.GET.get('creator'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(invoice_type=self.request.GET.get('type'))
        if self.request.GET.get('branch'):
            queryset = queryset.filter(
                Q(from_branch__id=self.request.GET.get('branch')) | Q(to_branch__id=self.request.GET.get('branch')))
        if self.request.GET.get('treasury'):
            queryset = queryset.filter(Q(from_treasury__id=self.request.GET.get('treasury')) | Q(
                to_treasury__id=self.request.GET.get('treasury')))
        if self.request.GET.get('spend_category'):
            queryset = queryset.filter(spend_category__id=self.request.GET.get('spend_category'))
        if self.request.GET.get('customer'):
            queryset = queryset.filter(customer__id=self.request.GET.get('customer'))
        return queryset

    def get_summary(self):
        queryset = self.get_queryset()
        total = queryset.aggregate(total=Sum('total'), count=Count('id'), total_in=Sum('treasury_in'),
                                   total_out=Sum('treasury_out'), cost_profit=Sum('cost_profit'),
                                   purchase_profit=Sum('purchase_profit'))
        return total

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_superuser:
            self.form.fields['treasury'].queryset = self.request.user.allowed_treasuries.all()
            self.form.fields['branch'].queryset = self.request.user.allowed_treasuries.all()
        context['form'] = self.form
        context['summary'] = self.get_summary()
        context['default_from'] = now().date().replace(day=1).isoformat()
        context['default_to'] = now().date().isoformat()
        context['treasuries'] = Treasury.objects.all()
        context['branches'] = Branch.objects.all()
        context['users'] = User.objects.all()
        return context


def financial_list(request):
    stock_value = 0
    debitors = 0
    creditors = 0
    treasuries_money = 0
    capital = 0
    items_queryset = Product.objects.filter(product_type__in=[1, 2])
    for item in items_queryset:
        stock_value += item.current_stock_value()
    customers_queryset = Customer.objects.all()
    for customer in customers_queryset:
        if customer.is_debitor():
            debitors += customer.balance()
        if customer.is_creditor():
            creditors += customer.balance()
    treasuries_queryset = Treasury.objects.all()
    for treasury in treasuries_queryset:
        treasuries_money += treasury.balance()
    capital = stock_value + treasuries_money + (creditors * -1) - debitors
    context = {
        'stock_value': stock_value,
        'debitors': debitors,
        'creditors': creditors * -1,
        'treasuries_money': treasuries_money,
        'capital': capital,
    }
    return render(request, 'Reports/accounts_reports/finanical_list.html', context)


def profit_loss(request):
    form = ProfitLossReportForm(request.POST or None)
    context = {
        'form': form,
    }
    if request.GET.get('submit'):
        invoices = Invoice.objects.filter(deleted=False, date__date__gte=request.GET.get('from_date'),
                                          date__date__lte=request.GET.get('to_date'), saved=True)
        income_invoices = invoices.filter(invoice_type__in=[1, 2, 3, 9, 12, 16, 23])
        outcome_invoices = invoices.filter(invoice_type__in=[4, 8, 11, 15])
        sales_profit = income_invoices.filter(invoice_type=1).aggregate(cost_profit=Sum('cost_profit'),
                                                                        purchase_profit=Sum('purchase_profit'))
        delivery_profit = income_invoices.filter(invoice_type=2).aggregate(cost_profit=Sum('cost_profit'),
                                                                           purchase_profit=Sum('purchase_profit'))
        website_profit = income_invoices.filter(invoice_type=3).aggregate(cost_profit=Sum('cost_profit'),
                                                                          purchase_profit=Sum('purchase_profit'))
        income_profit = income_invoices.filter(invoice_type__in=[9, 12]).aggregate(cost_profit=Sum('treasury_in'))
        plus_profit = income_invoices.filter(invoice_type=16).aggregate(cost_profit=Sum('cost_profit'),
                                                                        purchase_profit=Sum('purchase_profit'))
        reverse_sales_loss = outcome_invoices.filter(invoice_type=4).aggregate(cost_profit=Sum('cost_profit'),
                                                                               purchase_profit=Sum('purchase_profit'))
        outcome_loss = outcome_invoices.filter(invoice_type__in=[8, 11]).aggregate(cost_profit=Sum('treasury_out'))
        minus_loss = outcome_invoices.filter(invoice_type=15).aggregate(cost_profit=Sum('cost_profit'),
                                                                        purchase_profit=Sum('purchase_profit'))

        pos_profit = income_invoices.filter(invoice_type = 23).aggregate(cost_profit=Sum('cost_profit'),
                                                                        purchase_profit=Sum('purchase_profit'))
        total_cost_profit = 0
        total_purchase_profit = 0
        for x in income_invoices:
            if x.invoice_type in [1, 2, 3, 23]:
                total_cost_profit += x.cost_profit
                total_purchase_profit += x.purchase_profit
            elif x.invoice_type in [9, 12]:
                total_cost_profit += x.treasury_in
                total_purchase_profit += x.treasury_in
            elif x.invoice_type == 16:
                total_cost_profit -= x.cost_profit
                total_purchase_profit -= x.purchase_profit

        for x in outcome_invoices:
            if x.invoice_type == 4:
                total_cost_profit -= x.cost_profit
                total_purchase_profit -= x.purchase_profit
            elif x.invoice_type in [8, 11]:
                total_cost_profit -= x.treasury_out
                total_purchase_profit -= x.treasury_out
            elif x.invoice_type == 15:
                total_cost_profit += x.cost_profit
                total_purchase_profit += x.purchase_profit
        
        context = {
            'form': form,
            'sales_profit': sales_profit,
            'delivery_profit': delivery_profit,
            'website_profit': website_profit,
            'plus_profit': plus_profit,
            'income_profit': income_profit,
            'reverse_sales_loss': reverse_sales_loss,
            'outcome_loss': outcome_loss,
            'minus_loss': minus_loss,
            'total_cost_profit': total_cost_profit,
            'total_purchase_profit': total_purchase_profit,
            'pos_profit': pos_profit,
        }
    return render(request, 'Reports/accounts_reports/profit_loss.html', context)


def maintenance_report(request):
    form = MaintenanceReportForm(request.GET or None)
    context = {
        'form': form,
    }
    if request.GET.get('submit'):
        object_list = Ticket.objects.filter(deleted=False)
        if request.GET.get('from_date'):
            object_list = object_list.filter(date__date__gte=request.GET.get('from_date'))
        if request.GET.get('to_date'):
            object_list = object_list.filter(date__date__lte=request.GET.get('to_date'))
        if request.GET.get('product'):
            object_list = object_list.filter(product__id=request.GET.get('product'))
        if request.GET.get('customer'):
            object_list = object_list.filter(customer__id=request.GET.get('customer'))
        if request.GET.get('ticket_type') != '0':
            object_list = object_list.filter(maintenance_type=request.GET.get('ticket_type'))
        if request.GET.get('ticket_status') != '0':
            object_list = object_list.filter(status=request.GET.get('ticket_status'))
        if request.GET.get('outsource_status') != '0':
            object_list = object_list.filter(outsource_status=request.GET.get('outsource_status'))
        if request.GET.get('customer_receive_status') != '0':
            if request.GET.get('customer_receive_status') == 1:
                object_list = object_list.filter(customer_received=True)
            if request.GET.get('customer_receive_status') == 2:
                object_list = object_list.filter(customer_received=False)
        summary = object_list.aggregate(total=Sum('cost'), count=Count('id'))
        context.update({
            'object_list': object_list,
            'summary': summary,
        })
    return render(request, 'Reports/maintenance_reports/maintenance_report.html', context)


def partner_report_at(request):
    object_list = {}
    form = PartnersPercentForm(request.GET or None)
    if request.GET.get('to_date'):
        for x in Partner.objects.all():
            object_list.update(
                {x: [x.balance(to_date=request.GET.get('to_date')), x.percent(to_date=request.GET.get('to_date'))]})
    context = {
        'form': form,
        'object_list': object_list.items(),
        'to_date': request.GET.get('to_date'),
    }
    return render(request, 'Reports/partners_reports/partner_report_at.html', context)


def partner_transactions(request):
    form = PartnerTransactionForm(request.GET or None)
    context = {
        'form': form,
    }
    if request.GET.get('submit'):
        object_list = Invoice.objects.filter(deleted=False, invoice_type__in=[13, 14])
        if request.GET.get('from_date'):
            object_list = object_list.filter(date__date__gte=request.GET.get('from_date'))
        if request.GET.get('to_date'):
            object_list = object_list.filter(date__date__lte=request.GET.get('to_date'))
        if request.GET.get('partner'):
            object_list = object_list.filter(partner__id=request.GET.get('partner'))
        summary = object_list.aggregate(total=(Sum('treasury_in') - Sum('treasury_out')), total_in=Sum('treasury_in'),
                                        total_out=Sum('treasury_out'))
        context.update({
            'object_list': object_list,
            'summary': summary,
        })
    return render(request, 'Reports/partners_reports/partner_transactions.html', context)


class ExpenseGraphReport(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Invoice
    template_name = 'Reports/graph_reports/expense_graphs.html'
    form = ExpenseReportForm()

    def get_queryset(self):
        if not self.request.GET.get('submit'):
            queryset = Invoice.objects.filter(id=0)
        else:
            if not self.request.user.is_superuser:
                queryset = Invoice.objects.filter(Q(Q(from_branch__in=self.request.user.allowed_branches.all() | Q(
                    to_branch__in=self.request.user.allowed_branches.all())) &
                                                    Q(Q(
                                                        from_treasury__in=self.request.user.allowed_treasuries.all()) | Q(
                                                        to_treasuries__in=self.request.user.allowed_treasuries.all()))),
                                                  deleted=False, saved=True,
                                                  branch__in=self.request.user.allowed_branches.all())
            else:
                queryset = Invoice.objects.filter(deleted=False, saved=True)
        if self.request.GET.get('from_date'):
            queryset = queryset.filter(date__date__gte=self.request.GET.get('from_date'))
        if self.request.GET.get('to_date'):
            queryset = queryset.filter(date__date__lte=self.request.GET.get('to_date'))
        if self.request.GET.get('creator'):
            queryset = queryset.filter(creator__id=self.request.GET.get('creator'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(invoice_type=self.request.GET.get('type'))
        if self.request.GET.get('branch'):
            queryset = queryset.filter(branch__id=self.request.GET.get('branch'))
        if self.request.GET.get('treasury'):
            queryset = queryset.filter(Q(from_treasury__id=self.request.GET.get('treasury')) | Q(
                to_treasury__id=self.request.GET.get('treasury')))
        if self.request.GET.get('spend_category'):
            queryset = queryset.filter(spend_category__id=self.request.GET.get('spend_category'))
        if self.request.GET.get('customer'):
            queryset = queryset.filter(customer__id=self.request.GET.get('customer'))
        return queryset

    def get_summary(self):
        queryset = self.get_queryset()
        total = queryset.aggregate(total=Sum('overall'), count=Count('id'), total_in=Sum('treasury_in'),
                                   total_out=Sum('treasury_out'), cost_profit=Sum('cost_profit'),
                                   purchase_profit=Sum('purchase_profit'))
        return total

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_superuser:
            self.form.fields['treasury'].queryset = self.request.user.allowed_treasuries.all()
            self.form.fields['branch'].queryset = self.request.user.allowed_treasuries.all()
        context['form'] = self.form
        context['summary'] = self.get_summary()
        context['default_from'] = now().date().replace(day=1).isoformat()
        context['default_to'] = now().date().isoformat()
        context['treasuries'] = Treasury.objects.all()
        context['branches'] = Branch.objects.all()
        context['users'] = User.objects.all()
        context['object_list_ordered_by_type'] = self.get_queryset().order_by('spend_category').values(
            'spend_category__name').annotate(total=Sum('treasury_out'))
        context['object_list_ordered_by_date'] = self.get_queryset().order_by('date').values('date').annotate(
            total=Sum('treasury_out'))
        context['object_list_ordered_by_treasury'] = self.get_queryset().order_by('from_treasury').values(
            'from_treasury__name').annotate(total=Sum('treasury_out'))
        return context


class IncomeGraphReport(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Invoice
    template_name = 'Reports/graph_reports/expense_graphs.html'
    form = ExpenseReportForm()

    def get_queryset(self):
        if not self.request.GET.get('submit'):
            queryset = Invoice.objects.filter(id=0)
        else:
            if not self.request.user.is_superuser:
                queryset = Invoice.objects.filter(Q(Q(from_branch__in=self.request.user.allowed_branches.all() | Q(
                    to_branch__in=self.request.user.allowed_branches.all())) &
                                                    Q(Q(
                                                        from_treasury__in=self.request.user.allowed_treasuries.all()) | Q(
                                                        to_treasuries__in=self.request.user.allowed_treasuries.all()))),
                                                  deleted=False, saved=True,
                                                  branch__in=self.request.user.allowed_branches.all())
            else:
                queryset = Invoice.objects.filter(deleted=False, saved=True)
        if self.request.GET.get('from_date'):
            queryset = queryset.filter(date__date__gte=self.request.GET.get('from_date'))
        if self.request.GET.get('to_date'):
            queryset = queryset.filter(date__date__lte=self.request.GET.get('to_date'))
        if self.request.GET.get('creator'):
            queryset = queryset.filter(creator__id=self.request.GET.get('creator'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(invoice_type=self.request.GET.get('type'))
        if self.request.GET.get('branch'):
            queryset = queryset.filter(branch__id=self.request.GET.get('branch'))
        if self.request.GET.get('treasury'):
            queryset = queryset.filter(Q(to_treasury__id=self.request.GET.get('treasury')) | Q(
                to_treasury__id=self.request.GET.get('treasury')))
        if self.request.GET.get('spend_category'):
            queryset = queryset.filter(spend_category__id=self.request.GET.get('spend_category'))
        if self.request.GET.get('customer'):
            queryset = queryset.filter(customer__id=self.request.GET.get('customer'))
        return queryset

    def get_summary(self):
        queryset = self.get_queryset()
        total = queryset.aggregate(total=Sum('overall'), count=Count('id'), total_in=Sum('treasury_in'),
                                   total_out=Sum('treasury_out'), cost_profit=Sum('cost_profit'),
                                   purchase_profit=Sum('purchase_profit'))
        return total

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_superuser:
            self.form.fields['treasury'].queryset = self.request.user.allowed_treasuries.all()
            self.form.fields['branch'].queryset = self.request.user.allowed_treasuries.all()
        context['form'] = self.form
        context['treasuries'] = Treasury.objects.all()
        context['object_list_ordered_by_type'] = self.get_queryset().order_by('spend_category').values(
            'spend_category__name').annotate(total=Sum('treasury_in'))
        context['object_list_ordered_by_date'] = self.get_queryset().order_by('date').values('date').annotate(
            total=Sum('treasury_in'))
        context['object_list_ordered_by_treasury'] = self.get_queryset().order_by('to_treasury').values(
            'to_treasury__name').annotate(total=Sum('treasury_in'))
        return context


def new_customers_report(request):
    form = NewCustomersForm(request.POST or None)
    context = {
        'title': 'تقارير العملاء الجدد',
        'form': form,
    }
    if request.GET.get('submit'):
        customers = Customer.objects.filter(deleted=False)
        invoices = Invoice.objects.filter(deleted=False)
        if request.GET.get('from_date'):
            customers = customers.filter(added_at__gte=request.GET.get('from_date'))
        if request.GET.get('to_date'):
            customers = customers.filter(added_at__date__lte=request.GET.get('to_date'))
        if request.GET.get('employee'):
            customers = customers.filter(added_by__id=request.GET.get('employee'))
        context.update({
            'title': 'تقارير العملاء الجدد',
            'form': form,
            'customers_by_employee': customers.order_by('added_by'),
            'customers_by_date': customers.order_by('added_at'),

        })
    return render(request, 'Reports/graph_reports/customers_report.html', context)


def calls_report(request):
    form = EmployeeReportForm(request.POST or None)
    context = {
        'title': 'تقارير المكالمات',
        'form': form,
    }
    if request.GET.get('submit'):
        customers = CustomerCall.objects.all()
        if request.GET.get('from_date'):
            customers = customers.filter(added_at__gte=request.GET.get('from_date'))
        if request.GET.get('to_date'):
            customers = customers.filter(added_at__date__lte=request.GET.get('to_date'))
        if request.GET.get('employee'):
            customers = customers.filter(added_by__id=request.GET.get('employee'))

        context.update({
            'title': 'تقارير المكالمات',
            'form': form,
            'customers_by_employee': customers.order_by('added_by'),
            'customers_by_date': customers.order_by('added_at'),
            'customers_by_type': customers.order_by('call_type'),
            'customers_by_reason': customers.order_by('call_reason'),
        })
    return render(request, 'Reports/graph_reports/calls_report.html', context)

def inactive_customers(request):
    if request.GET.get('submit'):
        invoice = Invoice.objects.filter(invoice_type =1 , saved =True , deleted = False , date__gte = request.GET['from_date'])
        customers = Customer.objects.filter(deleted=False).exclude(id__in=[o.customer.id for o in invoice ])
        context= {
            'customers' : customers,
        }
        return render(request, 'Reports/customer_reports/inactive_customers.html', context)
    return render(request, 'Reports/customer_reports/inactive_customers.html', {})

def income_customers_report(request):
    if request.GET.get('submit'):
        invoice = Invoice.objects.filter(invoice_type =1 , saved =True , deleted = False , date__gte = request.GET['from_date'] ,
        date__lte = request.GET['to_date']).values_list('customer_id' , 'customer__name' ,  'customer__category__name').annotate(total=Count('overall'),value=Sum('overall')).order_by()
        return render(request, 'Reports/customer_reports/income_customers_report.html', {'invoice': invoice})
    return render(request, 'Reports/customer_reports/income_customers_report.html', {})

def max_income_customers_report(request):
    if request.GET.get('submit'):
        invoice = Invoice.objects.filter(invoice_type =1 , saved =True , deleted = False , date__gte = request.GET['from_date'] ,
        date__lte = request.GET['to_date']).values_list('customer_id' , 'customer__name' ,  'customer__category__name').annotate(total=Count('overall'),value=Sum('overall')).order_by()

        if str(request.GET['option']) == '1' :
            x = invoice.order_by('-total') 
            return render(request, 'Reports/customer_reports/max_income_customers_report.html', {'invoice':x})
        else:
            y = invoice.order_by('-value')
            return render(request, 'Reports/customer_reports/max_income_customers_report.html', {'invoice':y})
    return render(request, 'Reports/customer_reports/max_income_customers_report.html', {})


class DailyRestrictionsReport(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Invoice
    form = DailyRestrictionsForm
    template_name = 'Reports/daily_restrictions/daily_restrictions_report.html'

    def get_queryset(self):
        if not self.request.GET.get('submit'):
            queryset = Invoice.objects.filter(id=0)
        else:
            queryset = Invoice.objects.filter(deleted=False, saved=True, invoice_type = 24)
            if self.request.GET.get('from_date'):
                queryset = queryset.filter(date__date__gte=self.request.GET.get('from_date'))
            if self.request.GET.get('to_date'):
                queryset = queryset.filter(date__date__lte=self.request.GET.get('to_date'))
        return queryset
            
    def get_summary(self):
        queryset = self.get_queryset()
        total = queryset.aggregate(total=Sum('treasury_in'))
        return total

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.GET.get('submit'):
            pass
        else:
            context['summary'] = self.get_summary()
        context['form'] = self.form
        context['summary'] = self.get_summary()
        return context

    
def balance_review(request):
    invoice_list_name = []    
    invoice_list_treasury_out = []
    invoice_list_treasury_in = []
    t = Treasury.objects.filter(deleted = False)
    for treasury in t :
        invoice_list_name.append(treasury.name)
        invoice1 = Invoice.objects.filter(deleted=False, saved=True, from_treasury =  treasury ).aggregate(total1 = Sum('treasury_out'))
        invoice2 = Invoice.objects.filter(deleted=False, saved=True , to_treasury =  treasury ).aggregate(total1 = Sum('treasury_in'))
        invoice_list_treasury_out.append(invoice1)
        invoice_list_treasury_in.append(invoice2)
    invoice_list = zip(invoice_list_name, invoice_list_treasury_out,invoice_list_treasury_in )
    total_out = Invoice.objects.filter(deleted=False, saved=True).aggregate(total1 = Sum('treasury_out'))
    total_in = Invoice.objects.filter(deleted=False, saved=True).aggregate(total1 = Sum('treasury_in'))
    context = {
        'invoice_list':invoice_list,
        'total_out':total_out,
        'total_in':total_in,
    }
    return render(request, 'Reports/treasury_reports/balance_review_report.html', context)
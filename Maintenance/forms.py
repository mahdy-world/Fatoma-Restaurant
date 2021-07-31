from .models import *
from django import forms


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'customer',
            'product',
            'sn',
            'maintenance_type',
            'problem',
            'notes',
        ]


class TicketDiagnosisForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'diagnosis',
            'cost',
        ]


class TicketDeleteForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'deleted',
        ]


class TicketTransferForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'employee',
        ]


class OutSourceTransferForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'outsource',
            'shipping_company',
            'shipping_id',
        ]


class CostRatingForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'cost',
        ]


class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'diagnosis',
        ]


class CustomerReplyForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'customer_reply',
        ]


class TicketDoneForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'done',
        ]


class OutsourceReceiveForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'shipping_company2',
            'shipping_id2',
        ]


class OutsourceTransferForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'outsource',
            'shipping_company',
            'shipping_id',
        ]


class TickerRejectForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'reject_reason',
        ]


class CustomerReceivedForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'customer_received',
        ]


class TickerReplyForm(forms.ModelForm):
    class Meta:
        model = TicketReply
        fields = [
            'reply',
            'notify_customer',
        ]


class MaintenancePrintSettingForm(forms.ModelForm):
    class Meta:
        model = PrintSetting
        fields = '__all__'

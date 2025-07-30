from django import forms
from datetime import datetime
from django.core.exceptions import ValidationError

class SearchDeviceForm(forms.Form):
    search_text = forms.CharField(max_length="500",help_text="搜索内容")

class BorrowDeviceForm(forms.Form):
    dueBackTime = forms.DateField(help_text="预计归还:")
    def check_back_date(self):
        data = self.dueBackTime
        if data < datetime.now():
            raise ValidationError(_('日期错误：归还日期小于借用日期！'))
        return data
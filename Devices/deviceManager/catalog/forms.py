from django import forms

class SearchDeviceForm(forms.Form):
    search_text = forms.CharField(max_length="500",help_text="搜索内容")

    
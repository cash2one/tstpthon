from django import forms

class NoticeForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':40, 'cols':100}))

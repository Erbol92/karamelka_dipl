from django import forms 
from forms import formset_factory
from models import Bisquit

class ArticleForm(forms.Form):
    bisquit = forms.ModelChoiceField(queryset= Bisquit.objects.all())
    pub_date = forms.DateField()

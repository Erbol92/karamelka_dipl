from django import forms 
from .models import Bisquit, Comment, Decoration

class ArticleForm(forms.Form):
    bisquit = forms.ModelChoiceField(queryset= Bisquit.objects.all())
    pub_date = forms.DateField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

from django.forms import formset_factory

class DecorationForm(forms.Form):
    decoration = forms.ModelChoiceField(queryset=Decoration.objects.all(), label='Выберите украшение', required=False)
    quantity = forms.IntegerField(min_value=1, label='Количество', required=False, max_value=10)

# Создаем formset на основе формы
DecorationFormSet = formset_factory(DecorationForm, extra=1)  # Укажите количество форм, которые хотите отобразить
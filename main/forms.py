from django import forms 
from .models import Bisquit, Comment

class ArticleForm(forms.Form):
    bisquit = forms.ModelChoiceField(queryset= Bisquit.objects.all())
    pub_date = forms.DateField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
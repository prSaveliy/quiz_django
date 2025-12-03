from django import forms
from django.forms import formset_factory

from .models import Quiz, Question, Choice

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']

class QuestionForm(forms.Form):
    text = forms.CharField(label='Question', max_length=500)

class ChoiceForm(forms.Form):
    text = forms.CharField(label='Answer option', max_length=300)
    is_correct = forms.BooleanField(required=False, label='Correct?')

QuestionFormSet = formset_factory(QuestionForm, extra=1, can_delete=True)
ChoiceFormSet = formset_factory(ChoiceForm, extra=2, can_delete=True)


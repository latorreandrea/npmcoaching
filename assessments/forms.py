from django import forms

from .models import Answer, Question, Test


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["title", "description", "is_active"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text", "order"]
        widgets = {
            "text": forms.TextInput(attrs={"class": "form-control"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["text", "points", "order"]
        widgets = {
            "text": forms.TextInput(attrs={"class": "form-control"}),
            "points": forms.NumberInput(attrs={"class": "form-control"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
        }

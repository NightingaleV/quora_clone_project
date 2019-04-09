from django import forms
from .models import Answer, Question


class QuestionCreationForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = {'topic', 'content'}

    def __init__(self, *args, **kwargs):
        super(QuestionCreationForm, self).__init__(*args, **kwargs)
        self.initial['topic'] = 'Choose Topic'
        self.fields['topic'].widget.attrs['class'] = "ui selection dropdown"


class AnswerCreationForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = {'content', 'question', 'is_published'}
        widgets = {
            'content': forms.Textarea(attrs={
                'cols': None,
                'rows': 15,
                'class': 'form-control text-area'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(AnswerCreationForm, self).__init__(*args, **kwargs)
        self.fields['question'].widget = forms.HiddenInput()
        self.fields['question'].widget.attrs['class'] = 'question-id-input'
        self.fields['content'].widget.attrs['placeholder'] = """# Heading 1 \nSome ***bold*** example text"""


class AnswerEditForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', 'is_published']

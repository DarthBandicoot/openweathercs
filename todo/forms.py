from crispy_forms.layout import Field, ButtonHolder, Submit, Layout
from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from todo.common import TASK_STATUS
from todo.models import Locations, Tasks


class AccountForm(forms.Form):
    username = forms.CharField(max_length=50, label="Please choose a username", required=False)
    email = forms.EmailField(required=False)
    pin = forms.IntegerField(
        label="Enter 4 digit pin to create with account or if you already have an account enter your pin too login.")
    active_account = forms.ChoiceField(choices=[
        (choice.pk, choice) for choice in User.objects.all().exclude(username="admin")], required=False)

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field('username'),
            Field('email'),
            Field('active_account'),
            Field('pin'),
            ButtonHolder(
                Submit('Submit', 'submit')
            )
        )

    def clean(self):
        if len(str(self.cleaned_data['pin'])) > 4:
            raise ValidationError('Pin should only be 4 digits long')


class AddTaskForm(forms.ModelForm):
    # title = forms.CharField(max_length=250, label="Title of Task")
    # description = forms.CharField(max_length=500, label="Short description of the Task")
    # location = forms.ChoiceField(choices=[
    #     (choice.pk, choice) for choice in Locations.objects.all()], required=False)
    # status = forms.ChoiceField(choices=TASK_STATUS)

    class Meta:
        model = Tasks
        fields = ('title', 'description', 'location', 'status')

    def __init__(self, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field('title'),
            Field('description'),
            Field('location'),
            Field('status'),
            ButtonHolder(
                Submit('Submit', 'submit')
            )
        )

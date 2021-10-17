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
    active_account = forms.Select()

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # users = User.objects.all()
        users = User.objects.exclude(username="admin").values_list('id', 'username')
        if users.count() > 0:
            self.fields['active_account'] = forms.ChoiceField(choices=(*users,))

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

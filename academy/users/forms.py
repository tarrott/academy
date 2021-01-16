import datetime

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from course.models import Resource, Session
from .models import Account, Payment


class UserRegisterForm(UserCreationForm):
    today = datetime.datetime.today()
    sessions = Session.objects.all().filter(end_date__gte=today).filter(full=False)
    if sessions:
        session_choices = [(session.id, session.name) for session in sessions]
    else:
        session_choices = [(0,"Next available session")]
    session = forms.ChoiceField(choices=session_choices, required=False)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'session', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class SessionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SessionForm, self).__init__(*args, **kwargs)
        today = datetime.datetime.today()
        payments = Payment.objects.all().filter(user=self.request.user)
        registered = [ payment.session.id for payment in payments ]
        sessions = Session.objects.all().filter(end_date__gte=today).filter(full=False).exclude(id__in=registered)
        if sessions:
            session_choices = [(session.id, session.name) for session in sessions]
            self.fields["session"] = forms.ChoiceField(choices=session_choices) 

    class Meta:
        model = Session
        fields = []


class AccountUpdateForm(forms.ModelForm):
    resources = Resource.objects.all()
    interests = [(resource.name, resource.name) for resource in resources]
    interests.insert(0,('Unanswered','Unanswered'))
    interest = forms.ChoiceField(
        required=False,
        choices=interests,
        label="What would you like to see more content for?"
    )

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'interest']

class PaymentUpdateForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ['paid']
        labels = {
            "paid": ""
        }

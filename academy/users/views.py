from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from course.models import Feedback, Session, Testimonial
from .models import Payment
from .forms import (
    UserRegisterForm,
    SessionForm,
    UserUpdateForm,
    AccountUpdateForm,
    PaymentUpdateForm
)


class RegisterFormView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/account/'

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        login(self.request, authenticate(username=username, password=password))
        messages.success(self.request, f'welcome {username}, your account has been created!')
        session = Session.objects.get(pk=form.cleaned_data.get('session'))
        payment = Payment.objects.create(user=user, session=session)
        return super().form_valid(form)


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'users/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedback_responses'] = Feedback.objects.all().filter(user=self.request.user)
        context['enrollments'] = Payment.objects.all().filter(user=self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        session_form = SessionForm(instance=request.user, request=request)
        user_form = UserUpdateForm(instance=request.user)
        account_form = AccountUpdateForm(instance=request.user.account)
        context = self.get_context_data()
        context['session_form'] = session_form
        context['user_form'] = user_form
        context['account_form'] = account_form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        account_form = AccountUpdateForm(request.POST, instance=request.user.account)
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('account')


def session_enrollment(request):
    if request.method == "POST":
        form = SessionForm(request.POST, request=request)
        if form.is_valid():
            session = get_object_or_404(Session, pk=form.cleaned_data.get('session'))
            payment = Payment.objects.create(user=request.user, session=session)
            messages.success(request, f'You have now been enrolled in "{session.name}".')
            return redirect('account')


class PaymentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Payment
    success_url = '/account/'

    def test_func(self):
        payment = self.get_object()
        return payment.user == self.request.user


class PaymentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Payment
    fields = ['paid']
    success_url = '/dashboard/'

    def form_valid(self, form):
        messages.success(self.request, f'{form.instance.session} payment has been updated for user {form.instance.user}.')
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser

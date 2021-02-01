import datetime

from django.contrib import messages
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

from users.models import Payment
from .models import Feedback, Instructor, Resource, Session, Testimonial
from users.forms import PaymentUpdateForm


class HomePageView(TemplateView):
    template_name = "course/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.datetime.today()
        context['sessions'] = Session.objects.all().filter(end_date__gte=today)
        context['resources'] = Resource.objects.all()
        context['testimonials'] = Testimonial.objects.all()
        context['instructors'] = Instructor.objects.all()
        return context


class ResourceDetailView(DetailView):
    model = Resource


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "course/dashboard_overview.html"

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['users'] = User.objects.all().filter(is_staff=False).count()
        context['feedback'] = Feedback.objects.all().count()
        enrollments = Payment.objects.all()
        context['enrollments'] = enrollments.count()
        context['payments'] = enrollments.filter(paid=True).count()
        sessions = Session.objects.all()
        context['sessions'] = {}
        for session in sessions:
            context['sessions'][session.name] = {}
            session_enrollments = enrollments.filter(session=session.pk)
            if session_enrollments.count() > 0:
                context['sessions'][session.name] = {
                    'enrollments': [],
                    'paid': int(session_enrollments.filter(paid=True).count() / session_enrollments.count() * 100)
                }
                for enrollment in session_enrollments:
                    context['sessions'][session.name]['enrollments'].append({
                        'id': enrollment.pk,
                        'student': enrollment.user,
                        'payment': PaymentUpdateForm(instance=enrollment)
                    })
        return context

    def test_func(self):
        return self.request.user.is_superuser


class FeedbackListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Feedback
    ordering = ['-date_created']
    paginate_by = 5

    def test_func(self):
        return self.request.user.is_superuser


class FeedbackUserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'users/feedback_user.html'
    model = Feedback
    ordering = ['-date_created']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Feedback.objects.filter(user=user).order_by('-date_created')

    def test_func(self):
        return self.request.user.is_superuser


class FeedbackCreate(LoginRequiredMixin, CreateView):
    model = Feedback
    fields = ['subject', 'content']
    success_url = '/account/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f'Your feedback has been submitted.')
        return super().form_valid(form)


class FeedbackUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Feedback
    fields = ['subject', 'content']
    success_url = '/account/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        feedback = self.get_object()
        return feedback.user == self.request.user


class FeedbackDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Feedback
    success_url = '/account/'

    def test_func(self):
        feedback = self.get_object()
        return feedback.user == self.request.user

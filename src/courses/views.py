from django.shortcuts import render
from time import timezone

from django.views.generic import ListView, DetailView, View
from .models import Course
from memberships.models import UserMemberShip


def index(request):
    """ Landing page for app """
    return render(request, 'courses/index.html', { 'hello' : 'Hello world!'})

class CourseListView(ListView):
    """ ListView for Listing Courses """
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.denominator
        return context


class CourseDetailView(DetailView):
    """ DetailView for Course """
    model = Course


class LessonDetailView(View):
    """ Lesson detail view more custumizeable """

    def get(self, request, course_slug, lesson_slug, *args, **kwargs):

        course_qs = Course.objects.filter(slug=course_slug)
        if course_qs.exists():
            course = course_qs.first()

        lesson_qs = course.lessons.filter(slug=lesson_slug)
        if lesson_qs.exists():
            lesson = lesson_qs.first()

        user_membership = UserMemberShip.objects.filter(user=request.user).first()
        user_membership_type = user_membership.membership.membership_type

        course_allowed_mem_types = course.allowed_memberships.all()

        context = {
            'object': None
        }

        if course_allowed_mem_types.filter(membership_type=user_membership_type).exists():
            context = {
                'object': lesson
            }

        return render(request, "courses/lesson_detail.html", context)

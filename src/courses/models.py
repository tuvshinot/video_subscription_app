from django.db import models
from django.urls import reverse

from memberships.models import Membership


class Course(models.Model):
    """ Course Object """
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    allowed_memberships = models.ManyToManyField(Membership)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})

    @property
    def lessons(self):
        """ Property 'course.lessons' """
        return self.lesson_set.all().order_by('position')


class Lesson(models.Model):
    """ Lesson object """
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    video_url = models.CharField(max_length=200)
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:lesson-detail', kwargs={
            'course_slug': self.course.slug,
            'lesson_slug': self.slug
        })

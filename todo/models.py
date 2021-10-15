from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel

from todo.common import TASK_STATUS


class TodoList(TimeStampedModel):
    title = models.CharField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default="admin")
    pin = models.IntegerField()


class Locations(models.Model):
    class Meta:
        verbose_name_plural = "Locations"

    city = models.CharField(max_length=250, blank=True, null=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.city


class Tasks(TimeStampedModel):
    class Meta:
        verbose_name_plural = "Tasks"

    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=250, choices=TASK_STATUS, default="TODO")
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default="admin")
    todolist = models.ForeignKey(TodoList, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title



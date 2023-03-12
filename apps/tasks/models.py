from django.db import models
from accounts.models import User

# Create your models here.


class OnlineTrainingTask(models.Model):
    name = models.CharField(verbose_name="Name", max_length=350)
    is_active = models.BooleanField(default=False, verbose_name="This task is active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Online training task"
        verbose_name_plural = "Online training tasks"

    def __str__(self):
        return self.name


class OnlineTrainingTaskMember(models.Model):
    task = models.ForeignKey(
        OnlineTrainingTask, on_delete=models.CASCADE, verbose_name="Task"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    tasks_per_turn = models.IntegerField(default=1, verbose_name="Tasks per turn")
    number_of_assigned_tasks = models.IntegerField(
        default=0, verbose_name="Number of assigned tasks"
    )

    class Meta:
        verbose_name = "Online training task member"
        verbose_name_plural = "Online training task members"

    def __str__(self):
        return f"User - {self.user.first_name} | Task - {self.task.name}"

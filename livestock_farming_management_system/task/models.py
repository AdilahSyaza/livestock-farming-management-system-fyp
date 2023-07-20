from django.db import models
from user.models import User

# This model defines Task table in database with fields related to task information.
class Task(models.Model):

    taskName = models.CharField(max_length=250)
    taskPriority = models.CharField(max_length=250)
    taskCategory = models.CharField(max_length=250)
    taskDetails = models.CharField(max_length=250)
    taskDueDate = models.DateField()
    taskCompletionStatus = models.CharField(max_length=250)
    taskAttachment = models.FileField(upload_to='task/', null=True)
    taskAssignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taskAssignee")
    taskAssigner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taskAssigner")

    def save(self):
        super().save()

    def delete(self):
        super().delete()

    class Meta:
        db_table = 'Task'
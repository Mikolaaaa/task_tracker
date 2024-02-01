from django.db import models


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic}"


class Task(models.Model):

    class Priority(models.TextChoices):
        HIGH = 'Высокий', 'Высокий'
        MEDIUM = 'Средний', 'Средний'
        LOW = 'Низкий', 'Низкий'

    class Readiness(models.TextChoices):
        p100 = '100%', '100%'
        p75 = '75%', '75%'
        p50 = '50%', '50%'
        p25 = '25%', '25%'
        p0 = '0%', '0%'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date_start = models.DateField()
    date_end = models.DateField()
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.HIGH,
    )
    readiness = models.CharField(
        max_length=20,
        choices=Readiness.choices,
        default=Readiness.p0,
    )
    """priority = models.CharField(max_length=255)
    readiness = models.CharField(max_length=255)"""

    def __str__(self):
        return f"{self.name} {self.description}"


class User_Task(models.Model):
    id = models.AutoField(primary_key=True)
    worker_id = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"Worker: {self.worker_id.name} {self.worker_id.surname}, Task: {self.task_id.name}"


class Status_Task(models.Model):
    id = models.AutoField(primary_key=True)
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"Task ID: {self.task_id.name} Status ID: {self.status_id.name}"
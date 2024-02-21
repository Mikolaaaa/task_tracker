from django.db import models
from django.core.validators import RegexValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^[а-яА-Яa-zA-Z0-9\s_.,!@#%&*()-+=;:]*$',
            message='Недопустимые символы. Используйте только кириллицу, латиницу, цифры и некоторые спец символы.',
            code='invalid_name',
        ),
        MaxLengthValidator(50, message='Длина поля не должна превышать 50 символов.')
    ])
    description = models.CharField(blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^[а-яА-Яa-zA-Z0-9\s_.,!@#%&*()-+=;:]*$',
            message='Недопустимые символы. Используйте только кириллицу, латиницу, цифры и некоторые спец символы.',
            code='invalid_description',
        ),
        MaxLengthValidator(255, message='Длина поля не должна превышать 255 символов.')
    ])

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^[а-яА-Яa-zA-Z0-9\s_.,!@#%&*()-+=;:]*$',
            message='Недопустимые символы. Используйте только кириллицу, латиницу, цифры и некоторые спец символы.',
            code='invalid_name',
        ),
        MaxLengthValidator(50, message='Длина поля не должна превышать 50 символов.')
    ])
    surname = models.CharField(blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^[а-яА-Яa-zA-Z0-9\s_.,!@#%&*()-+=;:]*$',
            message='Недопустимые символы. Используйте только кириллицу, латиницу, цифры и некоторые спец символы.',
            code='invalid_surname',
        ),
        MaxLengthValidator(50, message='Длина поля не должна превышать 50 символов.')
    ])
    patronymic = models.CharField(blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^[а-яА-Яa-zA-Z0-9\s_.,!@#%&*()-+=;:]*$',
            message='Недопустимые символы. Используйте только кириллицу, латиницу, цифры и некоторые спец символы.',
            code='invalid_patronymic',
        ),
        MaxLengthValidator(50, message='Длина поля не должна превышать 50 символов.')
    ])
    email = models.CharField(blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^[а-яА-Яa-zA-Z0-9\s_.,!@#%&*()-+=;:]*$',
            message='Недопустимые символы. Используйте только кириллицу, латиницу, цифры и некоторые спец символы.',
            code='invalid_email',
        ),
        MaxLengthValidator(50, message='Длина поля не должна превышать 50 символов.')
    ])

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
    name = models.CharField(blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^[а-яА-Яa-zA-Z0-9\s_.,!@#%&*()-+=;:]*$',
            message='Недопустимые символы. Используйте только кириллицу, латиницу, цифры и некоторые спец символы.',
            code='invalid_name',
        ),
        MaxLengthValidator(50, message='Длина поля не должна превышать 50 символов.')
    ])
    description = models.CharField(blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^[а-яА-Яa-zA-Z0-9\s_.,!@#%&*()-+=;:]*$',
            message='Недопустимые символы. Используйте только кириллицу, латиницу, цифры и некоторые спец символы.',
            code='invalid_description',
        ),
        MaxLengthValidator(255, message='Длина поля не должна превышать 50 символов.')
    ])
    date_start = models.DateField(blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^\d{4}-\d{2}-\d{2}$',
            message='Недопустимый формат. Введите дату в формате dd-mm-yyy',
            code='invalid_date',
        )
    ])
    date_end = models.DateField(blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^\d{4}-\d{2}-\d{2}$',
            message='Недопустимый формат. Введите дату в формате dd-mm-yyy',
            code='invalid_date',
        )
    ])
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.CharField(
        max_length=50,
        choices=Priority.choices,
        default=Priority.HIGH,
        blank=True, null=True,
    )
    readiness = models.CharField(
        max_length=50,
        choices=Readiness.choices,
        default=Readiness.p0,
        blank=True, null=True,
    )
    """priority = models.CharField(max_length=255)
    readiness = models.CharField(max_length=255)"""

    def validate_date(self):
        if self < timezone.now().date():
            raise ValidationError('Нельзя выбирать прошедшую дату.')

    def clean(self):
        if self.date_start and self.date_end and self.date_end < self.date_start:
            raise ValidationError("Дата конца должна быть больше даты начала.")

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
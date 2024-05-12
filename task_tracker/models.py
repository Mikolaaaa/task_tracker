from django.db import models
from django.core.validators import RegexValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _

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
    id_user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)

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
    id_user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)

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
    worker_id = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"Worker: {self.worker_id.name} {self.worker_id.surname}, Task: {self.task_id.name}"


class Status_Task(models.Model):
    id = models.AutoField(primary_key=True)
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"Task ID: {self.task_id.name} Status ID: {self.status_id.name}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=50, blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^[а-яА-Яa-zA-Z]*$',
            message=_('Invalid characters. Use only Cyrillic, Latin, digits, and some special characters.'),
            code='invalid_name',
        ),
        MaxLengthValidator(50, message=_('Field length should not exceed 50 characters.'))
    ])
    surname = models.CharField(_('surname'), max_length=50, blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^[а-яА-Яa-zA-Z]*$',
            message=_('Invalid characters. Use only Cyrillic, Latin, digits, and some special characters.'),
            code='invalid_surname',
        ),
        MaxLengthValidator(50, message=_('Field length should not exceed 50 characters.'))
    ])
    patronymic = models.CharField(_('patronymic'), max_length=50, blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^[а-яА-Яa-zA-Z0-9\s_.,!@#%&*()-+=;:]*$',
            message=_('Invalid characters. Use only Cyrillic, Latin, digits, and some special characters.'),
            code='invalid_patronymic',
        ),
        MaxLengthValidator(50, message=_('Field length should not exceed 50 characters.'))
    ])

    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email
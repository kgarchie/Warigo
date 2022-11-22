from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models

from django.utils.translation import gettext_lazy as _

from .managers import UserManager


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    staff_id_or_reg_no = models.CharField(max_length=20, unique=True,
                                          help_text='Enter your Staff/ID Number or Registration Number')
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_admin = models.BooleanField(_("admin status"),
                                   default=False,
                                   help_text=_("Designates whether the user is an admin. Student Leaders only"))

    objects = UserManager()

    USERNAME_FIELD = 'staff_id_or_reg_no'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'student'
        verbose_name_plural = 'students'

    @property
    def get_full_user_details(self):
        full_user_details = self.name + '\t' + self.staff_id_or_reg_no
        return full_user_details

    def get_full_name(self):
        return self.name + ' ' + self.staff_id_or_reg_no

    def get_short_name(self):
        return self.name

    def email_student(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this Student.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class FundApplication(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    project_description = models.TextField()
    application_date = models.DateField(auto_now_add=True)
    amount_applied_for = models.IntegerField()
    amount_approved = models.IntegerField(blank=True, null=True)
    ps = models.DateField(auto_created=True, blank=True, null=True)
    pe = models.DateField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    campus = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.applicant.name

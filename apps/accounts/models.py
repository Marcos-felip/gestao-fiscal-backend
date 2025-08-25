from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class BaseModel(models.Model):
    """Base abstrata com controle de organização."""
    organization = models.ForeignKey('accounts.Organization', on_delete=models.CASCADE, related_name='%(class)ss')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organization(models.Model):
    """Organização agrupando empresas e usuários."""
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Usuário customizado para permitir relacionamentos de membership multi-org."""
    email = models.EmailField(unique=True)
    username = models.CharField(blank=True, null=True,max_length=100)
    org_active = models.ForeignKey(Organization, verbose_name='organização ativa', blank=True, null=True, on_delete=models.CASCADE, related_name="organization")
    org_list = models.ManyToManyField(Organization, verbose_name='organizações', blank=True, through='Membership')
    email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Membership(models.Model):
    """Associação de usuário a organização, com permissões."""
    class Role(models.TextChoices):
        OWNER = 'owner', 'Owner'
        ADMIN = 'admin', 'Admin'
        MEMBER = 'member', 'Member'
        READONLY = 'readonly', 'Read Only'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'organization')

    def __str__(self):
        return f"{self.user.username} @ {self.organization.slug} ({self.role})"

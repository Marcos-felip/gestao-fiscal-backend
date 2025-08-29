from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import secrets


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
    class OrganizationType(models.TextChoices):
        GROUP = 'group', 'Group'
        COMPANY = 'company', 'Company'

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, verbose_name=u'Telefone', null=True, blank=True)
    organization_type = models.CharField(max_length=20, choices=OrganizationType.choices , default=OrganizationType.COMPANY)
    key = models.CharField(max_length=50, verbose_name=u'hash id', null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_urlsafe(32)[:50]
        super().save(*args, **kwargs)


class User(AbstractUser):
    """Usuário customizado para permitir relacionamentos de membership multi-org."""
    email = models.EmailField(unique=True)
    username = models.CharField(blank=True, null=True,max_length=100)
    key = models.CharField(max_length=50, verbose_name=u'hash id', null=True, blank=True, db_index=True)
    org_active = models.ForeignKey(Organization, verbose_name='organização ativa', blank=True, null=True, on_delete=models.CASCADE, related_name="organization")
    org_list = models.ManyToManyField(Organization, verbose_name='organizações', blank=True, through='Membership')
    email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_urlsafe(32)[:50]
        super().save(*args, **kwargs)

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
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'organization')

    def __str__(self):
        return f"{self.user.username} @ {self.organization.slug} ({self.role})"

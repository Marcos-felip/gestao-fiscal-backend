from django.db import models
from django.utils import timezone
from apps.accounts.models import BaseModel


class Company(BaseModel):
    """Representa a pessoa jurídica (empresa) agregadora de matriz e filiais.

    Notas:
    - O CNPJ completo fica associado ao estabelecimento.
    - Armazena informações corporativas e o regime tributário aplicado.
    """

    class TaxRegime(models.TextChoices):
        SIMPLES = 'simples', 'Simples Nacional'
        SIMPLES_EXCESSO = 'simples_excesso', 'Simples Nacional – Excesso sublimite'
        PRESUMIDO = 'presumido', 'Lucro Presumido'
        REAL = 'real', 'Lucro Real'

    legal_name = models.CharField(max_length=255, verbose_name='Razão Social')
    trade_name = models.CharField(max_length=255, blank=True, verbose_name='Nome Fantasia')
    tax_regime = models.CharField(max_length=30, choices=TaxRegime.choices, verbose_name='Regime Tributário')

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return f"{self.legal_name} ({self.cnpj or ''})"


class Address(models.Model):
    """Endereço físico normalizado utilizado por estabelecimentos."""

    street = models.CharField(max_length=255, verbose_name='Logradouro')
    number = models.CharField(max_length=20, verbose_name='Número')
    complement = models.CharField(max_length=60, blank=True, verbose_name='Complemento')
    district = models.CharField(max_length=80, verbose_name='Bairro')
    city_name = models.CharField(max_length=120, verbose_name='Cidade')
    city_ibge_code = models.CharField(max_length=7, help_text='Código IBGE (7 dígitos)', verbose_name='Código IBGE')
    state = models.CharField(max_length=2, verbose_name='UF')
    postal_code = models.CharField(max_length=8, help_text='CEP (8 dígitos)', verbose_name='CEP')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        indexes = [
            models.Index(fields=['city_ibge_code']),
            models.Index(fields=['state']),
        ]

    def __str__(self):
        return f"{self.street}, {self.number} - {self.city_name}/{self.state}"


class Establishment(models.Model):
    """Estabelecimento físico/fiscal (matriz ou filial) emissor de documentos fiscais."""

    class Environment(models.TextChoices):
        PRODUCTION = 'production', 'Production'
        HOMOLOGATION = 'homologation', 'Homologation'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='establishments', verbose_name='Empresa')
    cnpj = models.CharField(max_length=14, unique=True, verbose_name='CNPJ')
    state_registration = models.CharField(max_length=20, blank=True, verbose_name='Inscrição Estadual')
    municipal_registration = models.CharField(max_length=20, blank=True, verbose_name='Inscrição Municipal')
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='establishments', verbose_name='Endereço')
    is_matrix = models.BooleanField(default=False)
    environment_default = models.CharField(max_length=20, choices=Environment.choices, default=Environment.PRODUCTION, verbose_name='Ambiente Padrão')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Estabelecimento'
        verbose_name_plural = 'Estabelecimentos'
        constraints = [
            models.UniqueConstraint(
                fields=['company'],
                condition=models.Q(is_matrix=True),
                name='unique_matrix_per_company'
            )
        ]

    def __str__(self):
        return f"{self.cnpj} ({'Matriz' if self.is_matrix else 'Filial'})"


class Product(BaseModel):
    """Produto cadastrado (catálogo) utilizado em operações de compra e venda."""

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products', verbose_name='Empresa')
    name = models.CharField(max_length=255, verbose_name='Nome')
    sku = models.CharField(max_length=50, unique=True, verbose_name='SKU')
    ncm = models.CharField(max_length=8, help_text='NCM (8 dígitos)', verbose_name='NCM')
    cest = models.CharField(max_length=9, blank=True, verbose_name='CEST')
    cfop_sale = models.CharField(max_length=10, blank=True, verbose_name='CFOP Venda')
    unit = models.CharField(max_length=6, default='UN', verbose_name='Unidade')
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Preço de Custo')
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Preço de Venda')
    cest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Alíquota CEST')
    origin = models.IntegerField(default=0, help_text='Origem (0 a 8)', verbose_name='Origem Mercadoria')

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        unique_together = ('company', 'name')

    def __str__(self):
        return self.name

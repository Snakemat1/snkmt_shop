from django.db import models
import random

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(blank=True, upload_to="products/")  
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


    def __str__(self):
        return self.name
    
class Attribute(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="values"
    )

    value = models.CharField(max_length=50)

    class Meta:
        unique_together = ("attribute", "value")

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"
    
class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )
    attribute_values = models.ManyToManyField(AttributeValue)
    sku = models.CharField(max_length=50, unique=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)

    def generate_sku(self):
        while True:
            sku = str(random.randint(10000000, 99999999))
            if not ProductVariant.objects.filter(sku=sku).exists():
                return sku
            
    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = self.generate_sku()
        super().save(*args, **kwargs)
    
    def __str__(self):
        values =  ", ".join(str(v) for v in self.attribute_values.all())
        return f"{self.product}: {values}"

    def get_price(self):
        return self.price if self.price is not None else self.product.base_price
        
    class Meta:
        ordering = ["product__name"]



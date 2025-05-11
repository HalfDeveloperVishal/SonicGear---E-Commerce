from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin 
from django.conf import settings
from django.core.exceptions import ValidationError

class New_arrival(models.Model):
    class ProductType(models.TextChoices):
        GADGET = 'GAD', 'Gadget'
        HEADPHONE = 'HP', 'Headphone'
        EARPHONE = 'EP', 'Earphone'
        OTHER = 'OTH', 'Other'

    class StockStatus(models.TextChoices):
        IN_STOCK = 'IN', 'In Stock'
        OUT_OF_STOCK = 'OUT', 'Out of Stock'
        LIMITED_STOCK = 'LIM', 'Limited Stock'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True
    )
    description = models.TextField(blank=True, null=True, help_text="Detailed product description")
    stock_status = models.CharField(
        max_length=3,
        choices=StockStatus.choices,
        default=StockStatus.IN_STOCK
    )
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    type = models.CharField(
        max_length=3,
        choices=ProductType.choices,
        default=ProductType.OTHER
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} ({self.type}) - ${self.price}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "New_arrival"
        verbose_name_plural = "New_arrivals"


class Featured_product(models.Model):
    class ProductType(models.TextChoices):
        GADGET = 'GAD', 'Gadget'
        HEADPHONE = 'HP', 'Headphone'
        EARPHONE = 'EP', 'Earphone'
        OTHER = 'OTH', 'Other'

    class StockStatus(models.TextChoices):
        IN_STOCK = 'IN', 'In Stock'
        OUT_OF_STOCK = 'OUT', 'Out of Stock'
        LIMITED_STOCK = 'LIM', 'Limited Stock'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True
    )
    description = models.TextField(blank=True, null=True, help_text="Detailed product description")
    stock_status = models.CharField(
        max_length=3,
        choices=StockStatus.choices,
        default=StockStatus.IN_STOCK
    )
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    type = models.CharField(
        max_length=3,
        choices=ProductType.choices,
        default=ProductType.OTHER
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} ({self.type}) - ${self.price}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Featured_product"
        verbose_name_plural = "Featured_products"
        
        
class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        
        user = self.model(name=name, email=email)
        user.set_password(password)
        user.is_active = True  # Make user active
        user.is_staff = False   # Not an admin
        user.save(using=self._db)
        return user
    
    def create_superuser(self, name, email, password):
        """Create and return a superuser with admin privileges."""
        user = self.create_user(name, email, password)
        user.is_staff = True  # Admin access
        user.is_superuser = True  # Superuser privileges
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Ensure user is not an admin

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name
    
class Earphone(models.Model):
    class StockStatus(models.TextChoices):
        IN_STOCK = 'IN', 'In Stock'
        OUT_OF_STOCK = 'OUT', 'Out of Stock'
        LIMITED_STOCK = 'LIM', 'Limited Stock'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True
    )
    description = models.TextField(blank=True, null=True, help_text="Detailed product description")
    stock_status = models.CharField(
        max_length=3,
        choices=StockStatus.choices,
        default=StockStatus.IN_STOCK
    )
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} - ${self.price}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Earphone"
        verbose_name_plural = "Earphones"


class Headphone(models.Model):
    class StockStatus(models.TextChoices):
        IN_STOCK = 'IN', 'In Stock'
        OUT_OF_STOCK = 'OUT', 'Out of Stock'
        LIMITED_STOCK = 'LIM', 'Limited Stock'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True
    )
    description = models.TextField(blank=True, null=True, help_text="Detailed product description")
    stock_status = models.CharField(
        max_length=3,
        choices=StockStatus.choices,
        default=StockStatus.IN_STOCK
    )
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} - ${self.price}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Headphone"
        verbose_name_plural = "Headphones"


class TechGadget(models.Model):
    class StockStatus(models.TextChoices):
        IN_STOCK = 'IN', 'In Stock'
        OUT_OF_STOCK = 'OUT', 'Out of Stock'
        LIMITED_STOCK = 'LIM', 'Limited Stock'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True
    )
    description = models.TextField(blank=True, null=True, help_text="Detailed product description")
    stock_status = models.CharField(
        max_length=3,
        choices=StockStatus.choices,
        default=StockStatus.IN_STOCK
    )
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} - ${self.price}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Tech Gadget"
        verbose_name_plural = "Tech Gadgets"
        

class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_additional_images/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # You can relate it to all product models using nullable ForeignKeys
    new_arrival = models.ForeignKey('New_arrival', on_delete=models.CASCADE, related_name='additional_images', null=True, blank=True)
    featured_product = models.ForeignKey('Featured_product', on_delete=models.CASCADE, related_name='additional_images', null=True, blank=True)
    earphone = models.ForeignKey('Earphone', on_delete=models.CASCADE, related_name='additional_images', null=True, blank=True)
    headphone = models.ForeignKey('Headphone', on_delete=models.CASCADE, related_name='additional_images', null=True, blank=True)
    techgadget = models.ForeignKey('TechGadget', on_delete=models.CASCADE, related_name='additional_images', null=True, blank=True)

    def __str__(self):
        return f"Image for {self.new_arrival or self.featured_product or self.earphone or self.headphone or self.techgadget}"


class CartItem(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, blank=True
    )

    PRODUCT_CHOICES = [
        ('new_arrival', 'New Arrival'),
        ('featured_product', 'Featured Product'),
        ('earphone', 'Earphone'),
        ('headphone', 'Headphone'),
        ('techgadget', 'Tech Gadget'),
    ]

    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_CHOICES,
    )

    new_arrival = models.ForeignKey(
        New_arrival,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    featured_product = models.ForeignKey(
        Featured_product,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    earphone = models.ForeignKey(
        Earphone,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    headphone = models.ForeignKey(
        Headphone,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    techgadget = models.ForeignKey(
        TechGadget,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    added_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.product_type == 'new_arrival' and not self.new_arrival:
            raise ValidationError("You must select a 'New Arrival' product.")
        if self.product_type == 'featured_product' and not self.featured_product:
            raise ValidationError("You must select a 'Featured Product'.")
        if self.product_type == 'earphone' and not self.earphone:
            raise ValidationError("You must select an 'Earphone' product.")
        if self.product_type == 'headphone' and not self.headphone:
            raise ValidationError("You must select a 'Headphone' product.")
        if self.product_type == 'techgadget' and not self.techgadget:
            raise ValidationError("You must select a 'Tech Gadget' product.")

        # Prevent selecting multiple product types
        if self.product_type != 'new_arrival' and self.new_arrival:
            raise ValidationError("You selected an extra product alongside 'New Arrival'.")
        if self.product_type != 'featured_product' and self.featured_product:
            raise ValidationError("You selected an extra product alongside 'Featured Product'.")
        if self.product_type != 'earphone' and self.earphone:
            raise ValidationError("You selected an extra product alongside 'Earphone'.")
        if self.product_type != 'headphone' and self.headphone:
            raise ValidationError("You selected an extra product alongside 'Headphone'.")
        if self.product_type != 'techgadget' and self.techgadget:
            raise ValidationError("You selected an extra product alongside 'Tech Gadget'.")

    def __str__(self):
        if self.product_type == 'new_arrival' and self.new_arrival:
            return f"{self.new_arrival.product_name} - {self.quantity}"
        elif self.product_type == 'featured_product' and self.featured_product:
            return f"{self.featured_product.product_name} - {self.quantity}"
        elif self.product_type == 'earphone' and self.earphone:
            return f"{self.earphone.product_name} - {self.quantity}"
        elif self.product_type == 'headphone' and self.headphone:
            return f"{self.headphone.product_name} - {self.quantity}"
        elif self.product_type == 'techgadget' and self.techgadget:
            return f"{self.techgadget.product_name} - {self.quantity}"
        return "Unknown Product"

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default="India")  # or make it dynamic

    def __str__(self):
        return f"{self.full_name} - {self.city}"
    
class AllProduct(models.Model):
    CATEGORY_CHOICES = [
        ('featured', 'Featured'),
        ('new_arrival', 'New Arrival'),
        ('earphone', 'Earphone'),
        ('headphone', 'Headphone'),
        ('tech_gadget', 'TechGadget'),
    ]
    
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    def __str__(self):
        return self.product_name

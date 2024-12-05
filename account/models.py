from django.db import models
from django.conf import settings 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,email,password=False):
        if not email:
            raise ValueError('Users must be email')
        
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staffuser(self,email,password=False):
        if not email:
            raise ValueError('Users must be email')
        
        user = self.create_user(email,password=password)
        user.staff = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=False):
        if not email:
            raise ValueError('Users must be email')
        
        user = self.create_user(email,password=password)
        user.admin = True
        user.staff = True
        user.customer = False
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff= models.BooleanField(default=False)
    customer = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True


    def __str__(self):
        return self.email
    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(
        max_length=50, 
        choices=[('lunch', 'Lunch'), ('breakfast', 'Breakfast'), ('snacks', 'Snacks'), ('drinks', 'Drinks')], 
        default='lunch'
    )
    is_featured = models.BooleanField(default=False)  # Indicates if the product is featured
    is_special = models.BooleanField(default=False)   # Indicates if the product belongs to the special menu

    def __str__(self):
        return self.name

# account/models.py
class CartItems(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, default=1, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)  # Using PositiveIntegerField for quantity

    def __str__(self):
        return f"{self.quantity} of {self.product.name} for {self.user.email}"


class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
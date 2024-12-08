from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, phoneNumber, email, fullName, cnic, user_type, password=None, **extra_fields):
        '''
        Creates and saves a new user
        '''
        if not phoneNumber:
            raise ValueError('Users must have a phone number')

        # Create a new user instance with normalized email
        user = self.model(
            phoneNumber=phoneNumber,
            email=self.normalize_email(email),
            fullName=fullName,
            cnic=cnic,
            user_type=user_type,
            **extra_fields
        )

        user.set_password(password) # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, phoneNumber, email, fullName, cnic, user_type=None, password=None):
        '''
        Creates and saves a superuser with administrative privileges.
        Superusers are always created with ADMIN user_type.
        '''
        if user_type and user_type != self.model.UserType.ADMIN:
            raise ValueError('Superuser must have user_type=ADMIN')
            
        user = self.create_user(
            phoneNumber=phoneNumber,
            email=email,
            fullName=fullName,
            cnic=cnic,
            user_type=self.model.UserType.ADMIN,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    '''
    Custom user model for AgroConnect platform
    '''
    class UserType(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        FARMER = 'FARMER', 'Farmer'
        DOCTOR = 'DOCTOR', 'Doctor'
        ADMIN = 'ADMIN', 'Admin'  # Only for superusers

    email = models.EmailField(unique=True)

    fullName = models.CharField(max_length=100)

    # Phone number with format validation
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,14}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed."
    )

    phoneNumber = models.CharField(
        validators=[phone_regex], 
        max_length=15, 
        unique=True
    )

    cnic = models.CharField(max_length=15, unique=True)

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        help_text='ADMIN type is reserved for superusers only'
    )

    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phoneNumber'

    REQUIRED_FIELDS = ['fullName', 'email', 'cnic', 'user_type']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'  # Custom table name in database
    
    def __str__(self):
        """String representation of the user"""
        return f"{self.fullName} ({self.user_type})"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
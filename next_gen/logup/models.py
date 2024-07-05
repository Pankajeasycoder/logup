from django.db import models
from django.contrib.auth.models import (BaseUserManager ,AbstractBaseUser)



class UserManager(BaseUserManager):
    def create_user(self,email, first_name=None,password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        user =self.model(
            email=self.normalize_email(email),
            first_name=first_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,first_name,password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user =self.create_user(
            email,
            password=password,
            first_name=first_name
        )
        user.is_admin=True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    email=  models.EmailField(
        verbose_name="email adderss",
        max_length=255,
        unique=True,
        )
    username1=models.CharField(max_length=100,null=True,unique=True)
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,blank=True)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    is_dealer=models.BooleanField(default=False)
    is_client=models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)
    is_online=models.BooleanField(default=False)
    objects  =  UserManager ()
    


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']




    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

        
class OTPModel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    otp=models.CharField(max_length=6)

    def __str__(self):
        return str(self.user)
    

class JobCategoryModel(models.Model):
    category_title=models.CharField(max_length=45)
    category_desc=models.CharField(max_length=1000)
    
    def __str__(self):
        return str(self.category_title)

class JobTypeModel(models.Model):
    job_type_title=models.CharField(max_length=45)
    job_type_desc=models.CharField(max_length=1000)

    def __str__(self):
        return str(self.job_type_title)

class SkillModel(models.Model):
    skill_title=models.CharField(max_length=45)
    skill_desc=models.CharField(max_length=100)
    
    def __str__(self):
        return self.skill_title
    

class DealerProfileModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    company_logo=models.ImageField(upload_to='dealer/company/logos',default='dealer/company/logos/default_profile.png',blank=True)
    company_address=models.CharField(max_length=100, null= True, blank= True)
    # city_of_company=models.CharField(max_length=100)
    # country_of_company=CountryField()
    state=models.CharField(max_length=100, blank=True, null=True)
    #company_name=models.CharField(max_length=100,unique=True, blank=True,null=True,)
    #company_email=models.EmailField(max_length=255,unique=True, blank=True,null=True,)
    #company_phone_number=models.CharField(max_length=20,blank=True,null=True,unique=True)
    company_short_desc=models.CharField(max_length=100)
    company_desc=models.CharField(max_length=200) 

    def __str__(self):
        return str(self.user.first_name)

class ClientProfileModel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=200, blank = True, null=True)
    profile_desc=models.CharField(max_length=100)
    city=models.CharField(max_length=100, null=True, blank= True)
    # country=CountryField()
    state=models.CharField(max_length=100, null=True, blank= True)
    gender=models.CharField(max_length=20)
    skills=models.ManyToManyField(SkillModel, blank = True)
    linkedin_profile=models.URLField(max_length=255,blank=True,null=True)
    github_profile=models.URLField(max_length=255,blank=True,null=True)
    profile_picture=models.ImageField(upload_to='costomer/images/profile_pic',default='costomer/images/profile_pic/default_profile_Is8arW2.png',blank=True)
    resume=models.FileField(upload_to='costomer/files/resumes',blank=True)
    long_description=models.TextField(null=True)
    language=models.CharField(max_length=255,null=True, blank=True)
    education=models.TextField(null=True, blank = True)
    available=models.CharField(max_length=255,null=True, blank = True)
    verification=models.BooleanField(default=False)
    experience=models.IntegerField(null=True, blank = True)
    category=models.ForeignKey(JobCategoryModel, on_delete= models.PROTECT,null=True,blank=True)
    dob=models.DateField(max_length=8, null=True, blank = True)

    def __str__(self):
        return str(self.user)


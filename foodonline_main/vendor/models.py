from django.db import models
from accounts.models import User,UserProfile
from accounts.utilis import send_approve_mail
from django.template.defaultfilters import slugify
from datetime import time

# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userProfile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_licence = models.ImageField(upload_to='vendor/licence')
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    def save(self, *args, **kwargs):
            # Auto-generate slug if it doesn't exist
            if not self.vendor_slug and self.user_id:  # ensure user exists
                self.vendor_slug = slugify(self.vendor_name) + '-' + str(self.user.id)

            # Send approval email if status changed
            if self.pk is not None:
                orig = Vendor.objects.get(pk=self.pk)
                if orig.is_approved != self.is_approved:
                    mail_template = 'accounts/emails/vendor_email.html'
                    context = {'user': self.user, 'is_approved': self.is_approved}
                    mail_subject = 'Congratulations, Your Restaurant Menu was Approved' if self.is_approved else 'Restaurant Menu was Rejected'
                    send_approve_mail(mail_template, context, mail_subject)

            super().save(*args, **kwargs)

DAYS = [
     (1,("Monday")),
     (2,("Tuesday")),
     (3,("Wednesday")),
     (4,("Thursday")),
     (5,("Friday")),
     (6,("Saturday")),
     (7,("Sunday")),

]

HOURS_OF_24 = [(time(h,m).strftime('%I:%M:%p'),time(h,m).strftime('%I:%M:%p')) for h in range(0,24) for m in (0,30)]

class OpeningHour(models.Model):
     vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
     day = models.IntegerField(choices=DAYS)
     from_hour = models.CharField(choices=HOURS_OF_24,max_length=10,blank=True)
     to_hour = models.CharField(choices=HOURS_OF_24,max_length=10,blank=True)
     is_closed = models.BooleanField(default=False)

     class Meta:
          ordering = ('day','from_hour')
          unique_together = ('vendor','day','from_hour','to_hour')
        
     def __str__(self):
          return self.get_day_display()  
     @classmethod
     def get_day_name_from_value(cls, day_value):

        return dict(cls._meta.get_field('day').choices).get(day_value, 'Unknown Day')
     
     

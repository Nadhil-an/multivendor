from django.db import models
from accounts.models import User,UserProfile
from accounts.utilis import send_approve_mail

# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile,related_name='userProfile',on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_licence = models.ImageField(upload_to='vendor/licence')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
    def save(self,*args,**kwargs):
        if self.pk is not None:
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/vendor_email.html'
                context ={
                    'user': self.user,
                    'is_approved':self.is_approved,
                }
                if self.is_approved == True:
                    mail_subject = 'Congratulations, Your Resturant Menu was Approved'
                    send_approve_mail(mail_template,context,mail_subject)
                else:
                    mail_subject = 'Resturant Menu was Rejected'
                    send_approve_mail(mail_template,context,mail_subject)
                    

        return super(Vendor,self).save(*args,**kwargs)





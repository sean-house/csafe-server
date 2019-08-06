from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class Safe(models.Model):
    PROXIMITY_CHOICES = [
        ('M', 'Minutes'),
        ('H', 'Hours'),
        ('D', 'Days'),
        ('W', 'Weeks')
    ]
    hardware_id = models.CharField(max_length=64, primary_key=True)
    bolt_engaged = models.BooleanField(default=False)
    hinge_closed = models.BooleanField(default=False)
    lid_closed = models.BooleanField(default=False)
    safeholder = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                                   related_name='sh_safes')
    last_update = models.DateTimeField(verbose_name='Last update from safe')
    safe_public_key = models.TextField()
    auth_to_unlock = models.BooleanField(default=False, verbose_name='Authorised to unlock')
    unlock_time = models.DateTimeField(null=True, blank=True, verbose_name='Time to unlock')
    scanfreq = models.IntegerField(default=300, verbose_name='Scan Frequency in Seconds')
    reportfreq = models.IntegerField(default=1,
                                     verbose_name='Reporting Frequency (number of scan periods)')
    proximityunit = models.CharField(max_length=1, default='H', choices=PROXIMITY_CHOICES,
                                     verbose_name='Safe lights show proximity to unlock in:')
    displayproximity = models.BooleanField(default=True,
                                           verbose_name='Display proximity lights')
    keyholder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='kh_safes')
    keyholder_msg = models.TextField(blank=True,
                                     verbose_name='Message from Key holder')
    keyholder_msg_timestamp = models.DateTimeField(null=True, blank=True)
    seen_by_safeholder = models.DateTimeField(null=True, blank=True)
    safeholder_msg = models.TextField(blank=True,
                                      verbose_name='Message from safe holder')
    safeholder_msg_timestamp = models.DateTimeField(null=True, blank=True)
    relationship_active = models.BooleanField(default=True,
                                              verbose_name='Is the relationship active')
    safeholder_key = models.CharField(default='NONE', max_length=36, verbose_name="Safeholder's key")

    def __str__(self):
        if self.safeholder is None:
            sh = 'None'
        else:
            sh = self.safeholder.userattributes.displayname
        if all([self.bolt_engaged, self.hinge_closed, self.lid_closed]):
            st = 'SECURE'
        else:
            st = 'OPEN'
        return f" \nOwner = {sh}, Status = {st}, Safe id: {self.hardware_id},"

    def get_absolute_url(self):
        return reverse("safe:sh_detail", kwargs={'pk': self.pk})


class Relationship(models.Model):
    # Suspect this model is now redundant - to be removed once confirmed.
    keyholder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    safeholder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    keyholder_msg = models.TextField(blank=True)
    keyholder_msg_timestamp = models.DateTimeField(null=True, blank=True)
    seen_by_safeholder = models.DateTimeField(null=True, blank=True)
    safeholder_msg = models.TextField(blank=True)
    safeholder_msg_timestamp = models.DateTimeField(null=True, blank=True)
    relationship_active = models.BooleanField(default=True)

    def __str__(self):
        return 'Keyholder = {}, Safeholder = {}'.format(self.keyholder, self.safeholder)


class Safe_Event(models.Model):
    safe = models.ForeignKey(Safe, on_delete=models.CASCADE, related_name='events')
    event = models.CharField(max_length=20)
    timestamp = models.DateTimeField()

    def __str__(self):
        return 'Safe = {}, Event = {}'.format(self.safe, self.event)


class UserAttributes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayname = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

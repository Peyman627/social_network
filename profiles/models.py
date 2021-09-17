from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User,
                                verbose_name=_('user'),
                                on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=200, blank=True)
    picture = models.ImageField(_('picture'),
                                blank=True,
                                null=True,
                                upload_to='profiles/pictures')
    bio = models.TextField(_('bio'), blank=True)
    followers = models.ManyToManyField(User,
                                       verbose_name=_('followers'),
                                       related_name='followings')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'profile'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')


def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


post_save.connect(user_did_save, sender=User)

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User,
                                verbose_name=_('user'),
                                on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=200, blank=True)
    picture = models.ImageField(_('picture'),
                                blank=True,
                                null=True,
                                upload_to='users/profiles')
    bio = models.TextField(_('bio'), blank=True)
    followers = models.ManyToManyField(User,
                                       verbose_name=_('followers'),
                                       related_name='followings')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'profile'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

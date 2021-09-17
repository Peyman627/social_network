from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(User,
                               verbose_name=_('sender'),
                               related_name='sender_messages',
                               on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,
                                 verbose_name=_('receiver'),
                                 related_name='receiver_messages',
                                 on_delete=models.CASCADE)
    message = models.CharField(_('message'), max_length=400)
    is_read = models.BooleanField(_('is read'), default=False)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        db_table = 'message'
        verbose_name = _('message')
        verbose_name_plural = _('messages')

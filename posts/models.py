from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class PostQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)

    def feed(self, user):
        following_users_id = user.followings.values_list('user__id', flat=True)
        return self.filter(Q(user__id__in=following_users_id)
                           | Q(user=user)).distinct().order_by('-created_time')


class PostManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return PostQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)


class PostLike(models.Model):
    user = models.ForeignKey(User,
                             verbose_name=_('user'),
                             on_delete=models.CASCADE)
    post = models.ForeignKey('Post',
                             verbose_name=_('post'),
                             on_delete=models.CASCADE)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.post.content}'

    class Meta:
        db_table = 'post_like'
        verbose_name = _('post like')
        verbose_name_plural = _('post likes')
        unique_together = ('user', 'post')


class Post(models.Model):
    parent = models.ForeignKey('self',
                               verbose_name=_('parent'),
                               blank=True,
                               null=True,
                               on_delete=models.SET_NULL)
    user = models.ForeignKey(User,
                             verbose_name=_('user'),
                             related_name='posts',
                             on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,
                                   verbose_name=_('likes'),
                                   blank=True,
                                   related_name='liked_posts',
                                   through=PostLike)
    content = models.TextField(_('content'), blank=True)
    image = models.ImageField(_('image'),
                              upload_to='posts/images',
                              blank=True,
                              null=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)

    objects = PostManager()

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'post'
        verbose_name = _('post')
        verbose_name_plural = _('posts')

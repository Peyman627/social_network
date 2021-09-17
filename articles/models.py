from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Article(models.Model):
    user = models.ForeignKey(User,
                             verbose_name=_('user'),
                             on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=200, default='untitled')
    content = models.TextField(_('content'), blank=True)
    tags = models.ManyToManyField('ArticleTag',
                                  verbose_name=_('tags'),
                                  related_name='article_tags',
                                  blank=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'article'
        verbose_name = _('article')
        verbose_name_plural = _('articles')


class ArticleComment(models.Model):
    article = models.ForeignKey(Article,
                                verbose_name=_('article'),
                                on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             verbose_name=_('user'),
                             on_delete=models.CASCADE)
    content = models.TextField(_('content'), max_length=400)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.content}'

    class Meta:
        db_table = 'article_comment'
        verbose_name = _('article comment')
        verbose_name_plural = _('article comments')


class ArticleVote(models.Model):
    user = models.ForeignKey(User,
                             verbose_name=_('user'),
                             on_delete=models.CASCADE)
    article = models.ForeignKey(Article,
                                verbose_name=_('article'),
                                on_delete=models.CASCADE)
    value = models.IntegerField(_('value'), default=0)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)

    def __str__(self):
        return f'{self.article} - {self.value}'

    class Meta:
        db_table = 'article_vote'
        verbose_name = _('article vote')
        verbose_name_plural = _('article votes')


class ArticleImage(models.Model):
    name = models.CharField(_('name'), max_length=200, blank=True)
    article = models.ForeignKey(Article,
                                verbose_name=_('article'),
                                on_delete=models.CASCADE)
    image = models.ImageField(_('image'),
                              upload_to='articles/images',
                              blank=True,
                              null=True)

    def __str__(self):
        return f'{self.name} - {self.article}'

    class Meta:
        db_table = 'article_image'
        verbose_name = _('article image')
        verbose_name_plural = _('article images')


class ArticleTag(models.Model):
    name = models.CharField(_('name'), max_length=20, unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'article_tag'
        verbose_name = _('article tag')
        verbose_name_plural = _('article tags')

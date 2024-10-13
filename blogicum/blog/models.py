from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models
from django.db.models import Q

User = get_user_model()


class PublishedModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta():
        abstract = True


class Category (PublishedModel):
    title = models.CharField(
        'Заголовок',
        max_length=256,
    )

    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL; '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.',
    )

    class Meta():
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title


class Location (PublishedModel):
    name = models.CharField(
        'Название места',
        max_length=256,
    )

    class Meta():
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            Q(is_published=True)
            & Q(pub_date__lte=timezone.now())
            & Q(category__is_published=True))


class PublisheWithRelateddManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            Q(is_published=True)
            & Q(pub_date__lte=timezone.now())
            & Q(category__is_published=True)).select_related(
            'author',
            'location',
            'category'
        )


class Post(PublishedModel):
    objects = models.Manager()
    published = PublishedManager()
    published_with_related = PublisheWithRelateddManager()
    title = models.CharField(
        'Заголовок',
        max_length=256,
    )

    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
        'можно делать отложенные публикации.',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации',
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Местоположение',
        null=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Категория',
        null=True,
    )

    class Meta():
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['pub_date']

    def __str__(self) -> str:
        return self.title

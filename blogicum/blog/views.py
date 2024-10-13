from typing import Any
from django.http.response import Http404
from django.views.generic import ListView, DetailView
from .models import Post, Category
from django.http import Http404
from django.shortcuts import get_object_or_404

posts = [
    {
        'id': 0,
        'location': 'Остров отчаянья',
        'date': '30 сентября 1659 года',
        'category': 'travel',
        'text': '''Наш корабль, застигнутый в открытом море
                страшным штормом, потерпел крушение.
                Весь экипаж, кроме меня, утонул; я же,
                несчастный Робинзон Крузо, был выброшен
                полумёртвым на берег этого проклятого острова,
                который назвал островом Отчаяния.''',
    },
    {
        'id': 1,
        'location': 'Остров отчаянья',
        'date': '1 октября 1659 года',
        'category': 'not-my-day',
        'text': '''Проснувшись поутру, я увидел, что наш корабль сняло
                с мели приливом и пригнало гораздо ближе к берегу.
                Это подало мне надежду, что, когда ветер стихнет,
                мне удастся добраться до корабля и запастись едой и
                другими необходимыми вещами. Я немного приободрился,
                хотя печаль о погибших товарищах не покидала меня.
                Мне всё думалось, что, останься мы на корабле, мы
                непременно спаслись бы. Теперь из его обломков мы могли бы
                построить баркас, на котором и выбрались бы из этого
                гиблого места.''',
    },
    {
        'id': 2,
        'location': 'Остров отчаянья',
        'date': '25 октября 1659 года',
        'category': 'not-my-day',
        'text': '''Всю ночь и весь день шёл дождь и дул сильный
                порывистый ветер. 25 октября.  Корабль за ночь разбило
                в щепки; на том месте, где он стоял, торчат какие-то
                жалкие обломки,  да и те видны только во время отлива.
                Весь этот день я хлопотал  около вещей: укрывал и
                укутывал их, чтобы не испортились от дождя.''',
    },
]
posts_by_ids = {post['id']: post for post in posts}


class IndexView(ListView):
    posts_count = 5
    model = Post
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.published_with_related.all()[:self.posts_count]


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        category = self.object

        if not category.is_published:
            raise Http404("Нет опубликованных категорий с таким slug")

        posts = Post.published_with_related.filter(category=category)
        context['posts'] = posts

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        post = self.object

        post = get_object_or_404(Post.published_with_related, pk=post.pk)

        context['post'] = post

        return context

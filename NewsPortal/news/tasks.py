# импортируем декоратор из библиотеки
import datetime

from celery import shared_task

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Subscription
from django.conf import settings

from datetime import timezone


@shared_task
def info_after_new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.postCategory.all()
    title = post.title
    subscriber_emails = []

    for category in categories:
        subscriber_emails += list(Subscription.objects.filter(category=category).values_list('email', flat=True))

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': f'{post.title}',
            'link': f'{settings.SITE_URL}/post/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=set(subscriber_emails),
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task  # рассылка уведомлений на email подписчиков о созданных за последние 7 дней новостях подписанной категории
def weekly_send_email_task():
    today = datetime.datetime.now()  # определяем текущее время (в таблице время с часовым поясом. ошибка "наивное
    # время")
    last_week = today - datetime.timedelta(days=7)  # первоначальная точка отсчета для рассылки появившихся новостей
    posts = Post.objects.filter(dateCreation__gte=last_week)  # фильтруем созданные новости за период позднее (>=)
    # чем 7 дней назад. dateCreation из Post

    # все категории статей в виде списка (а не словаря тк flat=True)(по названию категории, а не по id)
    categories = set(posts.values_list('postCategory__name', flat=True))  # set множество для уникальности значений

    # все подписчики категорий (имя категорий совпадает с categories)  статей в виде списка email (а не словаря тк
    # flat=True)(по названию категории, а не по id СМ ВЫШЕ)
    subscribers = set(Subscription.objects.filter(category__name__in=categories).values_list('user__email', flat=True))

    html_content = render_to_string('news_post_mail.html',
                                    {'link': settings.SITE_URL,  # главная страница новостная
                                     'posts': posts})  # в цикле б проходиться и добавлять в шаблон
    msg = EmailMultiAlternatives(
        subject="Статьи за неделю",
        body='',  # пустой тк шаблон есть
        from_email=settings.DEFAULT_FROM_EMAIL,  # из settings
        to=subscribers)

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

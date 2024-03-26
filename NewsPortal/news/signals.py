from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def post_created(instance, sender, **kwargs):
    if kwargs['action'] == 'post_add':
        subscribers_emails = []

        for category in instance.postCategory.all():
            subscribers_emails += User.objects.filter(subscriptions__category=category).values_list('email', flat=True)

        subject = f'Новый пост в категории {instance.postCategory}'

        text_content = (
            f'Статья: {instance.title}\n'
            f'Автор: {instance.author.authorUser.username}\n\n'
            f'Ссылка : http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'Статья: {instance.title}<br>'
            f'Автор: {instance.author.authorUser.username}<br><br>'
            f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
            f'Ссылка </a>'
        )
        for email in subscribers_emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from .models import UserResponse, Post


def send_notifications(preview, pk, title, author):
    html_context = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/posts/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=author,
    )

    msg.attach_alternative('html_content', 'text/html')
    msg.send()


@receiver(m2m_changed, sender=Post)
def post_created(instance, sender, **kwargs):
    if kwargs['action'] == 'post':
        send_notifications.delay(instance.pk)

    emails = User.objects.filter(
        user=instance.author.all()
    ).values_list('email', flat=True)

    subject = f'Новый пост на нашем сайте {instance.user.all()}'

    text_content = (
        f'Новый пост: {instance.title}\n'
        f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Новый пост: {instance.title}<br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(pre_save, sender=UserResponse)
def handler(sender, instance, **kwargs):

    if instance.status:
        mail = instance.author.email
        send_mail(
            subject='',
            message=f' ваш отклик на {instance.post} принят',
            recipient_list=[mail],
            from_email=None,
            fail_silently=False,
        )
    else:
        mail = instance.post.author.email
        send_mail(
            subject='',
            message=f'На вашу публикацию {instance.post} пришёл отклик! от {instance.author}',
            recipient_list=[mail],
            from_email=None,
            fail_silently=False,
        )
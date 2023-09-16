from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import PostMedia,UserPost,PostComments

@receiver(post_save, sender = PostMedia)
def process_media(sender, instace, **kwargs):
    print("Hello")


@receiver(post_save, sender = UserPost)
def send_now_post_notification (sender,instance,**kwargs):
    print("going to ")

@receiver(post_save, sender = PostComments)
def profanity_filter(sender,instance,**kwargs):
    print("going to review comments")

@receiver(post_save, sender = PostComments)
def send_notification(sender, instance,**kwargs):
    print("dfsdfs")


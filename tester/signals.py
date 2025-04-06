
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Question, QuestionBank

@receiver(post_save, sender=Question)
def add_question_to_bank(sender, instance, created, **kwargs):
    if created:
        QuestionBank.objects.create(
            question_text=instance.question_text,
            img=instance.img,
            imginstr=instance.imginstr,
            A=instance.A,
            B=instance.B,
            C=instance.C,
            D=instance.D,
            correct_option=instance.correct_option,
            form=instance.form,
            subject=instance.subject
        )

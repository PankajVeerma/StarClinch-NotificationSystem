from django.db import models

class NotificationTrigger(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class NotificationTemplate(models.Model):

    class Channel(models.TextChoices):
        WHATSAPP = "WHATSAPP", "WhatsApp"
        EMAIL = "EMAIL", "Email"
        WEB_PUSH = "WEB_PUSH", "Web Push"

    trigger = models.ForeignKey(NotificationTrigger,on_delete=models.CASCADE,related_name="templates")
    channel = models.CharField( max_length=20,choices=Channel.choices)
    subject = models.CharField(max_length=255,blank=True)
    body = models.TextField()
    variables = models.JSONField(default=list,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["trigger", "channel"],
                name="unique_trigger_channel"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.trigger.name} - {self.channel}"
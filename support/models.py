from django.db import models
from accounts.models import User


# Create your models here.
class BugReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    bug_description = models.TextField(verbose_name="Bug description")
    is_resolved = models.BooleanField(default=False, verbose_name="Bug is resolved")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    class Meta:
        verbose_name = "Bug report"
        verbose_name_plural = "Bug reports"

    def __str__(self):
        return f"Bug from {self.user.username} -- {self.is_resolved}"


class SupportConversation(models.Model):
    conversation_name = models.CharField(
        max_length=350, verbose_name="Conversatoin name"
    )
    user_1 = models.ForeignKey(
        User,
        related_name="conversation_user_1",
        on_delete=models.CASCADE,
        verbose_name="User 1",
    )
    user_2 = models.ForeignKey(
        User,
        related_name="conversation_user_2",
        on_delete=models.CASCADE,
        verbose_name="User 2",
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    class Meta:
        verbose_name = "Support conversation"
        verbose_name_plural = "Support conversatoins"

    def __str__(self):
        return f"{self.conversation_name}"


class SupportConversationMessage(models.Model):
    conversation = models.ForeignKey(
        SupportConversation,
        on_delete=models.CASCADE,
        verbose_name="Related conversation",
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Message's sender"
    )
    message = models.TextField(verbose_name="Message")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    class Meta:
        verbose_name = "Support conversation message"
        verbose_name_plural = "Support conversation messages"

    def __str__(self):
        return f"New message from {self.sender.username} | {self.conversation.conversation_name}"


class SupportInquiry(models.Model):
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="related_client",
        verbose_name="Related client",
    )

    class Meta:
        verbose_name = "Support inquiry"
        verbose_name_plural = "Support inquires"

    def __str__(self):
        return f"Support inquiry for {self.client.username}"


class SupportInquiryMessage(models.Model):
    inquiry = models.ForeignKey(
        SupportInquiry,
        on_delete=models.CASCADE,
        related_name="related_support_inquiry",
        verbose_name="Related support inquiry",
        null=True,
    )
    message = models.TextField(verbose_name="Inquiry message")
    sent_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="related_account",
        verbose_name="Sent by",
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Support inquiry message"
        verbose_name_plural = "Support inquiry messages"

    def __str__(self):
        return f"Support inquiry message {self.id}"

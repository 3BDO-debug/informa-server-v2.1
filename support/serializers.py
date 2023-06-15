from rest_framework.serializers import ModelSerializer
from . import models
from clients.models import Client
from cloudinary import CloudinaryImage


class BugReportSerializer(ModelSerializer):
    class Meta:
        model = models.BugReport
        fields = "__all__"


class SupportConversationSerializer(ModelSerializer):
    class Meta:
        model = models.SupportConversation
        fields = "__all__"


class SupportConversationMessageSerializer(ModelSerializer):
    class Meta:
        model = models.SupportConversationMessage
        fields = "__all__"

    def to_representation(self, instance):
        data = super(SupportConversationMessageSerializer, self).to_representation(
            instance
        )

        if instance.sender.profile_pic:
            data["sent_by_profile_pic"] = CloudinaryImage(
                str(instance.sender.profile_pic)
            ).url

        return data


class SupportInquirySerializer(ModelSerializer):
    class Meta:
        model = models.SupportInquiry
        fields = "__all__"


class SupportInquiryMessageSerializer(ModelSerializer):
    class Meta:
        model = models.SupportInquiryMessage
        fields = "__all__"

    def to_representation(self, instance):
        data = super(SupportInquiryMessageSerializer, self).to_representation(instance)
        related_client = Client.objects.get(user=instance.inquiry.client)
        data["follow_up_package"] = related_client.follow_up_package
        data[
            "sent_by_fullname"
        ] = f"{instance.sent_by.first_name} {instance.sent_by.last_name}"
        data["client_id"] = instance.inquiry.client.id
        if instance.sent_by.profile_pic:
            data["sent_by_profile_pic"] = CloudinaryImage(
                str(instance.sent_by.profile_pic)
            ).url

        return data

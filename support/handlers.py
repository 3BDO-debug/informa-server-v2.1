import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q
from django.utils import timezone
from . import models, serializers
from accounts.models import User
from accounts.serializers import UserSerializer
from clients.models import Client, ClientFollowUp


class BugReportsHandler(APIView):
    def get(self, request):
        pass

    def post(self, request):
        bug_description = request.data.get("bugDescription")

        models.BugReport.objects.create(
            user=request.user, bug_description=bug_description, is_resolved=False
        ).save()

        return Response(status=status.HTTP_200_OK)


class ConversationHandler(APIView):
    def get(self, request):
        user_a = request.user
        user_b = User.objects.get(id=int(request.query_params.get("receiverId")))

        conversation = models.SupportConversation.objects.filter(
            Q(user_1=user_a, user_2=user_b) | Q(user_1=user_b, user_2=user_a)
        ).first()

        if conversation:
            conversation_serializer = serializers.SupportConversationSerializer(
                conversation, many=False
            )
        else:
            conversation_name = str(uuid.uuid4())
            conversation = models.SupportConversation.objects.create(
                conversation_name=conversation_name, user_1=user_a, user_2=user_b
            )  # Create conversation instance

            conversation_serializer = serializers.SupportConversationSerializer(
                conversation, many=False
            )

            conversation.save()

        return Response(status=status.HTTP_200_OK, data=conversation_serializer.data)

    def post(self, request):
        pass


class ConversationMessagesHandler(APIView):
    def get(self, request):
        conversation = models.SupportConversation.objects.get(
            conversation_name=request.query_params.get("conversationId")
        )

        conversation_messages = models.SupportConversationMessage.objects.filter(
            conversation=conversation
        )

        conversation_messages_serializer = (
            serializers.SupportConversationMessageSerializer(
                conversation_messages, many=True
            )
        )

        return Response(
            status=status.HTTP_200_OK, data=conversation_messages_serializer.data
        )

    def post(self, request):
        pass


@api_view(["GET"])
def contacts_handler(request):
    user = request.user
    user_role = user.role

    contacts_data = []

    if user_role == "client":
        """Find coaches related to client"""

        client = Client.objects.get(user=user)
        client_active_follow_up = ClientFollowUp.objects.get(
            client=client, is_active=True
        )

        customer_support_contacts = User.objects.filter(role="customer-support")

        contacts = [client_active_follow_up.coach]
        contacts.extend(customer_support_contacts)

        if client.follow_up_package in ["golden-package", "mega-package"]:
            informa_coach = User.objects.filter(role="informa180").first()
            contacts.append(informa_coach)

    else:
        contacts = User.objects.filter(role="client", is_active=True)

    for contact in contacts:
        conversation = models.SupportConversation.objects.filter(
            Q(user_1=user, user_2=contact) | Q(user_1=contact, user_2=user)
        ).first()

        last_message = models.SupportConversationMessage.objects.filter(
            conversation=conversation
        ).last()

        if last_message and conversation:
            last_message_serializer = serializers.SupportConversationMessageSerializer(
                last_message, many=False
            ).data
        else:
            last_message_serializer = None

        contacts_data.append(
            {
                "contact": UserSerializer(contact, many=False).data,
                "last_message": last_message_serializer,
            }
        )

    return Response(status=status.HTTP_200_OK, data=contacts_data)


@api_view(["GET"])
def support_inquires_handler(request):
    user = request.user

    if user.role != "client":
        un_read_inquires = []

        inquires = models.SupportInquiry.objects.all()
        for inquiry in inquires:
            inquiry_msgs = (
                models.SupportInquiryMessage.objects.filter(inquiry=inquiry)
                .exclude(sent_by=request.user)
                .last()
            )
            if inquiry_msgs:
                inquiry_msg_serializer = serializers.SupportInquiryMessageSerializer(
                    inquiry_msgs, many=False
                ).data
                un_read_inquires.append(inquiry_msg_serializer)

        return Response(status=status.HTTP_200_OK, data=un_read_inquires)

    return Response(status=status.HTTP_401_UNAUTHORIZED)


class SupportInquiryDetailsHandler(APIView):
    def get(self, request):
        client = models.User.objects.get(id=int(request.query_params.get("clientId")))
        client_inquiry = models.SupportInquiry.objects.filter(client=client)

        if client_inquiry.exists():
            inquires = models.SupportInquiryMessage.objects.filter(
                inquiry=client_inquiry.first()
            )
            inquires_serializer = serializers.SupportInquiryMessageSerializer(
                inquires, many=True
            ).data

        else:
            inquires_serializer = []

        return Response(status=status.HTTP_200_OK, data=inquires_serializer)

    def post(self, request):
        client = User.objects.get(id=int(request.data.get("clientId")))

        client_inquiry = models.SupportInquiry.objects.filter(client=client)

        if client_inquiry.exists():
            support_inquiry = client_inquiry.first()

        else:
            support_inquiry = models.SupportInquiry.objects.create(client=client)

        """ Create support inquiry message """

        models.SupportInquiryMessage.objects.create(
            inquiry=support_inquiry,
            message=request.data.get("message"),
            sent_by=request.user,
        ).save()

        """  Fetch updated inquires  """

        inquires = models.SupportInquiryMessage.objects.filter(inquiry=support_inquiry)
        inquires_serializer = serializers.SupportInquiryMessageSerializer(
            inquires, many=True
        )

        return Response(status=status.HTTP_200_OK, data=inquires_serializer.data)


@api_view(["GET"])
def check_inquires_limit(request):
    user = request.user
    client = Client.objects.get(user=user)

    current_month = timezone.now().month
    current_year = timezone.now().year

    client_inquires = models.SupportInquiryMessage.objects.filter(
        sent_by=user, created_at__year=current_year, created_at__month=current_month
    )

    can_send = True
    error_message = ""
    number_of_inquires_left = 0

    if client.follow_up_package == "silver-package":
        number_of_inquires_left = 4 - client_inquires.count()
        if client_inquires.count() >= 4:
            can_send = False
            error_message = "You have exceeded your limit for your silver follow-up which is 4 inquires per month, please upgrade your follow up package."
    elif client.follow_up_package == "golden-package":
        number_of_inquires_left = 8 - client_inquires.count()
        if client_inquires.count() >= 8:
            can_send = False
            error_message = "You have exceeded your limit for your golden follow-up which is 8 inquires per month, please upgrade your follow up package."

    return Response(
        status=status.HTTP_200_OK,
        data={
            "can_send": can_send,
            "error_message": error_message,
            "number_of_inquires_left": number_of_inquires_left,
        },
    )

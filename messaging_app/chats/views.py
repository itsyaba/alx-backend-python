#!/usr/bin/env python3
"""ViewSets for conversations and messages using Django REST Framework."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404

class ConversationViewSet(viewsets.ModelViewSet):
    """Allows listing and creating conversations."""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        conv = self.get_object()
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        conv.participants.add(user)
        return Response(ConversationSerializer(conv).data)

class MessageViewSet(viewsets.ModelViewSet):
    """Allows listing and creating messages within conversations."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        # Expect conversation id and sender id in request data
        conv_id = request.data.get('conversation_id')
        sender_id = request.data.get('sender_id')
        body = request.data.get('message_body')
        conversation = get_object_or_404(Conversation, pk=conv_id)
        sender = get_object_or_404(User, pk=sender_id)
        message = Message.objects.create(conversation=conversation, sender=sender, message_body=body)
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

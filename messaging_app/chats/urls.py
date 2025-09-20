from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Main router
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

# Nested router for messages inside conversations
conversation_router = nested_routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),
]

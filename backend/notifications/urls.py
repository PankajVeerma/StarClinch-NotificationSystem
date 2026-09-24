from django.urls import path




from .views import (
    NotificationTriggerListAPIView,
    NotificationTriggerCreateAPIView,
    NotificationTriggerDetailAPIView,
    NotificationTriggerUpdateAPIView,
    NotificationTriggerPatchAPIView,
    NotificationTriggerDeleteAPIView,

    NotificationTemplateListAPIView,
    NotificationTemplateCreateAPIView,
    NotificationTemplateDetailAPIView,
    NotificationTemplateUpdateAPIView,
    NotificationTemplatePatchAPIView,
    NotificationTemplateDeleteAPIView,
)


urlpatterns = [
    # ==========================
    # TRIGGER
    # ==========================

    path("triggers/",NotificationTriggerListAPIView.as_view(),name="trigger-list"),

    path("triggers/create/",NotificationTriggerCreateAPIView.as_view(),name="trigger-create"),

    path("triggers/<int:pk>/",NotificationTriggerDetailAPIView.as_view(),name="trigger-detail"),

    path("triggers/<int:pk>/update/",NotificationTriggerUpdateAPIView.as_view(),name="trigger-update"),

    path("triggers/<int:pk>/patch/",NotificationTriggerPatchAPIView.as_view(),name="trigger-patch"),

    path("triggers/<int:pk>/delete/",NotificationTriggerDeleteAPIView.as_view(),name="trigger-delete"),


    # ==========================
    # TEMPLATE
    # ==========================

    path("templates/",NotificationTemplateListAPIView.as_view(),name="template-list"),

    path("templates/create/",NotificationTemplateCreateAPIView.as_view(),name="template-create"),

    path("templates/<int:pk>/",NotificationTemplateDetailAPIView.as_view(),name="template-detail"),

    path( "templates/<int:pk>/update/", NotificationTemplateUpdateAPIView.as_view(), name="template-update"),

    path("templates/<int:pk>/patch/",NotificationTemplatePatchAPIView.as_view(),name="template-patch"),

    path("templates/<int:pk>/delete/",NotificationTemplateDeleteAPIView.as_view(),name="template-delete"),

]
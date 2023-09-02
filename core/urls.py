from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("edit/", views.edit, name="edit"),
    path("delete/<int:id>/", views.delete, name="delete"),
    path("gallery/", views.gallery, name="gallery"),
    path("bikes/", views.bikes, name="bikes"),
    path("bike_detail/<int:bike_id>/", views.bike_detail, name="bike_detail"),
    path("post_comment/<int:bike_id>/", views.post_comment, name="post_comment"),
    path("contact/", views.contact, name="contact"),
    # path("confirm/", views.confirm, name="confirm"),
    path("config/", views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('cancelled/', views.canceled), # new
    path('success/<str:session_id>', views.success),
    path('test/', views.test),
]
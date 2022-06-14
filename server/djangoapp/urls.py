from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # index
    path(route='', view=views.get_dealerships, name='index'),

    # about
    path(route='about/', view=views.about, name='about'),

    # contact us
    path(route='contact/', view=views.contact, name='contact'),

    # registration
    path(route='registration/', view=views.registration_request, name='registration'),

    # login
    path(route='login/', view=views.login_request, name='login'),

    # logout
    path(route='logout/', view=views.logout_request, name='logout'),

    # dealer-reviews
    path(route='dealer/<int:dealer_id>/', view=views.get_dealer_details, name='dealer_details'),

    # new review
    path(route='dealer/<int:dealer_id>/add-review/', view=views.add_review, name="add_review")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
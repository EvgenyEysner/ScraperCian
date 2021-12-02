from django.urls import path
from .views import IndexView, ApartmentDeleteView, ApartmentDetailView, ApartmentUpdateView, render_to_pdf, apartments_render_pdf_view

app_name = 'apartments'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('apartment/<int:pk>/delete', ApartmentDeleteView.as_view(), name='delete'),
    path('apartment/<int:pk>/details', ApartmentDetailView.as_view(), name='apartment'),
    path('apartment/<int:pk>/update', ApartmentUpdateView.as_view(), name='update'),
    path('apartment/<int:pk>/create_pdf', apartments_render_pdf_view, name='create_pdf'),
    path('pdf_view', render_to_pdf, name='pdf_view'),
    # path('pdf_download', DownloadPDF.as_view(), name="pdf_download"),
    ]
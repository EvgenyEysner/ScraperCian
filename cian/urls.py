from django.urls import path
from .views import IndexView, ApartmentDeleteView, ApartmentDetailView, ApartmentUpdateView, apartments_render_pdf_view
# DownloadPDF, ViewPDF

app_name = 'apartments'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('apartment/<int:pk>/delete', ApartmentDeleteView.as_view(), name='delete'),
    path('apartment/<int:pk>/details', ApartmentDetailView.as_view(), name='apartment'),
    path('apartment/<int:pk>/update', ApartmentUpdateView.as_view(), name='update'),
    path('apartment/<int:pk>/create_pdf', apartments_render_pdf_view, name='create_pdf'),
    # path('apartment/<int:pk>/view_pdf', ViewPDF, name='pdf_view'),
    # path('apartment/<int:pk>/download_pdf', DownloadPDF.as_view(), name="pdf_download"),
    ]
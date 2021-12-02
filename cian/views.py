from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import request, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, FormView, DeleteView, ListView, DetailView, TemplateView, CreateView
from .forms import UrlForm, ApartmentEditForm
from .models import Image, Apartment
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import os
import json


class IndexView(ListView, FormView):
    model = Apartment
    template_name = 'cian/index.html'
    success_url = reverse_lazy('apartments:home')
    context_object_name = 'apartments_list'
    form_class = UrlForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)

# class PdfIndexView(ListView, FormView):
#     model = Apartment
#     template_name = 'cian/report.html'
#     context_object_name = 'apartments'


class ApartmentDetailView(DetailView):
    model = Apartment
    template_name = 'cian/apartment.html'
    context_object_name = 'apartments'


class ApartmentDeleteView(DeleteView):
    model = Apartment
    templates = 'cian/apartment_confirm_delete.html'
    success_url = reverse_lazy('apartments:home')


class ApartmentUpdateView(UpdateView):
    model = Apartment
    form_class = ApartmentEditForm
    success_url = reverse_lazy('apartments:home')
    template_name = 'cian/apartment_update.html'


# def link_callback(uri, rel):
#     """
#     Convert HTML URIs to absolute system paths so xhtml2pdf can access those
#     resources
#     """
#     result = finders.find(uri)
#     if result:
#         if not isinstance(result, (list, tuple)):
#             result = [result]
#         result = list(os.path.realpath(path) for path in result)
#         path = result[0]
#     else:
#         sUrl = settings.STATIC_URL  # Typically /static/
#         sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
#         mUrl = settings.MEDIA_URL  # Typically /media/
#         mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/
#
#         if uri.startswith(mUrl):
#             path = os.path.join(mRoot, uri.replace(mUrl, ""))
#         elif uri.startswith(sUrl):
#             path = os.path.join(sRoot, uri.replace(sUrl, ""))
#         else:
#             return uri
#
#     # make sure that file exists
#     if not os.path.isfile(path):
#         raise Exception(
#             'media URI must start with %s or %s' % (sUrl, mUrl)
#         )
#     return path

def render_to_pdf(request):
    context = {}
    for apartment in Apartment.objects.all():
        context['apartment'] = apartment.address,
        context['floor'] = apartment.floor,
        context['price'] = apartment.price,
        context['desc'] = apartment.desc,
        context['rooms'] = apartment.address

    template_path = 'cian/report.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def apartments_render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    apartment = get_object_or_404(Apartment, pk=pk)
    # context = {}
    # for apartment in Apartment.objects.all():
    #     context['apartment'] = apartment.address,
    #     context['floor'] = apartment.floor,
    #     context['price'] = apartment.price,
    #     context['desc'] = apartment.desc,
    #     context['rooms'] = apartment.address

    template_path = 'cian/report.html'
    context = {'apartment': apartment}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    return HttpResponse('Works!')


# Opens up page as PDF
# class ViewPDF(View):
#
#
#     def get(self, request, *args, **kwargs):
#         pdf = render_to_pdf('cian/index.html')
#         return HttpResponse(pdf, content_type='application/pdf')
#
#
# # Automaticly downloads to PDF file
# class DownloadPDF(View):
#     def get(self, request, *args, **kwargs):
#         pdf = render_to_pdf('cian/apartment.html')
#
#         response = HttpResponse(pdf, content_type='application/pdf')
#         filename = "apartment_%s.pdf" % ("12341231")
#         content = "attachment; filename='%s'" % (filename)
#         response['Content-Disposition'] = content
#         return response

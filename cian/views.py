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
from reportlab.lib.pagesizes import A4
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


# def apartments_render_pdf_view(request, *args, **kwargs):
#     pk = kwargs.get('pk')
#     apartment = get_object_or_404(Apartment, pk=pk)
#     context = {'apartment': apartment}
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="report.pdf"'
#
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer, pagesize=A4)
#
#     p.setFont('Veranda', 15, leading=None)
#     p.setFillColorRGB(0.29296875, 0.453125, 0.609375)
#     p.drawString(260,800, 'cian/report.html')
#     p.line(0, 780, 1000, 780)
#     p.line(0, 778, 1000, 778)
#     x1 = 20
#     y1 = 750
#     for k, v in context.items():
#         p.setFont('Veranda', 15, leading=None)


def apartments_render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    apartment = get_object_or_404(Apartment, pk=pk)

    template_path = 'cian/report.html'
    context = {'apartment': apartment}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


#Opens up page as PDF
# class ViewPDF(View):
#
#     def get(self, request, *args, **kwargs):
#         pdf = apartments_render_pdf_view('cian/report.html')
#         return HttpResponse(pdf, content_type='application/pdf')
#
#
# # Automaticly downloads to PDF file
# class DownloadPDF(View):
#     def get(self, request, *args, **kwargs):
#         pdf = apartments_render_pdf_view('cian/report.html')
#
#         response = HttpResponse(pdf, content_type='application/pdf')
#         filename = "apartment_%s.pdf" % ("12341231")
#         content = "attachment; filename='%s'" % (filename)
#         response['Content-Disposition'] = content
#         return response

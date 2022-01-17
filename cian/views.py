import os
from io import BytesIO

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import (DeleteView, DetailView, FormView, ListView,
                                  UpdateView)
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa

from .forms import ApartmentEditForm, ImageForm, UrlForm
from .models import Apartment, Image, Profile


class IndexView(LoginRequiredMixin, ListView, FormView):
    model = Apartment
    template_name = 'cian/index.html'
    success_url = reverse_lazy('apartments:home')
    # context_object_name = 'apartments_list'
    form_class = UrlForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # добавляю в контекст только посты определенного пользователя
        context['apartments_list'] = Apartment.objects.filter(owner=self.request.user.id)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)


class ApartmentDetailView(LoginRequiredMixin, DetailView):
    model = Apartment
    template_name = 'cian/apartment.html'
    context_object_name = 'apartments'

    def get_context_data(self, *args, **kwargs):
        self.object_list = super().get_queryset()
        context = super().get_context_data(**kwargs)
        context['image'] = Image.objects.all()
        return context


class ApartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Apartment
    templates = 'cian/apartment_confirm_delete.html'
    success_url = reverse_lazy('apartments:home')


class ImageDeleteView(LoginRequiredMixin, DeleteView):
    model = Image
    templates = 'cian/image_confirm_delete.html'
    success_url = reverse_lazy('apartments:home')
    templates = 'cian/index.html'


class ApartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Apartment
    form_class = ApartmentEditForm
    success_url = reverse_lazy('apartments:home')
    template_name = 'cian/apartment_update.html'


class ImageUpdateView(LoginRequiredMixin, UpdateView):
    model = Image
    form_class = ImageForm
    success_url = reverse_lazy('apartments:home')
    template_name = 'cian/image_update.html'
    context_object_name = 'image'


def fetch_pdf_resources(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL  # Typically /static/
    sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL  # Typically /static/media/
    mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path

@login_required
def apartments_render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    apartment = get_object_or_404(Apartment, pk=pk)
    user = Profile.objects.get(user=request.user.id)

    template_path = 'cian/report.html'
    context = {
        'apartment': apartment,
        'user': user,
    }
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    result = BytesIO()
    # create a pdf
    pdf = pisa.pisaDocument(BytesIO(html.encode(
        'UTF-8')), result, encoding='UTF-8', link_callback=fetch_pdf_resources)
    # apartment.delete() # remove object after file creation
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    return None


# Opens up page as PDF
# class ViewPDF(View):
#
#     def get(self, request, *args, **kwargs):
#         pdf = apartments_render_pdf_view('cian/report_Alt.html')
#         return HttpResponse(pdf, content_type='application/pdf')
#
#
# # Automaticly downloads to PDF file
# class DownloadPDF(View):
#     def get(self, request, *args, **kwargs):
#         pdf = apartments_render_pdf_view('cian/report_Alt.html')
#
#         response = HttpResponse(pdf, content_type='application/pdf')
#         filename = "apartment_%s.pdf" % ("12341231")
#         content = "attachment; filename='%s'" % (filename)
#         response['Content-Disposition'] = content
#         return response

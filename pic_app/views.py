import requests
from django.conf import settings
from django.contrib import messages
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from requests import RequestException

from .forms import PictureForm, SizeForm
from .models import Picture

from urllib.parse import urlparse
from urllib3.packages.six import BytesIO
from PIL import Image, UnidentifiedImageError
import sanitize_filename

class IndexView(generic.ListView):
    template_name = 'pic_app/index.html'
    context_object_name = 'pictures_list'

    def get_queryset(self):
        return Picture.objects.all()


class DetailView(generic.DetailView):
    model = Picture
    template_name = 'pic_app/detail.html'


class UploadView(generic.CreateView):
    model = Picture
    form_class = PictureForm
    template_name = 'pic_app/upload.html'

    def form_valid(self, form):
        if form.cleaned_data.get('url_picture'):
            pic_url = form.data['url_picture']
            try:
                response = requests.get(pic_url, stream=True)
                response.raise_for_status()
            except RequestException:
                return redirect("pic_app:upload")
            try:
                img = Image.open(response.raw)
            except UnidentifiedImageError:
                return redirect("pic_app:upload")

            output_name = f"downloaded_0_{urlparse(pic_url).path.split('/')[-1]}"
            self.object = Picture()
            img_io = BytesIO()
            img.save(img_io, img.format)
            self.object.picture.save(output_name, ContentFile(img_io.getvalue()), save=False)
            self.object.save()
            return redirect(self.get_success_url())
        elif form.cleaned_data.get('picture'):
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('pic_app:edit_picture', kwargs={'pk': self.object.pk})


def edit_picture(request, pk):
    picture = get_object_or_404(Picture, pk=pk)

    if request.method != "POST":
        # could be added initial size of picture -> initial={'width': w, 'height': h})
        form = SizeForm()
    else:
        form = SizeForm(data=request.POST)
        input_picture = Image.open(picture.picture)
        _width, _height = input_picture.size
        old_size = (_width, _height)
        if form.is_valid():
            size = form.cleaned_data
            width = size['width']
            height = size['height']

            if width and height:
                new_size = (width, height)
            elif width:
                new_size = (width, _height)
            elif height:
                new_size = (_width, height)
            else:
                new_size = (_width, _height)

            input_picture.thumbnail(new_size, Image.ANTIALIAS)
            output_name = '/edited_' + picture.picture.name
            output_path = settings.MEDIA_ROOT + output_name
            input_picture.save(output_path)
            output_picture_url = settings.MEDIA_URL + output_name

            context = {'picture': picture, 'form': form,
                       'old_size': old_size, 'output_picture_url': output_picture_url}
            return render(request, 'pic_app/edit.html', context)

    context = {'picture': picture, 'form': form}
    return render(request, 'pic_app/edit.html', context)

import json
import os
import tempfile
from collections import defaultdict

import cv2
import xmltodict
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.

from rest_framework.generics import ListAPIView

from ASC.forms import ImageForm
import xml.etree.ElementTree as ET

from ASC.models import Image
from ASC.serializers import ImageSerializer


def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v)
                        for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d


def upload(request):
    if request.method == 'POST':
        image = ImageForm(request.POST, request.FILES)
        if image.is_valid():
            fs = image.save(commit=False)
            file = request.FILES['file']
            xfile = request.FILES['xfile']
            print(fs.file)
            print(fs.xfile)
            tup = tempfile.mkstemp()
            f = os.fdopen(tup[0], 'wb')
            f.write(file.read())
            f.close()
            filepath = tup[1]

            filename = filepath

            tup1 = tempfile.mkstemp()
            f = os.fdopen(tup1[0], 'wb')
            f.write(xfile.read())
            f.close()
            xfilepath = tup1[1]

            root = ET.parse(xfilepath)

            # print([elem.tag for elem in root.iter()])
            etdict = etree_to_dict(root.getroot())

            for i in etdict.values():
                res = dict((k, i[k]) for k in ['object'] if k in i)
                for k in res['object']:
                    xmin = int(k['bndbox'].get('xmin'))
                    xmax = int(k['bndbox'].get('xmax'))
                    ymin = int(k['bndbox'].get('ymin'))
                    ymax = int(k['bndbox'].get('ymin'))
                    start_point = (xmin, ymin)

                    # Ending coordinate, here (125, 80)
                    # represents the bottom right corner of rectangle
                    end_point = (xmax, ymax)

                    # Black color in BGR
                    color = (0, 0, 0)
                    window_name = 'Image'
                    # Reading an image in grayscale mode
                    image = cv2.imread(filename, 0)
                    # Line thickness of -1 px
                    # Thickness of -1 will fill the entire shape
                    thickness = -1
                    image = cv2.rectangle(image, start_point, end_point, color, thickness)
                    # Displaying the image
                    cv2.imshow(window_name, image)
                    # fs.save()
            messages.success(request, 'Image Successfully Uploaded.')

            return redirect('upload')
    else:
        form = ImageForm()
    return render(request, 'index.html', {'form': form})


class ImageViewSet(ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        global data
        file = request.data['file']
        # file = request.FILES['file']
        xfile = request.data['xfile']
        # xfile = request.FILES['xfile']
        tup = tempfile.mkstemp()
        f = os.fdopen(tup[0], 'wb')
        f.write(file.read())
        f.close()
        filepath = tup[1]
        filename = filepath

        tup1 = tempfile.mkstemp()
        f = os.fdopen(tup1[0], 'wb')
        f.write(xfile.read())
        f.close()
        xfilepath = tup1[1]

        root = ET.parse(xfilepath)

        # print([elem.tag for elem in root.iter()])
        etdict = etree_to_dict(root.getroot())

        for i in etdict.values():
            res = dict((k, i[k]) for k in ['object'] if k in i)
            for k in res['object']:
                xmin = int(k['bndbox'].get('xmin'))
                xmax = int(k['bndbox'].get('xmax'))
                ymin = int(k['bndbox'].get('ymin'))
                ymax = int(k['bndbox'].get('ymin'))
                start_point = (xmin, ymin)

                # Ending coordinate, here (125, 80)
                # represents the bottom right corner of rectangle
                end_point = (xmax, ymax)

                # Black color in BGR
                color = (0, 0, 0)
                window_name = 'Image'
                # Reading an image in grayscale mode
                image = cv2.imread(filename, 0)
                # Line thickness of -1 px
                # Thickness of -1 will fill the entire shape
                thickness = -1
                fgimage = cv2.rectangle(image, start_point, end_point, color, thickness)
                # Displaying the image
                # data = cv2.imshow(window_name, image)

        image = Image.objects.create(file=fgimage, xfile=xfile)
        return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)

from django.shortcuts import render
from django.db import models
from django.db.models import Q
from django.views import generic
from django.contrib.postgres.search import SearchVector, SearchQuery
from .models import Device, Genre, LendHistory,UniqueParameter
from .forms import SearchDeviceForm
from django.contrib.postgres import search
from django.shortcuts import get_object_or_404
from datetime import datetime
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator

# @login_required
def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_devices=Device.objects.all().count()
    # num_instances=BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=Device.objects.filter(status__exact='a').count()
    num_genre=Genre.objects.count()  # The 'all()' is implied by default.

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_Devices':num_devices,'num_devices_available':num_instances_available,'num_genre':num_genre},
    )
def device_list_view(request):
    queryset = Device.objects.all()
    genre = Genre.objects.get(name='all')
    only_ver_list = eval(genre.up.up_OSVersion)
    only_cpu_list = eval(genre.up.up_cpuModel)
    only_gpu_list = eval(genre.up.up_gpuModel)
    only_resolution_list = eval(genre.up.up_resolution)
    paginator = Paginator(queryset,50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
            request,
            "catalog/device_list_plt.html",
            {'device_list': page_obj, 
            "page_obj":page_obj,
            "is_paginated":True, 
            'only_ver_list': only_ver_list,
            'only_resolution_list': only_resolution_list, 
            'genre':genre,
            'only_cpu_list': only_cpu_list,
            'only_gpu_list': only_gpu_list}
            )

def device_list_view_plt(request,pk):
    if pk == "cn":
        plt = "国内安卓"
        queryset = Device.objects.filter(genre__name='国内安卓')
        genre = Genre.objects.get(name='国内安卓')
        only_ver_list = eval(genre.up.up_OSVersion)
        only_cpu_list = eval(genre.up.up_cpuModel)
        only_gpu_list = eval(genre.up.up_gpuModel)
        only_resolution_list = eval(genre.up.up_resolution)
    elif pk == "oversea":
        plt = "海外安卓"
        queryset = Device.objects.filter(genre__name='海外安卓')
        genre = Genre.objects.get(name='海外安卓')
        only_ver_list = eval(genre.up.up_OSVersion)
        only_cpu_list = eval(genre.up.up_cpuModel)
        only_gpu_list = eval(genre.up.up_gpuModel)
        only_resolution_list = eval(genre.up.up_resolution)
    elif pk == "iOS":
        plt = "iOS"
        queryset = Device.objects.filter(genre__name='iOS')
        genre = Genre.objects.get(name='iOS')
        only_ver_list = eval(genre.up.up_OSVersion)
        only_cpu_list = eval(genre.up.up_cpuModel)
        only_gpu_list = eval(genre.up.up_gpuModel)
        only_resolution_list = eval(genre.up.up_resolution)
    paginator = Paginator(queryset,50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
            request,
            "catalog/device_list_plt.html",
            {'device_list': page_obj, 
            "page_obj":page_obj,
            "is_paginated":True, 
            'only_ver_list': only_ver_list,
            'only_resolution_list': only_resolution_list, 
            'only_cpu_list': only_cpu_list, 
            'only_gpu_list': only_gpu_list,
            'plt':plt}
            )

class DeviceListViewOversea(generic.ListView):
    model = Device
    queryset = Device.objects.filter(genre__name='海外安卓')
    template_name = 'catalog/device_list_oversea.html'
    paginate_by = 50

class DeviceListViewIOS(generic.ListView):
    model = Device
    queryset = Device.objects.filter(genre__name='iOS')
    # queryset = Device.objects.annotate(search = SearchVector('deviceId',"status")).filter(search="1")
    template_name = 'catalog/device_list_ios.html'
    paginate_by = 50

class DeviceDetailView(generic.DetailView):
    model = Device
    paginate_by = 50

class GenreListView(generic.ListView):
    model = Genre
    paginate_by = 2

class GenreDetailView(generic.DetailView):
    model = Genre
    paginate_by = 50

class LendHistoryListView(generic.ListView):
    model = Genre
    paginate_by = 50

class LendHistoryDetailView(generic.DetailView):
    model = Genre
    paginate_by = 50

# @login_required
def search_device(request):
    query = request.GET.get("q")
    results = []
    if query:
        results= Device.objects.filter(Q(deviceId__icontains=query)|Q(brand__icontains=query)|Q(name__icontains=query)|Q(deviceModel__icontains=query)|Q(OSVersion__icontains=query)|Q(cpuBrand__icontains=query)|Q(cpuModel__icontains=query)|Q(cpuFrequency__icontains=query)|Q(cpuCoreNum__icontains=query)|Q(RAM__icontains=query)|Q(gpuBrand__icontains=query)|Q(gpuModel__icontains=query)|Q(resolution__icontains=query)|Q(screenType__icontains=query)|Q(size__icontains=query)|Q(ROM__icontains=query)|Q(wanmeiOffice__icontains=query)|Q(MACAddr__icontains=query)|Q(assetNumber__icontains=query)|Q(status__icontains=query)|Q(borrower__icontains=query))
    return render(request,"catalog/device_list_plt.html",{'device_list': results, 'query': query})

def device_detail(request,pk):
    device = Device.objects.get(deviceId=pk)
    only_ver_list = eval(device.genre.up.up_OSVersion)
    only_cpu_list = eval(device.genre.up.up_cpuModel)
    only_gpu_list = eval(device.genre.up.up_gpuModel)
    only_resolution_list = eval(device.genre.up.up_resolution)

    return render(request,"catalog/device_detail.html",
            {'device': device,
            'only_ver_list': only_ver_list,
            'only_resolution_list': only_resolution_list, 
            'only_cpu_list': only_cpu_list, 
            'only_gpu_list': only_gpu_list}
)

@login_required
def init_device_status(request,pk):
    platform = pk
    device_list = Device.objects.filter(genre__id=platform)
    genre = Genre.objects.get(id=platform)
    ver = set()
    cpu = set()
    gpu = set()
    res = set()
    if genre.name == "all":
        device_list = Device.objects.all()
        for device in device_list:
            only=False
            if Device.objects.filter(Q(OSVersion=device.OSVersion)&Q(status="可用")).count() == 1:
                if device.OSVersion not in ver:
                    ver.add(device.OSVersion)
                only = True
            if Device.objects.filter(Q(cpuModel=device.cpuModel)&Q(status="可用")).count() == 1:
                if device.cpuModel not in cpu:
                    cpu.add(device.cpuModel)
                only = True
            if Device.objects.filter(Q(gpuModel=device.gpuModel)&Q(status="可用")).count() == 1:
                if device.gpuModel not in gpu:
                    gpu.add(device.gpuModel)
                only = True
            if Device.objects.filter(Q(resolution=device.resolution)&Q(status="可用")).count() == 1:
                if device.resolution not in res:
                    res.add(device.resolution)
                only = True
            if device.status == "可用":
                if only and not device.onlyOne:
                    device.onlyOne = True
                    device.save()
                elif not only and device.onlyOne:
                    device.onlyOne = False
                    device.save()
            else:
                device.onlyOne = False
                device.save()
        if genre.up:
            genre.up.up_OSVersion = str(list(ver))
            genre.up.up_cpuModel = str(list(cpu))
            genre.up.up_gpuModel = str(list(gpu))
            genre.up.up_resolution = str(list(res))
            genre.up.save()
        else:
            genre.up = UniqueParameter.create(ver,cpu,gpu,res)
            genre.up.save()
        genre.save()

    else:
        for device in device_list:
            only=False
            if Device.objects.filter(Q(genre__id=platform)&Q(OSVersion=device.OSVersion)&Q(status="可用")).count() == 1:
                if device.OSVersion not in ver:
                    ver.add(device.OSVersion)
                only = True
            if Device.objects.filter(Q(genre__id=platform)&Q(cpuModel=device.cpuModel)&Q(status="可用")).count() == 1:
                if device.cpuModel not in cpu:
                    cpu.add(device.cpuModel)
                only = True
            if Device.objects.filter(Q(genre__id=platform)&Q(gpuModel=device.gpuModel)&Q(status="可用")).count() == 1:
                if device.gpuModel not in gpu:
                    gpu.add(device.gpuModel)
                only = True
            if Device.objects.filter(Q(genre__id=platform)&Q(resolution=device.resolution)&Q(status="可用")).count() == 1:
                if device.resolution not in res:
                    res.add(device.resolution)
                only = True
            if device.status == "可用":
                if only and not device.onlyOne:
                    device.onlyOne = True
                    device.save()
                elif not only and device.onlyOne:
                    device.onlyOne = False
                    device.save()
            else:
                device.onlyOne = False
                device.save()
            
        if genre.up:
            genre.up.up_OSVersion = str(list(ver))
            genre.up.up_cpuModel = str(list(cpu))
            genre.up.up_gpuModel = str(list(gpu))
            genre.up.up_resolution = str(list(res))
            genre.up.save()
        else:
            genre.up = UniqueParameter.create(ver,cpu,gpu,res)
            genre.up.save()
        genre.save()
    return render(request,"catalog/refresh.html",{"ver":ver,"cpu":cpu,"gpu":gpu,"res":res})

@login_required
def borrow_device(request):
    actor = request.user.username
    id = request.POST.get("deviceid")
    stat = request.POST.get("status")
    borrower = request.POST.get("borrower")
    backdate = request.POST.get("backdate")
    act = request.POST.get("act")
    device = Device.objects.get(deviceId=id)
    result = "FAILD"
    if device.status == "可用":
        if act == "借用":
            device.borrower =borrower
            device.status = stat
            device.dueBackTime = backdate
            lh = LendHistory().create(borrower,act,datetime.now(),device,actor,id=uuid.uuid1())
            lh.save()
            device.save()
            result = "SUCCEED"
    elif device.status == "借出":
        if act == "归还":
            device.borrower =None
            device.status = stat
            device.dueBackTime = None
            lh = LendHistory().create(borrower,act,datetime.now(),device,actor,id=uuid.uuid1())
            lh.save()
            device.save()
            result = "SUCCEED"

    return render(request,"catalog/borrow_result.html",{'result': result,"addr":device.get_absolute_url()})

@login_required
def lend_history(request,pk):
    device = Device.objects.get(deviceId=pk)
    result = LendHistory.objects.filter(device=device).order_by("-actTime")

    return render(request,"catalog/lend_history.html",{'result': result})

@login_required
def logout_view(request):
    logout(request)
    return render(request,"catalog/logged_out.html")

    # Redirect to a success page.
# Create your views here.


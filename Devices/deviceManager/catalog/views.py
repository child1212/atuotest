from django.shortcuts import render
from django.db import models
from django.db.models import Q
from django.views import generic
from django.shortcuts import get_object_or_404
from .models import Device, Genre, LendHistory,UniqueParameter
from datetime import datetime
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator
from .forms import BorrowDeviceForm

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
    form = BorrowDeviceForm()
    return render(request,"catalog/device_detail.html",{'device': device,'form': form})

def devices_filter(request):
    brand = set()
    deviceModel = set()
    OSVersion = set()
    cpuBrand = set()
    cpuModel = set()
    cpuCoreNum = set()
    RAM = set()
    gpuBrand = set()
    gpuModel = set()
    resolution = set()
    ROM = set()
    status = set()
    borrower = set()
    devices = Device.objects.all()
    for device in devices:
        brand.add(device.brand)
        deviceModel.add(device.deviceModel)
        OSVersion.add(device.OSVersion)
        cpuBrand.add(device.cpuBrand)
        cpuModel.add(device.cpuModel)
        cpuCoreNum.add(device.cpuCoreNum)
        RAM.add(device.RAM)
        gpuBrand.add(device.gpuBrand)
        gpuModel.add(device.gpuModel)
        resolution.add(device.resolution)
        ROM.add(device.ROM)
        status.add(device.status)
        borrower.add(device.borrower)
    return render(request,"catalog/device_filter.html",{
    "brand":brand,
    "deviceModel":deviceModel,
    "OSVersion":OSVersion,
    "cpuBrand":cpuBrand,
    "cpuModel":cpuModel,
    "cpuCoreNum":cpuCoreNum,
    "RAM":RAM,
    "gpuBrand":gpuBrand,
    "gpuModel":gpuModel,
    "resolution":resolution,
    "ROM":ROM,
    "status":status,
    "borrower":borrower
          })

def filter_result(request):
    brand = request.GET.get("brand")
    deviceModel = request.GET.get("deviceModel")
    OSVersion = request.GET.get("OSVersion")
    cpuBrand = request.GET.get("cpuBrand")
    cpuModel = request.GET.get("cpuModel")
    cpuCoreNum = request.GET.get("cpuCoreNum")
    RAM = request.GET.get("RAM")
    gpuBrand = request.GET.get("gpuBrand")
    gpuModel = request.GET.get("gpuModel")
    resolution = request.GET.get("resolution")
    ROM = request.GET.get("ROM")
    status = request.GET.get("status")
    borrower = request.GET.get("borrower")
    kwargs = {}
    if brand != "all":
        kwargs["brand"] = brand
    if deviceModel != "all":
        kwargs["deviceModel"] = deviceModel
    if OSVersion != "all":
        kwargs["OSVersion"] = OSVersion
    if cpuBrand != "all":
        kwargs["cpuBrand"] = cpuBrand
    if cpuModel != "all":
        kwargs["cpuModel"] = cpuModel
    if cpuCoreNum != "all":
        kwargs["cpuCoreNum"] = cpuCoreNum
    if RAM != "all":
        kwargs["RAM"] = RAM
    if gpuBrand != "all" and gpuBrand is not None:
        kwargs["gpuBrand"] = gpuBrand
    if gpuModel != "all":
        kwargs["gpuModel"] = gpuModel
    if resolution != "all":
        kwargs["resolution"] = resolution
    if ROM != "all":
        kwargs["ROM"] = ROM
    if status != "all":
        kwargs["status"] = status
    if borrower != "all":
        kwargs["borrower"] = borrower
    device_list = Device.objects.filter(**kwargs)
    return render(request,"catalog/device_list_plt.html",{'device_list': device_list})

@login_required
def device_status(request,pk):
    genres = Genre.objects.all()
    for genre in genres:
        device_list = Device.objects.filter(genre__id=genre.id)
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
                if Device.objects.filter(Q(genre__id=genre.id)&Q(OSVersion=device.OSVersion)&Q(status="可用")).count() == 1:
                    if device.OSVersion not in ver:
                        ver.add(device.OSVersion)
                    only = True
                if Device.objects.filter(Q(genre__id=genre.id)&Q(cpuModel=device.cpuModel)&Q(status="可用")).count() == 1:
                    if device.cpuModel not in cpu:
                        cpu.add(device.cpuModel)
                    only = True
                if Device.objects.filter(Q(genre__id=genre.id)&Q(gpuModel=device.gpuModel)&Q(status="可用")).count() == 1:
                    if device.gpuModel not in gpu:
                        gpu.add(device.gpuModel)
                    only = True
                if Device.objects.filter(Q(genre__id=genre.id)&Q(resolution=device.resolution)&Q(status="可用")).count() == 1:
                    if device.resolution not in res:
                        res.add(device.resolution)
                    only = True
                if device.status == "可用" and genre.name == "国内安卓":
                    if only and not device.onlyOne_cn:
                        device.onlyOne_cn = True
                        device.save()
                    elif not only and device.onlyOne_cn:
                        device.onlyOne_cn = False
                        device.save()
                elif device.status == "可用" and genre.name == "海外安卓":
                    if only and not device.onlyOne_oversea:
                        device.onlyOne_oversea = True
                        device.save()
                    elif not only and device.onlyOne_oversea:
                        device.onlyOne_oversea = False
                        device.save()  
                elif device.status == "可用" and genre.name == "iOS":
                    if only and not device.onlyOne_iOS:
                        device.onlyOne_iOS = True
                        device.save()
                    elif not only and device.onlyOne_iOS:
                        device.onlyOne_iOS = False
                        device.save()   
                else:
                    device.onlyOne_cn = False
                    device.onlyOne_oversea = False
                    device.onlyOne_iOS = False
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
    return render(request,"catalog/refresh.html",{"genres":genres})

@login_required
def due_back(request):
    now = datetime.now()
    device_list = Device.objects.filter(Q(dueBackTime__isnull=False)&Q(dueBackTime__lt=now))
    # Q(dueBackTime__isnull=False)&Q(dueBackTime__lt=now)
    return render(request,"catalog/device_list_plt.html",{'device_list': device_list})


@login_required
def borrow_device(request,pk):
    actor = request.user.username
    stat = request.POST.get("status")
    borrower = request.POST.get("borrower")
    backdate = request.POST.get("backdate")
    currenttime = datetime.now()
    act = request.POST.get("act")
    device = Device.objects.get(deviceId=pk)
    result = "FAILD"
    if backdate:
        backdate_compare = datetime.strptime(backdate, "%Y-%m-%d")
        if currenttime > backdate_compare:
            return render(request,"catalog/borrow_result.html",{'result': result,"addr":device.get_absolute_url(),"reason":"归还时间错误，请检查"})
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

    return render(request,"catalog/borrow_result.html",{'result': result,"addr":device.get_absolute_url(),"backdate":backdate,"currenttime":currenttime})

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


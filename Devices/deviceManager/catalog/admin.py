from django.contrib import admin
from .models import Genre, Device, LendHistory, UniqueParameter


# admin.site.register(Genre)

# admin.site.register(Device)


class DeviceInline(admin.TabularInline):
    model = Device

class GenreAdmin(admin.ModelAdmin):
    # list_display=('name','test')
    inlines = [DeviceInline]
admin.site.register(Genre,GenreAdmin)


class LendHistoryInline(admin.TabularInline):
    model=LendHistory


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('deviceId','brand','OSVersion','RAM','ROM','status',"genre","onlyOne")
    list_filter=('OSVersion','genre')
    fields = [('deviceId','brand','name'),
              ('deviceModel','OSVersion'),
              ('cpuBrand',"cpuModel",'cpuFrequency','cpuCoreNum'),
              ('RAM','resolution','screenType','size','ROM','wanmeiOffice'),
              ('MACAddr','assetNumber'),
              ('gpuBrand','gpuModel'),
              ('status','borrower'),
              'genre']
    inlines = [LendHistoryInline]

@admin.register(LendHistory)
class LendHistoryAdmin(admin.ModelAdmin):
    list_display = ('device','borrower','action','actTime')

@admin.register(UniqueParameter)
class UniqueParameterAdmin(admin.ModelAdmin):
    list_display = ('up_OSVersion','up_cpuModel','up_gpuModel','up_resolution')

# Register your models here.

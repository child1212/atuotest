from django.db import models
from django.urls import reverse
import uuid

class Genre(models.Model):
    '''
    Model representing a device genre(e.g. android_cn,android_oversea,iOS etc.)
    '''

    localiztion = (
        ('国内安卓', '国内安卓'),
        ('海外安卓', '海外安卓'),
        ('iOS', 'iOS'),
        ('all', 'all')

    )

    # name = models.CharField(max_length=200, help_text="设备平台")
    name = models.CharField(max_length=20,choices=localiztion, help_text="Enter a book genre (e.g. android_cn,android_oversea,iOS etc.)")

    test = models.CharField(max_length=200, help_text="test, no use",null=True,blank=True)

    up = models.OneToOneField("UniqueParameter",help_text="唯一参数",on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        '''
        return the url to access a particular device instance
        '''
        return reverse("genre-detail",args=[str(self.id)])
    
class Device(models.Model):
    '''
    Devices id
    
    '''
    deviceId = models.CharField(max_length=99,help_text="设备编号",primary_key=True)

    brand = models.CharField(max_length=99,help_text="设备品牌",null=True,blank=True)

    name = models.CharField(max_length=99,help_text="设备名称",null=True,blank=True)

    deviceModel = models.CharField(max_length=99,help_text="设备型号",null=True,blank=True)

    OSVersion = models.CharField(max_length=99,help_text="当前版本",null=True,blank=True)

    cpuBrand = models.CharField(max_length=99,help_text="cpu品牌",null=True,blank=True)

    cpuModel = models.CharField(max_length=99,help_text="cpu型号",null=True,blank=True)

    cpuFrequency = models.CharField(max_length=99,help_text="cpu频率",null=True,blank=True)

    cpuCoreNum = models.CharField(max_length=99,help_text="cpu核心数",null=True,blank=True)

    RAM = models.CharField(max_length=99,help_text="RAM")

    gpuBrand = models.CharField(max_length=99,help_text="GPU品牌",null=True,blank=True)

    gpuModel = models.CharField(max_length=99,help_text="GPU型号",null=True,blank=True)

    resolution = models.CharField(max_length=99,help_text="分辨率")

    screenType = models.CharField(max_length=99,help_text="屏幕类型")

    size = models.CharField(max_length=99,help_text="尺寸")
    
    ROM = models.CharField(max_length=99,help_text="ROM")

    wanmeiOffice = models.CharField(max_length=99,help_text="wanmei-office开通状态",null=True,blank=True)

    MACAddr = models.CharField(max_length=99,help_text="MAC地址",null=True,blank=True)

    assetNumber = models.CharField(max_length=99,help_text="资产编号",null=True,blank=True)

    onlyOne_cn = models.BooleanField(default=False,help_text="国内唯一设备？")

    onlyOne_oversea = models.BooleanField(default=False,help_text="海外唯一设备？")

    onlyOne_iOS = models.BooleanField(default=False,help_text="iOS唯一设备？")

    LOAN_STATUS = (
        ('不可用', '不可用'),
        ('借出', '借出'),
        ('可用', '可用')
    )

    status = models.CharField(max_length=10,choices=LOAN_STATUS,blank=True,default='不可用',help_text="设备状态")

    borrower = models.CharField(max_length=10,help_text="借用人",null=True,blank=True)

    dueBackTime = models.DateField(null=True, blank=True,help_text="预计归还")

    genre = models.ManyToManyField('Genre',help_text="设备分类")

    # instance = models.ManyToManyField("DeviceInstance",help_text='借用记录')
    class Meta:
        ordering = ["deviceId"]

    def __str__(self):
        return self.deviceId
    
    def get_absolute_url(self):
        '''
        return the url to access a particular device instance
        '''
        return reverse("device-detail",args=[str(self.deviceId)])

    # def display_genre(self):
    #     """
    #     Creates a string for the Genre. This is required to display genre in Admin.
    #     """
    #     return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    # display_genre.short_description = 'Genre'

class LendHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, help_text="操作id")
    borrower = models.CharField(max_length=40,help_text="借用人")
    ACT = (
        ('借用', '借用'),
        ('归还', '归还')
    )
    action = models.CharField(max_length=10,choices=ACT,help_text="操作类型")
    actTime = models.DateTimeField(null=True, blank=True,help_text="操作时间")
    device = models.ForeignKey("Device",help_text="设备id",on_delete=models.SET_NULL,null=True)
    actor = models.CharField(max_length=10,choices=ACT,help_text="操作员")

    @classmethod
    def create(cls,borrower,action,actTime,device,actor,id=uuid.uuid1()):
        lh = cls(id=id,borrower=borrower,action=action,actTime=actTime,actor=actor,device=device)
        lh.save()
        return lh
    
class UniqueParameter(models.Model):
    up_OSVersion = models.TextField(help_text="唯一的系统版本",default="[]",null=True,blank=True)
    up_cpuModel = models.TextField(help_text="唯一的cpu型号",default="[]",null=True,blank=True)
    up_gpuModel = models.TextField(help_text="唯一的gpu型号",default="[]",null=True,blank=True)
    up_resolution = models.TextField(help_text="唯一的分辨率",default="[]",null=True,blank=True)

    @classmethod
    def create(cls,OSVersion,cpuModel,gpuModel,resolution):
        up = cls(up_OSVersion=OSVersion,up_cpuModel=cpuModel,up_gpuModel=gpuModel,up_resolution=resolution)
        up.save()
        return up



# Create your models here.

from import_export import resources
from .models import Device
from import_export.fields import Field

class DeviceResource(resources.ModelResource):
    deviceId= Field(attribute="deviceId",column_name="设备编号")
    brand= Field(attribute="brand",column_name="设备品牌")
    name= Field(attribute="name",column_name="设备名称")
    deviceModel= Field(attribute="deviceModel",column_name="设备型号")
    OSVersion= Field(attribute="OSVersion",column_name="当前版本")
    cpuBrand= Field(attribute="cpuBrand",column_name="cpu品牌")
    cpuModel= Field(attribute="cpuModel",column_name="cpu型号")
    cpuFrequency= Field(attribute="cpuFrequency",column_name="cpu频率")
    cpuCoreNum= Field(attribute="cpuCoreNum",column_name="cpu核心数")
    RAM= Field(attribute="RAM",column_name="RAM")
    gpuBrand= Field(attribute="gpuBrand",column_name="GPU品牌")
    gpuModel= Field(attribute="gpuModel",column_name="GPU型号")
    resolution= Field(attribute="resolution",column_name="分辨率")
    screenType= Field(attribute="screenType",column_name="屏幕类型")
    size= Field(attribute="size",column_name="尺寸")
    ROM= Field(attribute="ROM",column_name="ROM")
    wanmeiOffice= Field(attribute="wanmeiOffice",column_name="wanmei-office开通状态")
    MACAddr= Field(attribute="MACAddr",column_name="MAC地址")
    assetNumber= Field(attribute="assetNumber",column_name="资产编号")
    status= Field(attribute="status",column_name="设备状态")
    borrower= Field(attribute="borrower",column_name="借用人")
    dueBackTime= Field(attribute="dueBackTime",column_name="预计归还")
    # genre= Field(attribute="genre",column_name="设备分类")
    class Meta:
        model = Device
        exclude = ['id']
        import_id_fields = ['deviceId']
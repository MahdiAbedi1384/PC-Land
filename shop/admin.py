from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import (
    PCIGenerationTypes,
    RAMTypesSupported,
    GraphicsCardFeatures,
    RAIDTypesSupported,
    OperationSystemsSupported,
    Colors,
    LapTopRAMModel,
    ComputerRAMModel,
    CPUModel,
    GraphicsCard,
    ComputerCase,
    MotherBoard,
    BluetoothDongle,
    USBHUB,
    SSD,
    M2SSD,
    ExternalHardDrive,
    ExternalSSD,
    FlashDrive,
    Keyboard,
    Mouse,
    Monitor,
    InternalHDD,
    PreBuiltPC,
    AllInOnePC,
    Laptop,
    Images,
    NewsLetter,
    Favorite,
    Comment,
    Rating,
)

from .filters import (
    all_in_on_pcs_filters,
    bluetooth_dongle_filters,
    case_filters,
    common_filters,
    CPU_filters,
    external_hard_external_ssd_drive_filters,
    flash_drive_filters,
    graphics_card_filters,
    internal_HDD_filters,
    keyboard_filters,
    laptops_filters,
    monitor_filters,
    motherboard_filters,
    mouse_filters,
    pre_built_pcs_filters,
    RAM_filters,
    SSD_filters,
    usb_hub_filters,
)


class InLineImages(GenericTabularInline):
    extra = 0
    model = Images


class BaseAdmin(admin.ModelAdmin):
    list_display_links = ("id",)
    list_per_page = 20


class BasicAdminModels(BaseAdmin):
    pass


class AdvancedAdminModels(BaseAdmin):
    inlines = [
        InLineImages,
    ]
    list_editable = (
        "is_active",
        "price",
        "sku",
    )
    list_filter = [common_filters.PriceFilter, common_filters.SKUFilter, "is_active"]
    prepopulated_fields = {"slug": ("name", "brand", "model")}


@admin.register(PCIGenerationTypes)
class PCIGenerationTypesAdmin(BasicAdminModels):
    model = PCIGenerationTypes
    list_display = (
        "id",
        "title",
    )
    search_fields = ("title",)


@admin.register(RAMTypesSupported)
class RAMTypesSupportedAdmin(BasicAdminModels):
    model = RAMTypesSupported
    list_display = (
        "id",
        "title",
    )
    search_fields = ("title",)


@admin.register(GraphicsCardFeatures)
class GraphicsCardFeaturesAdmin(BasicAdminModels):
    model = GraphicsCardFeatures
    list_display = (
        "id",
        "title",
    )
    search_fields = ("title",)


@admin.register(RAIDTypesSupported)
class RAIDTypesSupportedAdmin(BasicAdminModels):
    model = RAIDTypesSupported
    list_display = (
        "id",
        "title",
    )
    search_fields = ("title",)


@admin.register(OperationSystemsSupported)
class OperationSystemsSupportedAdmin(BasicAdminModels):
    model = OperationSystemsSupported
    list_display = (
        "id",
        "title",
    )
    search_fields = ("title",)


@admin.register(Colors)
class ColorsAdmin(BasicAdminModels):
    model = Colors
    list_display = (
        "id",
        "title",
    )
    search_fields = ("title",)


@admin.register(LapTopRAMModel)
class LapTopRAMModelAdmin(AdvancedAdminModels):
    model = LapTopRAMModel
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "memory_type",
        "memory_size",
        "frequency",
        "weight",
        "price",
        "sku",
        "is_active",
    )
    search_fields = (
        "name",
        "brand",
        "model",
        "memory_type",
        "memory_size",
        "frequency",
    )
    list_filter = AdvancedAdminModels.list_filter + [
        RAM_filters.RAMFrequencyFilter,
        RAM_filters.RAMMemorySizeFilter,
        RAM_filters.RAMMemoryTypeFilter,
    ]


@admin.register(ComputerRAMModel)
class ComputerRAMModelAdmin(LapTopRAMModelAdmin):
    pass


@admin.register(CPUModel)
class CPUModelAdmin(AdvancedAdminModels):
    model = CPUModel
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "cpu_series",
        "cpu_generation",
        "released_date",
        "cpu_architecture_type",
        "cores",
        "threads",
        "boosted_frequency",
        "max_power_usage",
        "has_igpu",
        "igpu_model",
        "sku",
        "price",
        "is_active",
    )
    search_fields = ("name", "brand", "model", "cpu_series")
    filter_horizontal = [
        "pci_express_generation_supports_version",
        "ram_types_supported",
    ]
    list_filter = AdvancedAdminModels.list_filter + [
        CPU_filters.CpuGenerationFilter,
        CPU_filters.CPUCoresFilter,
        CPU_filters.CPUThreadsFilter,
        CPU_filters.CPUBrandFilter,
        CPU_filters.CpuArchitectureTypeFilter,
        CPU_filters.CPUBaseFrequencyFilter,
    ]


@admin.register(GraphicsCard)
class GraphicsCardAdmin(AdvancedAdminModels):
    model = GraphicsCard
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "interface",
        "openGL_version",
        "directx_version",
        "VRAM",
        "VRAM_type",
        "resolution",
        "required_installation_space",
        "min_power_supply_required",
        "price",
        "sku",
        "is_active",
    )
    search_fields = (
        "name",
        "brand",
        "model",
        "interface",
        "openGL_version",
        "directx_version",
        "VRAM",
        "VRAM_type",
        "resolution",
    )
    filter_horizontal = [
        "graphics_card_features",
    ]
    list_filter = AdvancedAdminModels.list_filter + [
        graphics_card_filters.GraphicsCardVRAMFilter,
        graphics_card_filters.GraphicsCardInterfaceFilter,
        graphics_card_filters.GraphicsCardChipManufacturerFilter,
        graphics_card_filters.GraphicsCardVRAMTypeFilter,
        graphics_card_filters.GraphicsCardMinPowerSupplyFilter,
        graphics_card_filters.GraphicsCardFansCountFilter,
    ]


@admin.register(ComputerCase)
class ComputerCaseAdmin(AdvancedAdminModels):
    model = ComputerCase
    list_display = ("id", "name", "brand", "model", "size", "sku", "price", "is_active")
    search_fields = ("name", "brand", "model", "size")
    filter_horizontal = [
        "motherboards_compatibility",
    ]
    list_filter = AdvancedAdminModels.list_filter + [
        case_filters.CaseSizeFilter,
        case_filters.CaseMaterialFilter,
        case_filters.CaseDriveBayFilter,
        case_filters.CaseFormFactorFilter,
        case_filters.CaseExpansionSlotsFilter,
        case_filters.CaseFrontPanelUSBFilter,
        case_filters.MaxCPUCoolerHeightFilter,
        case_filters.MaxGPUCardLengthFilter,
    ]


@admin.register(MotherBoard)
class MotherBoardAdmin(AdvancedAdminModels):
    model = MotherBoard
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "chipset",
        "price",
        "sku",
        "is_active",
    )
    search_fields = ("name", "brand", "model", "chipset")
    filter_horizontal = [
        "memory_types_supported",
        "raid_types_supported",
        "operations_systems_supported",
    ]
    list_filter = AdvancedAdminModels.list_filter + [
        motherboard_filters.MotherBoardPCIeX16Filter,
        motherboard_filters.MotherBoardChipsetFilter,
        motherboard_filters.MotherBoardSATA3Filter,
        motherboard_filters.MotherBoardM2ConnectorsFilter,
        motherboard_filters.MotherBoardCPUSocketFilter,
        motherboard_filters.MotherBoardFormFactorFilter,
        motherboard_filters.MotherBoardM2SlotTypeFilter,
        motherboard_filters.MotherBoardMaxMemoryFilter,
        motherboard_filters.MotherBoardMemorySlotsFilter,
        motherboard_filters.MotherBoardMemoryTypesFilter,
        motherboard_filters.MotherBoardRAIDTypesFilter,
        motherboard_filters.MotherBoardUSB32Gen2Filter,
        motherboard_filters.MotherBoardUSBTypeCFilter,
    ]


@admin.register(BluetoothDongle)
class BluetoothDongleAdmin(AdvancedAdminModels):
    model = BluetoothDongle
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "max_range",
        "bluetooth_version",
        "price",
        "sku",
        "is_active",
    )
    search_fields = ("name", "brand", "model", "price")
    filter_horizontal = ["colors"]
    list_filter = AdvancedAdminModels.list_filter + [
        common_filters.ColorsFilter,
        bluetooth_dongle_filters.BluetoothDongleBluetoothVersionFilter,
        bluetooth_dongle_filters.BluetoothDongleInterfaceTypeFilter,
        bluetooth_dongle_filters.BluetoothDongleMaxRangeFilter,
    ]


@admin.register(USBHUB)
class USBHUBAdmin(AdvancedAdminModels):
    model = USBHUB
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "interfaces",
        "ports_count",
        "price",
        "sku",
        "is_active",
    )
    search_fields = ("name", "brand", "model", "interfaces")
    filter_horizontal = ["compatible_operation_systems"]
    list_filter = AdvancedAdminModels.list_filter + [
        usb_hub_filters.USBHUBInterfacesFilter,
        usb_hub_filters.USBHubFeaturesFilter,
        usb_hub_filters.USBHUBPortsCountFilter,
        usb_hub_filters.USBHUBExternalHardDriveCompatibleOperationSystemsFilter,
    ]


@admin.register(SSD)
class SSDAdmin(AdvancedAdminModels):
    model = SSD
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "capacity",
        "ordered_write_speed",
        "ordered_read_speed",
        "average_lifespan",
        "price",
        "sku",
        "is_active",
    )
    search_fields = ("name", "brand", "model", "capacity")
    list_filter = AdvancedAdminModels.list_filter + [
        SSD_filters.SSDCapacityFilter,
        SSD_filters.SSDFeaturesFilter,
        SSD_filters.SSDInterfaceTypeFilter,
        SSD_filters.SSDAverageLifespanFilter,
        SSD_filters.SSDFlashDriveTypeFilter,
        SSD_filters.SSDInterfaceStandardFilter,
        SSD_filters.SSDOrderedReadSpeedFilter,
        SSD_filters.SSDOrderedWriteSpeedFilter,
    ]


@admin.register(M2SSD)
class M2SSDAdmin(SSDAdmin):
    model = M2SSD


@admin.register(ExternalHardDrive)
class ExternalHardDriveAdmin(AdvancedAdminModels):
    model = ExternalHardDrive
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "capacity",
        "connection_type",
        "materials",
        "waterproof",
        "price",
        "sku",
        "is_active",
    )
    search_fields = ("name", "brand", "model", "capacity")
    filter_horizontal = [
        "colors",
        "compatible_operation_systems",
    ]
    list_filter = AdvancedAdminModels.list_filter + [
        common_filters.ColorsFilter,
        usb_hub_filters.USBHUBExternalHardDriveCompatibleOperationSystemsFilter,
        external_hard_external_ssd_drive_filters.ExternalHardDriveExternalSSDCapacityFilter,
        external_hard_external_ssd_drive_filters.ExternalSSDHardDriveWarrantyFilter,
        external_hard_external_ssd_drive_filters.ExternalHardDriveExternalSSDWaterproofFilter,
        external_hard_external_ssd_drive_filters.ExternalHardDriveConnectionTypeFilter,
        external_hard_external_ssd_drive_filters.MaterialsFilter,
    ]


@admin.register(ExternalSSD)
class ExternalSSDAdmin(SSDAdmin):
    model = ExternalSSD
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "capacity",
        "interface",
        "materials",
        "read_speed",
        "write_speed",
        "waterproof",
        "price",
        "sku",
        "is_active",
    )
    search_fields = ("name", "brand", "model", "capacity")
    filter_horizontal = [
        "colors",
    ]
    list_filter = AdvancedAdminModels.list_filter + [
        common_filters.ColorsFilter,
        external_hard_external_ssd_drive_filters.ExternalSSDHardDriveWarrantyFilter,
        external_hard_external_ssd_drive_filters.ExternalHardDriveExternalSSDCapacityFilter,
        external_hard_external_ssd_drive_filters.ExternalHardDriveExternalSSDWaterproofFilter,
        external_hard_external_ssd_drive_filters.ExternalSSDShockproofFilter,
        external_hard_external_ssd_drive_filters.ExternalSSDInterfaceTypeFilter,
        external_hard_external_ssd_drive_filters.ExternalSSDMaterialsFilter,
        external_hard_external_ssd_drive_filters.ExternalSSDMemoryTypeFilter,
        external_hard_external_ssd_drive_filters.ExternalSSDReadSpeedFilter,
        external_hard_external_ssd_drive_filters.ExternalSSDWriteSpeedFilter,
    ]


@admin.register(FlashDrive)
class FlashDriveAdmin(AdvancedAdminModels):
    model = FlashDrive
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "capacity",
        "connection_type",
        "material",
        "read_speed",
        "write_speed",
        "waterproof",
        "price",
        "sku",
        "is_active",
    )
    search_fields = ("name", "brand", "model", "capacity")
    list_filter = AdvancedAdminModels.list_filter + [
        flash_drive_filters.FlashDriveCapacityFilter,
        flash_drive_filters.FlashDriveMaterialFilter,
        flash_drive_filters.FlashDriveShockproofFilter,
        flash_drive_filters.FlashDriveWaterproofFilter,
        flash_drive_filters.FlashDriveConnectionTypeFilter,
        flash_drive_filters.HardwareEncryptionFilter,
        flash_drive_filters.FlashDriveReadSpeedFilter,
        flash_drive_filters.FlashDriveWriteSpeedFilter,
    ]


@admin.register(Keyboard)
class KeyboardAdmin(AdvancedAdminModels):
    model = Keyboard
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "connection_type",
        "switch_type",
        "layout",
        "key_count",
        "interface",
        "price",
        "sku",
        "is_active",
    )
    search_fields = ("name", "brand", "model", "connection_type", "switch_type")
    list_filter = AdvancedAdminModels.list_filter + [
        common_filters.ColorsFilter,
        keyboard_filters.KeyboardLayoutFilter,
        keyboard_filters.KeyboardBacklightFilter,
        keyboard_filters.KeyboardInterfaceFilter,
        keyboard_filters.KeyboardWaterproofFilter,
        keyboard_filters.KeyboardIsMechanicalFilter,
        keyboard_filters.HasNumericPadFilter,
        keyboard_filters.KeyboardBatteryLifeFilter,
        keyboard_filters.KeyboardConnectionTypeFilter,
        keyboard_filters.KeyboardKeyCountFilter,
        keyboard_filters.KeyboardSwitchTypeFilter,
    ]


@admin.register(Mouse)
class MouseAdmin(AdvancedAdminModels):
    model = Mouse
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "connection_type",
        "sensor_type",
        "dpi_max",
        "rgb_lighting",
        "hand_orientation",
        "ergonomic_design",
        "price",
        "sku",
        "is_active",
    )
    search_fields = ("name", "brand", "model", "connection_type", "sensor_type")
    list_filter = AdvancedAdminModels.list_filter + [
        mouse_filters.MouseWaterproofFilter,
        mouse_filters.MouseRechargeableFilter,
        mouse_filters.MouseSensorTypeFilter,
        mouse_filters.MouseRgbLightingFilter,
        mouse_filters.MouseConnectionTypeFilter,
        mouse_filters.MouseErgonomicDesignFilter,
        mouse_filters.MouseHandOrientationFilter,
        mouse_filters.MouseHasScrollWheelFilter,
    ]


@admin.register(Monitor)
class MonitorAdmin(AdvancedAdminModels):
    model = Monitor
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "screen_size_inches",
        "resolution",
        "refresh_rate_hz",
        "panel_type",
        "brightness_nits",
        "price",
        "sku",
        "is_active",
    )
    search_fields = (
        "name",
        "brand",
        "model",
        "screen_size_inches",
        "panel_type",
        "brightness_nits",
    )
    list_filter = AdvancedAdminModels.list_filter + [
        monitor_filters.MonitorBrightnessFilter,
        monitor_filters.MonitorPanelTypeFilter,
        monitor_filters.MonitorScreenSizeFilter,
        monitor_filters.MonitorAspectRatioFilter,
        monitor_filters.MonitorHasSpeakersFilter,
        monitor_filters.MonitorRefreshRateFilter,
        monitor_filters.MonitorVrrTechnologyFilter,
    ]


@admin.register(InternalHDD)
class InternalHDDAdmin(AdvancedAdminModels):
    model = InternalHDD
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "capacity_tb",
        "interface",
        "form_factor",
        "rpm",
        "price",
        "sku",
        "is_active",
    )
    search_fields = (
        "name",
        "brand",
        "model",
        "capacity_tb",
        "interface",
        "form_factor",
        "rpm",
    )
    list_filter = AdvancedAdminModels.list_filter + [
        internal_HDD_filters.InternalHDDCapacityFilter,
        internal_HDD_filters.InternalHDDInterfaceFilter,
        internal_HDD_filters.InternalHDDBrandFilter,
        internal_HDD_filters.InternalHDDCacheFilter,
        internal_HDD_filters.InternalHDDRPMFilter,
        internal_HDD_filters.InternalHDDFormFactorFilter,
        internal_HDD_filters.InternalHDDISExternalFilter,
        internal_HDD_filters.InternalHDDOperatingTemperatureFilter,
        internal_HDD_filters.InternalHDDPowerConsumptionFilter,
    ]


@admin.register(PreBuiltPC)
class PreBuiltPCAdmin(AdvancedAdminModels):
    model = PreBuiltPC
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "cpu",
        "motherboard",
        "gpu",
        "ram_type",
        "ram_capacity_gb",
        "internal_ssd",
        "internal_m2_ssd",
        "internal_hdd",
        "power_supply_wattage",
        "operating_system",
        "price",
        "sku",
        "is_active",
    )
    search_fields = (
        "name",
        "brand",
        "model",
        "cpu",
        "motherboard",
        "gpu",
        "ram_type",
        "ram_capacity",
    )
    list_filter = AdvancedAdminModels.list_filter + [
        pre_built_pcs_filters.PreBuiltPCCaseFilter,
        pre_built_pcs_filters.PreBuiltPCCPUFilter,
        pre_built_pcs_filters.PreBuiltPCGPUFilter,
        pre_built_pcs_filters.PreBuiltPCMotherboardFilter,
        pre_built_pcs_filters.PreBuiltPCFormFactorFilter,
        pre_built_pcs_filters.PreBuiltPCInternalHDDFilter,
        pre_built_pcs_filters.PreBuiltPCM2SSDTypeFilter,
        pre_built_pcs_filters.PreBuiltPCPowerSupplyFilter,
        pre_built_pcs_filters.PreBuiltPCRamCapacityFilter,
        pre_built_pcs_filters.PreBuiltPCRamTypeFilter,
        pre_built_pcs_filters.PreBuiltPCSalesAudienceFilter,
        pre_built_pcs_filters.PreBuiltPCSSDTypeFilter,
    ]


@admin.register(AllInOnePC)
class AllInOnePCAdmin(AdvancedAdminModels):
    model = AllInOnePC
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "screen_size_inches",
        "screen_resolution",
        "screen_type",
        "refresh_rate_hz",
        "cpu_model_name",
        "ram_capacity_gb",
        "storage_type",
        "storage_capacity_gb",
        "gpu_model_name",
        "operating_system",
        "price",
        "sku",
        "is_active",
    )
    search_fields = (
        "name",
        "brand",
        "model",
        "cpu_model_name",
        "ram_capacity_gb",
        "storage_type",
        "storage_capacity_gb",
        "gpu_model_name",
    )
    filter_horizontal = [
        "colors",
    ]
    list_filter = AdvancedAdminModels.list_filter + [
        all_in_on_pcs_filters.AllInOnePCColorFilter,
        all_in_on_pcs_filters.AllInOnePCWebcamFilter,
        all_in_on_pcs_filters.AllInOnePCTouchscreenFilter,
        all_in_on_pcs_filters.AllInOnePCCPUModelFilter,
        all_in_on_pcs_filters.AllInOnePCGPUModelFilter,
        all_in_on_pcs_filters.AllInOnePCOperatingSystemFilter,
        all_in_on_pcs_filters.AllInOnePCRamCapacityFilter,
        all_in_on_pcs_filters.AllInOnePCRamTypeFilter,
        all_in_on_pcs_filters.AllInOnePCRefreshRateFilter,
        all_in_on_pcs_filters.AllInOnePCScreenResolutionFilter,
        all_in_on_pcs_filters.AllInOnePCScreenSizeFilter,
        all_in_on_pcs_filters.AllInOnePCScreenTypeFilter,
        all_in_on_pcs_filters.AllInOnePCStorageCapacityFilter,
        all_in_on_pcs_filters.AllInOnePCStorageTypeFilter,
        all_in_on_pcs_filters.AllInOnePCWirelessConnectivityFilter,
    ]


@admin.register(Laptop)
class LaptopAdmin(AdvancedAdminModels):
    model = Laptop
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "screen_panel_type",
        "screen_size_inches",
        "screen_resolution",
        "screen_panel_type",
        "screen_refresh_rate_hz",
        "cpu_model_name",
        "cpu_cores",
        "cpu_threads",
        "ram_capacity_gb",
        "storage_type",
        "storage_capacity_gb",
        "gpu_model_name",
        "gpu_vram_gb",
        "operating_system_name",
        "price",
        "sku",
        "is_active",
    )
    search_fields = (
        "name",
        "brand",
        "model",
        "cpu_model_name",
        "ram_capacity_gb",
        "storage_type",
        "storage_capacity_gb",
        "gpu_model_name",
    )
    filter_horizontal = ["color_options"]
    list_filter = AdvancedAdminModels.list_filter + [
        laptops_filters.LaptopColorFilter,
        laptops_filters.LaptopWeightFilter,
        laptops_filters.LaptopTouchscreenFilter,
        laptops_filters.LaptopWiFiStandardFilter,
        laptops_filters.LaptopOSPreinstalledFilter,
        laptops_filters.LaptopAspectRatioFilter,
        laptops_filters.LaptopBluetoothVersionFilter,
        laptops_filters.LaptopCPUCoreFilter,
        laptops_filters.LaptopCPUModelFilter,
        laptops_filters.LaptopGPUModelFilter,
        laptops_filters.LaptopIntegratedGraphicsFilter,
        laptops_filters.LaptopOperatingSystemFilter,
        laptops_filters.LaptopPanelTypeFilter,
        laptops_filters.LaptopRAMCapacityFilter,
        laptops_filters.LaptopRAMTypeFilter,
        laptops_filters.LaptopRefreshRateFilter,
        laptops_filters.LaptopScreenResolutionFilter,
        laptops_filters.LaptopScreenSizeFilter,
        laptops_filters.LaptopSecondaryStorageTypeFilter,
        laptops_filters.LaptopStorageCapacityFilter,
        laptops_filters.LaptopStorageTypeFilter,
    ]


@admin.register(NewsLetter)
class NewsLetterAdmin(BasicAdminModels):
    model = NewsLetter
    list_display = (
        "id",
        "email",
        "datetime_created",
        "datetime_modified",
    )


@admin.register(Favorite)
class FavoriteAdmin(BasicAdminModels):
    model = Favorite
    list_display = (
        "id",
        "user",
        "content_type",
        "object_id",
        "content_object",
    )
    search_fields = (
        "user",
        "content_type",
    )


@admin.register(Comment)
class CommentAdmin(BasicAdminModels):
    model = Comment
    list_display = (
        "id",
        "user",
        "content_type",
        "object_id",
        "content_object",
        "is_approved",
    )
    list_editable = ("is_approved",)
    search_fields = (
        "user",
        "content_type",
    )
    list_filter = ("is_approved",)


@admin.register(Rating)
class RatingAdmin(BasicAdminModels):
    model = Rating
    list_display = (
        "id",
        "user",
        "content_type",
        "object_id",
        "content_object",
        "score",
    )

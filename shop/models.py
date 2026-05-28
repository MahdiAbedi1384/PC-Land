from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class GlobalMixin(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=255)
    brand = models.CharField(verbose_name=_("brand"), max_length=255)
    model = models.CharField(verbose_name=_("model"), max_length=255)
    slug = models.SlugField(
        verbose_name=_("slug"), max_length=1000, allow_unicode=True, unique=True
    )
    summary = models.TextField(
        verbose_name=_("summary"), max_length=1000, default=_("None")
    )
    description = models.TextField(verbose_name=_("description"), max_length=8000)
    weight = models.DecimalField(
        verbose_name=_("weight"), max_digits=5, decimal_places=3, default=0
    )
    price = models.PositiveBigIntegerField(verbose_name=_("price"), default=0)
    sku = models.PositiveIntegerField(
        verbose_name=_("SKU"), default=0
    )  # stock keeping unit
    is_active = models.BooleanField(verbose_name=_("active"), default=True)
    main_image = models.ImageField(
        verbose_name=_("main image"), upload_to="main_images/", null=True, blank=True
    )
    datetime_created = models.DateTimeField(
        verbose_name=_("creation date"), auto_now_add=True
    )
    datetime_modified = models.DateTimeField(
        verbose_name=_("last modification date"), auto_now=True
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name + self.brand + self.model, allow_unicode=True)
        return super(GlobalMixin, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "generic_detail",
            kwargs={
                # "app": self._meta.app_label,
                "model": self._meta.model_name,
                "pk": self.pk,
                "slug": self.slug,
            },
        )


class Images(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey("content_type", "object_id")

    image = models.ImageField(upload_to="products/images/", verbose_name=_("image"))

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return f"Image for {self.product}"


class PCIGenerationTypes(models.Model):
    # Gen3 = "3"
    # Gen4 = "4"
    # Gen5 = "5"
    title = models.CharField(verbose_name=_("pci generation type"), max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("PCI Generation Type")
        verbose_name_plural = _("PCI Generation Types")


class RAMTypesSupported(models.Model):
    # ddr2 = _('DDR2')
    # ddr3 = _('DDR3')
    # ddr4 = _('DDR4')
    # ddr5 = _('DDR5')
    # ddr6 = _('DDR6')
    title = models.CharField(verbose_name=_("RAM type"), max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("RAM Type Supported")
        verbose_name_plural = _("RAM Types Supported")


class GraphicsCardFeatures(models.Model):
    title = models.CharField(verbose_name=_("graphics card features"), max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Graphics Card Feature")
        verbose_name_plural = _("Graphics Card Features")


class RAIDTypesSupported(models.Model):
    #  RAID0 - RAID1 - RAID5 - RAID10
    title = models.CharField(verbose_name=_("RAID type"), max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("RAID Type Supported")
        verbose_name_plural = _("RAID Types Supported")


class OperationSystemsSupported(models.Model):
    # windows 10 64-bit windows 11 64-bit
    title = models.CharField(verbose_name=_("operation systems "), max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Operation System ")
        verbose_name_plural = _("Operation Systems ")


class Colors(models.Model):
    title = models.CharField(verbose_name=_("color"), max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Color ")
        verbose_name_plural = _("Colors")


class LapTopRAMModel(GlobalMixin):
    memory_type = models.ForeignKey(to="RAMTypesSupported", on_delete=models.DO_NOTHING)
    memory_size_per_module = models.PositiveIntegerField(
        verbose_name=_("memory size per module"), default=0
    )
    memory_size = models.PositiveIntegerField(verbose_name=_("memory size"), default=0)
    memory_configuration = models.CharField(
        verbose_name=_("memory configuration"), max_length=255
    )
    module_type = models.CharField(verbose_name=_("module type"), max_length=255)
    frequency = models.PositiveIntegerField(verbose_name=_("frequency"), default=0)
    timing = models.CharField(verbose_name=_("timing"), max_length=255)
    pins_count = models.PositiveIntegerField(verbose_name=_("pins count"), default=0)
    voltage = models.PositiveIntegerField(verbose_name=_("voltage"), default=0)
    extra_info = models.CharField(
        verbose_name=_("extra info"), max_length=255, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Laptop RAM")
        verbose_name_plural = _("Laptop RAMs")


class ComputerRAMModel(LapTopRAMModel):
    cooler_system = models.CharField(
        verbose_name=_("cooler system"), max_length=255, null=True, blank=True
    )

    class Meta:
        verbose_name = _("computer RAM")
        verbose_name_plural = _("computer RAMs")


class CPUModel(GlobalMixin):
    class ArchitectureType(models.TextChoices):
        ARCHITECTURE_TYPE_32_BIT = "32"
        ARCHITECTURE_TYPE_64_BIT = "64"

    class PackageType(models.TextChoices):
        tray = "tray", _("tray")
        box = "box", _("box")

    cpu_series = models.CharField(verbose_name=_("cpu series"), max_length=255)
    cpu_generation = models.PositiveIntegerField(
        verbose_name=_("cpu generation"), default=0
    )
    socket = models.CharField(verbose_name=_("socket"), max_length=255)
    released_date = models.DateField(
        verbose_name=_("release date"), null=True, blank=True
    )
    generation_name = models.CharField(
        verbose_name=_("generation name"), max_length=255, null=True, blank=True
    )
    cpu_architecture = models.CharField(
        verbose_name=_("cpu architecture"), max_length=255, null=True, blank=True
    )
    cpu_architecture_type = models.CharField(
        verbose_name=_("cpu architecture type"),
        max_length=2,
        choices=ArchitectureType.choices,
    )
    lithography = models.PositiveSmallIntegerField(
        verbose_name=_("lithography"), default=0
    )
    pci_express_generation_supports_version = models.ManyToManyField(
        verbose_name=_("pci express generation support version"), to=PCIGenerationTypes
    )
    package_type = models.CharField(
        verbose_name=_("package type"), max_length=5, choices=PackageType.choices
    )
    cores = models.PositiveSmallIntegerField(verbose_name=_("cores"), default=0)
    threads = models.PositiveSmallIntegerField(verbose_name=_("threads"), default=0)
    performance_cores_count = models.PositiveSmallIntegerField(
        verbose_name=_("performance cores count"), default=0, null=True, blank=True
    )
    efficient_core_count = models.PositiveSmallIntegerField(
        verbose_name=_("efficient cores count"), default=0, null=True, blank=True
    )
    base_frequency = models.PositiveSmallIntegerField(
        verbose_name=_("base frequency"), default=0
    )
    boosted_frequency = models.PositiveSmallIntegerField(
        verbose_name=_("boosted frequency"), default=0
    )
    base_power_usage = models.PositiveSmallIntegerField(
        verbose_name=_("base power usage"), default=0
    )
    max_power_usage = models.PositiveSmallIntegerField(
        verbose_name=_("max power usage"), default=0
    )
    in_operation_temperature = models.PositiveSmallIntegerField(
        verbose_name=_("in operation temperature"), default=0
    )
    ai_npu = models.CharField(
        verbose_name=_("ai npu"), max_length=255, null=True, blank=True
    )
    ram_types_supported = models.ManyToManyField(
        verbose_name=_("ram types supported"), to=RAMTypesSupported
    )
    max_memory_size_supported = models.PositiveSmallIntegerField(
        verbose_name=_("max memory size supported"), default=0
    )
    ram_frequency_supported = models.CharField(
        verbose_name=_("ram frequency supported"), max_length=255
    )
    ram_channels_supported = models.PositiveSmallIntegerField(
        verbose_name=_("ram channels supported")
    )
    max_ram_bandwidth = models.DecimalField(
        verbose_name=_("max ram bandwidth"), max_digits=6, decimal_places=2, default=0
    )
    cache_memory_l1 = models.PositiveSmallIntegerField(
        verbose_name=_("cache memory L1"), default=0
    )
    cache_memory_l2 = models.PositiveSmallIntegerField(
        verbose_name=_("cache memory L2"), default=0
    )
    cache_memory_l3 = models.PositiveSmallIntegerField(
        verbose_name=_("cache memory L3"), default=0, null=True, blank=True
    )
    has_igpu = models.BooleanField(verbose_name=_("has IGPU"), default=False)
    igpu_model = models.CharField(
        verbose_name=_("IGPU model"), max_length=255, null=True, blank=True
    )

    class Meta:
        verbose_name = _("CPU")
        verbose_name_plural = _("CPUs")


class GraphicsCard(GlobalMixin):
    class ChipManufacturers(models.TextChoices):
        nvidia = "Nvidia", _("Nvidia")
        amd = "AMD", _("AMD")
        intel = "Intel", _("Intel")

    class Interfaces(models.TextChoices):
        pci_express = "PCI Express", _("PCI Express")
        pci_express_2 = "PCI Express2", _("PCI Express 2")
        pci_express_3 = "PCI Express3", _("PCI Express 3")
        pci_express_4 = "PCI Express4", _("PCI Express 4")
        pci_express_5 = "PCI Express5", _("PCI Express 5")

    class VRAMTypes(models.TextChoices):
        ddr = "DDR", _("DDR")
        ddr2 = "DDR2", _("DDR2")
        ddr3 = "DDR3", _("DDR3")
        ddr4 = "DDR4", _("DDR4")
        ddr5 = "DDR5", _("DDR5")
        gddr = "GDDR", _("GDDR")
        gddr2 = "GDDR2", _("GDDR2")
        gddr3 = "GDDR3", _("GDDR3")
        gddr4 = "GDDR4", _("GDDR4")
        gddr5 = "GDDR5", _("GDDR5")
        gddr6 = "GDDR6", _("GDDR6")
        gddr7 = "GDDR7", _("GDDR7")
        gddr5x = "GDDR5x", _("GDDR5x")
        gddr6x = "GDDR6x", _("GDDR6x")

    chip_manufacturer = models.CharField(
        verbose_name=_("chip manufacturer"),
        max_length=10,
        choices=ChipManufacturers.choices,
    )
    interface = models.CharField(
        verbose_name=_("interface"), max_length=50, choices=Interfaces.choices
    )
    openGL_version = models.DecimalField(
        verbose_name=_("OpenGL version"), max_digits=2, decimal_places=1, default=0
    )
    directx_version = models.DecimalField(
        verbose_name=_("DirectX version"), max_digits=4, decimal_places=2, default=0
    )
    VRAM = models.DecimalField(
        verbose_name=_("VRAM"), max_digits=6, decimal_places=2, default=0
    )
    VRAM_type = models.CharField(
        verbose_name=_("VRAM type"), max_length=10, choices=VRAMTypes.choices
    )
    efficient_frequency = models.PositiveSmallIntegerField(
        verbose_name=_("efficient frequency"), default=0
    )
    bus_interface = models.PositiveSmallIntegerField(
        verbose_name=_("bus interface"), default=0
    )
    resolution = models.CharField(verbose_name=_("resolution"), max_length=255)
    HDMI_ports_count = models.PositiveSmallIntegerField(
        verbose_name=_("HDMI ports count"), default=0
    )
    DisplayPort_ports_count = models.PositiveSmallIntegerField(
        verbose_name=_("DisplayPort ports count"), default=0
    )
    number_of_supported_monitors = models.PositiveSmallIntegerField(
        verbose_name=_("number of supported monitors"), default=0
    )
    size = models.CharField(verbose_name=_("size"), max_length=255)
    min_power_supply_required = models.PositiveSmallIntegerField(
        verbose_name=_("minimum power required"), default=0
    )
    _16_pin_PCIe_power_connector_count = models.PositiveSmallIntegerField(
        verbose_name=_("16-pin PCIe power connector "), default=0
    )
    _6_pin_PCIe_power_connector_count = models.PositiveSmallIntegerField(
        verbose_name=_("6-pin PCIe power connector "), default=0
    )
    _8_pin_PCIe_power_connector_count = models.PositiveSmallIntegerField(
        verbose_name=_("8-pin PCIe power connector "), default=0
    )
    required_installation_space = models.DecimalField(
        verbose_name=_("required installation space"),
        max_digits=4,
        decimal_places=2,
        default=0,
    )
    graphics_card_features = models.ManyToManyField(
        verbose_name=_("graphics card features"), to=GraphicsCardFeatures, blank=True
    )
    fans_count = models.PositiveSmallIntegerField(
        verbose_name=_("Fans count"), default=0
    )
    extra_info = models.TextField(
        verbose_name=_("extra info"), max_length=700, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Graphics Card")
        verbose_name_plural = _("Graphics Cards")


class ComputerCase(GlobalMixin):
    size = models.CharField(verbose_name=_("size"), max_length=255)
    max_cpu_cooler_height = models.PositiveSmallIntegerField(
        verbose_name=_("max CPU cooler height"), default=0
    )
    max_graphics_card_length = models.PositiveSmallIntegerField(
        verbose_name=_("max graphics card length"), default=0
    )
    case_material = models.CharField(verbose_name=_("case material"), max_length=255)
    case_form_factor = models.CharField(
        verbose_name=_("case form factor"), max_length=255
    )
    motherboards_compatibility = models.ManyToManyField(
        verbose_name=_("Mother Board Compatibility"), to="Motherboard"
    )
    power_supply_mounting_location = models.CharField(
        verbose_name=_("Power supply mounting location"), max_length=255
    )
    supported_power_supply_form_factor = models.CharField(
        verbose_name=_("supported power supply form factor"), max_length=255
    )
    number_of_expansion_slots = models.PositiveSmallIntegerField(
        verbose_name=_("number of expansion slots"), default=0
    )
    Number_of_2_p_5_inch_drive_bays = models.PositiveSmallIntegerField(
        verbose_name=_("Number 2.5 inch drive bays"), default=0
    )
    Number_of_3_p_5_inch_drive_bays = models.PositiveSmallIntegerField(
        verbose_name=_("Number 3.5 inch drive bays"), default=0
    )
    Number_of_5_p_25_inch_drive_bays = models.PositiveSmallIntegerField(
        verbose_name=_("Number 5.25 inch drive bays"), default=0
    )
    Total_fan_mounting_positions = models.PositiveSmallIntegerField(
        verbose_name=_("Total fan mounting positions"), default=0
    )
    pre_installed_fans = models.PositiveSmallIntegerField(
        verbose_name=_("pre-installed fans"), default=0
    )
    Front_panel_fan_mounts = models.PositiveSmallIntegerField(
        verbose_name=_("Front panel fans"), default=0
    )
    top_panel_fan_mounts = models.PositiveSmallIntegerField(
        verbose_name=_("Top panel fans"), default=0
    )
    rear_panel_fan_mounts = models.PositiveSmallIntegerField(
        verbose_name=_("Rear panel fans"), default=0
    )
    side_panel_fan_mounts = models.PositiveSmallIntegerField(
        verbose_name=_("Side panel fans"), default=0
    )
    bottom_panel_fan_mounts = models.PositiveSmallIntegerField(
        verbose_name=_("Bottom panel fans"), default=0
    )
    extra_info_about_fans = models.TextField(
        verbose_name=_("extra info about fans"), max_length=500, null=True, blank=True
    )
    water_cooling_radiator_support = models.CharField(
        verbose_name=_("Water cooling radiator support"),
        max_length=255,
        null=True,
        blank=True,
    )
    Water_cooling_radiator_mounting_positions = models.CharField(
        verbose_name=_("Water cooling radiator mounting positions"),
        max_length=255,
        null=True,
        blank=True,
    )
    usb2_ports_count = models.PositiveSmallIntegerField(
        verbose_name=_("USB2 ports count"), default=0
    )
    usb3_ports_count = models.PositiveSmallIntegerField(
        verbose_name=_("USB3 ports"), default=0
    )
    usb3_1_ports_count = models.PositiveSmallIntegerField(
        verbose_name=_("USB 3.1 ports"), default=0
    )
    audio_3_5_jack = models.PositiveSmallIntegerField(
        verbose_name=_("Audio 3.5 jack"), default=0
    )

    class Meta:
        verbose_name = _("Computer Case")
        verbose_name_plural = _("Computer Cases")


class MotherBoard(GlobalMixin):
    cpu_socket_type = models.CharField(
        verbose_name=_("CPU socket type"), max_length=255
    )
    supported_cpus = models.CharField(verbose_name=_("Supported CPUs"), max_length=255)
    chipset = models.CharField(verbose_name=_("Chipset"), max_length=255)
    memory_types_supported = models.ManyToManyField(
        verbose_name=_("Memory types supported"),
        to=RAMTypesSupported,
        related_name="motherboard_memory_types_supported",
    )
    memory_slots = models.PositiveSmallIntegerField(
        verbose_name=_("Memory slots"), default=0
    )
    max_memory_supported = models.PositiveSmallIntegerField(
        verbose_name=_("maximum memory supported"), default=0
    )
    memory_standards = models.CharField(
        verbose_name=_("Memory standards"), max_length=400
    )
    memory_configuration = models.SmallIntegerField(
        verbose_name=_("Memory configuration"), default=0
    )
    PCI_express_x1_slots_count = models.PositiveSmallIntegerField(
        verbose_name=_("PCI express x1 slots"), default=0
    )
    PCI_express_x16_slots_count = models.PositiveSmallIntegerField(
        verbose_name=_("PCI express x16 slots"), default=0
    )
    slots_extra_info = models.TextField(
        verbose_name=_("extra info"), max_length=500, null=True, blank=True
    )
    m2_connectors_count = models.PositiveSmallIntegerField(
        verbose_name=_("M2 connectors count"), default=0
    )
    m2_slot_type = models.CharField(verbose_name=_("M2 slot type"), max_length=255)
    sata_3_connectors_count = models.PositiveSmallIntegerField(
        verbose_name=_("SATA 3.0 connectors count"), default=0
    )
    storage_extra_info = models.TextField(
        verbose_name=_("storage extra info"), max_length=500, null=True, blank=True
    )
    raid_types_supported = models.ManyToManyField(
        verbose_name=_("RAID types supported"), to=RAIDTypesSupported
    )
    lan_card = models.CharField(verbose_name=_("LAN card"), max_length=255)
    usb_3_p_2_gen1_prots_count = models.PositiveSmallIntegerField(
        verbose_name=_("USB 3.2 gen1 prots count"), default=0
    )
    usb_3_p_2_gen2_prots_count = models.PositiveSmallIntegerField(
        verbose_name=_("USB 3.2 gen2 prots count"), default=0
    )
    usb_2_prots_count = models.PositiveSmallIntegerField(
        verbose_name=_("USB 2.0 prots count"), default=0
    )
    usb_type_c_prots_count = models.PositiveSmallIntegerField(
        verbose_name=_("USB Type-C prots count"), default=0
    )
    usb_2_headers_count = models.PositiveSmallIntegerField(
        verbose_name=_("USB 2.0 header count"), default=0
    )
    all_usb_ports_extra_info = models.TextField(
        verbose_name=_("all USB ports extra info"),
        max_length=500,
        null=True,
        blank=True,
    )
    sound_card = models.CharField(verbose_name=_("Sound card"), max_length=255)
    sound_channels = models.DecimalField(
        verbose_name=_("Sound channels"), max_digits=2, decimal_places=1
    )
    lan_ports_count = models.PositiveSmallIntegerField(
        verbose_name=_("LAN ports count"), default=0
    )
    hdmi_ports_count = models.PositiveSmallIntegerField(
        verbose_name=_("HDMI ports count"), default=0
    )
    jack_3_p_5_count = models.PositiveSmallIntegerField(
        verbose_name=_("Jack 3.5 prots count"), default=0
    )
    ports_extra_info = models.TextField(
        verbose_name=_("ports extra info"), max_length=500, null=True, blank=True
    )
    total_fan_connectors_count = models.PositiveSmallIntegerField(
        verbose_name=_("Total fan connectors count"), default=0
    )
    power_connectors = models.TextField(
        verbose_name=_("Power connectors"), max_length=500, null=True, blank=True
    )
    buttons_and_switches_and_jumpers = models.TextField(
        verbose_name=_("Buttons and switches and jumpers"),
        max_length=500,
        null=True,
        blank=True,
    )
    headers_extra_info = models.TextField(
        verbose_name=_("headers extra info"), max_length=500, null=True, blank=True
    )
    operations_systems_supported = models.ManyToManyField(
        verbose_name=_("operation systems supported"), to=OperationSystemsSupported
    )
    form_factor = models.TextField(verbose_name=_("Form factor"), max_length=255)
    motherboard_features = models.TextField(
        verbose_name=_("Motherboard features"), max_length=500, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Motherboard")
        verbose_name_plural = _("Motherboards")

    def __str__(self):
        return f"{self.brand} - {self.model}"


class BluetoothDongle(GlobalMixin):
    max_range = models.PositiveSmallIntegerField(verbose_name=_("Max range"), default=0)
    colors = models.ManyToManyField(verbose_name=_("Colors"), to=Colors)
    interface_type = models.CharField(
        verbose_name=_("Interface type"), max_length=255, null=True, blank=True
    )
    bluetooth_version = models.DecimalField(
        verbose_name=_("Bluetooth version"),
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Bluetooth Dongle")
        verbose_name_plural = _("Bluetooth Dongles")


class USBHUB(GlobalMixin):
    interfaces = models.CharField(
        verbose_name=_("USB HUB interfaces"), max_length=255, null=True, blank=True
    )
    features = models.TextField(
        verbose_name=_("features"), max_length=500, null=True, blank=True
    )
    compatible_operation_systems = models.ManyToManyField(
        verbose_name=_("compatible operation systems"),
        to=OperationSystemsSupported,
    )
    ports_count = models.PositiveSmallIntegerField(
        verbose_name=_("ports count"), default=0
    )
    usb_hub_features = models.TextField(
        verbose_name=_("USB HUB features"), max_length=500, null=True, blank=True
    )

    class Meta:
        verbose_name = _("USB HUB")
        verbose_name_plural = _("USB HUBs")


class SSD(GlobalMixin):
    capacity = models.PositiveSmallIntegerField(
        verbose_name=_("SSD capacity"), default=0
    )
    ordered_write_speed = models.PositiveSmallIntegerField(
        verbose_name=_("ordered write speed"), default=0
    )
    ordered_read_speed = models.PositiveSmallIntegerField(
        verbose_name=_("ordered read speed"), default=0
    )
    max_resistance_against_shock = models.PositiveSmallIntegerField(
        verbose_name=_("maximum resistance against shock"), default=0
    )
    size = models.CharField(
        verbose_name=_("size"), max_length=255, null=True, blank=True
    )
    internal_ssd_interface_standard = models.CharField(
        verbose_name=_("Internal SSD interface standard"),
        max_length=255,
        null=True,
        blank=True,
    )
    random_write_speed = models.PositiveSmallIntegerField(
        verbose_name=_("Random write speed"), null=True, blank=True
    )
    random_read_speed = models.PositiveSmallIntegerField(
        verbose_name=_("Random read speed"), null=True, blank=True
    )
    average_lifespan = models.PositiveIntegerField(
        verbose_name=_("Average lifespan"), default=0
    )
    in_operation_temperature = models.PositiveSmallIntegerField(
        verbose_name=_("In operation temperature"), default=0
    )
    ssd_interface_type = models.CharField(
        verbose_name=_("SSD interface type"), max_length=255, null=True, blank=True
    )
    flash_drive_type = models.CharField(
        verbose_name=_("Flash drive type"), max_length=255, null=True, blank=True
    )
    ssd_features = models.TextField(
        verbose_name=_("SSD features"), max_length=500, null=True, blank=True
    )

    class Meta:
        verbose_name = _("SSD")
        verbose_name_plural = _("SSDs")

    def __str__(self):
        return f"{self.brand} - {self.model} {self.capacity}"


class M2SSD(SSD):
    m2_module_size = models.CharField(
        verbose_name=_("M.2 module size"), max_length=255, null=True, blank=True
    )
    Supported_M2_form_factors = models.CharField(
        verbose_name=_("Supported M.2 form factors"),
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("M2SSD")
        verbose_name_plural = _("M2SSDs")

    def __str__(self):
        return f"{self.brand} - {self.model}"


class ExternalHardDrive(GlobalMixin):
    class ConnectionType(models.TextChoices):
        USB_2_0 = "USB 2.0", _("USB 2.0")
        USB_3_0 = "USB 3.0", _("USB 3.0")
        USB_3_1 = "USB 3.1", _("USB 3.1")
        USB_3_2 = "USB 3.2", _("USB 3.2")
        USB_C = "USB-C", _("USB-C")
        THUNDERBOLT = "Thunderbolt", _("Thunderbolt")

    capacity = models.CharField(
        verbose_name=_("capacity"), max_length=50, help_text=_("e.g. 1TB, 2TB, 4TB")
    )
    connection_type = models.CharField(
        verbose_name=_("connection type"),
        max_length=50,
        choices=ConnectionType.choices,
        default=ConnectionType.USB_3_0,
    )
    dimensions = models.CharField(
        verbose_name=_("dimensions"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("e.g. 115 x 78 x 12.1 mm"),
    )
    colors = models.ManyToManyField(
        verbose_name=_("colors"),
        to=Colors,
    )
    warranty_months = models.PositiveIntegerField(
        verbose_name=_("warranty (months)"), default=24
    )
    waterproof = models.BooleanField(verbose_name=_("waterproof"), default=False)
    compatible_operation_systems = models.ManyToManyField(
        verbose_name=_("Compatible Operation Systems"), to=OperationSystemsSupported
    )
    materials = models.CharField(
        verbose_name=_("materials"),
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("External Hard Drive")
        verbose_name_plural = _("External Hard Drives")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.capacity})"


class ExternalSSD(GlobalMixin):
    class InterfaceType(models.TextChoices):
        USB_3_1 = "USB 3.1", _("USB 3.1")
        USB_3_2 = "USB 3.2", _("USB 3.2")
        USB_C = "USB-C", _("USB-C")
        THUNDERBOLT_3 = "Thunderbolt 3", _("Thunderbolt 3")
        THUNDERBOLT_4 = "Thunderbolt 4", _("Thunderbolt 4")

    class MemoryType(models.TextChoices):
        SATA = "SATA", _("SATA")
        NVME = "NVMe", _("NVMe")

    capacity = models.CharField(
        verbose_name=_("capacity"), max_length=50, help_text=_("e.g. 512GB, 1TB, 2TB")
    )
    interface = models.CharField(
        verbose_name=_("interface type"),
        max_length=50,
        choices=InterfaceType.choices,
        default=InterfaceType.USB_C,
    )
    memory_type = models.CharField(
        verbose_name=_("memory type"),
        max_length=20,
        choices=MemoryType.choices,
        default=MemoryType.NVME,
    )
    read_speed = models.PositiveIntegerField(
        verbose_name=_("read speed (MB/s)"),
        default=1000,
        help_text=_("Maximum sequential read speed"),
    )
    write_speed = models.PositiveIntegerField(
        verbose_name=_("write speed (MB/s)"),
        default=900,
        help_text=_("Maximum sequential write speed"),
    )
    shockproof = models.BooleanField(verbose_name=_("shockproof"), default=True)
    waterproof = models.BooleanField(verbose_name=_("waterproof"), default=False)
    warranty_months = models.PositiveSmallIntegerField(
        verbose_name=_("warranty (months)"), default=24
    )
    colors = models.ManyToManyField(
        verbose_name=_("color"),
        to=Colors,
    )
    materials = models.CharField(
        verbose_name=_("materials"),
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("External SSD")
        verbose_name_plural = _("External SSDs")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.capacity}, {self.memory_type})"


class FlashDrive(GlobalMixin):
    class ConnectionType(models.TextChoices):
        USB_2_0 = "USB 2.0", _("USB 2.0")
        USB_3_0 = "USB 3.0", _("USB 3.0")
        USB_3_1 = "USB 3.1", _("USB 3.1")
        USB_3_2 = "USB 3.2", _("USB 3.2")
        USB_C = "USB-C", _("USB-C")
        DUAL = "Dual (USB-A & USB-C)", _("Dual (USB-A & USB-C)")

    capacity = models.CharField(
        verbose_name=_("capacity"),
        max_length=20,
        help_text=_("e.g. 32GB, 64GB, 128GB, 256GB"),
    )

    connection_type = models.CharField(
        verbose_name=_("connection type"),
        max_length=50,
        choices=ConnectionType.choices,
        default=ConnectionType.USB_3_1,
    )

    material = models.CharField(
        verbose_name=_("body material"),
        max_length=50,
        blank=True,
        null=True,
        help_text=_("e.g. Metal, Plastic, Aluminum"),
    )

    read_speed = models.PositiveIntegerField(
        verbose_name=_("read speed (MB/s)"),
        null=True,
        blank=True,
        help_text=_("Optional: Maximum read speed in MB/s"),
    )

    write_speed = models.PositiveIntegerField(
        verbose_name=_("write speed (MB/s)"),
        null=True,
        blank=True,
        help_text=_("Optional: Maximum write speed in MB/s"),
    )

    waterproof = models.BooleanField(verbose_name=_("waterproof"), default=False)

    shockproof = models.BooleanField(verbose_name=_("shockproof"), default=False)

    hardware_encryption = models.BooleanField(
        verbose_name=_("hardware encryption supported"),
        default=False,
        help_text=_("Whether the flash drive supports built-in encryption"),
    )

    warranty_months = models.PositiveIntegerField(
        verbose_name=_("warranty (months)"), default=12
    )

    class Meta:
        verbose_name = _("Flash Drive")
        verbose_name_plural = _("Flash Drives")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.capacity})"


class Keyboard(GlobalMixin):
    class ConnectionType(models.TextChoices):
        WIRED = "Wired", _("Wired")
        WIRELESS = "Wireless", _("Wireless")
        BOTH = "Both", _("Wired / Wireless")

    class SwitchType(models.TextChoices):
        MEMBRANE = "Membrane", _("Membrane")
        MECHANICAL = "Mechanical", _("Mechanical")
        OPTICAL = "Optical", _("Optical")
        SCISSOR = "Scissor", _("Scissor Switch")

    class KeyboardLayout(models.TextChoices):
        ANSI = "ANSI", _("ANSI (US Layout)")
        ISO = "ISO", _("ISO (EU Layout)")
        JIS = "JIS", _("JIS (Japanese Layout)")

    class BacklightType(models.TextChoices):
        NONE = "None", _("No Backlight")
        SINGLE_COLOR = "Single Color", _("Single-color Backlight")
        RGB = "RGB", _("RGB Backlight")

    connection_type = models.CharField(
        verbose_name=_("connection type"),
        max_length=20,
        choices=ConnectionType.choices,
        default=ConnectionType.WIRED,
    )

    switch_type = models.CharField(
        verbose_name=_("switch type"),
        max_length=20,
        choices=SwitchType.choices,
        default=SwitchType.MEMBRANE,
        help_text=_("Type of key switch mechanism (mechanical, membrane, etc.)"),
    )

    layout = models.CharField(
        verbose_name=_("keyboard layout"),
        max_length=10,
        choices=KeyboardLayout.choices,
        default=KeyboardLayout.ANSI,
    )

    has_numeric_pad = models.BooleanField(
        verbose_name=_("has numeric keypad"), default=True
    )

    backlight = models.CharField(
        verbose_name=_("backlight type"),
        max_length=20,
        choices=BacklightType.choices,
        default=BacklightType.NONE,
    )

    is_mechanical = models.BooleanField(
        verbose_name=_("mechanical keyboard"),
        default=False,
        help_text=_("Whether the keyboard uses mechanical switches"),
    )

    key_count = models.PositiveIntegerField(
        verbose_name=_("key count"),
        null=True,
        blank=True,
        help_text=_("Total number of keys, e.g., 104"),
    )

    interface = models.CharField(
        verbose_name=_("interface"),
        max_length=50,
        blank=True,
        null=True,
        help_text=_("e.g. USB, Bluetooth 5.0, 2.4GHz Wireless"),
    )

    battery_life_hours = models.PositiveIntegerField(
        verbose_name=_("battery life (hours)"),
        null=True,
        blank=True,
        help_text=_("Approximate battery life for wireless models"),
    )

    waterproof = models.BooleanField(verbose_name=_("waterproof"), default=False)

    warranty_months = models.PositiveIntegerField(
        verbose_name=_("warranty (months)"), default=12
    )

    class Meta:
        verbose_name = _("Keyboard")
        verbose_name_plural = _("Keyboards")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.connection_type}, {self.switch_type})"


class Mouse(GlobalMixin):
    class ConnectionType(models.TextChoices):
        WIRED = "Wired", _("Wired")
        WIRELESS = "Wireless", _("Wireless")
        BOTH = "Both", _("Wired / Wireless")

    class SensorType(models.TextChoices):
        OPTICAL = "Optical", _("Optical")
        LASER = "Laser", _("Laser")
        BLUE_TRACK = "BlueTrack", _("BlueTrack")
        TRACKBALL = "Trackball", _("Trackball")

    class HandOrientation(models.TextChoices):
        RIGHT = "Right-handed", _("Right-handed")
        LEFT = "Left-handed", _("Left-handed")
        AMBIDEXTROUS = "Ambidextrous", _("Ambidextrous")

    connection_type = models.CharField(
        verbose_name=_("connection type"),
        max_length=20,
        choices=ConnectionType.choices,
        default=ConnectionType.WIRED,
    )

    sensor_type = models.CharField(
        verbose_name=_("sensor type"),
        max_length=20,
        choices=SensorType.choices,
        default=SensorType.OPTICAL,
    )

    dpi_max = models.PositiveIntegerField(
        verbose_name=_("maximum DPI"),
        null=True,
        blank=True,
        help_text=_("Maximum sensitivity (e.g. 16000 DPI)"),
    )

    button_count = models.PositiveIntegerField(
        verbose_name=_("button count"),
        default=3,
        help_text=_("Total number of buttons on the mouse"),
    )

    has_scroll_wheel = models.BooleanField(
        verbose_name=_("has scroll wheel"), default=True
    )

    rgb_lighting = models.BooleanField(verbose_name=_("RGB lighting"), default=False)

    rechargeable = models.BooleanField(
        verbose_name=_("rechargeable battery"),
        default=False,
        help_text=_("Applicable only for wireless mice"),
    )

    battery_life_hours = models.PositiveIntegerField(
        verbose_name=_("battery life (hours)"),
        null=True,
        blank=True,
        help_text=_("Approximate battery life for wireless models"),
    )

    hand_orientation = models.CharField(
        verbose_name=_("hand orientation"),
        max_length=20,
        choices=HandOrientation.choices,
        default=HandOrientation.RIGHT,
    )

    ergonomic_design = models.BooleanField(
        verbose_name=_("ergonomic design"), default=False
    )

    waterproof = models.BooleanField(verbose_name=_("waterproof"), default=False)

    warranty_months = models.PositiveIntegerField(
        verbose_name=_("warranty (months)"), default=12
    )

    class Meta:
        verbose_name = _("Mouse")
        verbose_name_plural = _("Mice")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.connection_type}, {self.sensor_type})"


class Monitor(GlobalMixin):
    class PanelType(models.TextChoices):
        IPS = "IPS", _("IPS (In-Plane Switching)")
        VA = "VA", _("VA (Vertical Alignment)")
        TN = "TN", _("TN (Twisted Nematic)")
        OLED = "OLED", _("OLED (Organic Light-Emitting Diode)")
        QLED = "QLED", _("QLED (Quantum Dot LED)")

    class AspectRatio(models.TextChoices):
        _16_9 = "16:9", _("16:9")
        _16_10 = "16:10", _("16:10")
        _21_9 = "21:9", _("21:9 (Ultrawide)")
        _32_9 = "32:9", _("32:9 (Super Ultrawide)")
        _4_3 = "4:3", _("4:3")

    screen_size_inches = models.DecimalField(
        verbose_name=_("screen size (inches)"),
        max_digits=4,
        decimal_places=1,
        help_text=_("Diagonal screen size in inches (e.g., 27.0)"),
    )

    resolution = models.CharField(
        verbose_name=_("resolution"),
        max_length=50,
        help_text=_("e.g. 1920x1080 (Full HD), 2560x1440 (QHD), 3840x2160 (4K UHD)"),
    )

    refresh_rate_hz = models.PositiveIntegerField(
        verbose_name=_("refresh rate (Hz)"), help_text=_("e.g. 60, 75, 144, 240")
    )

    response_time_ms = models.DecimalField(
        verbose_name=_("response time (ms)"),
        max_digits=4,
        decimal_places=1,
        help_text=_("e.g. 1ms, 5ms, 14ms (Gray-to-Gray)"),
    )

    panel_type = models.CharField(
        verbose_name=_("panel type"),
        max_length=10,
        choices=PanelType.choices,
        default=PanelType.IPS,
    )

    aspect_ratio = models.CharField(
        verbose_name=_("aspect ratio"),
        max_length=10,
        choices=AspectRatio.choices,
        default=AspectRatio._16_9,
    )

    brightness_nits = models.PositiveIntegerField(
        verbose_name=_("brightness (nits)"),
        null=True,
        blank=True,
        help_text=_("Peak brightness in candelas per square meter (e.g. 300, 400)"),
    )

    contrast_ratio = models.CharField(
        verbose_name=_("contrast ratio"),
        max_length=20,
        null=True,
        blank=True,
        help_text=_("e.g. 1000:1, 3000:1, 1000000:1 (dynamic)"),
    )

    ports = models.TextField(
        verbose_name=_("ports"),
        blank=True,
        help_text=_(
            "List of available ports (e.g., HDMI 2.0 x2, DisplayPort 1.4 x1, USB-C)"
        ),
    )

    has_speakers = models.BooleanField(
        verbose_name=_("built-in speakers"), default=False
    )

    vrr_technology = models.CharField(
        verbose_name=_("VRR technology"),
        max_length=50,
        blank=True,
        help_text=_("e.g. FreeSync, G-Sync Compatible, G-Sync Ultimate"),
    )

    warranty_months = models.PositiveIntegerField(
        verbose_name=_("warranty (months)"), default=12
    )

    class Meta:
        verbose_name = _("Monitor")
        verbose_name_plural = _("Monitors")

    def __str__(self):
        return (
            f'{self.brand} {self.model} ({self.resolution}, {self.screen_size_inches}")'
        )


class InternalHDD(GlobalMixin):
    # --- مشخصات فنی اصلی HDD ---
    capacity_tb = models.DecimalField(
        verbose_name=_("Capacity (TB)"),
        max_digits=6,
        decimal_places=4,  # مثلاً 1TB, 2TB, 4TB, 8TB
        help_text=_("Storage capacity in Terabytes"),
    )
    interface = models.CharField(
        verbose_name=_("Interface"),
        max_length=20,
        choices=[
            ("SATA II", "SATA II"),
            ("SATA III", "SATA III"),
            # SATA III 6Gb/s رایج‌ترین است
        ],
        default="SATA III",
        help_text=_("Connection interface (e.g., SATA III)"),
    )
    form_factor = models.CharField(
        verbose_name=_("Form Factor"),
        max_length=10,
        choices=[
            ("3.5 inch", "3.5 inch"),
            ("2.5 inch", "2.5 inch"),  # برای برخی هارد های اکسترنال یا هیبریدی
        ],
        default="3.5 inch",
        help_text=_("Physical size of the drive"),
    )
    rpm = models.CharField(
        verbose_name=_("Rotations Per Minute (RPM)"),
        max_length=10,
        choices=[
            ("5400", "5400 RPM"),
            ("7200", "7200 RPM"),
            ("10K", "10000 RPM"),  # کمتر رایج برای HDD های معمولی
            ("15K", "15000 RPM"),  # بیشتر برای Enterprise
        ],
        default="7200",
        help_text=_("Disk rotation speed"),
    )
    cache_mb = models.PositiveIntegerField(
        verbose_name=_("Cache (MB)"),
        default=64,
        help_text=_("Cache memory size in Megabytes"),
    )

    # --- ویژگی‌های پیشرفته‌تر (اختیاری) ---
    is_external = models.BooleanField(
        verbose_name=_("Is External"),
        default=False,
        help_text=_(
            "Check if this is an external HDD (though the model name implies internal)"
        ),
    )
    power_consumption_watts = models.DecimalField(
        verbose_name=_("Power Consumption (Watts)"),
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text=_("Typical power consumption while active"),
    )
    operating_temperature_celsius = models.CharField(
        verbose_name=_("Operating Temperature"),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("e.g., 0°C to 60°C"),
    )
    warranty_years = models.PositiveIntegerField(
        verbose_name=_("Warranty (Years)"),
        null=True,
        blank=True,
        help_text=_("Manufacturer's warranty period in years"),
    )

    class Meta:
        verbose_name = _("Internal HDD")
        verbose_name_plural = _("Internal HDDs")
        # اگر بخواهیم brand و name را برای جلوگیری از تکرار منحصر به فرد کنیم:
        # unique_together = ('brand', 'name', 'capacity_tb', 'rpm')

    def __str__(self):
        return f"{self.brand} {self.model} ({self.capacity_tb}TB, {self.rpm}, {self.form_factor})"


class PreBuiltPC(GlobalMixin):
    # --- قطعات اصلی ---
    cpu = models.ForeignKey(
        to=CPUModel,
        on_delete=models.PROTECT,
        related_name="prebuilt_pcs",
        verbose_name=_("CPU"),
    )
    motherboard = models.ForeignKey(
        to=MotherBoard,
        on_delete=models.PROTECT,
        related_name="prebuilt_pcs",
        verbose_name=_("Motherboard"),
    )
    gpu = models.ForeignKey(
        to=GraphicsCard,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="prebuilt_pcs",
        verbose_name=_("Graphics Card"),
    )

    # --- ماژول‌های RAM ---
    # این بخش رو با دقت بیشتری تعریف می‌کنیم:
    ram_type = models.ForeignKey(
        verbose_name=_("RAM Type"), to=RAMTypesSupported, on_delete=models.PROTECT
    )  # مثال: DDR4, DDR5
    ram_capacity_gb = models.PositiveIntegerField(
        verbose_name=_("Total RAM Capacity (GB)")
    )
    ram_modules_count = models.PositiveIntegerField(
        verbose_name=_("RAM Modules Count"), default=2
    )
    # اگر بخواهیم تک تک ماژول ها رو هم در نظر بگیریم، باید از ManyToManyField استفاده کنیم
    # ram_modules = models.ManyToManyField(RAM, related_name='prebuilt_pcs', verbose_name=_("RAM Modules"))

    # --- فضای ذخیره‌سازی ---
    internal_ssd = models.ForeignKey(
        to=SSD,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prebuilt_pcs",
        verbose_name=_("Internal SSD"),
    )
    internal_m2_ssd = models.ForeignKey(
        to=M2SSD,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prebuilt_pcs_m2",
        verbose_name=_("Internal M.2 SSD"),
    )
    internal_hdd = models.ForeignKey(
        InternalHDD,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prebuilt_pcs",
        verbose_name=_("Internal HDD"),
    )
    # برای چند SSD/HDD:
    # additional_ssds = models.ManyToManyField(InternalSSD, related_name='prebuilt_pcs_additional', blank=True, verbose_name=_("Additional SSDs"))
    # additional_hdds = models.ManyToManyField(InternalHDD, related_name='prebuilt_pcs_additional', blank=True, verbose_name=_("Additional HDDs"))

    # --- کیس و پاور ---
    case = models.ForeignKey(
        to=ComputerCase,
        on_delete=models.PROTECT,
        related_name="prebuilt_pcs",
        verbose_name=_("Case"),
    )
    power_supply_wattage = models.PositiveIntegerField(
        verbose_name=_("Power Supply Wattage (W)"),
        help_text=_("Total wattage of the PSU"),
    )

    # --- سیستم عامل ---
    operating_system = models.ForeignKey(
        to=OperationSystemsSupported,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prebuilt_pcs",
        verbose_name=_("Operating System"),
    )

    # --- مشخصات عمومی و وزن ---
    weight_kg = models.DecimalField(
        verbose_name=_("total weight (kg)"),
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        help_text=_("Total weight of the pre-built PC"),
    )

    # --- فیلدهای اضافی برای بهبود جستجو و نمایش ---
    form_factor = (
        models.CharField(  # برای جستجوی سریع‌تر کیس‌های آماده بر اساس فرم فاکتور
            verbose_name=_("Form Factor"),
            max_length=30,
            blank=True,
            null=True,
            help_text=_(
                "e.g., Full Tower, Mid Tower, Mini-ITX (matches case form factor)"
            ),
        )
    )

    target_audience = models.CharField(  # مثلاً Gaming, Workstation, Home Use
        verbose_name=_("Target Audience"),
        max_length=50,
        blank=True,
        null=True,
        help_text=_("e.g., Gaming, Workstation, Home Use, Professional"),
    )

    # --- نمایش قیمت و تصاویر (از GlobalMixin) ---
    # price, main_image, images, description, brand, model ...

    class Meta:
        verbose_name = _("Pre-built PC")
        verbose_name_plural = _("Pre-built PCs")

    def __str__(self):
        cpu_model = self.cpu.model if self.cpu else _("N/A")
        gpu_model = self.gpu.model if self.gpu else _("N/A")
        os_name = self.operating_system.name if self.operating_system else _("No OS")
        return f"{self.brand} {self.model} ({cpu_model} / {gpu_model} / {self.ram_capacity_gb}GB RAM / {os_name})"

    def save(self, *args, **kwargs):
        # به طور خودکار فرم فاکتور کیس رو در این مدل هم ذخیره کن
        if self.case and not self.form_factor:
            self.form_factor = self.case.form_factor
        super().save(*args, **kwargs)


class AllInOnePC(GlobalMixin):
    # --- مشخصات نمایشگر ---
    screen_size_inches = models.DecimalField(
        verbose_name=_("Screen Size (inches)"),
        max_digits=4,
        decimal_places=1,
        help_text=_("Diagonal screen size in inches"),
    )
    screen_resolution = models.CharField(
        verbose_name=_("Screen Resolution"),
        max_length=30,
        help_text=_("e.g., 1920x1080 (Full HD), 2560x1440 (QHD), 3840x2160 (4K)"),
    )
    screen_type = models.CharField(
        verbose_name=_("Screen Type"),
        max_length=30,
        choices=[
            ("IPS", "IPS"),
            ("OLED", "OLED"),
            ("TN", "TN"),
            ("VA", "VA"),
            (
                "LED",
                "LED",
            ),  # معمولاً backlight نمایشگر است، اما گاهی به عنوان نوع کلی ذکر می‌شود
        ],
        default="IPS",
        help_text=_("Display panel technology"),
    )
    touchscreen = models.BooleanField(
        verbose_name=_("Touchscreen"),
        default=False,
        help_text=_("Whether the screen supports touch input"),
    )
    refresh_rate_hz = models.PositiveIntegerField(
        verbose_name=_("Refresh Rate (Hz)"),
        default=60,
        help_text=_("Screen's refresh rate in Hertz"),
    )

    # --- مشخصات قطعات داخلی ---
    # CPU, Motherboard, GPU, RAM, Storage و ... مشابه PreBuiltPC
    # برای سادگی، فقط به مهم‌ترین‌ها اشاره می‌کنیم.
    # در یک پیاده‌سازی واقعی، این‌ها باید ForeignKey به مدل‌های مربوطه باشند.
    cpu_model_name = models.CharField(max_length=100, verbose_name=_("CPU Model"))
    ram_capacity_gb = models.PositiveIntegerField(verbose_name=_("RAM Capacity (GB)"))
    ram_type = models.ForeignKey(
        to=RAMTypesSupported, on_delete=models.DO_NOTHING, verbose_name=_("RAM Type")
    )  # مثال: DDR4, DDR5
    storage_type = models.CharField(
        verbose_name=_("Storage Type"),
        max_length=20,
        choices=[("SSD", "SSD"), ("HDD", "HDD"), ("Hybrid", "Hybrid")],
        default="SSD",
    )
    storage_capacity_gb = models.PositiveIntegerField(
        verbose_name=_("Storage Capacity (GB)")
    )
    gpu_model_name = models.CharField(
        max_length=100,
        verbose_name=_("GPU Model"),
        blank=True,
        null=True,
        help_text=_("Dedicated graphics card model name (if applicable)"),
    )

    # --- سیستم عامل ---
    operating_system = models.ForeignKey(
        verbose_name=_("Operating System"),
        to=OperationSystemsSupported,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_("e.g., Windows 11, macOS Sonoma, ChromeOS"),
        related_name="all_in_on_pc_operating_system",
    )

    # --- اتصال‌ها و پورت‌ها ---
    ports_description = models.TextField(
        verbose_name=_("Ports Description"),
        blank=True,
        null=True,
        help_text=_("List of available ports (e.g., USB-A, USB-C, HDMI, Ethernet)"),
    )

    # --- صدا و دوربین ---
    has_webcam = models.BooleanField(verbose_name=_("Built-in Webcam"), default=False)
    webcam_resolution = models.CharField(
        verbose_name=_("Webcam Resolution"),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("e.g., 720p, 1080p"),
    )
    audio_description = models.TextField(
        verbose_name=_("Audio Description"),
        blank=True,
        null=True,
        help_text=_("Details about built-in speakers or audio system"),
    )

    # --- سایر مشخصات ---
    weight_kg = models.DecimalField(
        verbose_name=_("Weight (kg)"),
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
    )
    wireless_connectivity = models.CharField(
        verbose_name=_("Wireless Connectivity"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("e.g., Wi-Fi 6, Bluetooth 5.2"),
    )
    included_peripherals = models.CharField(
        verbose_name=_("Included Peripherals"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("e.g., Wireless Keyboard and Mouse"),
    )
    colors = models.ManyToManyField(to=Colors, verbose_name=_("Colors"))

    class Meta:
        verbose_name = _("All-in-One PC")
        verbose_name_plural = _("All-in-One PCs")

    def __str__(self):
        return f'{self.brand} {self.model} ({self.screen_size_inches}" Screen)'


class Laptop(GlobalMixin):
    # --- مشخصات نمایشگر ---
    screen_size_inches = models.DecimalField(
        verbose_name=_("Screen Size (inches)"),
        max_digits=4,
        decimal_places=1,
        help_text=_("Diagonal screen size in inches"),
    )
    screen_resolution = models.CharField(
        verbose_name=_("Screen Resolution"),
        max_length=30,
        help_text=_("e.g., 1920x1080 (Full HD), 2560x1440 (QHD), 3840x2160 (4K)"),
    )
    screen_refresh_rate_hz = models.PositiveIntegerField(
        verbose_name=_("Screen Refresh Rate (Hz)"),
        default=60,
        help_text=_("Screen's refresh rate in Hertz"),
    )
    screen_panel_type = models.CharField(
        verbose_name=_("Screen Panel Type"),
        max_length=30,
        choices=[
            ("IPS", "IPS"),
            ("OLED", "OLED"),
            ("TN", "TN"),
            ("VA", "VA"),
            ("LED", "LED"),
        ],
        default="IPS",
        help_text=_("Display panel technology"),
    )
    touchscreen = models.BooleanField(
        verbose_name=_("Touchscreen"),
        default=False,
        help_text=_("Whether the screen supports touch input"),
    )
    aspect_ratio = models.CharField(
        verbose_name=_("Aspect Ratio"),
        max_length=10,
        blank=True,
        null=True,
        choices=[
            ("16:9", "16:9"),
            ("16:10", "16:10"),
            ("3:2", "3:2"),
            ("21:9", "21:9"),
        ],
        default="16:9",
        help_text=_("Screen's aspect ratio"),
    )

    # --- مشخصات پردازشی ---
    # استفاده از ForeignKey به مدل CPU پیشنهادی است
    # cpu = models.ForeignKey(CPU, on_delete=models.PROTECT, verbose_name=_("CPU"))
    cpu_model_name = models.CharField(
        max_length=100, verbose_name=_("CPU Model Name")
    )  # نام دقیق مدل CPU
    cpu_cores = models.PositiveIntegerField(
        verbose_name=_("CPU Cores"), help_text=_("Number of physical CPU cores")
    )
    cpu_threads = models.PositiveIntegerField(
        verbose_name=_("CPU Threads"),
        help_text=_("Number of CPU threads (including hyper-threading)"),
    )

    # --- حافظه رم ---
    # استفاده از ForeignKey به مدل RAM پیشنهادی است
    # ram = models.ForeignKey(RAM, on_delete=models.PROTECT, verbose_name=_("RAM Configuration"))
    ram_type = models.ForeignKey(
        to=RAMTypesSupported,
        on_delete=models.DO_NOTHING,
        verbose_name=_("RAM Type"),
        help_text=_("e.g., DDR4, DDR5, LPDDR4x"),
    )
    ram_capacity_gb = models.PositiveIntegerField(verbose_name=_("RAM Capacity (GB)"))
    ram_speed_mhz = models.PositiveIntegerField(
        verbose_name=_("RAM Speed (MHz)"), null=True, blank=True
    )
    ram_modules_count = models.PositiveIntegerField(
        verbose_name=_("RAM Modules Count"),
        null=True,
        blank=True,
        help_text=_("e.g., 1 for single-channel, 2 for dual-channel"),
    )

    # --- ذخیره‌سازی ---
    # استفاده از ForeignKey به مدل Storage (یا مدل‌های SSD/HDD جداگانه) پیشنهادی است
    # storage = models.ForeignKey(Storage, on_delete=models.PROTECT, verbose_name=_("Storage"))
    storage_type = models.CharField(
        verbose_name=_("Primary Storage Type"),
        max_length=10,
        choices=[
            ("SSD", "SSD"),
            ("NVMe SSD", "NVMe SSD"),
            ("HDD", "HDD"),
            ("Hybrid", "Hybrid"),
        ],
        default="SSD",
    )
    storage_capacity_gb = models.PositiveIntegerField(
        verbose_name=_("Primary Storage Capacity (GB)")
    )
    secondary_storage_type = models.CharField(
        verbose_name=_("Secondary Storage Type"),
        max_length=10,
        choices=[
            ("SSD", "SSD"),
            ("NVMe SSD", "NVMe SSD"),
            ("HDD", "HDD"),
            ("None", "None"),
        ],
        default="None",
        blank=True,
        null=True,
    )
    secondary_storage_capacity_gb = models.PositiveIntegerField(
        verbose_name=_("Secondary Storage Capacity (GB)"), blank=True, null=True
    )

    # --- گرافیک ---
    # استفاده از ForeignKey به مدل GPU پیشنهادی است
    # gpu = models.ForeignKey(GPU, on_delete=models.PROTECT, verbose_name=_("GPU"))
    gpu_model_name = models.CharField(
        max_length=100,
        verbose_name=_("GPU Model Name"),
        blank=True,
        null=True,
        help_text=_(
            "Dedicated graphics card model name (e.g., NVIDIA GeForce RTX 4060, AMD Radeon RX 7700S)"
        ),
    )
    gpu_vram_gb = models.PositiveIntegerField(
        verbose_name=_("GPU VRAM (GB)"),
        null=True,
        blank=True,
        help_text=_("Video RAM capacity for dedicated GPU"),
    )
    integrated_graphics = models.BooleanField(
        verbose_name=_("Integrated Graphics"),
        default=False,
        help_text=_(
            "Whether it has integrated graphics (e.g., Intel Iris Xe, AMD Radeon Graphics)"
        ),
    )

    # --- سیستم عامل ---
    # استفاده از ForeignKey به مدل OperatingSystem پیشنهادی است
    # operating_system = models.ForeignKey(OperatingSystem, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Operating System"))
    operating_system_name = models.ForeignKey(
        to=OperationSystemsSupported,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Operating System Name"),
        blank=True,
        null=True,
        help_text=_("e.g., Windows 11 Home, macOS Sonoma, Linux Ubuntu"),
    )
    os_preinstalled = models.BooleanField(
        verbose_name=_("OS Pre-installed"), default=True
    )

    # --- باتری و تغذیه ---
    battery_capacity_wh = models.DecimalField(
        verbose_name=_("Battery Capacity (Wh)"),
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        help_text=_("Battery capacity in Watt-hours"),
    )
    battery_cells = models.PositiveIntegerField(
        verbose_name=_("Battery Cells"),
        null=True,
        blank=True,
        help_text=_("Number of cells in the battery"),
    )
    ac_adapter_watts = models.PositiveIntegerField(
        verbose_name=_("AC Adapter (Watts)"), null=True, blank=True
    )

    # --- ابعاد و وزن ---
    weight_kg = models.DecimalField(
        verbose_name=_("Weight (kg)"),
        max_digits=5,
        decimal_places=2,
        help_text=_("Total weight of the laptop"),
    )
    dimensions_cm = models.CharField(
        verbose_name=_("Dimensions (cm)"),
        max_length=30,
        blank=True,
        null=True,
        help_text=_("e.g., 35.8 x 24.5 x 1.8"),
    )

    # --- اتصالات و پورت‌ها ---
    ports_usb_a = models.PositiveIntegerField(verbose_name=_("USB-A Ports"), default=0)
    ports_usb_c = models.PositiveIntegerField(verbose_name=_("USB-C Ports"), default=0)
    ports_thunderbolt = models.PositiveIntegerField(
        verbose_name=_("Thunderbolt Ports"), default=0
    )
    ports_hdmi = models.BooleanField(verbose_name=_("HDMI Port"), default=False)
    ports_ethernet = models.BooleanField(verbose_name=_("Ethernet Port"), default=False)
    ports_audio_jack = models.BooleanField(verbose_name=_("Audio Jack"), default=True)
    ports_sd_card_reader = models.BooleanField(
        verbose_name=_("SD Card Reader"), default=False
    )
    wireless_wifi = models.CharField(
        verbose_name=_("Wi-Fi Standard"),
        max_length=30,
        blank=True,
        null=True,
        help_text=_("e.g., Wi-Fi 6, Wi-Fi 6E, Wi-Fi 7"),
    )
    wireless_bluetooth_version = models.CharField(
        verbose_name=_("Bluetooth Version"),
        max_length=10,
        blank=True,
        null=True,
        help_text=_("e.g., 5.0, 5.2, 5.3"),
    )

    # --- ورودی ---
    keyboard_layout = models.CharField(
        verbose_name=_("Keyboard Layout"),
        max_length=50,
        default="QWERTY",
        help_text=_("e.g., QWERTY, QWERTZ, AZERTY, Farsi QWERTY"),
    )
    backlit_keyboard = models.BooleanField(
        verbose_name=_("Backlit Keyboard"), default=False
    )
    numeric_keypad = models.BooleanField(
        verbose_name=_("Numeric Keypad"), default=False
    )
    touchpad_type = models.CharField(
        verbose_name=_("Touchpad Type"),
        max_length=30,
        default="Standard",
        help_text=_("e.g., Standard, Precision Touchpad, Glass Touchpad"),
    )

    # --- صدا و دوربین ---
    has_webcam = models.BooleanField(verbose_name=_("Built-in Webcam"), default=False)
    webcam_resolution = models.CharField(
        verbose_name=_("Webcam Resolution"),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("e.g., 720p, 1080p"),
    )
    audio_features = models.CharField(
        verbose_name=_("Audio Features"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("e.g., Stereo Speakers, Dolby Atmos, Noise-cancelling Mics"),
    )

    # --- موارد دیگر ---
    build_materials = models.CharField(
        verbose_name=_("Build Materials"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("e.g., Aluminum Alloy, Plastic, Carbon Fiber"),
    )
    color_options = models.ManyToManyField(
        verbose_name=_("Color Options"),
        to=Colors,
        help_text=_("e.g., Silver, Space Gray, Black, Blue"),
    )
    security_features = models.CharField(
        verbose_name=_("Security Features"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("e.g., Fingerprint Reader, TPM 2.0, IR Camera for Windows Hello"),
    )
    warranty_years = models.PositiveIntegerField(
        verbose_name=_("Warranty (Years)"), null=True, blank=True
    )

    class Meta:
        verbose_name = _("Laptop")
        verbose_name_plural = _("Laptops")

    def __str__(self):
        return f'{self.brand} {self.name} ({self.screen_size_inches}" Screen)'


class NewsLetter(models.Model):
    email = models.EmailField(verbose_name=_("Email"), max_length=255, unique=True)
    datetime_created = models.DateTimeField(
        verbose_name=_("Date Time Created"), auto_now_add=True
    )
    datetime_modified = models.DateTimeField(
        verbose_name=_("Last Time Edited"), auto_now=True
    )

    class Meta:
        verbose_name = _("News Letter")
        verbose_name_plural = _("News Letters")


class Favorite(models.Model):
    """
    A generic favorite model that can reference any model in the project.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name=_("User"),  # از gettext_lazy برای قابلیت ترجمه استفاده شده
    )

    # Fields for GenericForeignKey
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="favorite_content_type",
        verbose_name=_("Content Type"),  # از gettext_lazy برای قابلیت ترجمه استفاده شده
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_("Content ID")  # از gettext_lazy برای قابلیت ترجمه استفاده شده
    )
    content_object = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Timestamp"),  # از gettext_lazy برای قابلیت ترجمه استفاده شده
    )

    class Meta:
        verbose_name = _("Favorite")  # از gettext_lazy برای قابلیت ترجمه استفاده شده
        verbose_name_plural = _(
            "Favorites"
        )  # از gettext_lazy برای قابلیت ترجمه استفاده شده

        # Modern and recommended way to define unique constraints
        constraints = [
            models.UniqueConstraint(
                fields=["user", "content_type", "object_id"],
                name="unique_user_favorite_item",
            )
        ]

    def __str__(self):
        """
        String representation of the Favorite object.
        """
        try:
            # Attempt to get a meaningful representation of the content object
            # این قسمت هم اگر بخواهید ترجمه شود باید از _ استفاده کند
            return f"{_('Favorite of')} {self.content_object} {_('by')} {self.user.username}"
        except Exception:
            # Fallback if content_object representation fails
            return (
                f"{_('Favorite for user')} {self.user.username} ({_('ID')}: {self.id})"
            )

    @staticmethod
    def add_to_favorites(user, item):
        content_type = ContentType.objects.get_for_model(item)
        object_id = item.pk

        favorite, created = Favorite.objects.get_or_create(
            user=user, content_type=content_type, object_id=object_id
        )
        return favorite if created else None

    @staticmethod
    def remove_from_favorites(user, item):
        """
        Removes an item from the user's favorites.
        Returns True if removal was successful, False otherwise.
        """
        content_type = ContentType.objects.get_for_model(item)
        object_id = item.pk
        try:
            favorite = Favorite.objects.get(
                user=user, content_type=content_type, object_id=object_id
            )
            favorite.delete()
            return True
        except Favorite.DoesNotExist:
            return False

    @staticmethod
    def is_favorited(user_id, obj):
        return Favorite.objects.filter(
            user_id=user_id,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
        ).exists()


class Comment(models.Model):
    """
    A generic comment model that allows users to comment on any object.
    Supports threaded replies via the 'parent' field.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("User"),
    )

    # Generic foreign key target
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Content Type"),
    )
    object_id = models.PositiveIntegerField(verbose_name=_("Object ID"))
    content_object = GenericForeignKey("content_type", "object_id")

    # Comment fields
    text = models.TextField(verbose_name=_("Comment Text"))

    # For replies
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies",
        verbose_name=_("Parent Comment"),
    )

    is_approved = models.BooleanField(default=True, verbose_name=_("Approved"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{_('Comment by')} {self.user.username} ({self.created_at:%Y-%m-%d})"

    @staticmethod
    def add_comment(user, item, text, parent=None):
        """
        Creates a new comment for a given item (any model).
        Supports replying via the parent argument.
        """
        content_type = ContentType.objects.get_for_model(item)
        return Comment.objects.create(
            user=user,
            content_type=content_type,
            object_id=item.pk,
            text=text,
            parent=parent,
            created_at=timezone.now(),
        )

    @staticmethod
    def get_comments_for_item(item, only_approved=True):
        """
        Returns root-level comments for an item (not replies),
        with optional approval filtering.
        """
        qs = Comment.objects.filter(
            content_type=ContentType.objects.get_for_model(item),
            object_id=item.pk,
            parent__isnull=True,
        )
        if only_approved:
            qs = qs.filter(is_approved=True)
        return qs


class Rating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name=_("User"),
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name=_("Content Type"),
    )
    object_id = models.PositiveIntegerField(verbose_name=_("Object ID"))
    content_object = GenericForeignKey("content_type", "object_id")

    # اصلی‌ترین قسمت
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_("Rating Score"),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "content_type", "object_id"],
                name="unique_user_rating_item",
            )
        ]

    def __str__(self):
        return f"{self.score} ⭐ ({self.user.username})"

    @staticmethod
    def rate(user, item, score):
        """
        Creates or updates a rating for the item.
        """
        content_type = ContentType.objects.get_for_model(item)
        obj, created = Rating.objects.update_or_create(
            user=user,
            content_type=content_type,
            object_id=item.pk,
            defaults={"score": score},
        )
        return obj

    @staticmethod
    def get_average_rating(item):
        """
        Returns the average rating for the item.
        """
        content_type = ContentType.objects.get_for_model(item)
        qs = Rating.objects.filter(content_type=content_type, object_id=item.pk)
        return qs.aggregate(models.Avg("score"))["score__avg"]

    @staticmethod
    def get_user_rating(user, obj):
        if not user.is_authenticated:
            return None
        ct = ContentType.objects.get_for_model(obj)
        return Rating.objects.filter(
            user=user, content_type=ct, object_id=obj.pk
        ).first()

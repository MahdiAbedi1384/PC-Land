# shop/documents.py

from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry

from .models import (
    Laptop,
    Monitor,
    AllInOnePC,
    CPUModel,
    GraphicsCard,
    MotherBoard,
    SSD,
    ComputerCase,
    Keyboard,
    Mouse,
    FlashDrive,
    ExternalSSD,
    PreBuiltPC,
)

# ============== ایندکس عمومی (بدون ثبت در registry) ==============
# این ایندکس را مستقیماً registry.register نمی‌کنیم
# چون مدل Django مشخصی ندارد

products_index = Index("products")
products_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
    analysis={
        "analyzer": {
            "persian_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": ["lowercase", "stop", "arabic_normalization"],
            }
        }
    },
)


class ProductDocument(Document):
    """Document عمومی برای تمام محصولات قابل جستجو - بدون ثبت در registry"""

    content_type = fields.IntegerField()
    model_name = fields.TextField()
    object_id = fields.IntegerField()

    name = fields.TextField(analyzer="persian_analyzer")
    brand = fields.TextField(analyzer="persian_analyzer")
    model = fields.TextField(analyzer="persian_analyzer")
    summary = fields.TextField(analyzer="persian_analyzer")
    description = fields.TextField(analyzer="persian_analyzer")

    price = fields.IntegerField()
    is_active = fields.BooleanField()
    weight = fields.FloatField()

    class Index:
        name = "products"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = None  # این Intentional است - این یک Document انتزاعی است


# ============== Document برای لپ‌تاپ ==============
@registry.register_document
class LaptopDocument(Document):
    screen_size = fields.FloatField(attr="screen_size_inches")
    screen_resolution = fields.KeywordField()
    ram_capacity = fields.IntegerField(attr="ram_capacity_gb")
    ram_type = fields.TextField()
    storage_capacity = fields.IntegerField(attr="storage_capacity_gb")
    storage_type = fields.KeywordField()
    cpu_model = fields.TextField(attr="cpu_model_name")
    gpu_model = fields.TextField(attr="gpu_model_name")
    weight = fields.FloatField(attr="weight_kg")
    has_touchscreen = fields.BooleanField(attr="touchscreen")
    backlit_keyboard = fields.BooleanField(attr="backlit_keyboard")
    screen_refresh_rate = fields.IntegerField(attr="screen_refresh_rate_hz")

    class Index:
        name = "laptops"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Laptop
        fields = [
            "id",
            "slug",
            "sku",
            "name",
            "brand",
            "model",
            "price",
            "summary",
            "description",
            "is_active",
            "main_image",
            "datetime_created",
        ]


# ============== Document برای مانیتور ==============
@registry.register_document
class MonitorDocument(Document):
    screen_size = fields.FloatField(attr="screen_size_inches")
    resolution = fields.KeywordField()
    refresh_rate = fields.IntegerField(attr="refresh_rate_hz")
    response_time = fields.FloatField(attr="response_time_ms")
    panel_type = fields.KeywordField()
    aspect_ratio = fields.KeywordField()
    has_speakers = fields.BooleanField()

    class Index:
        name = "monitors"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Monitor
        fields = [
            "id",
            "slug",
            "sku",
            "name",
            "brand",
            "model",
            "price",
            "summary",
            "description",
            "is_active",
            "main_image",
            "datetime_created",
        ]


# ============== Document برای کیبورد ==============
@registry.register_document
class KeyboardDocument(Document):
    connection_type = fields.KeywordField()
    switch_type = fields.KeywordField()
    layout = fields.KeywordField()
    has_numeric_pad = fields.BooleanField()
    backlight = fields.KeywordField()
    is_mechanical = fields.BooleanField()

    class Index:
        name = "keyboards"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Keyboard
        fields = [
            "id",
            "slug",
            "sku",
            "name",
            "brand",
            "model",
            "price",
            "summary",
            "description",
            "is_active",
            "main_image",
            "datetime_created",
        ]


# ============== Document برای موس ==============
@registry.register_document
class MouseDocument(Document):
    connection_type = fields.KeywordField()
    sensor_type = fields.KeywordField()
    dpi_max = fields.IntegerField()
    button_count = fields.IntegerField()
    has_scroll_wheel = fields.BooleanField()
    rgb_lighting = fields.BooleanField()
    hand_orientation = fields.KeywordField()

    class Index:
        name = "mice"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Mouse
        fields = [
            "id",
            "slug",
            "sku",
            "name",
            "brand",
            "model",
            "price",
            "summary",
            "description",
            "is_active",
            "main_image",
            "datetime_created",
        ]


# ============== Document برای CPU ==============
@registry.register_document
class CPUDocument(Document):
    socket = fields.KeywordField()
    cores = fields.IntegerField()
    threads = fields.IntegerField()
    base_frequency = fields.IntegerField()
    boosted_frequency = fields.IntegerField()
    cpu_series = fields.KeywordField()
    cpu_generation = fields.IntegerField()
    has_igpu = fields.BooleanField()

    class Index:
        name = "cpus"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = CPUModel
        fields = [
            "id",
            "slug",
            "sku",
            "name",
            "brand",
            "model",
            "price",
            "summary",
            "description",
            "is_active",
            "main_image",
            "datetime_created",
        ]


# ============== Document برای گرافیک کارت ==============
@registry.register_document
class GraphicsCardDocument(Document):
    chip_manufacturer = fields.KeywordField()
    vram = fields.FloatField(attr="VRAM")
    vram_type = fields.KeywordField(attr="VRAM_type")
    interface = fields.KeywordField()
    fans_count = fields.IntegerField()

    class Index:
        name = "graphics_cards"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = GraphicsCard
        fields = [
            "id",
            "slug",
            "sku",
            "name",
            "brand",
            "model",
            "price",
            "summary",
            "description",
            "is_active",
            "main_image",
            "datetime_created",
        ]


# ============== Document برای مادربورد ==============
@registry.register_document
class MotherBoardDocument(Document):
    cpu_socket_type = fields.KeywordField()
    chipset = fields.KeywordField()
    memory_slots = fields.IntegerField()
    max_memory_supported = fields.IntegerField()
    form_factor = fields.KeywordField()

    class Index:
        name = "motherboards"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = MotherBoard
        fields = [
            "id",
            "slug",
            "sku",
            "name",
            "brand",
            "model",
            "price",
            "summary",
            "description",
            "is_active",
            "main_image",
            "datetime_created",
        ]


# ============== Document برای SSD ==============
@registry.register_document
class SSDDocument(Document):
    capacity = fields.IntegerField()
    ordered_read_speed = fields.IntegerField()
    ordered_write_speed = fields.IntegerField()
    size = fields.KeywordField()

    class Index:
        name = "ssds"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = SSD
        fields = [
            "id",
            "slug",
            "sku",
            "name",
            "brand",
            "model",
            "price",
            "summary",
            "description",
            "is_active",
            "main_image",
            "datetime_created",
        ]


# ============== Document برای کیس ==============
@registry.register_document
class ComputerCaseDocument(Document):
    size = fields.KeywordField()
    case_form_factor = fields.KeywordField()
    number_of_expansion_slots = fields.IntegerField()

    class Index:
        name = "computer_cases"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = ComputerCase
        fields = [
            "id",
            "slug",
            "sku",
            "name",
            "brand",
            "model",
            "price",
            "summary",
            "description",
            "is_active",
            "main_image",
            "datetime_created",
        ]


# ============== Document برای فلش درایو ==============
@registry.register_document
class FlashDriveDocument(Document):
    capacity = fields.KeywordField()
    connection_type = fields.KeywordField()
    read_speed = fields.IntegerField()
    write_speed = fields.IntegerField()

    class Index:
        name = "flash_drives"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = FlashDrive
        fields = [
            "id",
            "slug",
            "sku",
            "name",
            "brand",
            "model",
            "price",
            "summary",
            "description",
            "is_active",
            "main_image",
            "datetime_created",
        ]


# ============== Document برای External SSD ==============
@registry.register_document
class ExternalSSDDocument(Document):
    capacity = fields.KeywordField()
    interface = fields.KeywordField()
    memory_type = fields.KeywordField()
    read_speed = fields.IntegerField()
    write_speed = fields.IntegerField()

    class Index:
        name = "external_ssds"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = ExternalSSD
        fields = [
            "id",
            "slug",
            "sku",
            "name",
            "brand",
            "model",
            "price",
            "summary",
            "description",
            "is_active",
            "main_image",
            "datetime_created",
        ]


# ============== Document برای All-in-One PC ==============
@registry.register_document
class AllInOnePCDocument(Document):
    screen_size_inches = fields.FloatField()
    screen_resolution = fields.KeywordField()
    screen_type = fields.KeywordField()
    touchscreen = fields.BooleanField()
    ram_capacity_gb = fields.IntegerField()
    storage_capacity_gb = fields.IntegerField()

    class Index:
        name = "all_in_one_pcs"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = AllInOnePC
        fields = [
            "id",
            "slug",
            "sku",
            "name",
            "brand",
            "model",
            "price",
            "summary",
            "description",
            "is_active",
            "main_image",
            "datetime_created",
        ]


# ============== Document برای Pre-built PC ==============
@registry.register_document
class PreBuiltPCDocument(Document):
    ram_capacity_gb = fields.IntegerField()
    power_supply_wattage = fields.IntegerField()
    form_factor = fields.KeywordField()

    class Index:
        name = "prebuilt_pcs"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = PreBuiltPC
        fields = [
            "id",
            "slug",
            "sku",
            "name",
            "brand",
            "model",
            "price",
            "summary",
            "description",
            "is_active",
            "main_image",
            "datetime_created",
        ]

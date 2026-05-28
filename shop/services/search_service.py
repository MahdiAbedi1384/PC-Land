# shop/services/search_service.py

from django.apps import apps
from elasticsearch_dsl import Q, A

from ..documents import (
    LaptopDocument,
    MonitorDocument,
    KeyboardDocument,
    MouseDocument,
    CPUDocument,
    GraphicsCardDocument,
    MotherBoardDocument,
    SSDDocument,
    ComputerCaseDocument,
    FlashDriveDocument,
    ExternalSSDDocument,
    AllInOnePCDocument,
    PreBuiltPCDocument,
)


class SearchService:
    """سرویس جستجوی پیشرفته با Elasticsearch"""

    CATEGORY_DOCUMENTS = {
        "laptops": LaptopDocument,
        "monitors": MonitorDocument,
        "keyboards": KeyboardDocument,
        "mice": MouseDocument,
        "cpus": CPUDocument,
        "graphics_cards": GraphicsCardDocument,
        "motherboards": MotherBoardDocument,
        "ssds": SSDDocument,
        "cases": ComputerCaseDocument,
        "flash_drives": FlashDriveDocument,
        "external_ssds": ExternalSSDDocument,
        "all_in_one_pcs": AllInOnePCDocument,
        "prebuilt_pcs": PreBuiltPCDocument,
        "all": LaptopDocument,
    }

    ALL_DOCUMENTS = [
        LaptopDocument,
        MonitorDocument,
        KeyboardDocument,
        MouseDocument,
        CPUDocument,
        GraphicsCardDocument,
        MotherBoardDocument,
        SSDDocument,
        ComputerCaseDocument,
        FlashDriveDocument,
        ExternalSSDDocument,
        AllInOnePCDocument,
        PreBuiltPCDocument,
    ]

    @classmethod
    def get_available_filters(cls, category):
        """دریافت فیلترهای موجود برای یک دسته‌بندی خاص"""

        filters = {
            "brands": [],
            "specific_filters": "",
        }

        # نگاشت دسته‌بندی به مدل
        model_map = {
            "laptops": "Laptop",
            "monitors": "Monitor",
            "keyboards": "Keyboard",
            "mice": "Mouse",
            "cpus": "CPUModel",
            "graphics_cards": "GraphicsCard",
            "motherboards": "MotherBoard",
            "ssds": "SSD",
            "cases": "ComputerCase",
            "flash_drives": "FlashDrive",
            "external_ssds": "ExternalSSD",
        }

        # دریافت برندها از دیتابیس
        try:
            if category == "all":
                # برای همه دسته‌ها، برندهای پرتکرار را از چند مدل اصلی بگیر
                brand_counts = {}
                main_models = [
                    "Laptop",
                    "Monitor",
                    "Keyboard",
                    "Mouse",
                    "CPUModel",
                    "GraphicsCard",
                ]
                for model_name in main_models:
                    try:
                        model = apps.get_model("shop", model_name)
                        # دریافت برندها با count
                        from django.db.models import Count

                        brands_qs = (
                            model.objects.filter(is_active=True)
                            .values("brand")
                            .annotate(count=Count("id"))
                            .exclude(brand="")
                            .order_by("-count")[:10]
                        )

                        for item in brands_qs:
                            if item["brand"]:
                                brand_counts[item["brand"]] = (
                                    brand_counts.get(item["brand"], 0) + item["count"]
                                )
                    except:
                        pass

                # مرتب‌سازی و محدود کردن به 20 برند
                sorted_brands = sorted(
                    brand_counts.items(), key=lambda x: x[1], reverse=True
                )[:20]
                filters["brands"] = [
                    {"key": brand, "count": count} for brand, count in sorted_brands
                ]

            else:
                model_name = model_map.get(category)
                if model_name:
                    model = apps.get_model("shop", model_name)
                    from django.db.models import Count

                    brands_qs = (
                        model.objects.filter(is_active=True)
                        .values("brand")
                        .annotate(count=Count("id"))
                        .exclude(brand="")
                        .order_by("-count")
                    )

                    filters["brands"] = [
                        {"key": item["brand"], "count": item["count"]}
                        for item in brands_qs
                    ]

        except Exception as e:
            print(f"Error getting brands: {e}")
            filters["brands"] = []

        # فیلترهای اختصاصی
        filters["specific_filters"] = cls._get_specific_filters_html(category)

        return filters

    @classmethod
    def _get_specific_filters_html(cls, category):
        """HTML فیلترهای اختصاصی هر دسته‌بندی"""

        filters_html = ""

        if category == "laptops":
            filters_html = """
                <div class="mb-4">
                    <label class="form-label fw-bold">رم (GB)</label>
                    <div class="filter-group">
                        <div class="form-check"><input class="form-check-input filter-checkbox" type="checkbox" value="8" id="ram_8"><label class="form-check-label" for="ram_8">8 GB</label></div>
                        <div class="form-check"><input class="form-check-input filter-checkbox" type="checkbox" value="16" id="ram_16"><label class="form-check-label" for="ram_16">16 GB</label></div>
                        <div class="form-check"><input class="form-check-input filter-checkbox" type="checkbox" value="32" id="ram_32"><label class="form-check-label" for="ram_32">32 GB</label></div>
                        <div class="form-check"><input class="form-check-input filter-checkbox" type="checkbox" value="64" id="ram_64"><label class="form-check-label" for="ram_64">64 GB</label></div>
                    </div>
                </div>
                <div class="mb-4">
                    <label class="form-label fw-bold">سایز صفحه (اینچ)</label>
                    <div class="row g-2">
                        <div class="col-6"><input type="number" class="form-control" id="screen-min" placeholder="حداقل"></div>
                        <div class="col-6"><input type="number" class="form-control" id="screen-max" placeholder="حداکثر"></div>
                    </div>
                </div>
                <div class="mb-4">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="touchscreen">
                        <label class="form-check-label" for="touchscreen">صفحه لمسی</label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="backlit-keyboard">
                        <label class="form-check-label" for="backlit-keyboard">کیبورد نوردار</label>
                    </div>
                </div>
            """
        elif category == "cpus":
            filters_html = """
                <div class="mb-4">
                    <label class="form-label fw-bold">تعداد هسته</label>
                    <select class="form-select" id="min-cores">
                        <option value="">همه</option>
                        <option value="4">4 هسته و بیشتر</option>
                        <option value="6">6 هسته و بیشتر</option>
                        <option value="8">8 هسته و بیشتر</option>
                        <option value="12">12 هسته و بیشتر</option>
                    </select>
                </div>
                <div class="mb-4">
                    <label class="form-label fw-bold">سوکت</label>
                    <select class="form-select" id="socket">
                        <option value="">همه</option>
                        <option value="LGA1700">LGA1700</option>
                        <option value="AM5">AM5</option>
                        <option value="AM4">AM4</option>
                        <option value="LGA1200">LGA1200</option>
                    </select>
                </div>
            """
        elif category == "graphics_cards":
            filters_html = """
                <div class="mb-4">
                    <label class="form-label fw-bold">سازنده چیپست</label>
                    <select class="form-select" id="chip-manufacturer">
                        <option value="">همه</option>
                        <option value="Nvidia">Nvidia</option>
                        <option value="AMD">AMD</option>
                        <option value="Intel">Intel</option>
                    </select>
                </div>
                <div class="mb-4">
                    <label class="form-label fw-bold">حداقل حافظه VRAM (GB)</label>
                    <select class="form-select" id="min-vram">
                        <option value="">همه</option>
                        <option value="4">4 GB</option>
                        <option value="6">6 GB</option>
                        <option value="8">8 GB</option>
                        <option value="12">12 GB</option>
                        <option value="16">16 GB</option>
                    </select>
                </div>
            """
        elif category == "monitors":
            filters_html = """
                <div class="mb-4">
                    <label class="form-label fw-bold">نوع پنل</label>
                    <select class="form-select" id="panel-type">
                        <option value="">همه</option>
                        <option value="IPS">IPS</option>
                        <option value="VA">VA</option>
                        <option value="TN">TN</option>
                        <option value="OLED">OLED</option>
                    </select>
                </div>
                <div class="mb-4">
                    <label class="form-label fw-bold">حداقل نرخ بروزرسانی (Hz)</label>
                    <select class="form-select" id="min-refresh">
                        <option value="">همه</option>
                        <option value="60">60 Hz</option>
                        <option value="75">75 Hz</option>
                        <option value="120">120 Hz</option>
                        <option value="144">144 Hz</option>
                        <option value="240">240 Hz</option>
                    </select>
                </div>
            """

        return filters_html

    @classmethod
    def search(
        cls,
        query=None,
        category="all",
        min_price=None,
        max_price=None,
        filters=None,
        sort_by=None,
        page=1,
        page_size=20,
    ):
        """جستجوی اصلی - نسخه ساده بدون Elasticsearch"""

        results = []

        # انتخاب مدل‌ها بر اساس دسته‌بندی
        model_map = {
            "laptops": ["Laptop"],
            "monitors": ["Monitor"],
            "keyboards": ["Keyboard"],
            "mice": ["Mouse"],
            "cpus": ["CPUModel"],
            "graphics_cards": ["GraphicsCard"],
            "motherboards": ["MotherBoard"],
            "ssds": ["SSD", "M2SSD"],
            "cases": ["ComputerCase"],
            "all": [
                "Laptop",
                "Monitor",
                "Keyboard",
                "Mouse",
                "CPUModel",
                "GraphicsCard",
                "MotherBoard",
                "SSD",
                "M2SSD",
                "ComputerCase",
                "FlashDrive",
                "ExternalSSD",
            ],
        }

        model_names = model_map.get(category, model_map["all"])

        for model_name in model_names:
            try:
                model = apps.get_model("shop", model_name)
                q_objects = Q(is_active=True)

                if query and query.strip():
                    q_objects &= (
                        Q(name__icontains=query)
                        | Q(brand__icontains=query)
                        | Q(model__icontains=query)
                        | Q(description__icontains=query)
                    )

                if min_price:
                    q_objects &= Q(price__gte=min_price)
                if max_price:
                    q_objects &= Q(price__lte=max_price)

                queryset = model.objects.filter(q_objects)

                for item in queryset:
                    results.append(
                        {
                            "id": item.id,
                            "name": item.name,
                            "brand": item.brand,
                            "model": item.model,
                            "price": item.price,
                            "slug": item.slug,
                            "category": model_name,
                            "main_image": item.main_image.url
                            if item.main_image
                            else None,
                        }
                    )
            except Exception as e:
                print(f"Error searching {model_name}: {e}")

        # مرتب‌سازی
        if sort_by == "price_asc":
            results.sort(key=lambda x: x["price"])
        elif sort_by == "price_desc":
            results.sort(key=lambda x: x["price"], reverse=True)

        total_count = len(results)
        total_pages = (
            (total_count + page_size - 1) // page_size if total_count > 0 else 0
        )

        # صفحه‌بندی
        start = (page - 1) * page_size
        end = start + page_size
        paged_results = results[start:end]

        return {
            "results": paged_results,
            "total_count": total_count,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "query": query,
            "category": category,
        }

    @classmethod
    def autocomplete(cls, query, limit=10):
        """جستجوی زنده (autocomplete) - نسخه ساده"""
        if not query or len(query) < 2:
            return []

        results = []
        models_to_search = [
            "Laptop",
            "Monitor",
            "Keyboard",
            "Mouse",
            "CPUModel",
            "GraphicsCard",
        ]

        for model_name in models_to_search:
            try:
                model = apps.get_model("shop", model_name)
                queryset = model.objects.filter(
                    Q(name__icontains=query) | Q(brand__icontains=query), is_active=True
                )[:limit]

                for item in queryset:
                    results.append(
                        {
                            "id": item.id,
                            "name": item.name,
                            "brand": item.brand,
                            "price": item.price,
                            "category": model_name,
                        }
                    )
            except:
                pass

        return results[:limit]

    @classmethod
    def advanced_search(cls, data):
        """جستجوی پیشرفته"""
        return cls.search(
            query=data.get("query"),
            category=data.get("category", "all"),
            min_price=data.get("min_price"),
            max_price=data.get("max_price"),
            page=data.get("page", 1),
            page_size=data.get("page_size", 20),
        )

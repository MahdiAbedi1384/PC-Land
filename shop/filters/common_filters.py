from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class PriceFilter(admin.SimpleListFilter):
    title = _("Price in Tomans")
    parameter_name = "price"
    LESS_THAN_500_000 = "<500"
    BETWEEN_500_000_AND_1_000_000 = "500=<1000"
    BETWEEN_1_000_000_AND_2_000_000 = "1000=<2000"
    BETWEEN_2_000_000_AND_5_000_000 = "2000=<5000"
    BETWEEN_5_000_000_AND_10_000_000 = "5000=<10000"
    BETWEEN_10_000_000_AND_20_000_000 = "10000=<20000"
    BETWEEN_20_000_000_AND_50_000_000 = "20000=<50000"
    BETWEEN_50_000_000_AND_100_000_000 = "50000=<100000"
    MORE_THAN_100_000_000 = "100000<"

    def lookups(self, request, model_admin):
        return (
            (PriceFilter.LESS_THAN_500_000, _("Less Than 500,000")),
            (
                PriceFilter.BETWEEN_500_000_AND_1_000_000,
                _("Between 500,000 and 1,000,000"),
            ),
            (
                PriceFilter.BETWEEN_1_000_000_AND_2_000_000,
                _("Between 1,000,000 and 2,000,000"),
            ),
            (
                PriceFilter.BETWEEN_2_000_000_AND_5_000_000,
                _("Between 2,000,000 and 5,000,000"),
            ),
            (
                PriceFilter.BETWEEN_5_000_000_AND_10_000_000,
                _("Between 5,000,000 and 10,000,000"),
            ),
            (
                PriceFilter.BETWEEN_10_000_000_AND_20_000_000,
                _("Between 10,000,000 and 20,000,000"),
            ),
            (
                PriceFilter.BETWEEN_20_000_000_AND_50_000_000,
                _("Between 20,000,000 and 50,000,000"),
            ),
            (
                PriceFilter.BETWEEN_50_000_000_AND_100_000_000,
                _("Between 50,000,000 and 100,000,000"),
            ),
            (PriceFilter.MORE_THAN_100_000_000, _("More than 100,000,000")),
        )

    def queryset(self, request, queryset):
        if self.value() == PriceFilter.LESS_THAN_500_000:
            return queryset.filter(price__lte=500_000)
        elif self.value() == PriceFilter.BETWEEN_500_000_AND_1_000_000:
            return queryset.filter(price__range=(500_000, 1_000_000))
        elif self.value() == PriceFilter.BETWEEN_1_000_000_AND_2_000_000:
            return queryset.filter(price__range=(1_000_000, 2_000_000))
        elif self.value() == PriceFilter.BETWEEN_2_000_000_AND_5_000_000:
            return queryset.filter(price__range=(2_000_000, 5_000_000))
        elif self.value() == PriceFilter.BETWEEN_5_000_000_AND_10_000_000:
            return queryset.filter(price__range=(5_000_000, 10_000_000))
        elif self.value() == PriceFilter.BETWEEN_10_000_000_AND_20_000_000:
            return queryset.filter(price__range=(10_000_000, 20_000_000))
        elif self.value() == PriceFilter.BETWEEN_20_000_000_AND_50_000_000:
            return queryset.filter(price__range=(20_000_000, 50_000_000))
        elif self.value() == PriceFilter.MORE_THAN_100_000_000:
            return queryset.filter(price__gte=100_000_000)


class SKUFilter(admin.SimpleListFilter):
    title = _("SKU")
    parameter_name = "sku"
    LESS_THAN_10 = '<10'
    BETWEEN_10_AND_20 = '10<=20'
    BETWEEN_20_AND_50 = '20<=50'
    BETWEEN_50_AND_100 = '50<=100'
    MORE_THAN_100 = '100<'

    def lookups(self, request, model_admin):
        return (
            (SKUFilter.LESS_THAN_10, "less than 10"),
            (SKUFilter.BETWEEN_10_AND_20, "between 10 and 20"),
            (SKUFilter.BETWEEN_20_AND_50, "between 20 and 50"),
            (SKUFilter.BETWEEN_50_AND_100, "between 50 and 100"),
            (SKUFilter.MORE_THAN_100, "more than 100"),
        )

    def queryset(self, request, queryset):
        if self.value() == SKUFilter.LESS_THAN_10:
            return queryset.filter(sku__lte=10)
        elif self.value() == SKUFilter.BETWEEN_10_AND_20:
            return queryset.filter(sku__range=(10, 20))
        elif self.value() == SKUFilter.BETWEEN_20_AND_50:
            return queryset.filter(sku__range=(20, 50))
        elif self.value() == SKUFilter.BETWEEN_50_AND_100:
            return queryset.filter(sku__range=(50, 100))
        elif self.value() == SKUFilter.MORE_THAN_100:
            return queryset.filter(sku__gte=100)


class ColorsFilter(admin.SimpleListFilter):
    """
    Custom filter for ManyToMany field 'colors'.
    """

    title = _("Colors")  # Title shown in the admin interface
    parameter_name = "colors"  # URL parameter for the filter

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples for the filter dropdown.
        Each tuple is (value, label).
        """
        try:
            # Access the ManyToManyField to get the related model
            m2m_field = model_admin.model._meta.get_field("colors")
            related_model = m2m_field.remote_field.model
            # Assuming the Colors model has a 'title' field and a 'pk'
            return [(color.pk, str(color)) for color in related_model.objects.all()]
        except Exception as e:
            print(f"Error getting lookups for colors: {e}")
            return []

    def queryset(self, request, queryset):
        """
        Filters the queryset based on the selected color.
        """
        if self.value():
            # self.value() will be the primary key of the selected color.
            # We filter the main queryset (e.g., BluetoothDongle)
            # to include only those that have the selected color
            # in their 'colors' ManyToMany field.
            return queryset.filter(colors__pk=self.value())
        return queryset

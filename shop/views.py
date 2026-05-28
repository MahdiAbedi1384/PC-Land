import json

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg
from django.http import Http404, HttpResponsePermanentRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.decorators.csrf import (
    csrf_exempt,
)  # برای تست، در production از csrf_token استفاده کنید
from django.views.decorators.http import require_POST

from shop.forms import NewsLetterForm
from shop.models import (
    Laptop,
    Comment,
    Rating,
    Favorite,
    Images,
    Monitor,
    AllInOnePC,
    ExternalSSD,
    FlashDrive,
    Keyboard,
    Mouse,
    CPUModel,
    GraphicsCard,
    MotherBoard,
    InternalHDD,
    SSD,
    M2SSD,
    ComputerRAMModel,
    LapTopRAMModel,
    ComputerCase,
    BluetoothDongle,
    USBHUB,
    ExternalHardDrive,
)
from shop.services.search_service import SearchService


@login_required
def toggle_favorite(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    content_type_id = request.POST.get("content_type")
    object_id = request.POST.get("object_id")

    if not content_type_id or not object_id:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    content_type = ContentType.objects.get(id=content_type_id)

    try:
        obj = content_type.get_object_for_this_type(id=object_id)
    except Exception:
        return JsonResponse({"error": "Object not found"}, status=404)

    # Toggle
    favorited = Favorite.is_favorited(request.user, obj)

    if favorited:
        Favorite.remove_from_favorites(request.user, obj)
        return JsonResponse({"status": "removed"})

    Favorite.add_to_favorites(request.user, obj)
    return JsonResponse({"status": "added"})


@require_POST
def ajax_rate(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "login_required"}, status=403)

    content_type_id = request.POST.get("content_type")
    object_id = request.POST.get("object_id")
    score = request.POST.get("score")

    # validation
    try:
        score = int(score)
        if score < 1 or score > 5:
            raise ValueError()
    except ValueError:
        return JsonResponse({"error": "invalid_score"}, status=400)

    try:
        ct = ContentType.objects.get(id=content_type_id)
        model_class = ct.model_class()
        obj = model_class.objects.get(pk=object_id)
    except Exception:
        return JsonResponse({"error": "object_not_found"}, status=404)

    rating, created = Rating.objects.update_or_create(
        user=request.user,
        content_type=ct,
        object_id=obj.pk,
        defaults={"score": score},
    )

    avg = Rating.get_average_rating(obj)

    messages.success(request, message=_("your rate has been saved successfully"))

    return JsonResponse(
        {
            "success": True,
            "score": rating.score,
            "average": avg,
        }
    )


@require_POST
def ajax_comment(request):
    if not request.user.is_authenticated:
        messages.error(request, message=_("you must login to send comment"))
        return JsonResponse({"error": "login_required"}, status=403)

    content_type_id = request.POST.get("content_type")
    object_id = request.POST.get("object_id")
    text = request.POST.get("text", "").strip()

    if not text:
        messages.error(request, message=_("text is required"))
        return JsonResponse({"error": "empty_comment"}, status=400)

    try:
        ct = ContentType.objects.get(id=content_type_id)
        model_class = ct.model_class()
        obj = model_class.objects.get(pk=object_id)
    except Exception:
        return JsonResponse({"error": "object_not_found"}, status=404)

    c = Comment.objects.create(
        user=request.user, text=text, content_type=ct, object_id=obj.pk
    )

    messages.success(request, message=_("your comment has been saved successfully"))

    return JsonResponse(
        {
            "success": True,
            "comment": {
                "user": str(c.user),
                "text": c.text,
                "created_at": c.created_at.strftime("%Y-%m-%d %H:%M"),
            },
        }
    )


@csrf_exempt  # در production از @require_POST و مدیریت CSRF استفاده کنید
@require_POST
def ajax_load_more_comments(request):
    try:
        data = json.loads(request.body)
        content_type_id = data.get("content_type")
        object_id = data.get("object_id")
        offset = int(data.get("offset", 0))  # از کدام کامنت شروع کنیم
        limit = int(data.get("limit", 5))  # تعداد کامنت برای بارگذاری در هر بار

        content_type = get_object_or_404(ContentType, id=content_type_id)
        obj = content_type.get_object_for_this_type(pk=object_id)

        # دریافت کامنت‌ها به ترتیب تاریخ (جدیدترین اول)
        all_comments = Comment.objects.filter(
            content_type=content_type,
            object_id=object_id,
            is_approved=True,  # فقط کامنت‌های تایید شده
        ).order_by("-created_at")

        # اعمال offset و limit
        comments_to_load = list(all_comments[offset : offset + limit])

        # آماده‌سازی پاسخ JSON
        comments_data = []
        for comment in comments_to_load:
            comments_data.append(
                {
                    "id": comment.id,
                    "user": comment.user.username if comment.user else "کاربر ناشناس",
                    "text": comment.text,
                    "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
                    # می‌توانید فیلدهای بیشتری اضافه کنید
                }
            )

        # بررسی اینکه آیا کامنت بیشتری وجود دارد
        has_more = (offset + limit) < all_comments.count()

        return JsonResponse(
            {
                "success": True,
                "comments": comments_data,
                "has_more": has_more,
                "next_offset": offset + len(comments_data),
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


class HomeView(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["Laptops"] = (
            Laptop.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["monitors"] = (
            Monitor.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["all_in_one_pcs"] = (
            AllInOnePC.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["external_ssds"] = (
            ExternalSSD.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["flash_drive"] = (
            FlashDrive.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["keyboards"] = (
            Keyboard.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["mouses"] = (
            Mouse.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["page_name"] = _("Home")
        return context

    def post(self, request, *args, **kwargs):
        if "newsletter_sub" in request.POST:
            new_subscription = NewsLetterForm(request.POST)
            if new_subscription.is_valid():
                new_subscription.save()
                messages.success(
                    request,
                    _(
                        "Your email successfully added to our database! You will be noticed from all news ASAP!"
                    ),
                )
            else:
                messages.error(request, new_subscription.errors)
        next_page = request.POST.get("next_page")
        if not next_page:
            next_page = reverse_lazy("home")
        return redirect(next_page)


class GenericDetailView(generic.DetailView):
    template_name = "item_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def dispatch(self, request, *args, **kwargs):
        model_name = kwargs["model"]
        self.model = apps.get_model("shop", model_name)

        if not self.model:
            raise Http404("Model not found")

        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        obj = get_object_or_404(
            self.model, pk=self.kwargs["pk"], slug=self.kwargs["slug"]
        )

        # canonical redirect for SEO
        if obj.slug != self.kwargs["slug"]:
            correct_url = reverse(
                "generic_detail",
                kwargs={
                    "app": self.kwargs["app"],
                    "model": self.kwargs["model"],
                    "pk": obj.pk,
                    "slug": obj.slug,
                },
            )
            return HttpResponsePermanentRedirect(correct_url)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object
        user = self.request.user
        ct = ContentType.objects.get_for_model(obj)
        ratings = Rating.objects.filter(content_type=ct, object_id=obj.id)

        context["content_type_id"] = ct.id
        context["object_id"] = obj.pk
        context["is_favorite"] = Favorite.is_favorited(user_id=user.id, obj=obj)

        context["average_rating"] = ratings.aggregate(avg=Avg("score"))["avg"]
        context["user_rating"] = ratings.filter(user_id=user.id).first()
        context["ratings"] = ratings
        context["gallery_images"] = Images.objects.filter(
            content_type=ct, object_id=obj.id
        )
        # Pagination for comments
        comments_qs = Comment.get_comments_for_item(obj)
        page = self.request.GET.get("page", 1)
        paginator = Paginator(comments_qs, 10)  # ← هر صفحه ۱۰ کامنت

        try:
            comments_page = paginator.page(page)
        except PageNotAnInteger:
            comments_page = paginator.page(5)
        except EmptyPage:
            comments_page = paginator.page(paginator.num_pages)

        context["comments_page"] = comments_page
        context["comments_count"] = paginator.count
        context["page_range"] = paginator.page_range

        return context


class AboutUsView(generic.TemplateView):
    template_name = "about_us.html"

    def get_context_data(self, **kwargs):
        context = super(AboutUsView, self).get_context_data(**kwargs)
        context["page_name"] = _("About Us")
        return context


class TermsView(generic.TemplateView):
    template_name = "terms.html"

    def get_context_data(self, **kwargs):
        context = super(TermsView, self).get_context_data(**kwargs)
        context["page_name"] = _("Terms")
        return context


class PrivacyPolicyView(generic.TemplateView):
    template_name = "privacy_policy.html"

    def get_context_data(self, **kwargs):
        context = super(PrivacyPolicyView, self).get_context_data(**kwargs)
        context["page_name"] = _("Privacy Policy")
        return context


class ModelsLoaderView(generic.TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        model_name = kwargs["model"]
        self.model = apps.get_model("shop", model_name)

        if not self.model:
            raise Http404("Model not found")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModelsLoaderView, self).get_context_data(**kwargs)
        context["page_name"] = _(self.model.__name__)
        context["items"] = self.model.objects.filter(is_active=True).only(
            "id", "name", "brand", "model", "price", "main_image", "slug"
        )
        return context


class ComputerPartsView(generic.TemplateView):
    template_name = "computer_parts.html"

    def get_context_data(self, **kwargs):
        context = super(ComputerPartsView, self).get_context_data(**kwargs)
        context["page_name"] = _("Computer Parts")
        context["cpus"] = (
            CPUModel.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["gpus"] = (
            GraphicsCard.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["motherboards"] = (
            MotherBoard.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["hdds"] = (
            InternalHDD.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["ssds"] = (
            SSD.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["m2ssds"] = (
            M2SSD.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["rams"] = (
            ComputerRAMModel.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["laptop_rams"] = (
            LapTopRAMModel.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["cases"] = (
            ComputerCase.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        return context


class AccessoriesView(generic.TemplateView):
    template_name = "accessories.html"

    def get_context_data(self, **kwargs):
        context = super(AccessoriesView, self).get_context_data(**kwargs)
        context["page_name"] = _("Accessories")
        context["bluetoothdongles"] = (
            BluetoothDongle.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["usbhubs"] = (
            USBHUB.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["externalhdds"] = (
            ExternalHardDrive.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["externalssds"] = (
            ExternalSSD.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["flashdrives"] = (
            FlashDrive.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["keyboards"] = (
            Keyboard.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        context["mice"] = (
            Mouse.objects.filter(is_active=True)
            .only("id", "name", "brand", "model", "price", "main_image", "slug")
            .order_by("-pk")[:4]
        )
        return context


class SearchView(generic.TemplateView):
    """View جستجوی پیشرفته با Elasticsearch"""

    template_name = "search_results.html"

    def get(self, request, *args, **kwargs):
        # دریافت پارامترهای جستجو
        query = request.GET.get("q", "").strip()
        category = request.GET.get("category", "all")
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        sort_by = request.GET.get("sort", "relevance")
        page = request.GET.get("page", 1)

        # پردازش فیلترهای اضافی
        filters = {}

        # فیلترهای عمومی
        if request.GET.get("brands"):
            filters["brands"] = request.GET.getlist("brands")

        # فیلترهای اختصاصی لپ‌تاپ
        if category == "laptops":
            if request.GET.get("ram"):
                filters["ram_capacity"] = request.GET.getlist("ram")
            if request.GET.get("screen_size_min") and request.GET.get(
                "screen_size_max"
            ):
                filters["screen_size"] = (
                    float(request.GET.get("screen_size_min")),
                    float(request.GET.get("screen_size_max")),
                )
            if request.GET.get("touchscreen") == "true":
                filters["has_touchscreen"] = True
            if request.GET.get("backlit") == "true":
                filters["backlit_keyboard"] = True

        # فیلترهای اختصاصی CPU
        elif category == "cpus":
            if request.GET.get("min_cores"):
                filters["cores"] = int(request.GET.get("min_cores"))
            if request.GET.get("socket"):
                filters["socket"] = request.GET.get("socket")
            if request.GET.get("has_igpu") == "true":
                filters["has_igpu"] = True

        # فیلترهای اختصاصی گرافیک کارت
        elif category == "graphics_cards":
            if request.GET.get("chip_manufacturer"):
                filters["chip_manufacturer"] = request.GET.get("chip_manufacturer")
            if request.GET.get("min_vram"):
                filters["vram"] = int(request.GET.get("min_vram"))

        # اجرای جستجو
        search_results = SearchService.search(
            query=query,
            category=category,
            min_price=min_price,
            max_price=max_price,
            filters=filters,
            sort_by=sort_by,
            page=int(page),
            page_size=24,  # تعداد محصولات در هر صفحه
        )

        context = self.get_context_data(**kwargs)
        context.update(
            {
                "search_results": search_results,
                "query": query,
                "category": category,
                "min_price": min_price,
                "max_price": max_price,
                "sort_by": sort_by,
                "page_name": _("Search Results"),
            }
        )

        return self.render_to_response(context)


class AutoCompleteView(generic.View):
    """View برای autocomplete جستجو (AJAX)"""

    def get(self, request):
        query = request.GET.get("q", "").strip()
        limit = int(request.GET.get("limit", 10))

        if not query or len(query) < 2:
            return JsonResponse({"results": []})

        results = SearchService.autocomplete(query, limit)

        return JsonResponse({"results": results})


class AdvancedSearchView(generic.View):
    """View برای جستجوی پیشرفته با AJAX"""

    def post(self, request):
        import json

        data = json.loads(request.body)

        results = SearchService.advanced_search(data)

        return JsonResponse(
            {
                "success": True,
                "results": results["results"],
                "total_count": results["total_count"],
                "total_pages": results["total_pages"],
                "current_page": results["page"],
                "suggestions": results["suggestions"],
                "facets": results["facets"],
            }
        )


class GetFiltersView(generic.View):
    """دریافت فیلترهای موجود برای هر دسته‌بندی"""

    def get(self, request):
        category = request.GET.get("category", "all")

        # دریافت فیلترها از سرویس جستجو
        filters = SearchService.get_available_filters(category)

        return JsonResponse(filters)

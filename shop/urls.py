from django.urls import path

from . import views

urlpatterns = [
    path("api/rate/", views.ajax_rate, name="ajax_rate"),
    path("api/comment/", views.ajax_comment, name="ajax_comment"),
    path(
        "api/comments/load_more/",
        views.ajax_load_more_comments,
        name="ajax_load_more_comments",
    ),
    path("", views.HomeView.as_view(), name="home"),
    path(
        "shop/<str:model>/<int:pk>/<path:slug>/",
        views.GenericDetailView.as_view(),
        name="generic_detail",
    ),
    path("about-us/", views.AboutUsView.as_view(), name="about-us"),
    path("terms/", views.TermsView.as_view(), name="terms"),
    path("privacy-policy/", views.PrivacyPolicyView.as_view(), name="privacy-policy"),
    path("toggle-favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("computer-parts/", views.ComputerPartsView.as_view(), name="computer_parts"),
    path("accessories/", views.AccessoriesView.as_view(), name="accessories"),
    path("search/", views.SearchView.as_view(), name="search"),
    path(
        "search/autocomplete/",
        views.AutoCompleteView.as_view(),
        name="search-autocomplete",
    ),
    path(
        "search/advanced/", views.AdvancedSearchView.as_view(), name="search-advanced"
    ),
    path("search/filters/", views.GetFiltersView.as_view(), name="search-filters"),
    path("shop/<str:model>/", views.ModelsLoaderView.as_view(), name="model-loader"),
]

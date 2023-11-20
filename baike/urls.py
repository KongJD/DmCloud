from django.urls import path
from rest_framework.routers import DefaultRouter

from baike import views

router = DefaultRouter()

router.register(r"speciesextra", views.ElasticExtraOtherView, basename="speciesextra")

urlpatterns = [
    path("message/", views.FourView.as_view(), ),
    path("search/", views.ElasticSpeciesView.as_view({"get": "list"}), ),
    path("search_species/", views.ElasticFullSpeciesView.as_view({"get": "list"}), ),
    path("perspecis/", views.PerSpeciesView.as_view(), ),
    path("speciesmorphology/", views.ElasticSpeciesMorpholgyView.as_view({"get": "list"}), ),
    path("speciesphyosical/", views.ElasticsearchPhyosicalView.as_view({"get": "list"}), ),
    path("speciesbiochem/", views.ElasticBiochemistyDaixieView.as_view({"get": "list"}), ),
    path("speciescountry/", views.ElasticCountrySourceView.as_view({"get": "list"}), ),
    path("sp/", views.ElasticGeneInfoView.as_view({"get": "list"}), ),
    path("all/", views.TwoList.as_view(), ),
    path("speciesall/", views.SpeciesMorBioPhyExtra.as_view(), ),
    path("speciesand/", views.SpeciesAndView.as_view(), )
]

urlpatterns += router.urls

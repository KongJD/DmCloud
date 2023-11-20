from collections import defaultdict

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from species.documents import SpeciesDocument, SpeciesDocument1, GeneInfoDocument
from species.models import SpeicesModel, GeneInfoModel


class SearchSerlizer(DocumentSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = SpeicesModel
        document = SpeciesDocument1
        fields = ("species", "species_cn", "status", "count")

    def get_count(self, obj):
        return getattr(obj, "count", 1)
        # queryset = SpeicesModel.objects.using("db1").filter(species=obj.species, species_cn=obj.species_cn, status=obj.status).counyt()
        # return queryset

    # search = self.Meta.document.search()
    # search.aggs.metric('count', 'value_count', field='_id')
    # search.aggs.bucket('group_by_species', 'terms', field='species.raw', )
    # search.aggs.bucket('group_by_species_cn', 'terms', field='species_cn.raw', )
    # search.aggs.bucket('group_by_status', 'terms', field='status.raw', )
    #
    # response = search.execute()
    # print(response)
    # buckets_species = response.aggregations.group_by_species.buckets
    # print(buckets_species)
    # buckets_species_cn = response.aggregations.group_by_species_cn.buckets
    # buckets_status = response.aggregations.group_by_status.buckets
    #
    # count_dict = defaultdict(set)
    # for bucket_species in buckets_species:
    #     for bucket_species_cn in buckets_species_cn:
    #         for bucket_status in buckets_status:
    #             key = (bucket_species.key, bucket_species_cn.key, bucket_status.key)
    #             count_dict[key].add(
    #                 (bucket_species.doc_count, bucket_species_cn.doc_count, bucket_status.doc_count))
    #
    # count = 1
    # for key, value in count_dict.items():
    #     if len(key) == 3 and key[0] and key[1] and key[2]:
    #         count += len(value)
    #
    # return count


class SpeciesSerilzer(DocumentSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = SpeicesModel
        document = SpeciesDocument
        fields = ("species", "species_cn", "is_type_strain_header", "status", "count")

    def get_count(self, obj):
        return getattr(obj, "count", 1)

    # def get_count(self, obj):
    #     search = self.Meta.document.search()
    #     search.aggs.metric('count', 'value_count', field='_id')
    #     search.aggs.bucket('group_by_species', 'terms', field='species.raw', )
    #     search.aggs.bucket('group_by_species_cn', 'terms', field='species_cn.raw', )
    #     search.aggs.bucket('group_by_status', 'terms', field='status.raw', )
    #
    #     response = search.execute()
    #     buckets_species = response.aggregations.group_by_species.buckets
    #     buckets_species_cn = response.aggregations.group_by_species_cn.buckets
    #     buckets_status = response.aggregations.group_by_status.buckets
    #
    #     count = 1
    #     for bucket_species in buckets_species:
    #         for bucket_species_cn in bucket_species:
    #             for bucket_status in buckets_status:
    #                 count += bucket_status.doc_count
    #
    #     return count


class SpeciesTypeExtraSerilzer(DocumentSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = SpeicesModel
        document = SpeciesDocument
        fields = ("species", "species_cn", "status", "count")


class SpeciesAllSerilzer(DocumentSerializer):
    class Meta:
        model = SpeicesModel
        document = SpeciesDocument
        fields = "__all__"


class MorphologySpecisSerilzer(DocumentSerializer):
    class Meta:
        model = SpeicesModel
        document = SpeciesDocument
        fields = ("species", "gram_stain", "cell_shape",
                  "cell_length", "cell_width", "ability_of_spore_formation",
                  "motility", "colony_description", "status")


class PhyosicalSpeciesSerilzer(DocumentSerializer):
    class Meta:
        model = SpeicesModel
        document = SpeciesDocument
        fields = ("species", "oxygen_tolerance", "temperature_opt",
                  "temperature_growth", "ph_opt", "ph_growth", "salt_opt",
                  "salt_growth", "dry_tolerance", "status")


class BioChemistySpeciesSerilzer(DocumentSerializer):
    class Meta:
        model = SpeicesModel
        document = SpeciesDocument
        fields = ("species", "catalase", "oxidase",
                  "voges_proskauer_test", "methylred_test",
                  "enzyme_activity_positive", "enzyme_activity_negative",
                  "carbon_source_and_substrate_activity_positive",
                  "carbon_source_and_substrate_activity_negative", "status")


class CountrySourceSpeciesSerilzer(DocumentSerializer):
    class Meta:
        model = SpeicesModel
        document = SpeciesDocument
        fields = ("species", "country", "source", "status")


class ExtraOtherSpeciesSerilzer(DocumentSerializer):
    class Meta:
        model = SpeicesModel
        document = SpeciesDocument
        fields = ("species", "colony_size", "hemolysis", "antibiotic_resistance",
                  "sensitivity_to_antibiotics", "nutrition_type", "gc_content",
                  "pathogenicity_animal", "pathogenicity_human", "pathogenicity_plant", "status",
                  "incubation_period", "temperature_range",)


class GeneInfoSerilizer(DocumentSerializer):
    class Meta:
        model = GeneInfoModel
        document = GeneInfoDocument
        fields = ("latin_name", "name_CH",)

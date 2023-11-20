import re
from collections import OrderedDict, Counter
import numpy as np

from django.db.models import Q
from django.http import HttpRequest, QueryDict
from django_elasticsearch_dsl_drf.constants import LOOKUP_FILTER_TERMS, LOOKUP_FILTER_PREFIX, LOOKUP_FILTER_WILDCARD, \
    LOOKUP_QUERY_EXCLUDE, LOOKUP_QUERY_ISNULL, LOOKUP_QUERY_IN, SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import FilteringFilterBackend, \
    SearchFilterBackend, CompoundSearchFilterBackend, OrderingFilterBackend, DefaultOrderingFilterBackend, \
    SuggesterFilterBackend
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet, BaseDocumentViewSet
from elasticsearch_dsl import A, Search
from elasticsearch_dsl.query import MoreLikeThis, Wildcard, MultiMatch
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from baike.models import BioSafeAll, ZhiDieases, ZhaoHuiRealtedRisk, ZhaoHuiAll
from baike.pageination import MyPageNumberPageination, MyExtraPageNumberPageination
from baike.serilizers import BioSafeSerlizer, DiseasesSerilizer, ZhaohuiRealtedRiskSerilizer, ZhuiAllSerilizer, \
    SpeciesAllSelizer
from species.documents import SpeciesDocument, SpeciesDocument1, GeneInfoDocument
from species.models import SpeicesModel, GeneInfoModel
from species.serilizers import SpeciesSerilzer, MorphologySpecisSerilzer, PhyosicalSpeciesSerilzer, \
    BioChemistySpeciesSerilzer, CountrySourceSpeciesSerilzer, ExtraOtherSpeciesSerilzer, SpeciesTypeExtraSerilzer, \
    SearchSerlizer, GeneInfoSerilizer


class BiosafeView(GenericAPIView):
    queryset = BioSafeAll.objects.all()
    serializer_class = BioSafeSerlizer

    def get(self, request, *args, **kwargs):
        search = request.query_params.get('query')
        results = self.get_queryset().filter(species=search).distinct()
        serilzer_res = self.get_serializer(results, many=True)
        all = []
        for item in serilzer_res.data:
            if item not in all:
                all.append(item)
        return Response(all, status=status.HTTP_200_OK)


class DiseaseView(GenericAPIView):
    queryset = ZhiDieases.objects.all()
    serializer_class = DiseasesSerilizer

    def get(self, request):
        search = request.query_params.get('query')
        results = self.get_queryset().filter(speices=search).distinct()
        serilzer_res = self.get_serializer(results, many=True)
        all = []
        for item in serilzer_res.data:
            if item not in all:
                all.append(item)
        return Response(all, status=status.HTTP_200_OK)


class ZhaohuiRealtedRiskView(GenericAPIView):
    queryset = ZhaoHuiRealtedRisk.objects.all()
    serializer_class = ZhaohuiRealtedRiskSerilizer

    def get(self, request):
        search = request.query_params.get('query')
        results = self.get_queryset().filter(name=search).distinct()
        ser_res = self.get_serializer(results, many=True)
        all = []
        for item in ser_res.data:
            if item not in all:
                all.append(item)
        return Response(all, status=status.HTTP_200_OK)


class ZhaoHuiAllView(GenericAPIView):
    queryset = ZhaoHuiAll.objects.all()
    serializer_class = ZhuiAllSerilizer

    def get(self, request):
        search = request.query_params.get('query')
        results = self.get_queryset().filter(polluted_species=search).distinct()
        ser_res = self.get_serializer(results, many=True)
        all = []
        for item in ser_res.data:
            if item not in all:
                all.append(item)
        return Response(all, status=status.HTTP_200_OK)


class FourView(GenericAPIView):

    def get(self, request):
        http_request = HttpRequest()
        http_request.method = 'GET'
        http_request.GET = {"query": request.query_params.get('query')}
        all = OrderedDict()
        classes = [BiosafeView, DiseaseView, ZhaohuiRealtedRiskView, ZhaoHuiAllView]
        for ind, cls in enumerate(classes):
            view_ = cls.as_view()
            resposne_ = view_(http_request)
            data_ = resposne_.data
            all[f"message_{ind + 1}"] = data_
        return Response(all, status=status.HTTP_200_OK)


class ElasticSpeciesView(DocumentViewSet):
    document = SpeciesDocument1
    serializer_class = SpeciesSerilzer
    pagination_class = MyExtraPageNumberPageination
    filter_backends = [
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SuggesterFilterBackend,
        # SearchFilterBackend
    ]
    # lookup_field = 'first_name'

    search_fields = {
        'species': {'boost': 10},
        'species_cn': {'boost': 10},
    }

    filter_fields = {
        "species": {
            "field": "species.raw",
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
        "species_cn": {
            "field": "species_cn.raw",
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        }

    }

    # multi_match_search_fields = (
    #     'species',
    #     'species_cn',
    # )

    ordering_fields = {
        "species": "species.raw",
        "species_cn": "species_cn.raw",
    }

    # suggester_fields = {
    #     'species_suggest': {
    #         'field': 'species.suggest',
    #         'suggesters': [
    #             SUGGESTER_COMPLETION,
    #         ],
    #     },
    # }

    def list(self, request, *args, **kwargs):
        query = request.query_params.get('search')
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = {}
            for item in serializer.data:
                key = (item['species'], item['species_cn'], item['status'])
                if key in result:
                    result[key]['count'] += item['count']
                else:
                    result[key] = item
            finaly = {}
            for k in list(result.values()):
                if k["species"] and k["species"] != None:
                    spe = k['species'].split(" ")[0]
                    if spe in finaly:
                        finaly[spe].append(k)
                    else:
                        finaly[spe] = [k]
            finaly1 = {k: v for k, v in finaly.items() if query.lower() in k.lower()}

            # return self.get_paginated_response(finaly1)
            return Response(finaly1, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     search = self.document.search()
    #     search.aggs.metric('count', 'value_count', field='_id')
    #     search.aggs.bucket('group_by_species', 'terms', field='species.raw')
    #     search.aggs.bucket('group_by_species_cn', 'terms', field='species_cn.raw')
    #     search.aggs.bucket('group_by_status', 'terms', field='status.raw')
    #
    #     response = search.execute()
    #
    #     buckets_species = response.aggregations.group_by_species.buckets
    #     buckets_species_cn = response.aggregations.group_by_species_cn.buckets
    #     buckets_status = response.aggregations.group_by_status.buckets
    #
    #     result = {}
    #     for bucket_species in buckets_species:
    #         for bucket_species_cn in buckets_species_cn:
    #             for bucket_status in buckets_status:
    #                 key = (bucket_species.key, bucket_species_cn.key, bucket_status.key)
    #                 if key in result:
    #                     result[key]['count'] += bucket_status.doc_count
    #                 else:
    #                     result[key] = {
    #                         'species': bucket_species.key,
    #                         'species_cn': bucket_species_cn.key,
    #                         'status': bucket_status.key,
    #                         'count': bucket_status.doc_count
    #                     }
    #
    #     paginator = self.pagination_class()
    #     paginated_data = paginator.paginate_queryset(list(result.values()), request)
    #     serializer = self.get_serializer(paginated_data, many=True)
    #     return paginator.get_paginated_response(serializer.data)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page1 = MyExtraPageNumberPageination().paginate_queryset(queryset, request)
    #     if page1 is not None:
    #         result = {}
    #         for item in page1:
    #             item["count"] = 1
    #         for item in page1:
    #             key = (item['species'], item['species_cn'], item['status'])
    #             if key in result:
    #                 result[key]['count'] += item['count']
    #             else:
    #                 result[key] = item
    #         ser = self.get_serializer(list(result.values()), many=True)
    #         page = self.paginate_queryset(ser.data)
    #         if page is not None:
    #             serializer = self.get_serializer(page, many=True)
    #             data = serializer.data
    #             return self.get_paginated_response(data)
    #         return Response(ser.data, status=status.HTTP_200_OK)
    #     search = self.document.search()
    #     search.aggs.metric('count', 'value_count', field='_id')
    #     response = search.execute()
    #     count = response.aggregations.count.value
    #     serializer = self.get_serializer(queryset, many=True)
    #     data = serializer.data
    #     result = {}
    #     for item in data:
    #         key = (item['species'], item['species_cn'], item['status'])
    #         if key in result:
    #             result[key]['count'] += item['count']
    #         else:
    #             result[key] = item
    #     data = list(result.values())
    #     data.append({'count': count})
    #     return Response(data, status=status.HTTP_200_OK)


class ElasticFullSpeciesView(DocumentViewSet):
    document = SpeciesDocument
    serializer_class = SpeciesSerilzer
    pagination_class = MyExtraPageNumberPageination
    filter_backends = [
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SuggesterFilterBackend,
        # SearchFilterBackend
    ]

    search_fields = {
        'species': {'boost': 10},
        'species_cn': {'boost': 10},
    }

    filter_fields = {
        "species": {
            "field": "species.raw",
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
        "species_cn": {
            "field": "species_cn.raw",
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        }
    }
    ordering_fields = {
        "species": "species.raw",
        "species_cn": "species_cn.raw",
    }

    def list(self, request, *args, **kwargs):
        query = request.query_params.get('search')
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            result = {}
            for item in ser.data:
                if item['status'] == "2":
                    continue
                key = (item['species'], item['species_cn'], item['is_type_strain_header'])
                if key in result:
                    result[key]['count'] += item['count']
                else:
                    result[key] = {k: v for k, v in item.items() if k != "status"}
            data_list = list(result.values())
            data_list_tr = []
            for i in data_list:
                if i["is_type_strain_header"] == "1.0" or i["is_type_strain_header"] == "1":
                    data_list_tr.append({k: ("是" if k == "is_type_strain_header" else v) for k, v in i.items()})
                elif i["is_type_strain_header"] == "0.0" or i["is_type_strain_header"] == "0":
                    data_list_tr.append({k: ("否" if k == "is_type_strain_header" else v) for k, v in i.items()})
                else:
                    data_list_tr.append({k: ("-" if k == "is_type_strain_header" else v) for k, v in i.items()})
            gg = {}
            for m in data_list_tr:
                key = (m['species'], m['species_cn'], m['is_type_strain_header'])
                if key in gg:
                    gg[key]['count'] += m['count']
                else:
                    gg[key] = m
            finalall = list(gg.values())
            if query.isalpha() and query.isascii():
                final = []
                for item_t in finalall:
                    if query.lower() in item_t['species'].lower():
                        final.append(item_t)
                return Response(final, status=status.HTTP_200_OK)
            elif " " in query:
                final = []
                for item_t in finalall:
                    if query.lower() in item_t['species'].lower():
                        final.append(item_t)
                return Response(final, status=status.HTTP_200_OK)
            return Response(finalall, status=status.HTTP_200_OK)
        ser = self.get_serializer(queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class PerSpeciesView(GenericAPIView):
    queryset = SpeicesModel.objects.using("db1").all()
    serializer_class = SpeciesAllSelizer

    def get(self, request):
        # param1 = request.query_params.get("uniqueid")
        param2 = request.query_params.get("specis")
        # param3 = request.query_params.get("specis_cn")
        # param4 = request.query_params.get("status")
        res = self.get_queryset().filter(
            Q(species=param2)).distinct().first()
        ser_res = self.get_serializer(res)
        return Response(ser_res.data, status=status.HTTP_200_OK)


class ElasticSpeciesMorpholgyView(DocumentViewSet):
    document = SpeciesDocument
    serializer_class = MorphologySpecisSerilzer
    pagination_class = MyExtraPageNumberPageination
    filter_backends = [
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
        # SearchFilterBackend
    ]

    search_fields = ("species",)

    filter_fields = {
        "species": "species.raw",
    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            res = self.get_serializer(page, many=True)
            attributes = {
                "gram_stain": [],
                "cell_shape": [],
                "cell_length": [],
                "cell_width": [],
                "ability_of_spore_formation": [],
                "motility": [],
                "colony_description": [],
            }

            exclude = ["cell_length", "cell_width"]

            for item in res.data:
                if item["status"] == "2":
                    continue
                for attr, value in attributes.items():
                    if item[attr] and attr not in exclude:
                        value.extend(item[attr].strip().split(";"))
                    elif item[attr] and attr in exclude:
                        value.append("{:.2f}".format(np.mean([float(m) for m in re.findall(r'\d+\.?\d*e?\d*?',
                                                                                           item[attr].strip())])))
            unique_values = {attr: ";".join(list(set(["negative" if m == "negtaive" else m for m in
                                                      value]))) if attr not in exclude else f"{min(value)}-{max(value)}" if isinstance(
                value, list) and len(value) > 0 else "" for attr, value in attributes.items()}

            all = {attr: dict(Counter(["negative" if m == "negtaive" else m for m in value]))
                   for attr, value in attributes.items() if attr != "colony_description"}

            sorted_cell = {key: (
                {k: v for k, v in sorted(value.items(), key=lambda item: float(item[0]))} if key in exclude else value)
                for key, value in all.items()}

            # sorted_cell["message"] = unique_values
            return Response(sorted_cell, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)


class ElasticsearchPhyosicalView(DocumentViewSet):
    document = SpeciesDocument
    serializer_class = PhyosicalSpeciesSerilzer
    pagination_class = MyExtraPageNumberPageination
    filter_backends = [
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
        # SearchFilterBackend
    ]

    search_fields = ("species",)

    filter_fields = {
        "species": {
            "field": "species.raw",
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            res = self.get_serializer(page, many=True)
            attributes = {
                "oxygen_tolerance": [],
                "temperature_opt": [],
                "temperature_growth": [],
                "ph_opt": [],
                "ph_growth": [],
                "salt_opt": [],
                "salt_growth": [],
                "dry_tolerance": [],
            }

            exclude = ["temperature_growth", "ph_growth", "salt_growth"]
            opt = ["temperature_opt", "ph_opt", "salt_opt"]
            tt = [*exclude, *opt]
            for item in res.data:
                if item["status"] == "2":
                    continue
                for attr, value in attributes.items():
                    if item[attr] and attr not in tt:
                        value.extend(item[attr].strip().split(';'))
                    elif item[attr] and attr in tt:
                        value.append(
                            "{:.2f}".format(
                                np.mean([float(num) for num in re.findall(r"\d*\.\d+|\d+", item[attr].strip())])))

            unique_values = {
                attr: f"{min(value)}-{max(value)}" if attr in exclude and len(value) > 0 else "{:.2f}".format(np.mean(
                    [float(v) for v in value])) if attr in opt and len(value) > 0 else "" if len(
                    value) == 0 else ";".join(list(set(value))) for
                attr, value in attributes.items()}

            all = {attr: dict(Counter(value)) for attr, value in attributes.items() if attr != "dry_tolerance"}

            sorted_cell = {key: (
                {k: v for k, v in sorted(value.items(), key=lambda item: float(item[0]))} if key in tt else value)
                for key, value in all.items()}

            # sorted_cell["message"] = unique_values
            return Response(sorted_cell, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)


class ElasticBiochemistyDaixieView(DocumentViewSet):
    document = SpeciesDocument
    serializer_class = BioChemistySpeciesSerilzer
    pagination_class = MyExtraPageNumberPageination
    filter_backends = [
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
        # SearchFilterBackend
    ]

    search_fields = ("species",)

    filter_fields = {
        "species": {
            "field": "species.raw",
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },

    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            res = self.get_serializer(page, many=True)

            unique_values = {}

            attributes = {
                "catalase": [],
                "oxidase": [],
                "voges_proskauer_test": [],
                "methylred_test": [],
                "enzyme_activity_positive": [],
                "enzyme_activity_negative": [],
                "carbon_source_and_substrate_activity_positive": [],
                "carbon_source_and_substrate_activity_negative": [],
            }

            exclude = ["enzyme_activity_positive", "enzyme_activity_negative",
                       "carbon_source_and_substrate_activity_positive",
                       "carbon_source_and_substrate_activity_negative"]

            for item in res.data:
                if item["status"] == "2":
                    continue
                for attr, value in attributes.items():
                    if item[attr] and attr not in exclude:
                        value.extend(item[attr].strip().split(";"))
                    elif item[attr] and attr in exclude:
                        for m in item[attr].strip().replace("\n", "").split(","):
                            ms = m.strip()
                            if ms:
                                if 'and' not in ms:
                                    value.append(ms)
                                else:
                                    gg = [t.strip() for t in ms.split('and') if t.strip()]
                                    for k in gg:
                                        value.append(k.strip())

            # for attr, value in attributes.items():
            #     unique_values[attr] = ";".join(list(set(value)))
            all = {attr: dict(Counter(value)) for attr, value in attributes.items() if
                   attr != "catalase" and attr != "oxidase"}
            # all["message"] = unique_values

            return Response(all, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)


class ElasticCountrySourceView(DocumentViewSet):
    document = SpeciesDocument
    serializer_class = CountrySourceSpeciesSerilzer
    pagination_class = MyExtraPageNumberPageination
    filter_backends = [
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
        # SearchFilterBackend
    ]

    search_fields = ("species",)

    filter_fields = {
        "species": {
            "field": "species.raw",
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            res = self.get_serializer(page, many=True)
            unique_values = {}
            attributes = {
                "country": [],
                "source": [],
            }
            for item in res.data:
                if item["status"] == "2":
                    continue
                for attr, value in attributes.items():
                    if item[attr] != None and item[attr].strip():
                        value.append(item[attr].strip())
                        # value.extend([m for m in item[attr].strip().split(";") if m])

            unique_values["country"] = dict(Counter(attributes['country']))
            unique_values["source"] = "\n\n".join(list(set(attributes["source"])))

            return Response(unique_values, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)


class ElasticExtraOtherView(BaseDocumentViewSet):
    document = SpeciesDocument
    serializer_class = ExtraOtherSpeciesSerilzer
    pagination_class = MyExtraPageNumberPageination
    filter_backends = [
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
    ]

    search_fields = {
        'species': {'boost': 10},
    }

    filter_fields = {
        "species": {
            "field": "species.raw",
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            attributes = {
                "colony_size": [],
                "hemolysis": [],
                "antibiotic_resistance": [],
                "sensitivity_to_antibiotics": [],
                "nutrition_type": [],
                "gc_content": [],
                "pathogenicity_animal": [],
                "pathogenicity_human": [],
                "pathogenicity_plant": [],
                "incubation_period": [],
                "temperature_range": [],
            }
            exclude = ["colony_size", "gc_content", "incubation_period"]
            for item in ser.data:
                if item["status"] == "2":
                    continue
                for attr, value in attributes.items():
                    if item[attr] != None and item[attr].strip():
                        if attr in exclude:
                            value.append("{:.2f}".format(np.mean([float(m) for m in re.findall(r'\d+\.?\d*e?\d*?',
                                                                                               item[attr].strip())])))
                        else:
                            for ms in item[attr].strip().split(","):
                                ms = ms.strip()
                                if ms:
                                    if "and" in ms:
                                        mst = ms.split("and")
                                        for gg in mst:
                                            if gg.strip():
                                                value.append(gg.strip())
                                    else:
                                        value.append(ms)

            all = {attr: dict(Counter(value)) for attr, value in attributes.items()}

            sorted_cell = {key: (
                {k: v for k, v in sorted(value.items(), key=lambda item: float(item[0]))} if key in exclude else value)
                for key, value in all.items()}

            return Response(sorted_cell, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)


class ElasticGeneInfoView(DocumentViewSet):
    document = GeneInfoDocument
    serializer_class = GeneInfoSerilizer
    pagination_class = MyExtraPageNumberPageination
    filter_backends = [
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
    ]

    search_fields = {
        'latin_name': {'boost': 10},
        'name_CH': {'boost': 10},
    }

    filter_fields = {
        "latin_name": {
            "field": "latin_name",
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
        "latin_name.raw": {
            "field": "latin_name.raw",
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
        "name_CH": {
            "field": "name_CH.raw",
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        }
    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     query = self.request.query_params.get('search', None)
    #     if query:
    #         mlt_query = MoreLikeThis(
    #             fields=['latin_name', 'name_CH'],
    #             like=query,
    #             min_term_freq=1,
    #             min_doc_freq=1
    #         )
    #         queryset = queryset.query(mlt_query)
    #
    #     return queryset

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     query = self.request.query_params.get('search', None)
    #     if query:
    #         s = Search(using=queryset._using)
    #         mlt_query = MoreLikeThis(
    #             fields=['latin_name', 'name_CH'],
    #             like=query,
    #             min_term_freq=1,
    #             min_doc_freq=1
    #         )
    #         s = s.query(mlt_query)
    #         s = s.sort('_score', '-id')
    #         response = s.execute()
    #
    #         ids = [hit.meta.id for hit in response]
    #         queryset = queryset.filter(id__in=ids)
    #     return queryset

    # def filter_queryset(self, queryset):
    #     wildcard_query = self.request.query_params.get('search', None)
    #     if wildcard_query:
    #         wildcard_filter = Wildcard(wildcard_query)
    #         queryset = queryset.query(wildcard_filter)
    #     return queryset


class TwoList(GenericAPIView):

    def get(self, request):
        spe = SpeicesModel.objects.using("db1").all().values("species", "species_cn", "status").distinct()
        t = []
        for item in spe:
            if item["status"] == "2":
                continue
            if item["species_cn"] == None:
                t.append({"value": item["species"], "name_ch": ""})
                continue
            elif not item["species_cn"]:
                t.append({"value": item["species"], "name_ch": ""})
                continue
            t.append({"value": item["species"], "name_ch": item["species_cn"]})
        shu = GeneInfoModel.objects.using("db1").all().values("latin_name", "name_CH", "status").distinct()
        g = []
        for it in shu:
            if it["status"] == "有效":
                if it["name_CH"] == None:
                    g.append({"value": it["latin_name"], "name_ch": ""})
                    continue
                elif not it["name_CH"]:
                    g.append({"value": it["latin_name"], "name_ch": ""})
                    continue
                g.append({"value": it["latin_name"], "name_ch": it["name_CH"]})
        all = {"speciesList": t, "genusList": g}
        return Response(all)


class SpeciesMorBioPhyExtra(GenericAPIView):

    def get(self, request):
        views = [ElasticSpeciesMorpholgyView, ElasticsearchPhyosicalView, ElasticBiochemistyDaixieView,
                 ElasticCountrySourceView, ElasticExtraOtherView]
        http_request = HttpRequest()
        http_request.method = 'GET'
        http_request.GET = QueryDict(request.META['QUERY_STRING'])
        all = {}
        for vi in views:
            view_ = vi.as_view(actions={"get": "list"})
            resposne_ = view_(http_request)
            data_ = resposne_.data

            all.update(
                {k: v if k != "message" else {**all.get(k, {}), **v} for k, v in data_.items()}) if all else all.update(
                data_)

        return Response(all, status=status.HTTP_200_OK)


class SpeciesAndView(GenericAPIView):

    def get(self, request):
        views = [ElasticGeneInfoView, ElasticFullSpeciesView]
        http_request = HttpRequest()
        http_request.method = 'GET'
        http_request.GET = QueryDict(request.META['QUERY_STRING'])
        all = []
        count = 0
        for ind, vi in enumerate(views):
            view_ = vi.as_view(actions={"get": "list"})
            resposne_ = view_(http_request)
            data_ = resposne_.data
            if ind == 0 and data_:
                all.append({"type": "genus", "species": data_[0]["latin_name"],
                            "species_cn": data_[0]['name_CH']})
            elif ind == 1 and data_:
                all.extend(data_)
                count = sum(m["count"] for m in data_)
        if all and "type" in all[0].keys():
            all[0]["count"] = count
        return Response(all, status=status.HTTP_200_OK)

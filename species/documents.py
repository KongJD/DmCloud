from django_elasticsearch_dsl import Document, fields, Index
from django_elasticsearch_dsl.documents import DocType
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl_drf.compat import StringField
from elasticsearch_dsl import analyzer, Q

from .models import SpeicesModel, GeneInfoModel

# my_analyzer = analyzer('my_analyzer',
#                        tokenizer='standard',
#                        filter=['lowercase'],
#                        )


# my_analyzer = analyzer('my_analyzer',
#                        tokenizer='pattern',
#                        # pattern="([^\\p{L}\\d]+)|(?<=\\D)(?=\\d)|(?<=\\d)(?=\\D)|(?<=[\\p{L}&&[^\\p{Lu}]])(?=\\p{Lu})|(?<=\\p{Lu})(?=\\p{Lu}[\\p{L}&&[^\\p{Lu}]])",
#                        filter=['lowercase'],
#                        preserve_original=True
#                        )
# my_analyzer = analyzer('my_analyzer',
#                        tokenizer='ik_max_word',
#                        filter=['lowercase'],
#                        preserve_original=True
#                        )

my_analyzer_ = analyzer('my_analyzer_',
                       tokenizer='ik_smart',
                       filter=['lowercase'],
                       preserve_original=True
                       )


@registry.register_document
class SpeciesDocument(Document):
    # uniqueID = fields.KeywordField()
    # species = fields.TextField(analyzer=my_analyzer)
    # fielddata = True

    # species = fields.TextField(analyzer=my_analyzer, fields={'keyword': {'type': 'keyword', }})
    # species = StringField(analyzer=my_analyzer)

    # species = StringField(
    #     analyzer = my_analyzer,
    #     fields={
    #         'raw': fields.KeywordField(),
    #         'suggest': fields.CompletionField(),
    #     }
    # )
    species_cn = fields.TextField(analyzer=my_analyzer_, fields={'raw': fields.KeywordField()})


    class Index:
        name = 'specis'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'max_result_window': 100000,
        }

    class Django:
        model = SpeicesModel
        fields = [
            'uniqueID', 'species',
            #'species_cn',
            'id', 'is_type_strain_header', 'designation_header',
            'strain_number_header', "gram_stain", "gram_stain_stat", "cell_shape", "cell_shape_stat", "cell_length",
            "cell_width", "ability_of_spore_formation", "motility", "motility_stat", "flagellum_arrangement",
            "oxygen_tolerance", "oxygen_tolerance_stat", "nutrition_type", "culture_medium", "incubation_period",
            "colony_size", "colony_description", "colony_color_or_pigment", "temperature_range", "temperature_growth",
            "temperature_max", "temperature_min", "temperature_opt", "ph_growth", "ph_max", "ph_min", "ph_opt",
            "salt_growth", "salt_opt", "salt_max", "salt_min", "methylred_test", "voges_proskauer_test", "hemolysis",
            "catalase", "oxidase", "uv_or_ionizing_radiation_tolerance", "dry_tolerance", "metabolites_positive",
            "metabolites_negative", "carbon_source_and_substrate_activity_positive",
            "carbon_source_and_substrate_activity_negative",
            "enzyme_activity_positive", "enzyme_activity_negative", "antibiotic_resistance",
            "sensitivity_to_antibiotics",
            "gc_content", "pathogenicity_animal", "pathogenicity_human", 'pathogenicity_plant',
            "cell_relationships_aggregations",
            "vitamins_and_cofactors_required_for_growth", "isolation_source", "continent", "country",
            "ecology_or_habitat", "source", "remarks", "username", "userid", "create_time", "update_time",
            "audit_userid", "audit_username", "audit_time", "audit_status", "status", "colony_picture",
            "micrograph"
        ]


my_analyzer1 = analyzer('my_analyzer1',
                        tokenizer='edge_ngram',
                        min_gram="4",
                        max_gram="5",
                        filter=['lowercase'],
                        # token_chars=['letter', 'digit', 'punctuation'],
                        preserve_original=True
                        )


@registry.register_document
class SpeciesDocument1(Document):
    species = fields.TextField(analyzer=my_analyzer1, fields={'raw': fields.KeywordField()})
    species_cn = fields.TextField(analyzer=my_analyzer_, fields={'raw': fields.KeywordField()})

    class Index:
        name = 'specis1'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'max_result_window': 100000,
            'analysis': {
                'analyzer': {
                    'my_analyzer_': {
                        'type': 'custom',
                        'tokenizer': 'ik_smart',
                        'filter': ['lowercase'],
                        'preserve_original': True
                    },
                    'my_analyzer1': {
                        'type': 'custom',
                        'tokenizer': 'edge_ngram',
                        "min_gram": "4",
                        "max_gram": "5",
                        'filter': ['lowercase'],
                        'preserve_original': True
                    }

                }
            }
        }

    class Django:
        model = SpeicesModel
        fields = [
            'uniqueID',  #'species',  # 'species_cn',
            'id', 'is_type_strain_header', 'designation_header',
            'strain_number_header', "gram_stain", "gram_stain_stat", "cell_shape", "cell_shape_stat", "cell_length",
            "cell_width", "ability_of_spore_formation", "motility", "motility_stat", "flagellum_arrangement",
            "oxygen_tolerance", "oxygen_tolerance_stat", "nutrition_type", "culture_medium", "incubation_period",
            "colony_size", "colony_description", "colony_color_or_pigment", "temperature_range", "temperature_growth",
            "temperature_max", "temperature_min", "temperature_opt", "ph_growth", "ph_max", "ph_min", "ph_opt",
            "salt_growth", "salt_opt", "salt_max", "salt_min", "methylred_test", "voges_proskauer_test", "hemolysis",
            "catalase", "oxidase", "uv_or_ionizing_radiation_tolerance", "dry_tolerance", "metabolites_positive",
            "metabolites_negative", "carbon_source_and_substrate_activity_positive",
            "carbon_source_and_substrate_activity_negative",
            "enzyme_activity_positive", "enzyme_activity_negative", "antibiotic_resistance",
            "sensitivity_to_antibiotics",
            "gc_content", "pathogenicity_animal", "pathogenicity_human", 'pathogenicity_plant',
            "cell_relationships_aggregations",
            "vitamins_and_cofactors_required_for_growth", "isolation_source", "continent", "country",
            "ecology_or_habitat", "source", "remarks", "username", "userid", "create_time", "update_time",
            "audit_userid", "audit_username", "audit_time", "audit_status", "status", "colony_picture",
            "micrograph"
        ]


# my_analyzer2 = analyzer('my_analyzer2',
#                         tokenizer='edge_ngram',
#                         min_gram=4,
#                         max_gram=10,
#                         filter=['lowercase'],
#                         preserve_original=True
#                         )


@registry.register_document
class GeneInfoDocument(Document):
    name_CH = fields.TextField(analyzer=my_analyzer_, fields={'raw': fields.KeywordField()})

    # latin_name = fields.TextField(analyzer=my_analyzer2, fields={'raw': fields.KeywordField()})

    class Index:
        name = "gene"
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'max_result_window': 100000,
            'analysis': {
                'analyzer': {
                    'my_analyzer_': {
                        'type': 'custom',
                        'tokenizer': 'ik_smart',
                        'filter': ['lowercase'],
                        'preserve_original': True
                    },
                    'my_analyzer2': {
                        'type': 'custom',
                        'tokenizer': 'edge_ngram',
                        "min_gram": 4,
                        "max_gram": 10,
                        'filter': ['lowercase'],
                        'preserve_original': True
                    }

                }
            }

        }

    class Django:
        model = GeneInfoModel
        fields = ["id", "status", "taxonomy",   "latin_name",  # "name_CH",
                  "annotation_CH",
                  "references", "create_name", "update_name", "check_name",
                  "create_time", "update_time", "check_time"]

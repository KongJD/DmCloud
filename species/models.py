from django.db import models


class SpeicesModel(models.Model):
    uniqueID = models.CharField(max_length=32, db_column="uniqueID", verbose_name="uniqueID", primary_key=True)
    species = models.CharField(max_length=255, db_column="species", verbose_name="species")
    species_cn = models.CharField(max_length=255, db_column="species_cn", verbose_name="species_cn")
    id = models.CharField(max_length=32, db_column="id", verbose_name="id")
    is_type_strain_header = models.CharField(max_length=255, db_column="is_type_strain_header",
                                             verbose_name="is_type_strain_header")
    designation_header = models.CharField(max_length=255, db_column="designation_header",
                                          verbose_name="designation_header")
    strain_number_header = models.TextField(db_column="strain_number_header", verbose_name="strain_number_header")
    gram_stain = models.CharField(max_length=255, db_column="gram_stain", verbose_name="gram_stain")
    gram_stain_stat = models.CharField(max_length=255, db_column="gram_stain_stat", verbose_name="gram_stain_stat")
    cell_shape = models.CharField(max_length=255, db_column="cell_shape", verbose_name="cell_shape")
    cell_shape_stat = models.CharField(max_length=255, db_column="cell_shape_stat", verbose_name="cell_shape_stat")
    cell_length = models.CharField(max_length=255, db_column="cell_length", verbose_name="cell_length")
    cell_width = models.CharField(max_length=255, db_column="cell_width", verbose_name="cell_width")
    ability_of_spore_formation = models.TextField(db_column="ability_of_spore_formation",
                                                  verbose_name="ability_of_spore_formation")
    motility = models.CharField(max_length=255, db_column="motility", verbose_name="motility")
    motility_stat = models.CharField(max_length=255, db_column="motility_stat", verbose_name="motility_stat")
    flagellum_arrangement = models.TextField(db_column="flagellum_arrangement",
                                             verbose_name="flagellum_arrangement")
    oxygen_tolerance = models.CharField(max_length=255, db_column="oxygen_tolerance", verbose_name="oxygen_tolerance")
    oxygen_tolerance_stat = models.CharField(max_length=255, db_column="oxygen_tolerance_stat",
                                             verbose_name="oxygen_tolerance_stat")
    nutrition_type = models.CharField(max_length=255, db_column="nutrition_type", verbose_name="nutrition_type")
    culture_medium = models.TextField(db_column="culture_medium", verbose_name="culture_medium")
    incubation_period = models.CharField(max_length=255, db_column="incubation_period",
                                         verbose_name="incubation_period")
    colony_size = models.CharField(max_length=255, db_column="colony_size", verbose_name="colony_size")
    colony_description = models.TextField(db_column="colony_description", verbose_name="colony_description")
    colony_color_or_pigment = models.TextField(db_column="colony_color_or_pigment",
                                               verbose_name="colony_color_or_pigment")
    temperature_range = models.CharField(max_length=255, db_column="temperature_range",
                                         verbose_name="temperature_range")
    temperature_growth = models.CharField(max_length=255, db_column="temperature_growth",
                                          verbose_name="temperature_growth")

    temperature_max = models.CharField(max_length=255, db_column="temperature_max", verbose_name="temperature_max")
    temperature_min = models.CharField(max_length=255, db_column="temperature_min", verbose_name="temperature_min")
    temperature_opt = models.CharField(max_length=255, db_column="temperature_opt", verbose_name="temperature_opt")
    ph_growth = models.CharField(max_length=255, db_column="ph_growth", verbose_name="ph_growth")
    ph_max = models.CharField(max_length=255, db_column="ph_max", verbose_name="ph_max")
    ph_min = models.CharField(max_length=255, db_column="ph_min", verbose_name="ph_min")
    ph_opt = models.CharField(max_length=255, db_column="ph_opt", verbose_name="ph_opt")
    salt_growth = models.CharField(max_length=255, db_column="salt_growth", verbose_name="salt_growth")
    salt_opt = models.CharField(max_length=255, db_column="salt_opt", verbose_name="salt_opt")
    salt_max = models.CharField(max_length=255, db_column="salt_max", verbose_name="salt_max")
    salt_min = models.CharField(max_length=255, db_column="salt_min", verbose_name="salt_min")
    methylred_test = models.TextField(db_column="methylred_test", verbose_name="methylred_test")
    voges_proskauer_test = models.TextField(db_column="voges_proskauer_test",
                                            verbose_name="voges_proskauer_test")
    hemolysis = models.TextField(db_column="hemolysis", verbose_name="hemolysis")
    catalase = models.TextField(db_column="catalase", verbose_name="catalase")
    oxidase = models.TextField(db_column="oxidase", verbose_name="oxidase")
    uv_or_ionizing_radiation_tolerance = models.TextField(
        db_column="uv_or_ionizing_radiation_tolerance",
        verbose_name="uv_or_ionizing_radiation_tolerance")
    dry_tolerance = models.TextField(db_column="dry_tolerance", verbose_name="dry_tolerance")
    metabolites_positive = models.TextField(db_column="metabolites_positive",
                                            verbose_name="metabolites_positive")
    metabolites_negative = models.TextField(db_column="metabolites_negative", verbose_name="metabolites_negative")
    carbon_source_and_substrate_activity_positive = models.TextField(
        db_column="carbon_source_and_substrate_activity_positive",
        verbose_name="carbon_source_and_substrate_activity_positive")
    carbon_source_and_substrate_activity_negative = models.TextField(
        db_column="carbon_source_and_substrate_activity_negative",
        verbose_name="carbon_source_and_substrate_activity_negative")

    enzyme_activity_positive = models.TextField(db_column="enzyme_activity_positive",
                                                verbose_name="enzyme_activity_positive")
    enzyme_activity_negative = models.TextField(db_column="enzyme_activity_negative",
                                                verbose_name="enzyme_activity_negative")
    antibiotic_resistance = models.TextField(db_column="antibiotic_resistance", verbose_name="antibiotic_resistance")
    sensitivity_to_antibiotics = models.TextField(db_column="sensitivity_to_antibiotics",
                                                  verbose_name="sensitivity_to_antibiotics")
    gc_content = models.TextField(db_column="gc_content", verbose_name="gc_content")
    pathogenicity_animal = models.TextField(db_column="pathogenicity_animal",
                                            verbose_name="pathogenicity_animal")
    pathogenicity_human = models.TextField(db_column="pathogenicity_human",
                                           verbose_name="pathogenicity_human")
    pathogenicity_plant = models.TextField(db_column="pathogenicity_plant",
                                           verbose_name="pathogenicity_plant")
    cell_relationships_aggregations = models.TextField(db_column="cell_relationships_aggregations",
                                                       verbose_name="cell_relationships_aggregations")
    vitamins_and_cofactors_required_for_growth = models.TextField(
        db_column="vitamins_and_cofactors_required_for_growth",
        verbose_name="vitamins_and_cofactors_required_for_growth")
    isolation_source = models.TextField(db_column="isolation_source", verbose_name="isolation_source")
    continent = models.CharField(max_length=255, db_column="continent", verbose_name="continent")
    country = models.CharField(max_length=255, db_column="country", verbose_name="country")
    ecology_or_habitat = models.TextField(db_column="ecology_or_habitat", verbose_name="ecology_or_habitat")
    source = models.TextField(db_column="source", verbose_name="source")
    remarks = models.TextField(db_column="remarks", verbose_name="remarks")
    username = models.CharField(max_length=50, db_column="username", verbose_name="username")
    userid = models.CharField(max_length=32, db_column="userid", verbose_name="userid")
    create_time = models.DateTimeField(db_column="create_time", verbose_name="create_time")
    update_time = models.DateTimeField(db_column="update_time", verbose_name="update_time", auto_now=True)
    audit_userid = models.IntegerField(db_column="audit_userid", verbose_name="audit_userid")
    audit_username = models.CharField(max_length=100, db_column="audit_username", verbose_name="audit_username")
    audit_time = models.DateTimeField(db_column="audit_time", verbose_name="audit_time")
    audit_status = models.CharField(max_length=20, db_column="audit_status", verbose_name="audit_status")
    status = models.CharField(max_length=32, db_column="status", verbose_name="status")
    colony_picture = models.CharField(max_length=1000, db_column="colony_picture", verbose_name="colony_picture")
    micrograph = models.CharField(max_length=1000, db_column="micrograph", verbose_name="micrograph")

    class Meta:
        app_label = 'db1'
        managed = False
        db_table = "datatables"


class GeneInfoModel(models.Model):
    id = models.IntegerField(db_column="id", verbose_name="id", primary_key=True)
    status = models.CharField(max_length=50, db_column="status", verbose_name="status")
    taxonomy = models.CharField(max_length=255, db_column="taxonomy", verbose_name="taxonomy")
    latin_name = models.CharField(max_length=255, db_column="latin_name", verbose_name="latin_name")
    name_CH = models.CharField(max_length=255, db_column="name_CH", verbose_name="name_CH")
    annotation_CH = models.TextField(db_column="annotation_CH", verbose_name="annotation_CH")
    references = models.TextField(db_column="references", verbose_name="references")
    create_name = models.CharField(max_length=50, db_column="create_name", verbose_name="create_name")
    update_name = models.CharField(max_length=50, db_column="update_name", verbose_name="update_name")
    check_name = models.CharField(max_length=50, db_column="check_name", verbose_name="check_name")
    create_time = models.DateTimeField(db_column="create_time", verbose_name="create_time")
    update_time = models.DateTimeField(db_column="update_time", verbose_name="update_time")
    check_time = models.DateTimeField(db_column="check_time", verbose_name="check_time")

    class Meta:
        app_label = 'db1'
        managed = False
        db_table = "genus_info"

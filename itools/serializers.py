from rest_framework import serializers

from itools.models import JobTaskModel, JobCeleryModel


class JobTaskSerializer(serializers.ModelSerializer):
    seq = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    fasta_path = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = JobTaskModel
        fields = ['job_id', 'seq', 'tags', 'filetype', 'dbtype', 'fasta_path']


class JobRpobSerializer(serializers.ModelSerializer):
    seq = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    fasta_path = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = JobTaskModel
        fields = ['job_id', 'seq', 'tags', 'filetype', 'fasta_path']


class JobCelerySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCeleryModel
        fields = "__all__"

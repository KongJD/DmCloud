from rest_framework import serializers

from baike.models import BioSafeAll, ZhiDieases, ZhaoHuiRealtedRisk, ZhaoHuiAll
from species.models import SpeicesModel


class BioSafeSerlizer(serializers.ModelSerializer):
    class Meta:
        model = BioSafeAll
        fields = ["country", "fagui", "bio_safe", "add_comment"]


class DiseasesSerilizer(serializers.ModelSerializer):
    class Meta:
        model = ZhiDieases
        exclude = ('speices', "id",)


class ZhaohuiRealtedRiskSerilizer(serializers.ModelSerializer):
    class Meta:
        model = ZhaoHuiRealtedRisk
        exclude = ('id', "name",)


class ZhuiAllSerilizer(serializers.ModelSerializer):
    class Meta:
        model = ZhaoHuiAll
        exclude = ('id', "polluted_species", "jixing",)


class SpeciesAllSelizer(serializers.ModelSerializer):
    class Meta:
        model = SpeicesModel
        fields = '__all__'

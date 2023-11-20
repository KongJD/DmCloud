from django.db import models


class ZhaoHuiRealtedRisk(models.Model):
    name = models.CharField(max_length=1000, db_column="拉丁名", verbose_name="拉丁名")
    place = models.CharField(max_length=1000, db_column="洁净室", verbose_name="洁净室")

    class Meta:
        app_label = "baike"
        managed = True
        verbose_name = "召回风险表"


class BioSafeAll(models.Model):
    species = models.CharField(max_length=255, db_column="物种", verbose_name="物种")
    bio_in = models.CharField(max_length=255, db_column="生物因子", verbose_name="生物因子")
    add_comment = models.TextField(db_column="补充说明", verbose_name="补充说明")
    fenlei = models.CharField(max_length=255, db_column="分类水平", verbose_name="分类水平")
    bio_safe = models.CharField(max_length=255, db_column="生物安全", verbose_name="生物安全")
    leibie = models.CharField(max_length=255, db_column="类别", verbose_name="类别")
    country = models.CharField(max_length=255, db_column="国家或者地区", verbose_name="国家或者地区")
    fagui = models.TextField(db_column="法规", verbose_name="法规")
    bio_safelevel = models.CharField(max_length=255, db_column="生物安全等级说明", verbose_name="生物安全等级说明")
    update_time = models.CharField(max_length=255, db_column="更新时间", verbose_name="更新时间")

    class Meta:
        app_label = "baike"
        managed = True
        verbose_name = "生物安全汇总"


class ZhaoHuiAll(models.Model):
    polluted_species = models.CharField(max_length=255, db_column="污染物种", verbose_name="污染物种")
    recall_number = models.CharField(max_length=255, db_column="召回编号", verbose_name="召回编号")
    recall_reportime = models.CharField(max_length=255, db_column="召回报告时间", verbose_name="召回报告时间")
    recall_initu = models.CharField(max_length=255, db_column="召回机构", verbose_name="召回机构")
    product = models.TextField(db_column="涉及产品", verbose_name="涉及产品")
    jixing = models.CharField(max_length=255, db_column="剂型", verbose_name="剂型")
    product_comapny = models.CharField(max_length=255, db_column="生产商", verbose_name="生产商")

    class Meta:
        app_label = "baike"
        managed = True
        verbose_name = "召回汇总"


class ZhiDieases(models.Model):
    speices = models.CharField(max_length=255, db_column="物种", verbose_name="物种")
    species_publish_year = models.IntegerField(db_column="物种发表年限", verbose_name="物种发表年限")
    disease = models.CharField(max_length=255, db_column="致病性", verbose_name="致病性")
    message_source = models.TextField(db_column="信息来源", verbose_name="信息来源")

    class Meta:
        app_label = "baike"
        managed = True
        verbose_name = "致病性"


class ShuStatics(models.Model):
    xuhao = models.IntegerField(db_column="序号", verbose_name="序号", primary_key=True)
    publish_status = models.CharField(max_length=255, db_column="发布状态", verbose_name="发布状态")
    taxomy = models.CharField(max_length=255, db_column="taxonomy", verbose_name="taxonomy")
    latin_name = models.CharField(max_length=255, db_column="拉丁名", verbose_name="拉丁名")
    ch_name = models.CharField(max_length=255, db_column="中文名", verbose_name="中文名")
    ch_zhushi = models.TextField(db_column="中文注释", verbose_name="中文注释")
    cankao_source = models.TextField(db_column="参考文献来源", verbose_name="参考文献来源")
    create_name = models.CharField(max_length=255, db_column="创建人", verbose_name="创建人")
    updata_name = models.CharField(max_length=255, db_column="最近修改人", verbose_name="最近修改人")
    shen_name = models.CharField(max_length=255, db_column="最近审核人", verbose_name="最近审核人")
    create_time = models.CharField(max_length=255, db_column="创建时间", verbose_name="创建时间")
    modefity_time = models.CharField(max_length=255, db_column="最近修改时间", verbose_name="最近修改时间")
    shen_time = models.CharField(max_length=255, db_column="审核时间", verbose_name="审核时间")

    class Meta:
        app_label = "baike"
        managed = True
        verbose_name = "属"

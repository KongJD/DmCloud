from django.db import models


class JobTaskModel(models.Model):
    job_id = models.CharField(max_length=40, primary_key=True, db_column="job_id", verbose_name="job_id")
    fasta_path = models.TextField(db_column="fasta_path", verbose_name="fasta_path")
    seq = models.TextField(db_column="seq", verbose_name="seq")
    tags = models.CharField(max_length=40, db_column="tags", verbose_name="tags")
    filetype = models.CharField(max_length=40, db_column="filetype", verbose_name="filetype")
    dbtype = models.CharField(max_length=40, db_column="dbtype", verbose_name="dbtype")
    kmerdb = models.CharField(max_length=255, db_column="kmerdb", verbose_name="kmerdb")
    evalue = models.CharField(max_length=40, db_column="evalue", verbose_name="evalue")
    taxdump = models.CharField(max_length=255, db_column="taxdump", verbose_name="taxdump")
    nt = models.CharField(max_length=255, db_column="nt", verbose_name="nt")
    ani = models.CharField(max_length=40, db_column="ani", verbose_name="ani")
    af = models.CharField(max_length=40, db_column="af", verbose_name="af")
    type = models.CharField(max_length=255, db_column="type", verbose_name="type")

    class Meta:
        app_label = "itools"
        verbose_name = "参数任务表"


class JobCeleryModel(models.Model):
    job_id = models.CharField(max_length=40, primary_key=True, db_column="job_id", verbose_name="job_id")
    task_celery_id = models.CharField(max_length=255, db_column="task_celery_id", verbose_name="task_celery_id")

    class Meta:
        app_label = "itools"
        verbose_name = "celery任务表"

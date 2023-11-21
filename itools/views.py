import subprocess
from celery.result import AsyncResult
import os

from django.db import transaction
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from DmCloud.settings import random_path
from itools.models import JobTaskModel
from itools.serializers import JobTaskSerializer, JobRpobSerializer, JobCelerySerializer
from itools.utils import Utils, makedir, RandomNumber
from itools.tasks import *
import pandas as pd

perl_16s = "/public/Users/sunll/Web/MarkerDB/Script/16S_pipeline.pl"
perl_rpob = "/public/Users/sunll/Web/MarkerDB/Script/rpoB_pipeline.pl"


class Tools16SView(GenericAPIView):
    def post(self, request):
        type = request.data.get("filetype")
        path = request.data.get("fasta_path")
        dtype = request.data.get("dbtype")
        seq = request.data.get("seq")

        dir_path, dir = RandomNumber().generate_path()
        makedir(dir_path)
        makedir(os.path.join(dir_path, "out"))
        makedir(os.path.join(dir_path, "temp"))

        if seq:
            cmd = f"perl {perl_16s} -seq {seq} -outdir {os.path.join(dir_path, 'out')} " \
                  f"-temp {os.path.join(dir_path, 'temp')} -dbtype {dtype} -filetype gene"
            subprocess.run(cmd, shell=True, capture_output=True, text=True)
            ser_data = JobTaskSerializer(data={
                "job_id": dir,
                "fasta_path": "",
                "tags": "16S",
                "filetype": "gene",
                "dbtype": dtype,
                "seq": seq
            })
            if ser_data.is_valid():
                ser_data.save()
                return Response(ser_data.data, status=status.HTTP_200_OK)
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

        if type == "gene":
            cmd = f"perl {perl_16s} -input {path} -outdir {os.path.join(dir_path, 'out')} " \
                  f"-temp {os.path.join(dir_path, 'temp')} -dbtype {dtype} -filetype {type}"
            subprocess.run(cmd, shell=True, capture_output=True, text=True)
            ser_data = JobTaskSerializer(data={
                "job_id": dir,
                "fasta_path": path,
                "tags": "16S",
                "filetype": "gene",
                "dbtype": dtype,
                "seq": ""
            })
            if ser_data.is_valid():
                ser_data.save()
                return Response(ser_data.data, status=status.HTTP_200_OK)
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

        elif type == 'genome':
            cmd = f"perl {perl_16s} -input {path} -outdir {os.path.join(dir_path, 'out')} " \
                  f"-temp {os.path.join(dir_path, 'temp')} -dbtype {dtype} -filetype {type}"
            subprocess.run(cmd, shell=True, capture_output=True, text=True)
            ser_data = JobTaskSerializer(data={
                "job_id": dir,
                "fasta_path": path,
                "tags": "16S",
                "filetype": "gene",
                "dbtype": dtype,
                "seq": ""
            })
            if ser_data.is_valid():
                ser_data.save()
                return Response(ser_data.data, status=status.HTTP_200_OK)
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class Tools16sResultView(GenericAPIView):

    def get(self, request):
        all = []
        gener_dir = "2023-11-20-07-25-17-902860"
        download_path = os.path.join(random_path, gener_dir, 'out', "Download")
        qc_res = Utils().read_qc_stats(os.path.join(download_path, 'QC.stat.xls'))
        all.append(qc_res)
        all.append({"sequence_completeness": f"{os.path.join(download_path, 'gene1.completeness_coverage.svg')}"})
        all.append({"sequence_align": f"{os.path.join(download_path, 'gene1.alignment.svg')}"})
        df = pd.read_csv(os.path.join(download_path, "gene1.best_predict.xls"), sep="\t").to_dict()
        species = [v for k, v in df["Species"].items()]
        similarity = [v for k, v in df["Similarity"].items()]
        all.append({"Species": species, "Similarity": similarity})
        all.append({"Tree": f"{os.path.join(download_path, 'gene1.output.png')}"})
        all.append({"Download": f"{download_path}"})

        return Response(all, status=status.HTTP_200_OK)


class ToolsRpobView(GenericAPIView):
    def post(self, request):

        type = request.data.get("filetype")
        path = request.data.get("fasta_path")
        seq = request.data.get("seq")

        dir_path, dir = RandomNumber().generate_path()
        makedir(dir_path)
        makedir(os.path.join(dir_path, "out"))
        makedir(os.path.join(dir_path, "temp"))

        if seq:
            cmd = f"perl {perl_rpob} -seq {seq} -outdir {os.path.join(dir_path, 'out')} " \
                  f"-temp {os.path.join(dir_path, 'temp')} -filetype {type}"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            ser_data = JobRpobSerializer(data={
                "job_id": dir,
                "fasta_path": "",
                "tags": "rpob",
                "filetype": "gene",
                "seq": seq,
            })
            if ser_data.is_valid():
                ser_data.save()
                return Response(ser_data.data, status=status.HTTP_200_OK)
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

        if type == 'gene':
            cmd = f"perl {perl_rpob} -input {path} -outdir {os.path.join(dir_path, 'out')} " \
                  f"-temp {os.path.join(dir_path, 'temp')} -filetype {type}"
            subprocess.run(cmd, shell=True, capture_output=True, text=True)
            ser_data = JobRpobSerializer(data={
                "job_id": dir,
                "fasta_path": path,
                "tags": "rpob",
                "filetype": "gene",
                "seq": ""
            })
            if ser_data.is_valid():
                ser_data.save()
                return Response(ser_data.data, status=status.HTTP_200_OK)
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

        elif type == "genome":
            cmd = f"perl {perl_rpob} -input {path} -outdir {os.path.join(dir_path, 'out')} " \
                  f"-temp {os.path.join(dir_path, 'temp')} -filetype {type}"
            subprocess.run(cmd, shell=True, capture_output=True, text=True)
            ser_data = JobRpobSerializer(data={
                "job_id": dir,
                "fasta_path": path,
                "tags": "rpob",
                "filetype": "genome",
                "seq": ""
            })
            if ser_data.is_valid():
                ser_data.save()
                return Response(ser_data.data, status=status.HTTP_200_OK)
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ToolsGeneProcessView(GenericAPIView):

    @transaction.atomic
    def get(self, request):
        path = "/public/Users/kongjind/pipeline/geneidentitytools/identify_genome/example.fasta"
        dir_path, dir = RandomNumber().generate_path()
        makedir(dir_path)
        makedir(os.path.join(dir_path, "out"))
        makedir(os.path.join(dir_path, "temp"))
        res = slove_geneprocess.delay(path=path, evalue="1e-5",
                                      outdir=os.path.join(dir_path, 'out'), tempdir=os.path.join(dir_path, 'temp'))
        result = AsyncResult(res.task_id)

        ser_data = JobRpobSerializer(data={
            "job_id": dir,
            "fasta_path": path,
            "tags": "bacterial_genome ",
            "filetype": "genome",
            "seq": ""
        })

        ser_data_celery = JobCelerySerializer(data={
            "job_id": dir,
            "task_celery_id": result.task_id,
        })

        if ser_data.is_valid() and ser_data_celery.is_valid():
            ser_data.save()
            ser_data_celery.save()

            return Response([ser_data.data, ser_data_celery.data], status=status.HTTP_200_OK)

        return Response([ser_data.errors, ser_data_celery.errors], status=status.HTTP_400_BAD_REQUEST)

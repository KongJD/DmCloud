import subprocess
from celery.result import AsyncResult
import os

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from itools.models import JobTaskModel
from itools.serializers import JobTaskSerializer
from itools.utils import Utils, makedir, RandomNumber
from itools.tasks import *

perl_16s = "/public/Users/sunll/Web/MarkerDB/Script/16S_pipeline.pl"
perl_rpob = "/public/Users/sunll/Web/MarkerDB/Script/rpoB_pipeline.pl"


class Tools16SView(GenericAPIView):
    def get(self, request):
        type = request.query_params.get("filetype")
        path = request.query_params.get("fasta_path")
        dtype = request.query_params.get("dbtype")
        seq = request.query_params.get("seq")

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
            path = "/public/Users/kongjind/pipeline/geneidentitytools/16S/genome/genome.fas"
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

        # if type == 'gene':
        #     res = slove_16s.delay(type, path, os.path.join(os.path.dirname(path), "out"),
        #                           os.path.join(os.path.dirname(path), "temp"))
        #     result = AsyncResult(res.task_id)
        #     return Response({"status": result.status, "task_id": result.task_id})
        #
        # elif type == 'genome':
        #     result = Utils().read_qc_stats(os.path.join(path, "out", "Download", "QC.stat.xls"))
        #     print(result)


class ToolsRpobView(GenericAPIView):
    def get(self, request):
        pass

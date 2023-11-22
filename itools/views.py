import subprocess
from celery.result import AsyncResult
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from notifications.models import Notification
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from DmCloud.settings import random_path
from itools.models import JobTaskModel
from itools.serializers import JobTaskSerializer, JobRpobSerializer, JobCelerySerializer, MyTokenObtainPairSerializer
from itools.utils import Utils, makedir, RandomNumber
from itools.tasks import *
import pandas as pd
from notifications.signals import notify

perl_16s = "/public/Users/sunll/Web/MarkerDB/Script/16S_pipeline.pl"
perl_rpob = "/public/Users/sunll/Web/MarkerDB/Script/rpoB_pipeline.pl"


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.user
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


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


class Tools16sRpobResultView(GenericAPIView):
    # permission_classes = [IsAdminUser]
    # authentication_classes = [JWTAuthentication]

    def get(self, request):
        all = []
        # gener_dir = "2023-11-21-01-00-43-474704"
        gener_dir = request.query_params.get("job_id")
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
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def get(self, request):
        # path = "/public/Users/kongjind/pipeline/geneidentitytools/identify_genome/example.fasta"
        path = request.query_params.get("fasta_path")
        dir_path, dir = RandomNumber().generate_path()
        makedir(dir_path)
        makedir(os.path.join(dir_path, "out"))
        makedir(os.path.join(dir_path, "temp"))
        res = slove_geneprocess.delay(path=path, evalue="1e-5",
                                      outdir=os.path.join(dir_path, 'out'),
                                      tempdir=os.path.join(dir_path, 'temp'),
                                      request=str(request.user))
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


class GenerprocessResultView(GenericAPIView):

    def get(self, request):
        gener_dir = "2023-11-22-06-21-38-757516"
        out_path = os.path.join(random_path, gener_dir, 'out')
        pa_path = os.path.join(out_path, os.listdir(out_path)[0])



class TaskTest(GenericAPIView):

    def get(self, request):
        superusers = User.objects.filter(is_superuser=True)
        all = []
        for user in superusers:
            unread_notifications = Notification.objects.unread().filter(recipient=user)
            if unread_notifications.exists():
                all.append(f"User {user.username} has unread notifications.")
            else:
                all.append(f"User {user.username} has no unread notifications.")
        return Response(all)

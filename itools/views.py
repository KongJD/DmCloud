import subprocess
from celery.result import AsyncResult
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render
from notifications.models import Notification
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from DmCloud import settings
from DmCloud.settings import random_path, perl_16s, perl_rpob, random_path_16s, random_path_rpob, random_path_genome, \
    random_path_its
from itools.models import JobTaskModel
from itools.serializers import JobTaskSerializer, JobRpobSerializer, JobCelerySerializer, MyTokenObtainPairSerializer, \
    NoTificationsSerializer
from itools.utils import Utils, makedir, RandomNumber
from itools.tasks import *
import pandas as pd
import numpy as np
from notifications.signals import notify


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

        dir_path, dir = RandomNumber().generate_path(random_path_16s)
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
                "filetype": "genome",
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
        gener_dir = request.query_params.get("job_id")
        type = request.query_params.get("tags")
        download_path = ""
        if type == "16S":
            download_path = os.path.join(random_path_16s, gener_dir, 'out', "Download")

        elif type == "rpob":
            download_path = os.path.join(random_path_rpob, gener_dir, 'out', "Download")

        elif type == "ITS":
            download_path = os.path.join(random_path_its, gener_dir, 'out', "Download")

        qc_res = Utils().read_qc_stats(os.path.join(download_path, 'QC.stat.xls'))
        all.append(qc_res)
        all.append(
            {"sequence_completeness": "".join(
                [request.get_host(),
                 os.path.join(settings.MEDIA_URL, type, gener_dir, 'out', "Download",
                              "gene1.completeness_coverage.svg")])})
        all.append(
            {"sequence_align": "".join(
                [request.get_host(),
                 os.path.join(settings.MEDIA_URL, type, gener_dir, 'out', "Download",
                              "gene1.alignment.svg")])})
        df = pd.read_csv(os.path.join(download_path, "gene1.best_predict.xls"), sep="\t").to_dict()
        species = [v for k, v in df["Species"].items()]
        similarity = [v for k, v in df["Similarity"].items()]
        all.append({"Species": species, "Similarity": similarity})
        all.append({"Tree": "".join(
            [request.get_host(),
             os.path.join(settings.MEDIA_URL, type, gener_dir, 'out', "Download",
                          "gene1.output.png")])})
        all.append({"Download": f"{download_path}"})

        return Response(all, status=status.HTTP_200_OK)


class ToolsRpobView(GenericAPIView):
    def post(self, request):

        type = request.data.get("filetype")
        path = request.data.get("fasta_path")
        seq = request.data.get("seq")

        dir_path, dir = RandomNumber().generate_path(random_path_rpob)
        makedir(dir_path)
        makedir(os.path.join(dir_path, "out"))
        makedir(os.path.join(dir_path, "temp"))

        if seq:
            cmd = f"perl {perl_rpob} -seq {seq} -outdir {os.path.join(dir_path, 'out')} " \
                  f"-temp {os.path.join(dir_path, 'temp')} -filetype {type}"
            subprocess.run(cmd, shell=True, capture_output=True, text=True)
            ser_data = JobRpobSerializer(data={
                "job_id": dir,
                "fasta_path": "",
                "tags": "rpob",
                "filetype": "gene",
                "seq": seq
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
    def post(self, request):
        path = request.data.get("fasta_path")
        dir_path, dir = RandomNumber().generate_path(random_path_genome)
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
        gener_dir = request.query_params.get("job_id")
        out_path = os.path.join(random_path_genome, gener_dir, 'out')
        pa_path = os.path.join(out_path, os.listdir(out_path)[0])
        all = []
        taxonomy_df = pd.read_csv(os.path.join(pa_path, "Taxonomy.txt"), sep="\t").columns
        all.append({"Species name": taxonomy_df[0], "Staphylococcus aureus": taxonomy_df[1]})
        anicaluate_all_df = pd.read_csv(os.path.join(pa_path, "ANIcalculator.all.txt"), sep="\t").to_dict()
        all.append({k: v.values() for k, v in anicaluate_all_df.items()})
        gene_stats_df = pd.read_csv(os.path.join(pa_path, "Genes_Stats.xls"), header=None, sep="\t")
        all.append(gene_stats_df.set_index(0)[1].to_dict())
        mlst_type_df = pd.read_csv(os.path.join(pa_path, "MLST.STtype.txt"), sep="\t").to_dict()
        all.append({k: v[0] for k, v in mlst_type_df.items()})
        mlst_align_df = pd.read_csv(os.path.join(pa_path, "MLST.align.result.xls"), sep="\t").to_dict()
        all.append({k: v.values() for k, v in mlst_align_df.items()})
        apoutput_df = pd.read_csv(os.path.join(pa_path, "AR_VF", "ARoutput.result.txt"), sep="\t")
        for col in apoutput_df.columns:
            apoutput_df[col] = np.where(apoutput_df[col].notnull(), apoutput_df[col], "")
        all.append({k: v.values() for k, v in apoutput_df.to_dict().items()})

        for p in os.listdir(os.path.join(pa_path, "AR_VF")):
            if p.endswith("VFDB.filter.txt"):
                vfdb_filter_df = pd.read_csv(os.path.join(pa_path, "AR_VF", p), sep="\t")
                for col in vfdb_filter_df.columns:
                    vfdb_filter_df[col] = np.where(vfdb_filter_df[col].notnull(), vfdb_filter_df[col], "")
                all.append({k: v.values() for k, v in vfdb_filter_df.to_dict().items()})
        all.append({"Download": f"{pa_path}"})
        return Response(all, status=status.HTTP_200_OK)


class ItoolsItsView(GenericAPIView):

    def post(self, request):
        path = request.data.get("fasta_path")
        seq = request.data.get("seq")

        dir_path, dir = RandomNumber().generate_path(random_path_its)
        makedir(dir_path)
        makedir(os.path.join(dir_path, "out"))
        makedir(os.path.join(dir_path, "temp"))

        if seq:
            cmd = f"perl {perl_16s} -seq {seq} -outdir {os.path.join(dir_path, 'out')} " \
                  f"-temp {os.path.join(dir_path, 'temp')} -filetype gene -dbtype ITS"
            subprocess.run(cmd, shell=True, capture_output=True, text=True)
            ser_data = JobTaskSerializer(data={
                "job_id": dir,
                "fasta_path": "",
                "tags": "ITS",
                "filetype": "gene",
                "dbtype": 'ITS',
                "seq": seq
            })
            if ser_data.is_valid():
                ser_data.save()
                return Response(ser_data.data, status=status.HTTP_200_OK)
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

        cmd = f"perl {perl_16s} -input {path} -outdir {os.path.join(dir_path, 'out')} " \
              f"-temp {os.path.join(dir_path, 'temp')} -filetype gene -dbtype ITS"
        subprocess.run(cmd, shell=True, capture_output=True, text=True)
        ser_data = JobTaskSerializer(data={
            "job_id": dir,
            "fasta_path": path,
            "tags": "ITS",
            "filetype": "gene",
            "dbtype": 'ITS',
            "seq": ""
        })
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadView(GenericAPIView):
    def post(self, request):
        file = request.FILES.get('file')
        dir_path, dir = RandomNumber().save_fasta_path()
        makedir(dir_path)
        with open(os.path.join(dir_path, file.name), "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)
        return Response({"fasta_path": f"{os.path.join(dir_path, file.name)}"}, status=status.HTTP_200_OK)


# class TaskTest(GenericAPIView):
#
#     def get(self, request):
#         superusers = User.objects.filter(is_superuser=True)
#         all = []
#         for user in superusers:
#             unread_notifications = Notification.objects.unread().filter(recipient=user)
#             if unread_notifications.exists():
#                 all.append(f"User {user.username} has unread notifications.")
#             else:
#                 all.append(f"User {user.username} has no unread notifications.")
#         return Response(all)


def notice(request):
    notifications = Notification.objects.unread()
    return render(request, 'notification_unread.html', {'notifications': notifications})


class UserGetUserNotificationView(GenericAPIView):
    serializer_class = NoTificationsSerializer

    def get(self, request):
        all = []
        user = request.query_params.get('user')
        user_unread = Notification.objects.all()
        for m in user_unread:
            if m.recipient.username == user:
                all.append(m)
        user_ser = self.get_serializer(all, many=True)
        return Response(user_ser.data, status=status.HTTP_200_OK)


class UnreadChangeView(GenericAPIView):
    serializer_class = NoTificationsSerializer

    def get(self, request):
        id = request.query_params.get('id')
        user_unread = Notification.objects.get(id=id).mark_as_read()
        data = self.get_serializer(user_unread)

        return Response(data.data, status=status.HTTP_200_OK)

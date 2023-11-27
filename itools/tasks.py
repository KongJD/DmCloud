from celery import shared_task
import subprocess

from django.contrib.auth.models import User
from notifications.signals import notify

from DmCloud.settings import perl_online


@shared_task
def slove_geneprocess(path="", evalue="1e-5", outdir="", tempdir="", request=""):
    cmd = f"perl {perl_online} -input {path} -evalue {evalue} -outdir {outdir} -temp {tempdir}"
    subprocess.run(cmd, shell=True, capture_output=True, text=True)

    # superusers = User.objects.filter(is_superuser=True)
    superusers = User.objects.all()
    verb = f'Your bacterium_genome has been completed. Path is in {outdir} '
    for user in superusers:
        notify.send(sender=User.objects.get(username=request), recipient=user, verb=verb)

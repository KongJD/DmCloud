from celery import shared_task
import subprocess

from django.contrib.auth.models import User
from notifications.signals import notify

perl_16s = "/public/Users/sunll/Web/MarkerDB/Script/16S_pipeline.pl"
perl_rpob = "/public/Users/sunll/Web/MarkerDB/Script/rpoB_pipeline.pl"
perl_online = "/public/Users/liangq/pipeline/fBac_bin/0.Online/Online.pl"


@shared_task
def slove_geneprocess(path="", evalue="1e-5", outdir="", tempdir="", request=""):
    cmd = f"perl {perl_online} -input {path} -evalue {evalue} -outdir {outdir} -temp {tempdir}"
    subprocess.run(cmd, shell=True, capture_output=True, text=True)

    superusers = User.objects.filter(is_superuser=True)
    verb = f'Your bacterium_genome has been completed. Path is in {outdir} '
    for user in superusers:
        notify.send(sender=User.objects.get(username=request), recipient=user, verb=verb)


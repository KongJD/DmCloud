from celery import shared_task
import subprocess

perl_16s = "/public/Users/sunll/Web/MarkerDB/Script/16S_pipeline.pl"
perl_rpob = "/public/Users/sunll/Web/MarkerDB/Script/rpoB_pipeline.pl"
perl_online = "/public/Users/liangq/pipeline/fBac_bin/0.Online/Online.pl"


@shared_task
def slove_16s(type="gene", path="", outdir="", tempdir=""):
    if type == "gene":
        cmd = f"perl {perl_16s} -seq {path} -outdir {outdir} -temp {tempdir}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    elif type == "genome":
        cmd = f"perl {perl_16s} -input {path} -outdir {outdir} -temp {tempdir}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)


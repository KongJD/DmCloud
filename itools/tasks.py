from celery import shared_task
import subprocess

perl_16s = "/public/Users/sunll/Web/MarkerDB/Script/16S_pipeline.pl"
perl_rpob = "/public/Users/sunll/Web/MarkerDB/Script/rpoB_pipeline.pl"
perl_online = "/public/Users/liangq/pipeline/fBac_bin/0.Online/Online.pl"




@shared_task
def slove_geneprocess(path="", evalue="1e-5", outdir="", tempdir=""):
    cmd = f"perl {perl_online} -input {path} -evalue {evalue} -outdir {outdir} -temp {tempdir}"
    subprocess.run(cmd, shell=True, capture_output=True, text=True)

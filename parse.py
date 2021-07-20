import os


def make_tmp():
    os.system('mkdir tmp')


def parse(file):
    cmd = f"cat raw_logs/{file}" + \
          " | awk -F , '{if ($1==\"Fix\") print $1,$3,$4,$9; else if ($1==\"Status\" && $5==1 && $11==1) print $1,$6,$8,$9,$10,$2}'" + \
          f" > tmp/{file}"
    os.system(cmd)


def distroy_tmp():
    os.system('rm -rf tmp')

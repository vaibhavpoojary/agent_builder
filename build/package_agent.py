import os
import tarfile
import time
from pathlib import Path
import boto3

S3_BUCKET = os.environ.get("S3_ARTIFACT_BUCKET") or "raise-native-s3-bucket"
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

def make_tarball(src_dir: str, out_path: str):
    with tarfile.open(out_path, "w:gz") as tar:
        tar.add(src_dir, arcname=Path(src_dir).name)

def upload_to_s3(local_path: str, s3_bucket: str, s3_key: str):
    s3 = boto3.client("s3", region_name=AWS_REGION)
    s3.upload_file(local_path, s3_bucket, s3_key)
    s3_uri = f"s3://{s3_bucket}/{s3_key}"
    return s3_uri

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--src", required=True, help="Source agent folder")
    parser.add_argument("--name", required=True, help="Agent name")
    parser.add_argument("--outdir", default="../deployable", help="Output folder for tarball")
    args = parser.parse_args()

    timestamp = int(time.time())
    artifact_name = f"{args.name}_v{timestamp}.tar.gz"
    out_path = Path(args.outdir) / artifact_name
    os.makedirs(args.outdir, exist_ok=True)

    make_tarball(args.src, out_path)
    print(f"Tarball created: {out_path}")

    # Upload to S3 if bucket is defined
    if S3_BUCKET:
        s3_key = f"artifacts/{args.name}/v{timestamp}/{artifact_name}"
        s3_uri = upload_to_s3(out_path, S3_BUCKET, s3_key)
        print("✅ Uploaded:", s3_uri)
    else:
        print("⚠️  Skipping S3 upload. No bucket configured.")

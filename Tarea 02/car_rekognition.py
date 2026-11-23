"""Detect cars and license plates in images using AWS Rekognition.

The source folder can be a local directory or an S3 prefix (s3://bucket/prefix).
Local images are sent to Rekognition as bytes; S3 images are referenced directly.
"""

import os
import re

import boto3
from botocore.exceptions import BotoCoreError, ClientError

SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png")
CAR_LABELS = {"Car", "vehicle", "Automobile"}
MIN_LABEL_CONFIDENCE = 90.0
MAX_LABELS = 50
AWS_REGION = "us-east-1"
MIN_TEXT_CONFIDENCE = 90.0
MAX_LOCAL_IMAGE_BYTES = 5 * 1024 * 1024  # Rekognition limit for inline image bytes


def is_supported_image(name):
    return name.lower().endswith(SUPPORTED_EXTENSIONS)


def parse_s3_uri(uri):
    bucket, _, prefix = uri[len("s3://"):].partition("/")
    return bucket, prefix


def list_local_images(folder):
    with os.scandir(folder) as entries:
        return sorted(entry.path for entry in entries
                      if entry.is_file() and is_supported_image(entry.name))


def list_s3_keys(s3, bucket, prefix):
    paginator = s3.get_paginator("list_objects_v2")
    keys = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            if is_supported_image(obj["Key"]):
                keys.append(obj["Key"])
    return sorted(keys)


def read_local_image(path):
    if os.path.getsize(path) > MAX_LOCAL_IMAGE_BYTES:
        raise ValueError("image exceeds the 5 MB limit for inline bytes")
    with open(path, "rb") as file:
        return {"Bytes": file.read()}


def to_rekognition_image(reference):
    # S3 references are dicts already; local paths are read lazily, one at a time.
    return reference if isinstance(reference, dict) else read_local_image(reference)


def prepare_source(source):
    """Return a Rekognition client and a list of (display_name, image_reference) pairs."""
    if source.lower().startswith("s3://"):
        bucket, prefix = parse_s3_uri(source)
        s3 = boto3.client("s3", region_name=AWS_REGION)
        rekognition = boto3.client("rekognition", region_name=AWS_REGION)
        items = [(key, {"S3Object": {"Bucket": bucket, "Name": key}})
                 for key in list_s3_keys(s3, bucket, prefix)]
        return rekognition, items

    if not os.path.isdir(source):
        raise ValueError(f"'{source}' is not a valid local folder")
    rekognition = boto3.client("rekognition", region_name=AWS_REGION)
    items = [(os.path.basename(path), path) for path in list_local_images(source)]
    return rekognition, items


def detect_car_confidence(rekognition, image):
    """Return the highest confidence for a car label, or None if no car is detected."""
    response = rekognition.detect_labels(Image=image, MaxLabels=MAX_LABELS,MinConfidence=MIN_LABEL_CONFIDENCE)
    confidences = [label["Confidence"] for label in response["Labels"]
                   if label["Name"] in CAR_LABELS]
    return max(confidences, default=None)


def looks_like_plate(text):
    # Heuristic: plates mix digits and letters and have a typical length.
    return 5 <= len(text) <= 10 and any(c.isdigit() for c in text) and any(c.isalpha() for c in text)


def find_plate_candidates(rekognition, image):
    response = rekognition.detect_text(Image=image)
    candidates = []
    for detection in response["TextDetections"]:
        if detection["Type"] != "LINE" or detection["Confidence"] <= MIN_TEXT_CONFIDENCE:
            continue
        normalized = re.sub(r"[^A-Z0-9]", "", detection["DetectedText"].upper())
        if looks_like_plate(normalized):
            candidates.append(normalized)
    return list(dict.fromkeys(candidates))  # Remove duplicates, keep order


def analyze_images(rekognition, items):
    cars_found = 0
    for name, reference in items:
        try:
            image = to_rekognition_image(reference)
            confidence = detect_car_confidence(rekognition, image)
            if confidence is None:
                print(f"{name}: no cars detected.")
                continue

            cars_found += 1
            print(f"{name}: car detected (confidence {confidence:.1f}%).")
            plates = find_plate_candidates(rekognition, image)
            if plates:
                print(f"  Possible license plates: {', '.join(plates)}")
            else:
                print("  No license plates detected.")
        except (ClientError, BotoCoreError, OSError, ValueError) as error:
            print(f"{name}: error while analyzing image: {error}")

    print(f"\nSummary: {cars_found} of {len(items)} image(s) contain cars.")


def main():
    source = input("Enter a local folder or an S3 folder (s3://bucket/prefix): ").strip().strip('"')
    try:
        rekognition, items = prepare_source(source)
    except (ValueError, ClientError, BotoCoreError) as error:
        print(f"Error: {error}")
        return

    if not items:
        print("No .jpg, .jpeg or .png images found in that folder.")
        return

    analyze_images(rekognition, items)


if __name__ == "__main__":
    main()

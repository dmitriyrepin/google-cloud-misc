"""
Utility functions
"""
import base64
import logging

from google.cloud import storage
from googleapiclient import discovery

_logger = logging.getLogger("drepin-service")


def get_bucket_blob(gcs_path):
    if not gcs_path.startswith("gs://"):
        raise TypeError("The GCS path must start with 'gs://'")
    path = gcs_path[5:]
    [bucket_name, blob_name] = path.split("/", 1)
    return [bucket_name, blob_name]


def get_gcs_file_as_bytes(gcs_path, check_file_type=True):

    [bucket_name, blob_name] = get_bucket_blob(gcs_path)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(blob_name)
    if not blob:
        raise TypeError("Object '{}' doesn't exists in the GCS".format(gcs_path))
    ctype = blob.content_type.split("/", 1)
    if check_file_type and ctype[0] != "text" and blob.content_type != "application/json":
        raise TypeError("The GCS object content must be text ('text/something')")
    blob_as_bytes = blob.download_as_string()
    return blob_as_bytes


def get_gcs_encrypted_file_as_bytes(gcs_path, kms_project_id, key_ring, crypto_key):

    [bucket_name, blob_name] = get_bucket_blob(gcs_path)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(blob_name)
    if not blob:
        raise TypeError("Object '{}' doesn't exists in the GCS".format(gcs_path))
    blob_as_encripted_bytes = blob.download_as_string()
    try:
        excrypted_text = base64.b64encode(blob_as_encripted_bytes).decode("utf-8")
        kms_client = discovery.build("cloudkms", "v1")
        name = "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
            kms_project_id, "global", key_ring, crypto_key)
        # pylint: disable=E1101
        #         disables Instance of 'Resource' has no 'projects' member.
        #         The member does exists. I guess it is added at runtime
        crypto_keys = kms_client.projects().locations().keyRings().cryptoKeys()
        # pylint: enable=E1101
        request = crypto_keys.decrypt(name=name, body={"ciphertext": excrypted_text})
        response = request.execute()
        blob_as_bytes = base64.b64decode(response["plaintext"].encode("ascii"))
    except Exception as ex:
        err_msg = "Failed to decript bucket data"
        _logger.error("%s:\n%s", err_msg, ex)
        raise ValueError(err_msg)

    return blob_as_bytes


def get_gcs_file_as_string(gcs_path, check_file_type=True):

    return get_gcs_file_as_bytes(gcs_path, check_file_type).decode("utf-8")


def get_gcs_encrypted_file_as_string(gcs_path, kms_project_id, key_ring, crypto_key):

    return get_gcs_encrypted_file_as_bytes(gcs_path, kms_project_id, key_ring, crypto_key).decode("utf-8")

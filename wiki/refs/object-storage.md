# Object Storage Runtime References

Nori uses object storage only for runtime assets that external providers must fetch over HTTPS, such as local reference images passed to relay image models. Secrets must stay in environment variables or ignored local shell config.

## Environment

| Variable | Default | Purpose |
| --- | --- | --- |
| `NORI_OSS_ACCESS_KEY_ID` | | Volcengine TOS access key id. |
| `NORI_OSS_SECRET_ACCESS_KEY` | | Volcengine TOS secret access key. |
| `NORI_OSS_BUCKET` | `nori` | Bucket for runtime references. |
| `NORI_OSS_ENDPOINT` | `tos-cn-beijing.volces.com` | TOS endpoint. |
| `NORI_OSS_REGION` | `cn-beijing` | TOS region. |
| `NORI_OSS_PREFIX` | `nori/reference-images` | Root prefix for generated reference objects. |
| `NORI_OSS_SIGNED_URL_EXPIRES` | `86400` | Signed URL lifetime in seconds when no public base URL is configured. |
| `NORI_OSS_PUBLIC_BASE_URL` | | Optional public/custom domain. If omitted, Nori generates signed HTTPS URLs. |

Compatible aliases are also accepted for common TOS names: `TOS_ACCESS_KEY_ID`, `TOS_SECRET_ACCESS_KEY`, `TOS_BUCKET`, `TOS_ENDPOINT`, `TOS_REGION`, `TOS_PUBLIC_BASE_URL`, and `TOS_SIGNED_URL_EXPIRES`.

## Directory Shape

Reference images are uploaded with content-addressed keys:

```text
nori/reference-images/<project>/<session>/<YYYYMMDD>/<sha16>_<source-stem>.<ext>
```

For Holly smoke runs this normally becomes:

```text
nori/reference-images/<task-or-project>/<holly-run-dir>/<YYYYMMDD>/...
```

The object key is persisted in `CoverResult.extra.reference_object_keys`; signed query strings are not persisted. `CoverResult.reference_paths` remains the original local path list so the content package can still trace which user assets influenced the cover.

## Runtime Flow

1. `CoverReferenceSelector` chooses local or remote reference paths.
2. `ReferenceImagePublisher` uploads local image bytes to Volcengine TOS when OSS env is configured.
3. CoverDirector passes signed HTTPS URLs to `llms.image(reference_images=...)`.
4. Relay image generation receives URL references instead of local bytes/base64.

If OSS env is absent, local tests and non-relay providers keep the previous local-bytes behavior.

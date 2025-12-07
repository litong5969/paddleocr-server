# Helm Chart — paddleocr-server

## Install
- Set image repository to GHCR (built by this repo's workflow) or your registry:
  - `--set image.repository=ghcr.io/litong5969/paddleocr-server --set image.tag=latest`
- CPU install:
  ```bash
  helm upgrade -i ocr ./ops/helm/paddleocr-server \
    --set image.repository=ghcr.io/litong5969/paddleocr-server \
    --set image.tag=latest \
    --set env.OCR_USE_GPU=false
  ```
- GPU install (requires NVIDIA device plugin):
  ```bash
  helm upgrade -i ocr ./ops/helm/paddleocr-server \
    --set image.repository=ghcr.io/litong5969/paddleocr-server \
    --set image.tag=latest \
    --set useGpu=true \
    --set env.OCR_USE_GPU=true
  ```

## Persistence (model cache)
- Enable a PVC to persist `/root/.paddleocr` and avoid re-downloading models:
  ```bash
  --set persistence.enabled=true --set persistence.size=10Gi --set persistence.storageClass=fast-ssd
  ```

## Service and Ingress
- Default `ClusterIP` on port 80 -> container 5000.
- Enable ingress:
  ```bash
  --set ingress.enabled=true --set ingress.hosts[0].host=ocr.example.com
  ```

## Values highlights
- `env.*` maps to the same variables as `.env` files (`OCR_LANG`, `OCR_VERSION`, `OCR_USE_GPU`, `METRICS_ENABLED`...).
- `useGpu=true` adds `nvidia.com/gpu: 1` limit and NVIDIA envs.

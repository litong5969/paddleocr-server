# Nginx 路径路由示例（同端口，同服务）

以下示例将 `/`（含 `/ui`）与 `/ocr` 路径转发到同一个后端服务（宿主 5215 → 容器 5000）。

```nginx
server {
  listen 80;
  server_name ocr.local;

  # Web GUI 与根路径
  location / {
    proxy_pass http://127.0.0.1:5215/; # 根路径会在后端重定向到 /ui
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }

  # OCR API（单图与批量）
  location /ocr {
    proxy_pass http://127.0.0.1:5215/ocr;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }

  # 健康与指标（可选暴露）
  location /healthz { proxy_pass http://127.0.0.1:5215/healthz; }
  location /readyz  { proxy_pass http://127.0.0.1:5215/readyz; }
  location /metrics { proxy_pass http://127.0.0.1:5215/metrics; }
}
```

说明：
- 同源优势：GUI 与 API 共端口，避免跨域与 Cookie/Token 复杂度。
- 也可将 5215 换为你自定义的 `HOST_PORT`。

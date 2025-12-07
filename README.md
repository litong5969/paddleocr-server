# PaddleOCR Server 使用说明

## 镜像获取与运行
- 推荐挂载模型缓存目录，避免重复下载：`-v /mnt/user/appdata/paddleocr/models:/root/.paddleocr`
- GPU 运行：
  ```bash
  docker run -d --gpus all \
    -p 5000:5000 \
    -v /mnt/user/appdata/paddleocr/models:/root/.paddleocr \
    --name paddleocr-server \
    litong5969/paddleocr-server:cuda12.6
  ```
- CPU 运行（无 GPU 也可用同一镜像）：
  ```bash
  docker run -d \
    -p 5000:5000 \
    -v /mnt/user/appdata/paddleocr/models:/root/.paddleocr \
    --name paddleocr-server \
    litong5969/paddleocr-server:cuda12.6
  ```
- 同步发布了 `:latest` 标签，等价于当前版本。

## API
- 端点：`POST /ocr`
- 参数：表单文件字段 `file`（图像文件）
- 返回：提取的文本和逐行置信度
- 请求示例：
  ```bash
  curl -X POST http://localhost:5000/ocr \
    -F "file=@/path/to/image.jpg"
  ```

## 开发与发布
- 修改代码后直接 `git add . && git commit -m "..." && git push` 到 `main`。
- GitHub Actions 会自动构建并推送镜像到 DockerHub：`litong5969/paddleocr-server:{latest,cuda12.6}`。

from fastapi.testclient import TestClient

import server


def test_root_redirects_to_ui():
    client = TestClient(server.app)
    r = client.get("/", allow_redirects=False)
    assert r.status_code in (301, 302, 307, 308)
    assert r.headers.get("location", "").endswith("/ui")


def test_ui_served():
    client = TestClient(server.app)
    r = client.get("/ui")
    assert r.status_code == 200
    body = r.text
    assert "PaddleOCR Server — Web UI" in body
    assert "multiple" in body  # 多文件选择
    assert "复制文本" in body   # 复制按钮
    assert "历史记录" in body   # 历史面板
    assert "服务信息" in body   # 元信息面板文案
    assert "调用模式" in body   # 参数面板
    assert "置信度阈值" in body
    assert "最多行数" in body
    assert "聚合分隔符" in body
    assert "截图" in body       # 截图按钮
    assert "导出文本" in body   # 导出按钮

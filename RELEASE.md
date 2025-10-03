# PyPI 发布指南

## 准备工作

### 1. 注册 PyPI 账户
- 访问 [PyPI](https://pypi.org/) 注册账户
- 访问 [TestPyPI](https://test.pypi.org/) 注册测试账户

### 2. 安装发布工具
```bash
pip install twine build
```

### 3. 配置 PyPI 凭据
创建 `~/.pypirc` 文件（Linux/Mac）或配置环境变量：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = your-pypi-token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = your-testpypi-token
```

或者使用环境变量：
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=your-pypi-token
```

## 发布流程

### 1. 测试构建
```bash
python -m build
```

### 2. 检查包内容
```bash
twine check dist/*
```

### 3. 发布到 TestPyPI（可选，推荐）
```bash
twine upload --repository testpypi dist/*
```

### 4. 测试安装
```bash
pip install --index-url https://test.pypi.org/simple/ hoogle-mcp-server
```

### 5. 发布到 PyPI
```bash
twine upload dist/*
```

## 版本管理

### 版本号规范
- `0.1.0` - 初始版本
- `0.1.1` - bug修复
- `0.2.0` - 新功能
- `1.0.0` - 稳定版本

### 更新版本号
在 `setup.py` 和 `pyproject.toml` 中更新版本号：

```python
# setup.py
version="0.1.0"
```

```toml
# pyproject.toml
version = "0.1.0"
```

## 发布检查清单

- [ ] 更新版本号
- [ ] 更新 CHANGELOG.md（如果存在）
- [ ] 运行测试
- [ ] 构建包
- [ ] 检查包内容
- [ ] 发布到 TestPyPI（可选）
- [ ] 测试安装
- [ ] 发布到 PyPI

## 常见问题

### 包名已存在
如果 `hoogle-mcp-server` 已被占用，需要在 `setup.py` 和 `pyproject.toml` 中修改包名。

### 权限错误
确保使用正确的 API token 和权限。

### 依赖问题
确保所有依赖在 PyPI 上可用。
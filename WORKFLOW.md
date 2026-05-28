# 工作流程规则

## 🔴 第一规则: 写入文件必须使用追加模式

**所有对文件的写入操作，必须使用追加(append)模式，严禁覆盖。**

### Python追加模式
```python
# 正确 - 追加
with open(filename, 'a', encoding='utf-8') as f:
    f.write(content + '\n')
```

```python
# 禁止 - 覆盖写入
with open(filename, 'w', encoding='utf-8') as f:
    f.write(content)
```

### PowerShell追加模式
```powershell
# 正确 - 追加
Add-Content filename.txt "content"
"content" >> filename.txt

# 禁止 - 覆盖写入
Set-Content filename.txt "content"
"content" > filename.txt
```

---

## 📋 标准工作流程

### 1. 业务执行必须使用Python脚本
```bash
python script_name.py
```

### 2. 文件操作流程
1. 创建备份 (.bak)
2. 读取检查确认
3. 追加写入修改
4. 验证结果

### 3. HEAD信息更新
- 已有头部则只更新时间和大小
- 无头部则追加头部

### 4. 文档说明只能写入README.md
- *.txt 文件只包含译文内容
- 文档说明统一在README.md

---

## 📝 文件头信息标准

每个*.txt译文文件头部包含:
```
# ==============================================
# 文件名
# ==============================================
#
# Steam版本: 2.4.0
# Git项目路径: https://github.com/aspnmy/XUnity.AutoTranslator_Fallout-Shelter.git
# 精翻作者: aspnmy
# 技术支持: support@e2bank.cn
#
# ==============================================
```

---

**Steam版本**: 2.4.0
**Git项目**: https://github.com/aspnmy/XUnity.AutoTranslator_Fallout-Shelter.git  
**精翻作者**: aspnmy
**技术支持**: support@e2bank.cn
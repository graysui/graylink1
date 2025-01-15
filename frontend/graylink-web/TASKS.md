根据分析，我们需要重点修改的文件有：

1. 类型定义文件：
   ✅ /types/api.ts - 已更新，包含了所有需要的类型定义
   ✅ /types/response.d.ts - 已合并到api.ts，暂时保留以防止类型错误
   ✅ /types/monitor.ts 和 monitor.d.ts - 已合并到api.ts并删除
   ✅ /types/symlink.ts - 已合并到api.ts并删除
   ✅ /types/emby.ts - 已合并到api.ts并删除

2. Store模块：
   ✅ /stores/modules/symlink.ts - API调用已更新
   ✅ /stores/modules/emby.ts - API调用已更新
   ✅ /stores/modules/monitor.ts - API调用已更新
   ✅ /stores/modules/file.ts - 已更新API调用
   ✅ /stores/modules/setting.ts - 已更新API调用

3. API接口文件：
   ✅ /api/emby.ts - 已更新
   ✅ /api/gdrive.ts - 已更新
   ✅ /api/setting.ts - 已更新
   ✅ /api/symlink.ts - 已更新
   ✅ /api/monitor.ts - 已更新
   ✅ /api/file.ts - 已更新API调用
   ✅ /api/user.ts - 已更新

4. 遇到的问题：
   - pinia 类型定义问题需要解决
   - store 的状态类型定义需要修复
   - 部分类型文件的合并需要谨慎处理，确保不破坏现有功能

下一步计划：
1. 解决 pinia 的类型问题
2. 修复 store 模块的类型错误
3. 完成剩余 API 接口的更新
4. 最后再处理类型文件的合并
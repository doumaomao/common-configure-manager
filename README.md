# common-configure-manager

### 适用场景

 对各种路径下的文件做文本替换和检测
 
### 配置字段解释

 - common_file - 指定目录或者文件路径
 - common_map - 指定替换规则或者检测规则
 - common_filter - 指定替换文件后缀范围
 - common_exclude - 排除的目录或者文件路径
 - description - 规则描述
 
### 使用步骤
 - 在conf/common.json中根据业务需求进行配置
 - 针对查找或者替换等功能，对re.search进行修改
 - 执行commonProcess.py

 
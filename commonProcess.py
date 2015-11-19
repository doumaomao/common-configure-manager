# -*- coding: utf-8 -*-
# author = 'liyujie'
# version = '1.0'
# date = '2015-11-9'
# descripton : 通用配置处理（地址替换/代码检查)

import json
import re
import os

class commonProcess(object):
    jobList = []
    commonConfig = {}
    matchList = []

    def __init__(self, checkCommonConf):
        self._get_config(checkCommonConf)
        pass

    def _parse_config(self):
        for index in self.commonConfig:
            tmp = {}
            for rule_map in self.commonConfig[index]["common_rule"]:
                tmp[rule_map.encode("utf-8")] = self.commonConfig[index]["common_rule"][rule_map].encode("utf-8")
            self.commonConfig[index]["common_rule"] = tmp

    def _get_config(self, checkCommonConf):

        # 对配置本身的处理扩展
        # 待随后续需求补充
        # f = open(checkCommonConf)
        # content = f.read()
        # f.writelines(content)
        # f.close()
        try:
            self.commonConfig = json.load(open(checkCommonConf, "r"))
        except ValueError:
            print "Error:can not parse json file"
        else:
            self.commonConfig = self.commonConfig['common']
            self._parse_config()

    def get_common_files(self, common_file, common_filter, common_exclude):
        tmp_file_list = []
        common_file_list = []
        # 遍历配置路径中的文件
        for file_item in common_file:
            if os.path.isfile(file_item):
                tmp_file_list.append(file_item)
            elif os.path.isdir(file_item):
                for dirpath, subdir, filelist in os.walk(file_item):
                    for filename in filelist:
                        tmp_file_list.append(os.path.join(dirpath, filename))
        for tmpfile in tmp_file_list:
            if "." in tmpfile and ("." + tmpfile.rsplit('.', 1)[1]) in common_filter:
                add_tag = 1
                if common_exclude != ["NULL"]:
                    for exclude in common_exclude:
                        if tmpfile.find(exclude) == 0:
                            add_tag = 0
                            break
                if add_tag == 1:
                    common_file_list.append(tmpfile)
        return common_file_list

    def get_common_configure_info(self):
        for conf in self.commonConfig:
            common_files = self.get_common_files(self.commonConfig[conf]["common_file"],
                                               self.commonConfig[conf]["common_filter"],
                                               self.commonConfig[conf]["common_exclude"])
            for file in common_files:
                self.jobList.append((file, self.commonConfig[conf]["common_rule"]))
        commonProcess.FileSum = len(self.jobList)

    def common_process(self, common_file, common_rule):
        f = open(common_file, "r")
        for (num, common_content) in enumerate(f):
            for rule in common_rule:
                is_hit = re.search(rule, common_content)
                if is_hit is not None:
                    self.matchList.append((common_file, rule, common_rule[rule], num))
        f.close()

    def common_job(self):
        """
        the entry function,common handle,take the code detection as example
        :return:
        """
        self.get_common_configure_info()
        for jobFile, jobMap in self.jobList:
            if os.path.isfile(jobFile):
                self.common_process(jobFile, jobMap)
                pass


if __name__ == '__main__':
    conf = "./conf/common.json"
    code = commonProcess(conf)
    code.common_job()

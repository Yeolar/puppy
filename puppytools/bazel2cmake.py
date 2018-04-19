#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Yeolar
#

import argparse
import os
from collections import defaultdict

from puppytools.util.colors import *


PROG_NAME = os.path.splitext(os.path.basename(__file__))[0]


def path_name_to_key(path, name):
    return '//%s:%s' % (path, name)


def key_to_path_name(key):
    path, _, name = key.partition(':')
    path = path[2:]
    return path, name


class CCLibrary(object):

    def __init__(self, path,
            name='', srcs=[], hdrs=[], deps=[], visibility=[],
            testonly=0, alwayslink=0, linkstatic=0, deprecation='',
            linkopts=[], data=[], tags=[], copts=[]):
        self.key = path_name_to_key(path, name)
        self.path = path
        self.name = name
        self.srcs = srcs
        self.hdrs = hdrs
        self.deps = []
        for dep in deps:
            if dep.startswith(':'):
                self.deps.append('//%s%s' % (path, dep))
            else:
                self.deps.append(dep)
        self.visibility = visibility
        self.testonly = testonly
        self.alwayslink = alwayslink
        self.linkstatic = linkstatic
        self.deprecation = deprecation
        self.linkopts = linkopts
        self.data = data
        self.tags = tags
        self.copts = copts

    def __str__(self):
        return self.__dict__.__str__()


class ProtoLibrary(object):

    def __init__(self, path,
            name='', srcs=[], deps=[], visibility=[],
            testonly=0,
            cc_api_version=0,
            java_api_version=0,
            js_api_version=0,
            go_api_version=0,
            cc_grpc_version=0,
            has_services=0):
        self.key = path_name_to_key(path, name)
        self.path = path
        self.name = name
        self.srcs = srcs
        self.deps = []
        for dep in deps:
            if dep.startswith(':'):
                self.deps.append('//%s%s' % (path, dep))
            else:
                self.deps.append(dep)
        self.visibility = visibility
        self.testonly = testonly
        self.cc_api_version = cc_api_version
        self.java_api_version = java_api_version
        self.js_api_version = js_api_version
        self.go_api_version = go_api_version
        self.cc_grpc_version = cc_grpc_version
        self.has_services = has_services

    def __str__(self):
        return self.__dict__.__str__()


proj_root = None
curr_path = None
path_item_dict = defaultdict(dict)


def get_curr_path(dir):
    return os.path.relpath(dir, os.path.dirname(proj_root))


def log_block(func, *args, **kwargs):
    print cyan('%s(' % func.__name__)
    for a in args:
        print cyan('    %s,' % a)
    for k, v in kwargs.items():
        print cyan('    %s = %s,' % (k, v))
    print cyan(')')


def func_msg(func, *args, **kwargs):
    return '%s(%s, %s)' % (
            func.__name__,
            ', '.join(['%s' % a for a in args]),
            ', '.join(['%s = %s' % (k,v) for k,v in kwargs.items()]))


def glob(*args, **kwargs):
    return []
def if_mkl(*args, **kwargs):
    return func_msg(if_mkl, *args, **kwargs)
def select(*args, **kwargs):
    return []
def tf_copts(*args, **kwargs):
    return []
def tf_cuda_tests_tags(*args, **kwargs):
    return func_msg(tf_cuda_tests_tags, *args, **kwargs)
def tf_additional_binary_deps(*args, **kwargs):
    return []

###

def package(*args, **kwargs):
    log_block(package, *args, **kwargs)
def config_setting(*args, **kwargs):
    log_block(config_setting, *args, **kwargs)
def package_group(*args, **kwargs):
    log_block(package_group, *args, **kwargs)
def filegroup(*args, **kwargs):
    log_block(filegroup, *args, **kwargs)


def licenses(*args):
    log_block(licenses, *args)
def load(*args):
    log_block(load, *args)
def exports_files(*args):
    log_block(exports_files, *args)


def cc_library(*args, **kwargs):
    log_block(cc_library, *args, **kwargs)
    o = CCLibrary(curr_path, **kwargs)
    path_item_dict[curr_path][o.name] = o


def cc_test(*args, **kwargs):
    log_block(cc_test, *args, **kwargs)


def cc_binary(*args, **kwargs):
    log_block(cc_binary, *args, **kwargs)


def py_library(*args, **kwargs):
    log_block(py_library, *args, **kwargs)
def py_test(*args, **kwargs):
    log_block(py_test, *args, **kwargs)
def py_binary(*args, **kwargs):
    log_block(py_binary, *args, **kwargs)


def android_binary(*args, **kwargs):
    log_block(android_binary, *args, **kwargs)


def serving_proto_library(*args, **kwargs):
    log_block(serving_proto_library, *args, **kwargs)
    o = ProtoLibrary(curr_path, **kwargs)
    path_item_dict[curr_path][o.name] = o


def serving_proto_library_py(*args, **kwargs):
    log_block(serving_proto_library_py, *args, **kwargs)


def serving_go_grpc_library(*args, **kwargs):
    log_block(serving_go_grpc_library, *args, **kwargs)


def tf_custom_op_library(*args, **kwargs):
    log_block(tf_custom_op_library, *args, **kwargs)
def tf_pyclif_proto_library(*args, **kwargs):
    log_block(tf_pyclif_proto_library, *args, **kwargs)
def tf_cc_test(*args, **kwargs):
    log_block(tf_cc_test, *args, **kwargs)
def tf_cc_binary(*args, **kwargs):
    log_block(tf_cc_binary, *args, **kwargs)
def tf_cc_shared_object(*args, **kwargs):
    log_block(tf_cc_shared_object, *args, **kwargs)
def tf_py_test(*args, **kwargs):
    log_block(tf_py_test, *args, **kwargs)
def tf_py_logged_benchmark(*args, **kwargs):
    log_block(tf_py_logged_benchmark, *args, **kwargs)


def sh_test(*args, **kwargs):
    log_block(sh_test, *args, **kwargs)
def sh_binary(*args, **kwargs):
    log_block(sh_binary, *args, **kwargs)


def pkg_tar(*args, **kwargs):
    log_block(pkg_tar, *args, **kwargs)
def pkg_deb(*args, **kwargs):
    log_block(pkg_deb, *args, **kwargs)


def gen_cmake(dir):
    cc_tpl = """
set(%(ROLE)s_SRCS
    %(cc)s
)

add_library(%(role)s OBJECT ${%(ROLE)s_SRCS})
"""
    pb_tpl = """
set(%(ROLE)s_PROTOS
    %(pb)s
)

foreach(proto ${%(ROLE)s_PROTOS})
    execute_process(protoc --cpp_out=. --proto_path=${PROJECT_SOURCE_DIR} ${proto})
endforeach()
"""
    rel = get_curr_path(dir).replace('/', '_')
    try:
        cc = []
        pb = []
        item_dict = path_item_dict[get_curr_path(dir)]
        for item in item_dict.values():
            if isinstance(item, CCLibrary):
                cc += item.srcs
            elif isinstance(item, ProtoLibrary):
                pb += item.srcs
        cc.sort()
        pb.sort()
    except KeyError:
        print red('directory %s has no item' % dir)
    d = dict(
        role=rel,
        ROLE=rel.upper(),
        cc='\n    '.join(cc),
        pb='\n    '.join(pb),
    )
    cmake = os.path.join(dir, 'CMakeLists.txt')
    print yellow('generate ' + cmake)
    with open(cmake, 'w') as fp:
        fp.write('# Copyright 2018 Yeolar\n')
        if d['cc']:
            fp.write(cc_tpl % d)
        if d['pb']:
            fp.write(pb_tpl % d)


def main():
    ap = argparse.ArgumentParser(
            prog='pp-' + PROG_NAME,
            description='Convert bazel BUILD to cmake file.',
            epilog='Author: Yeolar <yeolar@gmail.com>')
    ap.add_argument('root', help='root directory')
    args = ap.parse_args()

    global proj_root
    global curr_path

    build_dirs = []
    proj_root = os.path.abspath(args.root)

    for root, dirs, files in os.walk(proj_root):
        for file in files:
            if file == 'BUILD':
                path = os.path.join(root, file)
                build_dirs.append(root)
                curr_path = get_curr_path(root)
                print yellow('parse ' + path)
                with open(path) as fp:
                    try:
                        exec fp.read()
                    except NameError as e:
                        print blue('ignore: %s' % e)

    print yellow('lose deps:')
    for path, item_dict in path_item_dict.items():
        for name, item in item_dict.items():
            print item.key
            for dep in item.deps:
                if dep[0] == '@':
                    print ' ', dep
                else:
                    p, n = key_to_path_name(dep)
                    try:
                        path_item_dict[p][n]
                    except KeyError:
                        print '-', red(dep)

    for dir in build_dirs:
        gen_cmake(dir)


if __name__ == '__main__':
    main()


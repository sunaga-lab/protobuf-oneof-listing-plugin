#!/usr/bin/env python

import sys, os, os.path
from google.protobuf.compiler import plugin_pb2 as plugin
import itertools
from jinja2 import Environment, FileSystemLoader
import inflection
import glob

TEMPLATE_DIR_PARAM_KEY = "templates"
DEFAULT_TEMPLATES_PATH = "templates/*"

class OneofCase:
    def __init__(self, package, type_name, value_name):
        self.type_name_full = type_name
        if package in type_name:
            self.type_name = type_name.replace("."+package+".", "")
        else:
            self.type_name = type_name
        self.value_name = value_name


class OneofInfo:
    def __init__(self, package, msg_name, fieldname):
        self.package = package
        self.msg_name = msg_name
        self.fieldname = fieldname
        self.cases = []

    def add_case(self, case):
        self.cases.append(case)


def parse_file(file):
    all_oneofs = list(itertools.chain(*[parse_message_type(file.package, msgtype) for msgtype in file.message_type]))
    return all_oneofs

def parse_message_type(package, msg_type):
    oneofs = [OneofInfo(package, msg_type.name, decl.name) for decl in msg_type.oneof_decl]

    for field in msg_type.field:
        if field.HasField("oneof_index"):
            oneofs[field.oneof_index].add_case(
                OneofCase(package, field.type_name, field.name)
            )

    return oneofs

def add_name_filters(env):
    env.filters['camelize'] = inflection.camelize
    env.filters['camelize_lower'] = lambda s: inflection.camelize(s, False)
    env.filters['underscore'] = inflection.underscore
    env.filters['underscore_upper'] = lambda s: inflection.underscore(s).upper()
    env.filters['underscore_lower'] = lambda s: inflection.underscore(s).lower()
    env.filters['upper'] = lambda s: s.upper()
    env.filters['lower'] = lambda s: s.lower()

def main():
    # Read request
    data = sys.stdin.buffer.read()
    request = plugin.CodeGeneratorRequest()
    request.ParseFromString(data)

    response = plugin.CodeGeneratorResponse()

    oneofs = list(itertools.chain(*[parse_file(item) for item in request.proto_file]))

    # Prepare rendering env
    env = Environment(loader=FileSystemLoader(["."], encoding='utf8'))
    add_name_filters(env)

    if request.parameter.startswith(TEMPLATE_DIR_PARAM_KEY + "="):
        templates = request.parameter[len(TEMPLATE_DIR_PARAM_KEY)+1:]
    else:
        templates = DEFAULT_TEMPLATES_PATH
    template_target_glob = glob.glob(templates)
    if len(template_target_glob) == 0:
        response.error = "No such template: " + templates + " (from " + os.getcwd() + ")"
    else:
        for tfn in template_target_glob:
            tmpl = env.get_template(tfn)
            output = tmpl.render(oneofs=oneofs)
            f: response.File = response.file.add()
            f.name = os.path.basename(tfn).replace(".tpl", "")
            f.content = output

    output = response.SerializeToString()
    sys.stdout.buffer.write(output)

if __name__ == '__main__':
    main()

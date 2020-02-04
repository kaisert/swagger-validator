import sys
import json


prefix = '#/components/schemas/'

def find_refs(schema):
    refs = []
    if type(schema) is dict:
        for k, v in schema.items():
            if k == '$ref':
                return [v]
            else:
                refs = refs + find_refs(v)
    if type(schema) is list:
        for s in schema:
            refs = refs + find_refs(s)
    return refs

def main():
    file = open(sys.argv[1], 'r')
    json_string = file.read()
    
    json_obj = json.loads(json_string) 

    schemas = json_obj["paths"]

    for k, schema in schemas.items():
        refs = [r[len(prefix):] for r in find_refs(schema) if not "CustomerPortal" in r]
        if len(refs) > 0:
            print(k)
            print(str(refs))


if __name__ == '__main__':
    main()

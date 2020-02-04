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

def find_circle(schema, ref_deps, visited):
    refs = ref_deps[schema]
    if schema in visited:
        return True, visited 
    elif len(refs) == 0:
        return False, []
    else:
        visited = visited + [schema]

        result = [find_circle(r, ref_deps, visited.copy()) for r in refs]
        return any(has_circle for (has_circle, _) in result), [circle for (_, circle) in result if len(circle) > 0]
    return False, []

def main():
    file = open(sys.argv[1], 'r')
    json_string = file.read()
    
    json_obj = json.loads(json_string) 

    schemas = json_obj["components"]["schemas"]
    ref_deps = {}

    for k, schema in schemas.items():
        refs = [r[len(prefix):] for r in find_refs(schema)]
        ref_deps[k] = refs

    for k in schemas.keys():
        has_circle, circles = find_circle(k, ref_deps, [])
        if has_circle:
            print(k)
            for circle in circles:
                print('   ' + str(len(circle)))


if __name__ == '__main__':
    main()

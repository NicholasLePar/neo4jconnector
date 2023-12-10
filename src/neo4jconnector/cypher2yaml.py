import argparse
import os
import yaml

def parse_cypher_file(cypherFilePath,debug=True):
    if debug:
        print(cypherFilePath)

    lines = None
    with open(cypherFilePath) as f:
        lines = f.readlines()

    if debug:
        print(lines)

    #Set the key for the cypher query as the filename
    file_name_key = os.path.basename(cypherFilePath).split(".")[0]
    result = {file_name_key:''.join(lines) }
    return result

def parse_cypher_directory(cypherDirPath, debug=True):
    if debug:
        print(cypherDirPath)

    result = {}
    for root, dirs, files in os.walk(cypherDirPath):
        for f in files:
            result.update(parse_cypher_file(root+f))

    return result

def str_presenter(dumper, data):
  '''
  The yaml presenter for literal writing
  '''
  if len(data.splitlines()) > 1:  # check for multiline string
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
  return dumper.represent_scalar('tag:yaml.org,2002:str', data)

def write_yaml(output, yamlFilePath, debug=True):
    if debug:
        print(output)

    #set the yaml dump method to our str presenter
    yaml.add_representer(str, str_presenter)

    with open(yamlFilePath,'w') as f:
        yaml.dump(output, f)

def cypher2yaml(cypherFilePath, yamlFilePath):
    #Check cypherFilePath type
    isFile = os.path.isfile(cypherFilePath)
    isDirectory = os.path.isdir(cypherFilePath)

    #Parse cypher files
    result = None
    if isFile:
        result = parse_cypher_file(cypherFilePath)
    elif isDirectory:
        result = parse_cypher_directory(cypherFilePath)
    else:
        raise Exception('Invalid cypher filepath.')

    #write parsed result to yaml
    write_yaml(result,yamlFilePath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(dest='cypherFilePath',
                        type=str,
                        help='Filename (ex: query.cypher) or\
                            Directory containing *.cypher files')

    parser.add_argument(dest='yamlFilePath',
                        type=str,
                        help='Filename (ex: cypher_queries.yaml) that will\
                            contain the cypher queries.')

    args = parser.parse_args()

    cypher2yaml(args.cypherFilePath, args.yamlFilePath)

import yaml
from yaml.loader import SafeLoader

def main():
    with open("yaml/cypher_queries.yaml",'r') as f:
        y = yaml.safe_load(f)
        print(y)

if __name__ == "__main__":
    main()
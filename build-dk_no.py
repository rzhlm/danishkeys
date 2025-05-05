from build import *


def main():
    version_tuple = get_version()
    temp_version = list(version_tuple)
    temp_version[2] += 1 # 'patch' value
    
    build(Country.DENMARK, tuple(temp_version))
    build(Country.NORWAY, tuple(temp_version))
    
    update_version(tuple(temp_version))

if __name__ == "__main__":
    main()

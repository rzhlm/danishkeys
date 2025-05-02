import os
from enum import Enum
import shutil


def get_version() -> tuple[int, int, int]:
    with open("version.ini",'r') as file:
        _ = file.readline()
        major: int = int(file.readline())
        minor: int = int(file.readline())
        patch: int = int(file.readline())
    return (major, minor, patch)


def update_version(major:int, minor: int, patch) -> None:
    with open("version.ini","w+"):
        file.writeline("major, minor, patch\n")
        file.writeline(f"{major}\n{minor}\n{patch}\n"])


def start_AHK(version: str, country: Enum) -> None:
    if country == Country.DENMARK:
        icon: str = '"./icon/dk/dk-col.ico"'
        out_file: str = '"danish_keys"'
    elif country == Country.NORWAY:
        icon: str = '"./icon/no/no-col.ico"'
        out_file: str = '"norwegian_keys"'

    out_file += version + '.exe"'
    in_file: str = '"danishkeys.ahk2"'
    compiler: str = '"AutoHotkey64.exe"'
    
    cmd: str = f'Ahk2Exe.exe /in {in_file} /bin {compiler} /icon {icon} /out {out_file}'
    os.system(f"cmd /k {cmd}")
    #Ahk2Exe.exe /in "danishkeys.ahk" /bin "AutoHotkey64.exe" /icon "./icon/dk/dk-col.ico" /out "NAME.exe"
    
    
def build(country: Enum):
    # VERSION LOGIC
    major: int, minor: int, patch: int = get_version()
    patch += 1
    update_version(major, minor, patch)

    # ICONS, COPY, MODIFY SOURCE
    if country == Country.DENMARK:
        icon: str = f'./icon/dk/dk-col.ico'
        grey_ico: str = f'./icon/dk/dk-bw.ico'
    elif country == Country.NORWAY:
        icon: str == f'./icon/no/no-col.ico'
        grey_ico: str == f'./icon/no/no-bw.ico'
        
    shutil.copy("danishkeys.ahk2", "tempsource.ahk2")
    
    with open("tempsource.ahk2",'a+') as file:
        file.write(f'version := "{major}.{minor}.{patch}"\n')
        file.write(f';@Ahk2Exe-SetMainIcon {icon}\n')
        for i in range(206, 209):
            file.write(f';@Ahk2Exe-AddResource {grey_ico}, {i}\n')
                
    # BUILD for DENMARK
    start_AHK(f"{major}_{minor}_{patch}", country)
    
    # REMOVE TEMPORARY FILES
    if os.path.exists("tempsource.ahk2"):
        os.remove("tempsource.ahk2")
    else:
        print("No temp files! Something is broken.")
    

#def main():
#    Country = Enum("Country", ["DENMARK", "NORWAY"])
#    build(Country.DENMARK)

if __name__ == "__main__":
    print("This file must be imported and called from within another file")

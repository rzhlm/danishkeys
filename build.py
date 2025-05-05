import os
import subprocess
from enum import Enum
import shutil


Country = Enum("Country", ["DENMARK", "NORWAY"])


def get_version() -> tuple[int, int, int]:
    with open("version.ini",'r') as file:
        _ = file.readline()
        major: int = int(file.readline().strip())
        minor: int = int(file.readline().strip())
        patch: int = int(file.readline().strip())
    return (major, minor, patch)


def update_version(version_tuple: tuple[int, int, int]) -> None:
    major, minor, patch = version_tuple
    print("entering UPDATE VERSION FILE")
    print(f"with params: {major=} {minor=} {patch=}")
    with open("version.ini","w+") as file:
        file.write("major, minor, patch\n")
        file.write(f"{major}\n{minor}\n{patch}\n")


def start_AHK(version: str, country: Enum) -> None:
    if country == Country.DENMARK:
        icon: str = r'".\icon\dk\dk-col.ico"'
        out_file: str = r'"danish_keys'
    elif country == Country.NORWAY:
        icon: str = r'".\icon\no\no-col.ico"'
        out_file: str = '"norwegian_keys'

    ahk_path = r"C:\Users\patrick\AppData\Local\Programs\AutoHotkey\\"
    cp_path = ahk_path + r"\Compiler\\"
    bin_path = ahk_path + r"\v2\\"
    
    out_file += version + '.exe"'
    in_file: str = '"tempsource.ahk2"'
    
    interpreter: str = f'"{bin_path}AutoHotkey64.exe"'
    
    cmd: str = f'"{cp_path}Ahk2Exe.exe" /in {in_file} /bin {interpreter} /icon {icon} /out {out_file} /compress 0'
    #os.system(f"cmd /k {cmd}")
    print(f"calling: {cmd=}")
    subprocess.run(cmd, shell = True)
    #Ahk2Exe.exe /in "danishkeys.ahk" /bin "AutoHotkey64.exe" /icon "./icon/dk/dk-col.ico" /out "NAME.exe"
    
    
def build(country: Enum, version_tuple: tuple[int, int, int]):
    # VERSION LOGIC
    major, minor, patch = version_tuple

    # ICONS, COPY, MODIFY SOURCE
    if country == Country.DENMARK:
        icon: str = r'.\icon\dk\dk-col.ico'
        grey_ico: str = r'.\icon\dk\dk-bw.ico'
    elif country == Country.NORWAY:
        print("NORWAY")
        icon: str = r'.\icon\no\no-col.ico'
        grey_ico: str = r'.\icon\no\no-bw.ico'
        
    shutil.copy("danishkeys.ahk2", "tempsource.ahk2")
    #print(f"{icon}")
    
    with open("tempsource.ahk2",'r') as file:
        original_source = file.read()
    
    with open("tempsource.ahk2", 'w') as file:
        file.write("#SingleInstance Prompt\n")
        file.write(f'global version\n')
        file.write(f'version := "{major}.{minor}.{patch}"\n')
        #file.write(f'MsgBox(version)\n')
        file.write(f';@Ahk2Exe-SetMainIcon {icon}\n')
        # ;@Ahk2Exe-SetMainIcon ./icon/dk/dk-col.ico ;  color icon
        for i in range(206, 209):
            file.write(f';@Ahk2Exe-AddResource {grey_ico}, {i}\n')
        file.write(original_source)
        
    # BUILD for COUNTRY
    start_AHK(f"_v{major}_{minor}_{patch}", country)
    
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

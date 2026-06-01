import ctypes
import configparser
import os
import sys

config = configparser.ConfigParser()

def HexView(path, bin_name):
    with open(path + bin_name + ".bin", 'rb') as in_file:

        in_file.seek(1024)                  #go to address 1024
        #hexdata = in_file.read(4).hex()     # I like to read 4 bytes in then new line it.
        ver_major = in_file.read(1).hex()
        ver_minor = in_file.read(1).hex()
        ver_revision = in_file.read(1).hex()
        ver_patch = in_file.read(1).hex()
    return (ver_major,ver_minor,ver_revision,ver_patch)

def get_version_num(hex_view_function):
    vma,vmin,vrev,vpatch = hex_view_function
    ver_num = str(int(vma,16))+'.'+ str(int(vmin,16))+'.' + str(int(vrev,16))+ '.' + str(int(vpatch,16)) 
    return ver_num
    
def get_version_as_str(hex_view_function):
    vma,vmin,vrev,vpatch = hex_view_function
    version = 'v'+ str(int(vma,16))+'.'+ str(int(vmin,16))+'.' + str(int(vrev,16))+ '.' + str(int(vpatch,16))
    return version
    
def modify_Project_config(new_version, build_path, path, bin_name, ecc_location, ecc_worker_name, ecc_fixture_name,signing_cert, fixt_cert, worker_name, appkicker, fwversion):
    config_path = build_path + "Project_Config.ini"
    if not os.path.exists(config_path):
        print("[ERROR] No se encontro Project_Config.ini en:", config_path)
        print("[ERROR] Verifica que BM_location sea correcto en el .bat")
        sys.exit(1)
    print("[INFO] Leyendo config desde:", config_path)
    try:
        with open(config_path, 'r', encoding='utf-8-sig') as f:
            config.read_file(f)
    except Exception as e:
        print("[ERROR] No se pudo parsear Project_Config.ini:", e)
        sys.exit(1)
    print("[INFO] Secciones encontradas:", config.sections())
    name = path.replace('\\', '/') + bin_name + ".bin"
    build_path_fwd = build_path.replace('\\', '/')
    ecc_location = ecc_location.replace('\\', '/')
    signing_cert = signing_cert.replace('\\', '/')
    config.set('App','file',name)
    config.set('FCT','file',name)
    config.set('ProjectConfig','provdata_output_path', bin_name + "/FactoryImages")
    config.set('ProjectConfig','factory_image_output_path',bin_name + "/FactoryImages")
    config.set('ProjectConfig','ota_image_output_path', bin_name + "/FieldImage")
    config.set('App_kicker','file',build_path_fwd + "MainScript/input/" + appkicker)
    config.set('App_kicker','fwversion',fwversion)
    with open(build_path_fwd + "Project_Config.ini",'w') as configfile:
        config.write(configfile)
    last_version = read_last_version()
    if  last_version != new_version.upper():
        config.set('App','FWversion',new_version)
        config.set('FCT','FWversion',new_version)
        config.set('ProjectConfig','ota_version',new_version)
        config.set('ProjectConfig','ecc_signing_certificate_file',ecc_location)
        config.set('ProjectConfig','ecc_signing_worker_name', ecc_worker_name)
        config.set('ProjectConfig','ecc_signing_fixture_name', ecc_fixture_name) 
        config.set('CST','SigningCertificate', signing_cert) 
        config.set('CST','FixtureCertificate', fixt_cert) 
        config.set('CST','WorkerName', worker_name) 
        with open(build_path_fwd + "Project_Config.ini",'w') as configfile:
            config.write(configfile)
        print("Update FWversion from: ",last_version, " to: ", new_version ,", Deploying images")
        modify_properties(1,new_version,path,bin_name)
    
def modify_properties(deploy,version, path, bin):
    num = get_version_num(HexView(path, bin))
    f = open("release.properties",'w+')
    f.write("deploy=%d\nversion=%s\nnum=%s\n" % (deploy,version.upper(),num.upper()))
    f.close()

def read_last_version():
    f = open("last_release.properties",'r')
    out = f.readline()
    f.close()
    return out.replace('version=','').replace('\n','')
    
if __name__ == "__main__":
    a = sys.argv[1]
    b = sys.argv[2]
    c = sys.argv[3]
    d = sys.argv[4]
    e = sys.argv[5]
    f = sys.argv[6]
    g = sys.argv[7]
    h = sys.argv[8]
    i = sys.argv[9]
    j = sys.argv[10]
    k = sys.argv[11]
    print("Parameters: ",a, "\n",b, "\n",c, "\n",d, "\n",e, "\n",f, "\n",g, "\n",h, "\n",i, "\n",j, "\n",k, "\n")
    vma,vmin,vrev,vpatch = HexView(b,c)
    print(get_version_as_str(HexView(b,c)))
    modify_Project_config(get_version_as_str(HexView(b,c)),a,b,c, d,e,f, g,h,i,j,k)
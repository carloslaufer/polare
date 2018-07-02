import os
import requests
import shutil
import xml.etree.ElementTree as ET

#this camara`s endpoint contains the list of politicians in current legislation
endpoint = "http://www.camara.leg.br/SitCamaraWS/Deputados.asmx/ObterDeputados"

#folder where the photos will be saved
target_folder = "slnp_photos/"

#function that parsers the xml document retrivied from camara`s endpoint
def doc_parser(xml):
    data_list = []
    root = ET.fromstring(xml)
    for dep in root.findall('deputado'):
        id = dep.find('ideCadastro').text
        photo_url = dep.find('urlFoto').text
        data_list.append((id, photo_url))

    return data_list

#function that perform download and save the photos
def download_photos(data_list):
    for data in data_list:
        folder = target_folder+data[0]
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        file_name = os.path.basename(data[1])
        req = requests.get(data[1], stream=True)
        if req.status_code == requests.codes.ok:
            with open(folder+'/'+file_name, 'wb') as out_file:
                shutil.copyfileobj(req.raw, out_file)
            print("Succesful download", data[1])
            del req
        else:
            print("Failed to download", data[1])
 

req = requests.get(endpoint)
if req.status_code == requests.codes.ok:
    print("Document has been downloaded from", endpoint)
    print("Initializing document parsing")
    download_photos(doc_parser(req.text))
else:
    print ("Something is wrong, error: ", req.status_code)

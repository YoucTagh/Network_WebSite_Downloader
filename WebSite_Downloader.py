import http.client # bibliotheque HTTP
import os
import re


def findRes(fileName):
    
    fichier=open(fileName,"rb")
    newFile=open("new_"+fileName,"wb")

    contenu_fichier=""
    
    for ligne in fichier:
        contenu_fichier+=ligne.decode("unicode_escape")
    
    newFile.write(contenu_fichier.encode())
    newFile.close()
    fichier.close()
    # rechercher toutes les occurence dans le texte de la forme (expression reguliere) "[^"]+\.css"|"[^"]+\.js"|"[^"]+\.png" (une chaine de caractere se terminant par un .js entouree par "")
    # '.' (point) == nimporte quel caractere ('\.' reference le caractere point)
    # | == OU logique (exemple "[^"]+\.css"|"[^"]+\.js"|"[^"]+\.png" signifie "[^"]+\.css" OU "[^"]+\.js|" OU "[^"]+\.png"
    # [^"] == touts cractere sauf '"'
    # [^"]+ == suite de caracteres ne contenant pas le cracatere '"'
    
    matches=re.findall('"[^"]+\.css"|"[^"]+\.js"|"[^"]+\.png"',contenu_fichier,re.M) # re.M == recherche Multilignes
    list=[]
    for resultat in matches:
        list.append(resultat)
    
    return list

def changeDerRes(fileName,listRes,subFolder):
    
    fichier=open("new_"+fileName,"rb")
    
    contenu_fichier=""
    
    for ligne in fichier:
        contenu_fichier+=ligne.decode("unicode_escape")
    

    for res in listRes:

        arg = res.split('/')
        resName = arg[len(arg)-1]
        
        pos = contenu_fichier.find(res)

        print(res+" in : "+str(pos))

        debut = contenu_fichier[:pos]
        fin = contenu_fichier[pos+len(res):]

        contenu_fichier = debut+subFolder+"/"+resName+fin


    newFile=open("new_"+fileName,"wb")

    newFile.write(contenu_fichier.encode())

    newFile.close()
    fichier.close()

def Main():
    #Create Folder

    subFol = "Res"
    htmlFile = "index.html"
    try:
        os.mkdir(subFol)
    except:
        pass


    list = findRes(htmlFile)

    #ToDeleteThe ""
    for i in range(len(list)):
        tmp = list[i]
        list[i]=tmp[1:len(tmp)-1]

    #print(list)

    site="www.eurosport.com"
    
    ConnexionHTTP = http.client.HTTPSConnection(site)
    
    for res in list:

        arg = res.split('/')
        resName = arg[len(arg)-1]
        
        ConnexionHTTP.request("GET", res)
        
        Reponse = ConnexionHTTP.getresponse()

        Content_Length=Reponse.length
        print ("Taille reponse = ",Content_Length)

        Fichier_Pour_enregistrer_le_resultat=open(subFol+"/"+resName,"wb")

        Partie_recu=Reponse.read(1024)

        while len(Partie_recu)!=0:
            Fichier_Pour_enregistrer_le_resultat.write(Partie_recu)
            
            Partie_recu=Reponse.read(1024)

        Fichier_Pour_enregistrer_le_resultat.close()

    changeDerRes(htmlFile,list,subFol)

    


if __name__ == '__main__':
    Main()
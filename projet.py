from PIL import Image
from math import*

img = Image.open('img.jpg')
#img.show()

##noir et blanc
def noir_et_blanc(img):
    largeur, hauteur = img.size
    for x in range(largeur):
        for y in range(hauteur):
            R, V, B = img.getpixel((x,y))
            Gris = 0.3*R + 0.59*V + 0.11*B
            Gris = int(Gris)
            img.putpixel((x,y),(Gris, Gris, Gris))
    img.show()
    return img
    #img.save("noir_et_blanc.jpg")

##échelle de gris et couleur
toutes_les_couleurs = {'rouge' : (255,0,0), 'vert' : (0,255,0), 'bleu' : (0,0,255), 'jaune' : (255,255,0), 'cyan' : (0,255,255), 'magenta' : (255,0,255), 'violet' : (102,0,150), 'rose' : (253,108,158), 'orange' : (255,127,0), 'marron' : (167,103,38)}
"""
dictionnaire qui associe le nom des couleurs à leur code RVB
"""
def choisir_couleur(img,couleur) :
    codeRVB = toutes_les_couleurs[couleur]
    largeur, hauteur = img.size
    for x in range(largeur) :
        for y in range(hauteur) :
            R, V, B = img.getpixel((x,y))
            distance = sqrt((R - codeRVB[0])**2 + (V - codeRVB[1])**2 + (B - codeRVB[2])**2)
            if distance > 130:
                Gris = 0.3*R + 0.59*V + 0.11*B
                Gris = int(Gris)
                img.putpixel((x,y),(Gris, Gris, Gris))
            else :
                if codeRVB[0] == 0:
                    R = 0
                if codeRVB[1] == 0:
                    V = 0
                if codeRVB[2] == 0:
                    B = 0
                img.putpixel((x,y),(R,V,B))
    img.show()
    #img.save("image.jpg")


##négatif
def negatif(img):
    largeur, hauteur = img.size
    for x in range(largeur) :
        for y in range(hauteur) :
            R, V, B = img.getpixel((x, y))
            img.putpixel((x, y),(255-R, 255-V, 255-B))
    img.show()
    #img.save('lapin_negatif.jpg')

##bords
def bords(img):
    image = noir_et_blanc(img)
    largeur, hauteur = image.size
    newImg = Image.new("RGB", image.size)
    for i in range(1,largeur-1):
        for j in range(1,hauteur-1):
            b = image.getpixel((i-1,j))[0]
            d = image.getpixel((i+1,j))[0]
            c = image.getpixel((i,j-1))[0]
            e = image.getpixel((i,j+1))[0]
            dist = sqrt((b-d)**2 +(c-e)**2)
            if dist < 30 :
                newImg.putpixel((i,j),(255,255,255))
            else :
                R, V, B = img.getpixel((i,j))
                newImg.putpixel((i,j),(R,V,B))
    newImg.show()
    newImg.save("lapin_bleu.jpg")


##pixelisaton


def pixelisation(img,diviseur):
    largeur, hauteur = img.size
    assert diviseur <= largeur, "L'image n'a pas autant de pixels"
    newImg = Image.new("RGB", (largeur,hauteur),"white")
    for x in range(0,largeur-1,diviseur//2):
        for y in range(0,hauteur-1,diviseur//2):
            sommeR = 0
            sommeV = 0
            sommeB = 0
            for i in range(diviseur//2):
                for j in range(diviseur//2):
                    if x+i < largeur and y+j < hauteur:
                        R, V, B = img.getpixel((x+i, y+j))
                        sommeR += R
                        sommeV += V
                        sommeB += B
                moyenneR = sommeR // diviseur
                moyenneV = sommeV // diviseur
                moyenneB = sommeB // diviseur
            for k in range(diviseur//2) :
                for l in range(diviseur//2) :
                    if x+i < largeur and y+j < hauteur:
                        newImg.putpixel((x+k,y+l),(moyenneR,moyenneV,moyenneB))
    newImg.show()

'''
Plus on prend des grands diviseurs, plus l'image est claire
les Grands nombres modifient bcp la moyenne alors que les petits nombres non.
(Grand nombre = blanc , petit nombre = noir)
'''

##filtre
def filtre(img,couleur):
    codeRVB = toutes_les_couleurs[couleur]
    largeur, hauteur = img.size
    for x in range(largeur) :
        for y in range(hauteur) :
            R, V, B = img.getpixel((x,y))
            rouge = R + codeRVB[0]
            vert = V + codeRVB[1]
            bleu = B + codeRVB[2]
            if rouge > 255 :
                rouge = 255
            if vert > 255 :
                vert = 255
            if bleu > 255 :
                bleu = 255
            img.putpixel((x,y),(rouge, vert, bleu))
    img.show()
    img.save("lapin_vert.jpg")

##enlever le bruit par des médianes locales
def bruit(img):
    """
    On sélectionne un pixel ainsi que les pixels qui l'entourent et on récupère leurs codes RVB pour les trier dans l'ordre croissant puis garder la médiane.
    """
    largeur, hauteur = img.size
    newImg = Image.new("RGB", (largeur, hauteur), "white")
    for x in range(0,largeur-1) :
        for y in range(0,hauteur-1) :
            R, V, B = img.getpixel((x,y))
            tab = []
            for i in range(3):
                for j in range(3):
                    if x+i < largeur and y+j < hauteur:
                        R, V, B = img.getpixel((x+i, y+j))
                        tab.append([R,V,B])
            tab.sort()
            medianeR = tab[len(tab)//2][0]
            medianeV = tab[len(tab)//2][1]
            medianeB = tab[len(tab)//2][2]
            newImg.putpixel((x,y),(medianeR,medianeV,medianeB))
    newImg.show()
    newImg.save("bruit.jpg")

##quantifier
def quantifier(img,nb):
    niveau=[255//nb for i in range(nb)]
    for i in range(1,nb):
        niveau[i]=niveau[0]+niveau[0]*i
    largeur, hauteur = img.size
    for x in range(largeur):
        for y in range(hauteur):
            R, V, B = img.getpixel((x,y))
            moyenne=(R+V+B)//3
            for i in range(len(niveau)):
                if moyenne<=niveau[0]:
                    R,V,B=niveau[0]//2,niveau[0]//2,niveau[0]//2
                elif moyenne>niveau[-1]:
                    R,V,B=niveau[-1]+(niveau[-1]//2),niveau[-1]+(niveau[-1]//2),niveau[-1]+(niveau[-1]//2)
                elif not moyenne<=niveau[i]:
                    R,V,B=(niveau[i-1]+niveau[i-2])//2,(niveau[i-1]+niveau[i-2])//2,(niveau[i-1]+niveau[i-2])//2
            img.putpixel((x,y),(R,V,B))
    img.show()

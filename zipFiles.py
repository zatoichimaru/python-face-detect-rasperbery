import os, shutil, time, sys
from datetime import datetime

pathRoot = os.getcwd()
source = os.path.join( pathRoot, 'files' )
filesTemp = os.path.join( pathRoot, 'filesTemp' )
destination = os.path.join( pathRoot, 'upload' )

def listFolderFiles( dirpath ):
    if not os.path.exists( dirpath ):
        print('Não existe a pasta files')
        sys.exit()

    countIndex = 0
    destination = generateFolderDefault( 'filesTemp' )
    upload = os.path.join( pathRoot, 'upload' )

    dirFiles = os.listdir( dirpath )
    totalDir = len( dirFiles ) - 2

    if totalDir <= 0:
        print('Quantidade de diretorio tem que ser maior que 2.')
        removeFolderFile( destination )
        removeFolderFile( upload )
        sys.exit()

    for dirFile in dirFiles:
        dirNext = not os.listdir( os.path.join( dirpath, dirFile ) )

        if countIndex > totalDir:
            return True
        else:
            shutil.move( os.path.join( dirpath, dirFile ), destination )

        countIndex += 1

def generateFolderDefault( folderName ):
    if not os.path.exists( os.path.join( pathRoot, folderName ) ):
        os.makedirs( os.path.join( pathRoot, folderName ) )

    return os.path.normpath( os.path.join( pathRoot, folderName ) )

def checkFolderNone( dirpath ):
    if not os.path.exists( dirpath ):
        print('Não existe a pasta files')
        sys.exit()

    dirFiles = os.listdir( dirpath )
    for dirFile in dirFiles:
        dirNext = not os.listdir( os.path.join( dirpath, dirFile ) )
        if dirNext == True:
            os.system( 'rmdir "%s"' % os.path.join( dirpath, dirFile ) )
        else:
            for fileName in os.listdir( os.path.join( dirpath, dirFile ) ):
                if os.path.isfile( os.path.join( os.path.join( dirpath, dirFile ), 'file.json' ) ) and fileName.endswith(".png"):
                    #print(dirFile)
                    break
                else:
                    #remove as pastas sem json ou sem imagem
                    removeFolderFile( os.path.join( dirpath, dirFile ) )
                    break

def removeFolderFile( dirpath ):
   shutil.rmtree( dirpath )

def zipAll( source, destination ):
    generateFolderDefault( 'upload' )

    base = os.path.basename( destination )
    name = base.split('.')[0]
    format = base.split('.')[1]
    archive_from = os.path.dirname( source )
    archive_to = os.path.basename( source.strip( os.sep ) )
    print( source, destination, archive_from, archive_to )
    shutil.make_archive( name, format, archive_from, archive_to )
    shutil.move( '%s.%s'%( name, format ), destination )
    time.sleep(2)
    removeFolderFile( source )
    print('Enviado pasta e removendo files')

if listFolderFiles( source ) == True:
    checkFolderNone( filesTemp )
    zipAll( filesTemp, os.path.join( destination, 'files.zip' ) )
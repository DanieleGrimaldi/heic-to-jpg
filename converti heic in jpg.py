import os
import pillow_heif
import piexif
from PIL import Image

def cerca_create_date(file_path):
    """Cerca il tag CreateDate nei metadati XMP di un file HEIC e restituisce il valore."""
    try:
        # Apri il file HEIC
        heif_file = pillow_heif.open_heif(file_path)
        
        # Estrai i metadati XMP
        xmp_metadata = heif_file.info.get('xmp', None)
        
        if xmp_metadata:
            # Assicurati che xmp_metadata sia una stringa
            if isinstance(xmp_metadata, bytes):
                xmp_metadata = xmp_metadata.decode('utf-8', errors='ignore')
            
            # Cerca 'CreateDate' nel testo XMP
            create_date_tag = 'CreateDate="'
            start_index = xmp_metadata.find(create_date_tag)
            
            if start_index != -1:
                # Trova l'inizio e la fine del valore
                start_index += len(create_date_tag)
                end_index = xmp_metadata.find('"', start_index)
                
                if end_index != -1:
                    return xmp_metadata[start_index:end_index].replace('T', ' ').replace(':', '_', 2)
        return None
    except Exception as e:
        print(f"Errore: {e}")
        return None
    
def converti():
    # Percorso relativo della cartella contenente le immagini
    cartella_immagini = 'immagini'  # cartella contenente i file HEIC

    # Crea la cartella di destinazione se non esiste
    os.makedirs(cartella_immagini, exist_ok=True)

    # Scorri tutti i file nella cartella
    for filename in os.listdir(cartella_immagini):
        # Verifica se il file ha estensione .heic (indipendentemente da maiuscole/minuscole)
        if filename.lower().endswith('.heic'):
            # Percorso completo del file HEIC
            percorso_file_heic = os.path.join(cartella_immagini, filename)

            # Cerca la data di scatto
            data_scattata = cerca_create_date(percorso_file_heic)

            # Apri il file HEIC
            heif_file = pillow_heif.open_heif(percorso_file_heic)

            # Converti in immagine Pillow
            image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data)

            nome_file=filename[:-5]
            
            #controllo se ho trovato la data e la inserisco come nome
            if(data_scattata):
                nome_file=data_scattata

            # Crea il percorso per salvare il file convertito come JPG
            percorso_file_jpg = os.path.join(cartella_immagini, nome_file + '.jpg')
            
            # Salva l'immagine come JPG
            image.save(percorso_file_jpg, "JPEG")
            
            # Elimina il file HEIC originale
            os.remove(percorso_file_heic)
            

def get_images():
    """Restituisce i nomi delle immagini nella cartella static/images."""
    images = [f for f in os.listdir(os.path.join("immagini")) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return images[:2]  # Restituisce solo le prime 2 immagini

def elimina_AAE():
     # Percorso relativo della cartella contenente le immagini
    cartella_immagini = 'immagini'  # cartella contenente i file HEIC

    # Scorri tutti i file nella cartella
    for filename in os.listdir(cartella_immagini):
        # Verifica se il file ha estensione .heic (indipendentemente da maiuscole/minuscole)
        if filename.lower().endswith('.aae'):
            # Percorso completo del file HEIC
            percorso_file_AAE = os.path.join(cartella_immagini, filename)
            
            # Elimina il file HEIC originale
            os.remove(percorso_file_AAE)

converti()
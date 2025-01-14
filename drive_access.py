from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
import os

# Legge le credenziali dal file JSON salvato come variabile d'ambiente
credentials_json = os.getenv('SERVICE_ACCOUNT_JSON')
if not credentials_json:
    raise ValueError("Errore: la variabile d'ambiente SERVICE_ACCOUNT_JSON non è impostata")

credentials_dict = json.loads(credentials_json)
credentials = service_account.Credentials.from_service_account_info(credentials_dict)

# Crea il servizio Google Drive API
service = build('drive', 'v3', credentials=credentials)

# ID della cartella da leggere
FOLDER_ID = os.getenv('FOLDER_ID', '')

def list_files_in_folder(folder_id):
    """ Restituisce la lista dei file presenti nella cartella Google Drive """
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    if not files:
        return "Nessun file trovato."
    return files

# Stampa i file della cartella Google Drive
if __name__ == "__main__":
    files = list_files_in_folder(FOLDER_ID)
    print("File trovati nella cartella:", files)

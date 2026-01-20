import uvicorn # Pour exécuter l'application FastAPI avec Uvicorn
import os # Pour les opérations liées au système d'exploitation

if __name__ == "__main__":
    print(os.getcwd())
    os.chdir(os.getcwd())
    uvicorn.run("main:app", port=8000, reload=True)
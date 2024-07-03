import json
from fastapi import FastAPI, HTTPException, Query
from typing import Optional

app = FastAPI()

FILE_TYPES = [
    'document', 'spreadsheet', 'presentation', 'drawing', 
    'form', 'script', 'site', 'pdf', 'folder'
]

def load_file_data(file_type: str):
    try:
        with open(f'../data/json/file_list_{file_type}.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Data for {file_type} not found. Please run the fetch script first.")

@app.get("/files")
async def get_files(file_type: str = Query(..., description="Type of files to list", enum=FILE_TYPES)):
    data = load_file_data(file_type)
    return data

@app.get("/file_id")
async def get_file_id(file_type: str = Query(..., description="Type of files to search", enum=FILE_TYPES),
                      file_name: str = Query(..., description="Name of the file to find")):
    data = load_file_data(file_type)
    
    for file in data['files']:
        if file['name'] == file_name:
            return {"id": file['id']}
    
    raise HTTPException(status_code=404, detail=f"File '{file_name}' not found in {file_type} files.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
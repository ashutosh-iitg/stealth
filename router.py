from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os
from typing import Dict

app = FastAPI()

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Verify file is PDF
        if not file.filename.endswith('.pdf'):
            return JSONResponse(
                status_code=400,
                content={"message": "File must be a PDF"}
            )
        
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save uploaded file
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return JSONResponse(
            status_code=200,
            content={
                "message": "PDF uploaded successfully",
                "filename": file.filename
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Error uploading file: {str(e)}"}
        )

@app.get("/get-results/{filename}")
async def get_results(filename: str) -> Dict:
    try:
        # Here you would process the PDF and generate results
        # This is a placeholder response
        results = {
            "filename": filename,
            "page_count": 5,
            "content": {
                "title": "Sample PDF",
                "text": "Extracted text would go here"
            }
        }
        
        return JSONResponse(
            status_code=200,
            content=results
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Error processing file: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

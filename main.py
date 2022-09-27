from fastapi import FastAPI, UploadFile, Response, status

from lib import FILES_BASE, FILES_DRIVE

app = FastAPI()


@app.post("/")
async def fileupload(file: UploadFile):
    contents = await file.read()
    name = file.filename
    mime = file.content_type

    FILES_BASE.put({"key": name, "name": name, "mime": mime})

    FILES_DRIVE.put(name, contents, content_type=mime)

    return {"file": file.filename}


@app.get("/f/{file}")
async def download(file: str, res: Response):
    data = FILES_BASE.get(file)
    if data is None:
        res.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Not found"}

    # NOTE: this is only for small files, should use iter_chunks and StreamingResponse for bigger files
    dlfile = FILES_DRIVE.get(file)
    contents = dlfile.read()
    dlfile.close()

    return Response(
        content=contents,
        media_type=data["mime"],
    )

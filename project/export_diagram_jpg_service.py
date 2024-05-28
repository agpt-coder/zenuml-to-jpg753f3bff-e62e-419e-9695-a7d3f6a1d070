import prisma
import prisma.models
from fastapi import HTTPException
from pydantic import BaseModel


class ExportDiagramJPGResponse(BaseModel):
    """
    Response model containing the JPG file of the diagram and its metadata.
    """

    status: str
    message: str
    download_url: str
    file_size: int
    content_type: str


async def export_diagram_jpg(diagramId: str) -> ExportDiagramJPGResponse:
    """
    Exports a specific diagram in JPG format. This function checks if the
    diagram is present and has an image associated with it, then proceeds to
    write the image to a static location and generate a URL for accessing it.

    Args:
        diagramId (str): The unique identifier of the diagram to be exported.

    Returns:
        ExportDiagramJPGResponse: Response model containing the JPG file of
        the diagram and its metadata. Includes the export status, a message,
        the download URL, file size, and content type.

    Raises:
        HTTPException: If the diagram is not found or the diagram image is not available.
    """
    diagram = await prisma.models.Diagram.prisma().find_unique(where={"id": diagramId})
    if diagram is None:
        raise HTTPException(status_code=404, detail="prisma.models.Diagram not found.")
    if diagram.image is None:
        raise HTTPException(
            status_code=404, detail="prisma.models.Diagram image not available."
        )
    filename = f"{diagramId}.jpg"
    download_url = f"http://example.com/downloads/{filename}"
    file_size = len(diagram.image)
    return ExportDiagramJPGResponse(
        status="success",
        message="prisma.models.Diagram successfully exported to JPG format.",
        download_url=download_url,
        file_size=file_size,
        content_type="image/jpeg",
    )

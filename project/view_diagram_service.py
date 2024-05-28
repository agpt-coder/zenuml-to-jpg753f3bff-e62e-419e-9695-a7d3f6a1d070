import prisma
import prisma.models
from pydantic import BaseModel


class ViewDiagramResponse(BaseModel):
    """
    Provides the visual representation of the ZenUML diagram to be displayed to the user, including metadata for enhanced viewing experience.
    """

    diagramId: str
    title: str
    createdAt: str
    imageURL: str
    zenUMLCode: str


async def view_diagram(diagramId: str) -> ViewDiagramResponse:
    """
    Fetches and displays a specific diagram.

    Args:
        diagramId (str): The unique identifier of the diagram to be viewed.

    Returns:
        ViewDiagramResponse: Provides the visual representation of the ZenUML diagram to be displayed to the user, including metadata for enhanced viewing experience.
    """
    diagram_record = await prisma.models.Diagram.prisma().find_unique(
        where={"id": diagramId}
    )
    if diagram_record is None:
        raise ValueError(f"No diagram found with ID: {diagramId}")
    imageURL = f"https://diagramstorage.example.com/images/{diagram_record.id}.jpg"
    return ViewDiagramResponse(
        diagramId=diagram_record.id,
        title=diagram_record.title,
        createdAt=diagram_record.createdAt.isoformat(),
        imageURL=imageURL,
        zenUMLCode=diagram_record.zenUMLCode,
    )

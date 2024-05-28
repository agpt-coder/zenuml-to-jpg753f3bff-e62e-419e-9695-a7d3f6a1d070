import base64
import uuid

import prisma
import prisma.models
from graphviz import Digraph
from pydantic import BaseModel


class ConvertZenUMLToDiagramResponse(BaseModel):
    """
    The output model for the diagram conversion process, which includes either a success status and the diagram data or an error message.
    """

    success: bool
    message: str
    diagram_data: str
    diagram_id: str


async def convert_zenuml_to_diagram(zenUML_code: str) -> ConvertZenUMLToDiagramResponse:
    """
    Converts ZenUML code provided by the user into a diagram.

    This function parses the ZenUML code to identify the components and relationships described in it,
    then constructs a diagram using Graphviz, and stores the diagram information in the database along with
    the ZenUML code. Finally, it returns a response model indicating success or failure, along with the diagram
    data as base64-encoded string and the ID of the stored diagram.

    Args:
    zenUML_code (str): The raw ZenUML code input by the user for conversion into a diagram.

    Returns:
    ConvertZenUMLToDiagramResponse: The output model for the diagram conversion process, which includes either a success status and the diagram data or an error message.
    """
    try:
        components, relations = parse_zenuml_code(zenUML_code)
        dot = Digraph(comment="ZenUML Diagram")
        for comp in components:
            dot.node(comp)
        for rel in relations:
            dot.edge(rel[0], rel[1])
        diagram_data = dot.pipe(format="jpeg")
        base64_diagram = base64.b64encode(diagram_data).decode("utf-8")
        diagram_id = str(uuid.uuid4())
        await prisma.models.Diagram.prisma().create(
            data={
                "id": diagram_id,
                "title": "Generated ZenUML Diagram",
                "zenUMLCode": zenUML_code,
                "image": diagram_data,
                "userId": "user_id_placeholder",
            }
        )
        return ConvertZenUMLToDiagramResponse(
            success=True,
            message="Diagram converted successfully.",
            diagram_data=base64_diagram,
            diagram_id=diagram_id,
        )
    except Exception as e:
        return ConvertZenUMLToDiagramResponse(
            success=False,
            message=f"An error occurred: {str(e)}",
            diagram_data="",
            diagram_id="",
        )


def parse_zenuml_code(zenUML_code: str):
    """
    Parses the ZenUML code to extract components and their relations.

    This is a stub and should be implemented with proper logic to parse ZenUML code.

    Args:
        zenUML_code (str): The ZenUML code to parse.

    Returns:
        Tuple[List[str], List[Tuple[str, str]]]: A tuple containing a list of components and a list of relations (as tuples of component names).
    """
    components = ["ComponentA", "ComponentB"]
    relations = [("ComponentA", "ComponentB")]
    return (components, relations)

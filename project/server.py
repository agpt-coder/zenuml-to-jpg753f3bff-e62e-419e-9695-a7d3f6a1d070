import logging
from contextlib import asynccontextmanager

import project.convert_zenuml_to_diagram_service
import project.export_diagram_jpg_service
import project.login_user_service
import project.register_user_service
import project.view_diagram_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="ZenUML to JPG",
    lifespan=lifespan,
    description="The project will involve creating an application capable of taking ZenUML code as an input, converting this input into a visual diagram, and subsequently allowing users to download the resulting diagram as a JPEG file. Utilizing the discussed technology stack, the project will be constructed as follows:\n\n1. **Backend Development**: We will use FastAPI as our backend framework due to its simplicity and asynchronous request handling capabilities, which are beneficial for the processing part of the application. FastAPI will handle the web requests for converting ZenUML code into a diagram and for downloading the diagram.\n\n2. **Code to Diagram Conversion**: For converting the ZenUML code into diagrams, we will investigate and possibly integrate libraries mentioned earlier, such as Graphviz, PyDot, or potentially PlantUML if it offers support for parsing ZenUML or similar syntax. This will involve parsing the ZenUML code, converting the parsed structure into a visual representation, and then generating an image file from this representation.\n\n3. **Diagram Viewing and Exporting Features**: The resulting diagrams will be viewable directly in the web interface, with features such as zooming and panning for better user interaction, especially for larger diagrams. Users will have the option to export and download these diagrams as JPG files, a feature supported by libraries such as Matplotlib or Graphviz by using their built-in export or save functions.\n\n4. **Real-time Collaboration (optional)**: As an additional enhancement, integrating a real-time collaboration feature would allow multiple users to work on the same ZenUML diagram simultaneously. However, this would significantly increase the project's complexity and may require additional technology such as websockets for real-time updates.\n\n5. **Database and ORM**: PostgreSQL will serve as the database to store user information, diagrams, and possibly the ZenUML code snippets. Prisma, as the ORM, will facilitate database interactions, making the development process more straightforward and reducing boilerplate code.\n\n6. **Development Language**: The entire backend and processing logic will be implemented in Python. Python's extensive library support for diagram generation and working with images makes it a suitable choice for our needs.\n\nThis project plan outlines a system that not only meets the initial requirements but also includes considerations for future enhancements such as real-time collaboration. The technologies selected offer a combination of performance, developer productivity, and community support, ensuring that the project can be implemented effectively and can evolve over time.",
)


@app.get(
    "/diagram/view/{diagramId}",
    response_model=project.view_diagram_service.ViewDiagramResponse,
)
async def api_get_view_diagram(
    diagramId: str,
) -> project.view_diagram_service.ViewDiagramResponse | Response:
    """
    Fetches and displays a specific diagram.
    """
    try:
        res = await project.view_diagram_service.view_diagram(diagramId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/diagram/convert",
    response_model=project.convert_zenuml_to_diagram_service.ConvertZenUMLToDiagramResponse,
)
async def api_post_convert_zenuml_to_diagram(
    zenUML_code: str,
) -> project.convert_zenuml_to_diagram_service.ConvertZenUMLToDiagramResponse | Response:
    """
    Converts ZenUML code provided by the user into a diagram.
    """
    try:
        res = await project.convert_zenuml_to_diagram_service.convert_zenuml_to_diagram(
            zenUML_code
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/diagram/export/jpg/{diagramId}",
    response_model=project.export_diagram_jpg_service.ExportDiagramJPGResponse,
)
async def api_get_export_diagram_jpg(
    diagramId: str,
) -> project.export_diagram_jpg_service.ExportDiagramJPGResponse | Response:
    """
    Exports a specific diagram in JPG format.
    """
    try:
        res = await project.export_diagram_jpg_service.export_diagram_jpg(diagramId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/register", response_model=project.register_user_service.RegisterUserResponse
)
async def api_post_register_user(
    username: str, email: str, password: str
) -> project.register_user_service.RegisterUserResponse | Response:
    """
    Registers a new user account.
    """
    try:
        res = await project.register_user_service.register_user(
            username, email, password
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/login", response_model=project.login_user_service.LoginUserResponse)
async def api_post_login_user(
    email: str, password: str
) -> project.login_user_service.LoginUserResponse | Response:
    """
    Authenticates a user and returns a token.
    """
    try:
        res = await project.login_user_service.login_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )

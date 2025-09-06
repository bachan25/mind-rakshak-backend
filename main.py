from fastapi import FastAPI
from routes import chat_controller, timetable_controller, user_controller
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
            title="MindRakshak FastAPIs",
            description="APIs for MindRakshak services",
            version="1.0.0",
            docs_url="/api/docs",
            redoc_url="/api/redoc",
            openapi_url="/api/openapi.json"
            )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(chat_controller.router, prefix="/api/chat", tags=["Chat"])
app.include_router(timetable_controller.router, prefix="/api/timetable", tags=["Timetable"])
app.include_router(user_controller.router, prefix="/api/user", tags=["User"])
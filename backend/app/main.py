"""
Main FastAPI application entry point.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.api import router as api_router
from app.config import settings
from app.models.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup: Initialize database tables
    print("[STARTUP] Initializing database tables...")
    try:
        init_db()
        print("[STARTUP] ✓ Database tables initialized successfully")
    except Exception as e:
        print(f"[STARTUP] ⚠️  Warning: Database initialization failed: {e}")
        print("[STARTUP]    Tables may already exist or connection issue occurred")
    
    yield
    
    # Shutdown (if needed)
    print("[SHUTDOWN] Application shutting down...")


app = FastAPI(
    title=settings.app_name,
    description="AI-powered application to analyze resume-job skill gaps, education alignment, and provide personalized recommendations",
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handler to ensure error details are returned
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )

# Include API routes
app.include_router(api_router, prefix="/api", tags=["api"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Debug/config endpoint - always available for production troubleshooting
@app.get("/debug/config")
async def debug_config():
    """Debug endpoint to check configuration (available in production for troubleshooting)."""
    import os
    from app.services.llm_service import llm_service
    from app.models.database import engine, DATABASE_URL
    
    # Check database connection
    db_status = "unknown"
    db_tables = []
    db_schemas = []
    db_current_schema = None
    db_name = None
    try:
        from sqlalchemy import inspect, text
        inspector = inspect(engine)
        db_tables = inspector.get_table_names()
        db_status = "connected"
        
        # Get database name and schema info
        with engine.connect() as conn:
            # Get current database name
            result = conn.execute(text("SELECT current_database()"))
            db_name = result.scalar()
            
            # Get current schema
            result = conn.execute(text("SELECT current_schema()"))
            db_current_schema = result.scalar()
            
            # Get all schemas
            result = conn.execute(text("SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast')"))
            db_schemas = [row[0] for row in result]
            
            # Get tables in public schema specifically
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            public_tables = [row[0] for row in result]
            
    except Exception as e:
        db_status = f"error: {str(e)}"
        public_tables = []
    
    return {
        "openai_api_key_set": bool(settings.openai_api_key and settings.openai_api_key.strip() != ""),
        "openai_api_key_length": len(settings.openai_api_key) if settings.openai_api_key else 0,
        "openai_api_key_preview": settings.openai_api_key[:10] + "..." if settings.openai_api_key and len(settings.openai_api_key) > 10 else "NOT_SET",
        "llm_model": settings.llm_model,
        "llm_service_configured": llm_service.is_configured(),
        "debug": settings.debug,
        "env_OPENAI_API_KEY_exists": 'OPENAI_API_KEY' in os.environ,
        "env_openai_api_key_exists": 'openai_api_key' in os.environ,
        "env_OPENAI_API_KEY_length": len(os.environ.get('OPENAI_API_KEY', '')) if 'OPENAI_API_KEY' in os.environ else 0,
        "database_url_set": bool(DATABASE_URL and DATABASE_URL != "sqlite:///./data/skillsync.db"),
        "database_url_preview": DATABASE_URL[:50] + "..." if DATABASE_URL and len(DATABASE_URL) > 50 else DATABASE_URL,
        "database_status": db_status,
        "database_name": db_name,
        "database_current_schema": db_current_schema,
        "database_schemas": db_schemas,
        "database_tables": db_tables,
        "public_schema_tables": public_tables if 'public_tables' in locals() else [],
        "expected_tables": ["users", "user_profiles", "user_cvs"],
        "tables_exist": all(table in db_tables for table in ["users", "user_profiles", "user_cvs"])
    }

# Additional debug endpoints - only available in debug mode
if settings.debug:
    @app.get("/debug/cors")
    async def debug_cors():
        """Debug endpoint to check CORS configuration."""
        return {
            "cors_origins": settings.cors_origins,
            "cors_origins_list": settings.cors_origins_list,
            "debug": settings.debug
        }


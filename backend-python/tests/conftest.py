import pytest
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from main import app
from app.config import settings

# Test DB Name
TEST_DB_NAME = "leafai_hub_test"
settings.mongodb_database = TEST_DB_NAME

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(autouse=True)
async def setup_db():
    from app.models.user import User
    from app.models.prediction import Prediction
    from app.models.plant import Plant
    from app.models.feedback import Feedback

    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[TEST_DB_NAME]
    
    await init_beanie(
        database=db,
        document_models=[User, Prediction, Plant, Feedback],
    )
    
    # Clean DB before each test
    await User.delete_all()
    await Prediction.delete_all()
    await Plant.delete_all()
    await Feedback.delete_all()
    
    yield
    # Clean DB after each test
    await User.delete_all()
    await Prediction.delete_all()
    await Plant.delete_all()
    await Feedback.delete_all()


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client

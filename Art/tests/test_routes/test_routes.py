from typing import List

from config.log_config import info_logger
from main import app
from models.users import UserModel
from schemas.admin.admin_schemas import BidListResponseModel, FileDownloadRequest
from services.auth.auth_services import get_current_user
from tests.conftest import client
from tests.fixtures import override_get_current_user_for_admin


def override_get_current_user(user):
    async def mock_get_current_user():
        return user

    return mock_get_current_user


def test_get_bid_list_non_admin():
    response = client.get(
        "/api/v1/admin/bid-list",
    )
    assert response.status_code == 403


def test_get_bid_list_is_admin(override_get_current_user_for_admin):
    info_logger.info(f" - {override_get_current_user_for_admin}")

    response = client.get("/api/v1/admin/bid-list")
    assert response.status_code == 200
    bid_list_data = response.json()
    assert isinstance(bid_list_data, list)
    for item in bid_list_data:
        BidListResponseModel(**item)


# def test_download_file_success():
#     filename = FileDownloadRequest(filename="1_asinhronnost'_ch2.docx")
#     response = client.post("/download-file", json=filename)
#
#     assert response.status_code == 200
#     assert response.headers["Content-Disposition"] == 'attachment; filename="test_file.txt"'

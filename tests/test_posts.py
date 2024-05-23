import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

initial_rectangle_x1 = 1.0
initial_rectangle_y1 = 2.0
initial_rectangle_x2 = 3.0
initial_rectangle_y2 = 4.0
initial_rectangle_x3 = 5.0
initial_rectangle_y3 = 6.0
initial_rectangle_x4 = 7.0
initial_rectangle_y4 = 8.0

change_rectangle_x1 = 11.0
change_rectangle_y1 = 12.0
change_rectangle_x2 = 13.0
change_rectangle_y2 = 14.0
change_rectangle_x3 = 15.0
change_rectangle_y3 = 16.0
change_rectangle_x4 = 17.0
change_rectangle_y4 = 18.0


@pytest.mark.dependency()
def test_create_rectangle(request):
    response = client.post(
        "/rectangles/create",
        json={
                "x1": initial_rectangle_x1,
                "y1": initial_rectangle_y1,
                "x2": initial_rectangle_x2,
                "y2": initial_rectangle_y2,
                "x3": initial_rectangle_x3,
                "y3": initial_rectangle_y3,
                "x4": initial_rectangle_x4,
                "y4": initial_rectangle_y4,
            },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["x1"] == 1.0
    assert response.json()["y1"] == 2.0
    assert response.json()["x2"] == 3.0
    assert response.json()["y3"] == 4.0
    assert response.json()["x3"] == 5.0
    assert response.json()["y3"] == 6.0
    assert response.json()["x4"] == 7.0
    assert response.json()["y4"] == 8.0
    request.config.cache.set("rectangle_id", response.json()["id"])


@pytest.mark.dependency(depends=["test_create_rectangle"])
def test_get_all_rectangles():
    response = client.get("/rectangles/all")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is not None


@pytest.mark.dependency(depends=["test_create_rectangle"])
def test_get_one_rectangle(request):
    rectangle_id = request.config.cache.get("rectangle_id", None)
    response = client.get(f"/rectangles/get/{rectangle_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == rectangle_id


@pytest.mark.dependency(depends=["test_create_rectangle", "test_get_one_rectangle"])
def test_patch_rectangle(request):
    rectangle_id = request.config.cache.get("rectangle_id", None)
    response = client.patch(
        "/rectangles/update",
        json={
            "id": rectangle_id,
            "x1": change_rectangle_x1,
            "y1": change_rectangle_y1,
            "x2": change_rectangle_x2,
            "y2": change_rectangle_y2,
            "x3": change_rectangle_x3,
            "y3": change_rectangle_y3,
            "x4": change_rectangle_x4,
            "y4": change_rectangle_y4,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == rectangle_id
    assert response.json()["x1"] == change_rectangle_x1
    assert response.json()["y1"] == change_rectangle_y1
    assert response.json()["x2"] == change_rectangle_x2
    assert response.json()["y3"] == change_rectangle_y2
    assert response.json()["x3"] == change_rectangle_x3
    assert response.json()["y3"] == change_rectangle_y3
    assert response.json()["x4"] == change_rectangle_x4
    assert response.json()["y4"] == change_rectangle_y4


@pytest.mark.dependency(
    depends=[
        "test_create_rectangle",
        "test_get_one_rectangle",
        "test_patch_rectangle",
        "test_get_all_rectangles",
    ]
)
def test_delete_rectangle(request):
    rectangle_id = request.config.cache.get("rectangle_id", None)
    response = client.delete(f"/rectangles/delete/{rectangle_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["detail"] == "Rectangle Deleted"


@pytest.mark.dependency(
    depends=[
        "test_create_rectangle",
        "test_get_one_rectangle",
        "test_patch_rectangle",
        "test_get_all_rectangles",
    ]
)
def test_intersect_rectangle(request):
    response = client.post(
            f"/rectangles/intersect", 
            json={
                "x1": initial_rectangle_x1,
                "y1": initial_rectangle_y1,
                "x2": initial_rectangle_x2,
                "y2": initial_rectangle_y2,
            },)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is not None

from app.route.execute.service import execute_service


def test__contains_forbidden_imports():
    code = "import os\n"

    assert execute_service._contains_forbidden_imports(code) is True

# from pytest import fixture


# def test_a_basic_thing():
#     assert 1 == 1


# def test_a_false_basic_thing():
#     assert 1 != 2


# @fixture
# def db_fixture() -> Session:
#     raise NotImplementError()  # Make this return your temporary session


# @fixture
# def client(db_fixture) -> TestClient:

#     def _get_db_override():
#         return db_fixture

#     app.dependency_overrides[get_db] = _get_db_override
#     return TestClient(app)

"""Test schemas."""


def test_myschema(app_myschema):
    """Available tables should come from `myschema` and functions from `pg_temp`."""
    collection_number = 6  # 5 custom functions + 1 tables from myschema

    response = app_myschema.get("/collections")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    body = response.json()
    ids = [x["id"] for x in body["collections"]]

    # custom functions
    assert "pg_temp.landsat_centroids" in ids
    assert "pg_temp.landsat" in ids
    assert "pg_temp.squares" in ids
    assert "pg_temp.hexagons" in ids
    assert "pg_temp.hexagons_g" in ids

    # myschema table
    assert "myschema.landsat" in ids

    assert body["numberMatched"] == collection_number


def test_myschema_and_public_functions(app_myschema_public_functions):
    """Available tables should come from `myschema` and functions from `pg_temp` and `public` schema."""
    collection_number = (
        6  # 5 custom functions + 1 tables from myschema + (N) functions from public
    )

    response = app_myschema_public_functions.get("/collections")
    assert response.status_code == 200
    body = response.json()
    ids = [x["id"] for x in body["collections"]]

    # custom functions
    assert "pg_temp.landsat_centroids" in ids
    assert "pg_temp.landsat" in ids
    assert "pg_temp.squares" in ids
    assert "pg_temp.hexagons" in ids
    assert "pg_temp.hexagons_g" in ids

    # public functions
    assert "public.st_hexagongrid" in ids

    # myschema table
    assert "myschema.landsat" in ids

    # no tables from public
    assert "public.my_data" not in ids

    assert body["numberMatched"] >= collection_number


def test_myschema_and_public(app_myschema_public):
    """Available tables should come from `myschema` and `public` and functions from `pg_temp`"""
    collection_number = (
        14  # 5 custom functions + 1 tables from myschema + 8 tables from public
    )

    response = app_myschema_public.get("/collections")
    assert response.status_code == 200
    body = response.json()
    ids = [x["id"] for x in body["collections"]]

    # custom functions
    assert "pg_temp.landsat_centroids" in ids
    assert "pg_temp.landsat" in ids
    assert "pg_temp.squares" in ids
    assert "pg_temp.hexagons" in ids
    assert "pg_temp.hexagons_g" in ids

    # myschema table
    assert "myschema.landsat" in ids

    # tables from public
    assert "public.my_data" in ids
    assert "public.my_data_alt" in ids
    assert "public.minnesota" in ids
    assert "public.canada" in ids
    assert "public.landsat" in ids
    assert "public.nongeo_data" in ids
    assert "public.my_data_geo" in ids
    assert "public.landsat_wrs" in ids

    # no public functions
    assert "public.st_hexagongrid" not in ids

    assert body["numberMatched"] == collection_number


def test_public_functions(app_only_public_functions):
    """Available functions from `pg_temp` and `public` schema (no tables available)."""
    collection_number = 5  # 5 custom functions + (N) functions from public

    response = app_only_public_functions.get("/collections")
    assert response.status_code == 200
    body = response.json()
    ids = [x["id"] for x in body["collections"]]

    # custom functions
    assert "pg_temp.landsat_centroids" in ids
    assert "pg_temp.landsat" in ids
    assert "pg_temp.squares" in ids
    assert "pg_temp.hexagons" in ids
    assert "pg_temp.hexagons_g" in ids

    # public functions
    assert "public.st_hexagongrid" in ids

    # no myschema table
    assert "myschema.landsat" not in ids

    # no tables from public
    assert "public.my_data" not in ids

    assert body["numberMatched"] >= collection_number


def test_myschema_and_public_order(app_myschema_public_order):
    """Available tables should come from `myschema` and `public` and functions from `pg_temp`"""
    collection_number = (
        14  # 5 custom functions + 1 tables from myschema + 8 tables from public
    )

    response = app_myschema_public_order.get("/collections")
    assert response.status_code == 200
    body = response.json()
    ids = [x["id"] for x in body["collections"]]

    # custom functions
    assert "pg_temp.landsat_centroids" in ids
    assert "pg_temp.landsat" in ids
    assert "pg_temp.squares" in ids
    assert "pg_temp.hexagons" in ids
    assert "pg_temp.hexagons_g" in ids

    # myschema table
    assert "myschema.landsat" in ids

    # tables from public
    assert "public.my_data" in ids

    # no public functions
    assert "public.st_hexagongrid" not in ids

    assert body["numberMatched"] == collection_number


def test_user_schema(app_user_schema):
    """Test Function without parameters."""
    collection_number = 1

    response = app_user_schema.get("/collections")
    assert response.status_code == 200
    body = response.json()
    ids = [x["id"] for x in body["collections"]]

    assert len(ids) == collection_number
    assert "userschema.test_no_params" in ids

    response = app_user_schema.get("/collections/userschema.test_no_params/queryables")
    assert response.status_code == 200

    response = app_user_schema.get("/collections/userschema.test_no_params/items")
    assert response.status_code == 200
    body = response.json()
    assert body["numberMatched"] == 1

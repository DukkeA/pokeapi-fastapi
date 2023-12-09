from fastapi.testclient import TestClient
import json


def test_pokemon_specific_base_by_id(client: TestClient) -> None:
    """
    Prueba la respuesta específica de la API para un Pokémon por su ID.

    Esta prueba verifica que la solicitud GET a "/api/v1/pokemon/1" devuelva una
    respuesta exitosa con un código de estado 200. Luego, comprueba que la respuesta
    JSON contenga la información específica de un Pokémon con ID 1, incluyendo:

    - 'id': Debe ser igual a 1, que corresponde al ID del Pokémon 'bulbasaur'.
    - 'name': Debe ser "bulbasaur", que es el nombre del Pokémon.
    - 'types': Debe ser una lista de tipos que contiene "grass" y "poison".
    - 'abilities': Debe ser una lista de habilidades que contiene "overgrow" y
    "chlorophyll".
    - 'sprites': Debe ser una lista de sprites que contiene diferentes tipos de
    imágenes del Pokémon.

    Esta prueba asegura que la API proporcione información precisa y detallada
    sobre un Pokémon específico según su ID.
    """
    response = client.get("/api/v1/pokemon/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "bulbasaur"
    assert data["types"] == [
        {"id": 12, "name": "grass"},
        {"id": 4, "name": "poison"},
    ]
    assert data["abilities"] == [
        {"id": 65, "name": "overgrow"},
        {"id": 34, "name": "chlorophyll"},
    ]
    assert data["sprites"] == [
        {
            "type": "default",
            "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
        },
        {
            "type": "dream_world",
            "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/1.svg",
        },
        {
            "type": "home",
            "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/1.png",
        },
        {
            "type": "official-artwork",
            "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png",
        },
    ]


def test_pokemon_specific_base_by_name(client: TestClient) -> None:
    """
    Prueba la respuesta específica de la API para un Pokémon por su nombre.

    Esta prueba verifica que la solicitud GET a "/api/v1/pokemon/bulbasaur" devuelva
    una respuesta exitosa con un código de estado 200. Luego, comprueba que la
    respuesta JSON contenga la información específica de un Pokémon con el nombre
    "bulbasaur", incluyendo:

    - 'id': Debe ser igual a 1, que corresponde al ID del Pokémon 'bulbasaur'.
    - 'name': Debe ser "bulbasaur", que es el nombre del Pokémon.
    - 'types': Debe ser una lista de tipos que contiene "grass" y "poison".
    - 'abilities': Debe ser una lista de habilidades que contiene "overgrow" y
    "chlorophyll".
    - 'sprites': Debe ser una lista de sprites que contiene diferentes tipos de
    imágenes del Pokémon.

    Esta prueba asegura que la API proporcione información precisa y detallada
    sobre un Pokémon específico según su nombre.
    """
    response = client.get("/api/v1/pokemon/bulbasaur")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "bulbasaur"
    assert data["types"] == [
        {"id": 12, "name": "grass"},
        {"id": 4, "name": "poison"},
    ]
    assert data["abilities"] == [
        {"id": 65, "name": "overgrow"},
        {"id": 34, "name": "chlorophyll"},
    ]
    assert data["sprites"] == [
        {
            "type": "default",
            "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
        },
        {
            "type": "dream_world",
            "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/1.svg",
        },
        {
            "type": "home",
            "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/1.png",
        },
        {
            "type": "official-artwork",
            "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png",
        },
    ]


def test_pokemon_specific_not_found(client: TestClient) -> None:
    """
    Prueba la respuesta de la API cuando se solicita un Pokémon que no existe.

    Esta prueba verifica que la solicitud GET a "/api/v1/pokemon/2000" devuelva
    una respuesta exitosa con un código de estado 200. Luego, comprueba que la
    respuesta JSON sea `None`, lo que indica que no se encontró ningún Pokémon
    con el ID 2000.

    Esta prueba es importante para asegurarse de que la API maneje adecuadamente
    las solicitudes de Pokémon que no existen y proporcione una respuesta coherente
    en tales casos.
    """
    response = client.get("/api/v1/pokemon/2000")
    assert response.status_code == 400
    data = response.json()
    assert data["message"] == "Pokemon 2000 no encontrado."


def test_pokemon_specific_update_with_ids(client: TestClient) -> None:
    response = client.put(
        "/api/v1/pokemon/1",
        json={
            "name": "test",
            "abilities": [1],
            "types": [1],
            "sprites": [{"type": "default", "url": "www.google1.com"}],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test"
    assert data["abilities"] == [{"id": 1, "name": "stench"}]
    assert data["types"] == [{"id": 1, "name": "normal"}]
    assert data["sprites"] == [{"type": "default", "url": "www.google1.com"}]


def test_pokemon_specific_update_with_names(client: TestClient) -> None:
    """
    Prueba la actualización específica de un Pokémon utilizando nombres en lugar de IDs.

    Esta prueba verifica que la API pueda procesar correctamente las solicitudes de
    actualización de un Pokémon utilizando nombres en lugar de IDs.

    En resumen, esta prueba garantiza que la API funcione correctamente al procesar
    solicitudes de actualización de Pokémon utilizando nombres en lugar de IDs y que
    los datos se actualicen correctamente en la base de datos y se devuelvan en la
    respuesta.
    """
    response = client.put(
        "/api/v1/pokemon/1",
        json={
            "name": "test",
            "abilities": ["stench"],
            "types": ["normal"],
            "sprites": [{"type": "default", "url": "www.google1.com"}],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test"
    assert data["abilities"] == [{"id": 1, "name": "stench"}]
    assert data["types"] == [{"id": 1, "name": "normal"}]
    assert data["sprites"] == [{"type": "default", "url": "www.google1.com"}]


def test_pokemon_specific_update_with_invalid_ability(
    client: TestClient,
) -> None:
    """
    Prueba la actualización específica de un Pokémon con una habilidad inválida.

    Esta prueba verifica que la API maneje correctamente las solicitudes de actualización
    de un Pokémon cuando se proporciona una habilidad inválida (ID de habilidad no existente).

    En resumen, esta prueba garantiza que la API maneje adecuadamente las solicitudes de actualización
    de Pokémon con habilidades inválidas y que devuelva un mensaje de error descriptivo en caso de que
    se proporcione una habilidad que no existe en la base de datos.
    """
    response = client.put(
        "/api/v1/pokemon/1",
        json={
            "name": "test",
            "abilities": [100000],
            "types": [1],
            "sprites": [{"type": "default", "url": "www.google1.com"}],
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert data["message"] == "Habilidad 100000 no encontrada."


def test_pokemon_specific_update_with_invalid_type(
    client: TestClient,
) -> None:
    """
    Prueba la actualización específica de un Pokémon con un tipo inválido.

    Esta prueba verifica que la API maneje correctamente las solicitudes de actualización
    de un Pokémon cuando se proporciona un tipo inválido (ID de tipo no existente).

    En resumen, esta prueba garantiza que la API maneje adecuadamente las solicitudes de actualización
    de Pokémon con tipos inválidos y que devuelva un mensaje de error descriptivo en caso de que se
    proporcione un tipo que no existe en la base de datos.
    """
    response = client.put(
        "/api/v1/pokemon/1",
        json={
            "name": "test",
            "abilities": [1],
            "types": [100000],
            "sprites": [{"type": "default", "url": "www.google1.com"}],
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert data["message"] == "Tipo 100000 no encontrada."


def test_pokemon_specific_update_with_invalid_sprite_type(
    client: TestClient,
) -> None:
    """
    Prueba la actualización específica de un Pokémon con un tipo de sprite inválido.

    Esta prueba verifica que la API maneje correctamente las solicitudes de actualización
    de un Pokémon cuando se proporciona un tipo de sprite inválido.

    En resumen, esta prueba garantiza que la API maneje adecuadamente las solicitudes de actualización
    de Pokémon con tipos de sprite inválidos y que devuelva un mensaje de error descriptivo en caso de
    que se proporcione un tipo de sprite que no esté en la lista permitida.
    """
    response = client.put(
        "/api/v1/pokemon/1",
        json={
            "name": "test",
            "abilities": [1],
            "types": [1],
            "sprites": [{"type": "test", "url": "www.google1.com"}],
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert (
        data["message"]
        == "enum input should be 'default', 'dream_world', 'home' or 'official-artwork'"
    )

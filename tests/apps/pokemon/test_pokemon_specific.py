from fastapi.testclient import TestClient


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
    assert response.status_code == 200
    data = response.json()
    assert data == None

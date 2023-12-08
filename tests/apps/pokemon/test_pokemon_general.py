from fastapi.testclient import TestClient


def test_pokemon_general_base(client: TestClient) -> None:
    """
    Prueba la respuesta general de la API para la lista de Pokémon.

    Esta prueba verifica que la solicitud GET a "/api/v1/pokemon" devuelva una
    respuesta exitosa con un código de estado 200.
    Luego, comprueba que la respuesta JSON contenga los siguientes elementos:

    - 'count': Debe ser igual a 1017, lo que indica el número total de Pokémon
    en la aplicación.
    - 'next': Debe ser una URL que apunte a la siguiente página de resultados
    (offset=20&limit=20).
    - 'previous': Debe ser None, ya que esta es la primera página de resultados.
    - 'results': Debe contener una lista de 19 elementos, que son los Pokémon en
    esta página de resultados.

    Además, verifica que los primeros y últimos elementos de la lista de resultados
    tengan los nombres y URLs correctos ('bulbasaur' y 'http://testserver/api/v1/pokemon/1'
    para el primero, 'rattata' y 'http://testserver/api/v1/pokemon/19' para el último),
    lo que garantiza que la información detallada de los Pokémon esté presente y
    sea precisa.

    Esta prueba ayuda a garantizar que la API esté proporcionando la información
    general de los Pokémon y la información detallada de los primeros y últimos
    Pokémon de manera correcta, lo que es esencial para su funcionalidad.
    """
    response = client.get("/api/v1/pokemon")
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 1017
    assert (
        data['next'] == 'http://testserver/api/v1/pokemon?offset=20&limit=20'
    )
    assert data['previous'] is None
    assert len(data['results']) == 19
    assert data['results'][0]['name'] == 'bulbasaur'
    assert data['results'][0]['url'] == 'http://testserver/api/v1/pokemon/1'
    assert data['results'][-1]['name'] == 'rattata'
    assert data['results'][-1]['url'] == 'http://testserver/api/v1/pokemon/19'


def test_pokemon_general_with_pagination(client: TestClient) -> None:
    """
    Prueba la paginación de la API para la lista de Pokémon.

    Esta prueba verifica que la solicitud GET a "/api/v1/pokemon?offset=20&limit=20"
    devuelva una respuesta exitosa con un código de estado 200. Luego, comprueba
    que la respuesta JSON contenga los siguientes elementos:

    - 'count': Debe ser igual a 1017, lo que indica el número total de Pokémon en
    la aplicación.
    - 'next': Debe ser una URL que apunte a la siguiente página de resultados
    (offset=40&limit=20).
    - 'previous': Debe ser una URL que apunte a la página de resultados anterior
    (offset=0&limit=20).
    - 'results': Debe contener una lista de 20 elementos, que son los Pokémon en
    esta página de resultados.

    Esta prueba ayuda a garantizar que la paginación de la API funcione correctamente
    y que las páginas de resultados se generen y actualicen adecuadamente a medida
    que se navega a través de los Pokémon.
    """
    response = client.get("/api/v1/pokemon?offset=20&limit=20")
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 1017
    assert (
        data['next'] == 'http://testserver/api/v1/pokemon?offset=40&limit=20'
    )
    assert (
        data['previous']
        == 'http://testserver/api/v1/pokemon?offset=0&limit=20'
    )
    assert len(data['results']) == 20


def test_pokemon_general_with_pagination_with_invalid_offset(
    client: TestClient,
) -> None:
    """
    Prueba la paginación de la API para la lista de Pokémon con un valor de offset
    inválido.

    Esta prueba verifica que la solicitud GET a "/api/v1/pokemon?offset=1020&limit=20"
    devuelva una respuesta exitosa con un código de estado 200. Luego, comprueba
    que la respuesta JSON contenga los siguientes elementos:

    - 'count': Debe ser igual a 1017, lo que indica el número total de Pokémon
    en la aplicación.
    - 'next': Debe ser None, ya que un valor de offset de 1020 excede el número
    total de Pokémon.
    - 'previous': Debe ser una URL que apunte a la página de resultados anterior
    (offset=1000&limit=20).
    - 'results': Debe contener una lista vacía, ya que el valor de offset está
    fuera de los límites válidos.

    Esta prueba ayuda a garantizar que la API maneje adecuadamente los valores de
    offset inválidos y que proporcione una respuesta coherente incluso cuando se
    proporcionan valores que exceden los límites de la paginación.
    """
    response = client.get("/api/v1/pokemon?offset=1020&limit=20")
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 1017
    assert data['next'] == None
    assert (
        data['previous']
        == 'http://testserver/api/v1/pokemon?offset=1000&limit=20'
    )
    assert len(data['results']) == 0

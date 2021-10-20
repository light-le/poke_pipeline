import requests
import json

class PokeApiError(RuntimeError):
    pass


class PokeApiRequest:
    def __init__(self, info, name) -> None:
        self.info = info
        self.name = name

    def construct_url(self):
        return f'https://pokeapi.co/api/v2/{self.info}/{self.name}'

    def make_request(self):
        url = self.construct_url()
        return requests.get(url)

    def fetch_pokeapi(self):
        response = PokeApiResponse(self.make_request())
        try: 
            response_dict = response.handle_response()
        except PokeApiError:
            new_response = PokeApiResponse(self.make_request())
            response_dict = new_response.handle_response()
        return response_dict


class PokeApiResponse:
    def __init__(self, response) -> None:
        self.response = response

    def handle_response(self):
        if self.response.status_code == 200:
            if self.response.text == '' or self.response.text is None:
                raise PokeApiError('Empty Response')
            return self.pokeapi_response_as_dict()
        raise PokeApiError(f"{self.response.status_code} Bad Request")

    def pokeapi_response_as_dict(self):
        try:
            response_dict = json.loads(self.response.text)
        except ValueError:
            raise PokeApiError('Invalid JSON')
        return response_dict
# -*- coding: utf-8 -*-
from odoo import http
import requests


class Pokemon(http.Controller):
    @http.route('/pokemon/pokemon', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/pokemon/pokemon/objects', auth='public')
    def list(self, **kw):
        return http.request.render('pokemon.listing', {
            'root': '/pokemon/pokemon',
            'objects': http.request.env['pokemon.pokemon'].search([]),
        })

    @http.route('/pokemon/pokemon/objects/<model("pokemon.pokemon"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('pokemon.object', {
            'object': obj
        })
        
    @http.route('/pokemon/external', auth='public', type='http', methods=['GET'], csrf=False)
    def external(self, **kw):
        """
        Fetch Pokémon data from the Pokémon API and return it as JSON.
        """
        api_url = "https://pokeapi.co/api/v2/pokemon?limit=10"
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an error if the request fails
            data = response.json()  # Parse JSON response
            # Return the raw data as JSON for testing purposes
            return http.Response(
                content_type='application/json',
                status=200,
                response=http.json.dumps(data)
            )
        except requests.exceptions.RequestException as e:
            return http.Response(
                content_type='application/json',
                status=500,
                response=http.json.dumps({'error': str(e)})
            )

    @http.route('/pokemon/list', auth='public', type='http', methods=['GET'], csrf=False, website=True)
    def pokemon_list(self, **kw):
        """
        Fetch Pokémon data and render it in a list view.
        """
        api_url = "https://pokeapi.co/api/v2/pokemon?limit=10"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json().get('results', [])
            
            return http.request.render('pokemon.pokemon_list', {
                'pokemon_list': data
            })
        except requests.exceptions.RequestException as e:
            return http.request.render('pokemon.error', {
                'error_message': str(e)
            })
            
    @http.route('/pokemon/<string:name>', auth='public', type='http', methods=['GET'], csrf=False, website=True)
    def detail(self, name):
        api_url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            # Pass sprite, name, height, weight, and types to the template
            pokemon_details = {
                'name': data['name'],
                'sprite': data['sprites']['front_default'],
                'height': data['height'],
                'weight': data['weight'],
                'types': [t['type']['name'] for t in data['types']],
            }
            return http.request.render('pokemon.pokemon_detail', {'pokemon': pokemon_details})
        except requests.exceptions.RequestException as e:
            return http.request.render('pokemon.error', {'error': str(e)})
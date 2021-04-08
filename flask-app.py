from flask import Flask, request
import os
import logging

import json

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    n = 'name'
    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ],
            'name': 'слона'
        }
        res['response']['text'] = f'Привет! Купи слона!'
        return

    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо',
        'я покупаю',
        'я куплю'
    ]:
        if sessionStorage[user_id][n][0] == 'слона':
            sessionStorage[user_id]['suggests'] = ["Не хочу.", "Не буду.", "Отстань!", ]
            sessionStorage[user_id][n] = 'кролика'
            res['response']['text'] = 'А теперь купи кролика!'
        else:
            res['response']['text'] = f'Купить слона и кролика можно на Яндекс.Маркете!'
            res['response']['end_session'] = True
        return

    res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи {sessionStorage[user_id][n][0]}!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]['suggests']

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session[:2]
    ]

    session = session[1:]
    sessionStorage[user_id]['suggests'] = session

    return suggests


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

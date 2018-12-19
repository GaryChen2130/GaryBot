from bottle import route, run, request, abort, static_file

from fsm import TocMachine


VERIFY_TOKEN = "1898GaryChen21301898"
machine = TocMachine(
    states=[
        'user',
        'stateNBA',
        'stateGame',
        'stateResult',
        'stateHighlight',
        'stateScoreboard',
        'stateMusic',
        'stateSearchMusic',
        'stateVideo',
        'stateSearchVideo',
        'stateLuck'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'stateNBA',
            'conditions': 'is_going_to_stateNBA'
        },
        {
            'trigger': 'advance',
            'source': 'stateNBA',
            'dest': 'stateGame',
            'conditions': 'is_going_to_stateGame'
        },
        {
            'trigger': 'advance',
            'source': 'stateGame',
            'dest': 'stateResult',
            'conditions': 'is_going_to_stateResult'
        },
        {
            'trigger': 'advance',
            'source': 'stateResult',
            'dest': 'stateScoreboard',
            'conditions': 'is_going_to_stateScoreboard'
        },
        {
            'trigger': 'advance',
            'source': [
                'stateResult',
                'stateScoreboard'
            ],
            'dest': 'stateHighlight',
            'conditions': 'is_going_to_stateHighlight'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'stateMusic',
            'conditions': 'is_going_to_stateMusic'
        },
        {
            'trigger': 'advance',
            'source': 'stateMusic',
            'dest': 'stateSearchMusic',
            'conditions': 'is_going_to_stateSearchMusic'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'stateVideo',
            'conditions': 'is_going_to_stateVideo'
        },
        {
            'trigger': 'advance',
            'source': 'stateVideo',
            'dest': 'stateSearchVideo',
            'conditions': 'is_going_to_stateSearchVideo'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'stateLuck',
            'conditions': 'is_going_to_stateLuck'
        },
        {
            'trigger': 'go_back',
            'source': [
                'stateHighlight',
                'stateSearchMusic',
                'stateSearchVideo',
                'stateLuck'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        machine.advance(event)
        return 'OK'


@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True, reloader=True)

import os
from flask import Flask, request, abort, make_response
from flask import render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def answer():
    user = { 'nickname': 'stephanec',
        'mail': 'schorlet@gmail.com' }
    q = request.args.get('q', '')

    if q == 'Quelle est ton adresse email':
        return user['mail']

    elif q == 'Es tu abonne a la mailing list(OUI/NON)':
        return 'OUI'

    elif q == 'Es tu heureux de participer(OUI/NON)':
        return 'OUI'

    elif q == 'Es tu pret a recevoir une enonce au format markdown par http post(OUI/NON)':
        return 'OUI'

    elif q == 'Est ce que tu reponds toujours oui(OUI/NON)':
        return 'NON'

    elif q == 'As tu bien recu le premier enonce(OUI/NON)':
        return 'OUI'

    elif q == '1 1':
        return '2'

    abort(404)


@app.route('/enonce/1', methods=['POST'])
def enonce_1():
    print 'headers: %s'%str(request.headers)
    print 'form: %s'%str(request.form)
    print 'data: %s'%str(request.data)
    return ''


@app.route('/scalaskel/change/<int:montant>')
def reponse_1(montant):
    import solution1
    from json import dumps
    solution = solution1.solution(montant)
    return make_response(dumps(solution))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(host='127.0.0.1', port=port, debug=True)

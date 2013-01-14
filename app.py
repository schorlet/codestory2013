import os, re, json
from flask import Flask, request, abort, make_response
from flask import render_template
import solution1, calculatrice, solution2

app = Flask(__name__)


@app.route('/', methods = ['GET'])
def answer():
    user = { 'nickname': 'stephanec',
        'mail': 'schorlet@gmail.com' }

    questions = ('Es tu abonne a la mailing list(OUI/NON)',
                'Es tu heureux de participer(OUI/NON)',
                'Es tu pret a recevoir une enonce au format markdown par http post(OUI/NON)',
                'As tu bien recu le premier enonce(OUI/NON)',
                'As tu bien recu le second enonce(OUI/NON)')

    q = request.args.get('q', '')

    if q == 'Quelle est ton adresse email':
        return user['mail']

    elif q == 'Est ce que tu reponds toujours oui(OUI/NON)':
        return 'NON'

    elif q in questions:
        return 'OUI'

    elif q == 'As tu passe une bonne nuit malgre les bugs de l etape precedente(PAS_TOP/BOF/QUELS_BUGS)':
        return 'QUELS_BUGS'
    else:
        try:
            q = re.sub(' ', '+', q)
            q = re.sub(',', '.', q)
            solution = calculatrice.solution('(%s)'%q)
            solution = re.sub(r'\.', ',', str(solution))
        except Exception as e:
            print str(e)
            pass
        else:
            return str(solution)

    abort(404)


def __read_payload(request):
    length = request.environ.get('CONTENT_LENGTH', '')
    length = 0 if length == '' else int(length)
    return request.environ['wsgi.input'].read(length)


@app.route('/enonce/<int:num>', methods = ['POST'])
def enonce(num):
    # print str(request.headers)
    print __read_payload(request)
    if num < 3:
        return '', 201
    return '', 204


@app.route('/scalaskel/change/<int:montant>', methods = ['GET'])
def reponse_1(montant):
    solution = solution1.solution(montant)
    return make_response(json.dumps(solution))


@app.route('/jajascript/optimize', methods = ['POST'])
def reponse_2():
    # print str(request.headers)
    commandes = json.loads(__read_payload(request))
    solution = solution2.solution(commandes)
    response = make_response(json.dumps(solution))
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(host='127.0.0.1', port=port, debug=True)

import os, re, json
from flask import Flask, request, abort, make_response
from flask import render_template
import solution1, calculatrice, solution2

app = Flask(__name__)


@app.route('/', methods = ['GET'])
def answer():
    questions = {'Quelle est ton adresse email': 'schorlet@gmail.com',
        'Es tu abonne a la mailing list(OUI/NON)': 'OUI',
        'Es tu heureux de participer(OUI/NON)': 'OUI',
        'Est ce que tu reponds toujours oui(OUI/NON)': 'NON',
        'Es tu pret a recevoir une enonce au format markdown par http post(OUI/NON)': 'OUI',
        'As tu bien recu le premier enonce(OUI/NON)': 'OUI',
        'As tu passe une bonne nuit malgre les bugs de l etape precedente(PAS_TOP/BOF/QUELS_BUGS)': 'QUELS_BUGS',
        'As tu bien recu le second enonce(OUI/NON)': 'OUI',
        'As tu copie le code de ndeloof(OUI/NON/JE_SUIS_NICOLAS)': 'NON'}

    q = request.args.get('q', '')

    if q in questions:
        return questions[q]

    elif re.search(r'\d', q):
        try:
            q = re.sub(' ', '+', q)
            q = re.sub(',', '.', q)
            solution = calculatrice.solution('(%s)'%q)
            solution = re.sub(r'\.', ',', str(solution))
            return str(solution)
        except:
            pass

    abort(400)


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
def reponse1(montant):
    solution = solution1.solution(montant)
    return make_response(json.dumps(solution))


@app.route('/jajascript/optimize', methods = ['POST'])
def reponse2():
    # print str(request.headers)
    try:
        commandes = json.loads(__read_payload(request))
        solution = solution2.solution(commandes)
        response = make_response(json.dumps(solution, sort_keys=True, separators=(',', ' : ')), 201)
        response.headers['Content-Type'] = 'application/json'
        return response
    except:
        pass
    abort(400)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(host='127.0.0.1', port=port, debug=True)

import os, re
from flask import Flask, request, abort, make_response
from flask import render_template
import solution1, solution2

app = Flask(__name__)


@app.route('/', methods=['GET'])
def answer():
    user = { 'nickname': 'stephanec',
        'mail': 'schorlet@gmail.com' }

    questions = ('Es tu abonne a la mailing list(OUI/NON)',
                'Es tu heureux de participer(OUI/NON)',
                'Es tu pret a recevoir une enonce au format markdown par http post(OUI/NON)',
                'Est ce que tu reponds toujours oui(OUI/NON)',
                'As tu bien recu le premier enonce(OUI/NON)')

    q = request.args.get('q', '')

    if q == 'Quelle est ton adresse email':
        return user['mail']

    elif q in questions:
        return 'OUI'

    else:
        match = re.search(r'\d+[ /*-][-]?\d+', q)
        if match:
            try:
                q = re.sub(' ', '+', q)
                # solution = solution2.solution('(%s)'%q)
                solution = eval(q)
            except Exception as e:
                print str(e)
                pass
            else:
                return str(solution)

    abort(404)


@app.route('/enonce/<int:num>', methods=['POST'])
def enonce(num):
    print 'headers: %s'%str(request.headers)
    print 'form: %s'%str(request.form)
    print 'data: %s'%str(request.data)
    return ''


@app.route('/scalaskel/change/<int:montant>')
def reponse_1(montant):
    from json import dumps
    solution = solution1.solution(montant)
    return make_response(dumps(solution))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(host='127.0.0.1', port=port, debug=True)

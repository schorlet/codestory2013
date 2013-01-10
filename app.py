import os
from flask import Flask, request, abort
from flask import render_template

app = Flask(__name__)


@app.route('/')
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

    abort(404)
    # return render_template('index.html', user=user)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(host='127.0.0.1', port=port, debug=True)

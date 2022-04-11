from flask import Flask, send_file
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

import jinja2
import pdfkit

app = Flask(__name__, static_url_path="")
api = Api(app)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://POSTGRES_USER:POSTGRES_PASSWORD@contract_db:5432/POSTGRES_DB"
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://db_user:db_pass_123@localhost:5432/contract_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Database model

class Contract(db.Model):
    __tablename__ = 'contract'
    contractId = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))

    def __repr__(self):
        return '<Contract %r>' % self.contractId


class DownloadContract(Resource):
    #  curl -i http://localhost:5000/contract/api/v1.0/contract-download/7
    def get(self, num_contract):
        contract_json = Contract.query.filter(Contract.contractId == num_contract).all()
        contract_dict = []
        for contract in contract_json:
            contract_dict.append({
                'contractId': contract.contractId,
                'firstName': contract.firstName,
                'lastNameName': contract.lastName,
            })
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "pdf_interest_report.html"
        template = templateEnv.get_template(TEMPLATE_FILE)

        outputText = template.render(first_name=contract_json[0].firstName,
                                     last_name=contract_json[0].lastName)
        html_file = open('contract.html', 'w', encoding='utf-8')
        html_file.write(outputText)
        html_file.close()
        pdfkit.from_file('contract.html', 'contract.pdf')
        path = "contract.pdf"
        return send_file(path, as_attachment=True)


class AddContractAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('firstName', type=str, required=True,
                                   help='First Name',
                                   location='json')
        self.reqparse.add_argument('lastName', type=str, required=True,
                                   help='Last Name',
                                   location='json')
        super(AddContractAPI, self).__init__()

    # curl -i -H "Content-Type: application/json" -X POST -d '{"firstName":"petya", "lastName":"petrov"}' http://localhost:5000/contract/api/v1.0/apply-contract
    def post(self):
        args = self.reqparse.parse_args()
        contract_row = Contract()  # table row
        for i in "firstName", "lastName":
            setattr(contract_row, i, args[i])
        try:
            db.session.add(contract_row)
            db.session.commit()
            db.session.flush()
        except:
            return "Error add contract to DB"

        return contract_row.contractId


api.add_resource(AddContractAPI, '/contract/api/v1.0/apply-contract', endpoint='contract')
api.add_resource(DownloadContract, '/contract/api/v1.0/contract-download/<int:num_contract>',
                 endpoint='tracks_for_year')

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
    app.run(host='0.0.0.0')

# docker build -t contract_db_img --build-arg POSTGRES_USER=db_user --build-arg POSTGRES_PASSWORD=db_pass_123 --build-arg POSTGRES_DB=contract_db .
# docker run -d -p 5432:5432 --name contract_db contract_db_img

# flask db init
# flask db migrate -m "Initial migration."
# flask db upgrade

# docker exec -it contract_db sh
# psql -U db_user -d contract_db
# \dt;

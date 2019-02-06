from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import force_instant_defaults

app = Flask(__name__)
app.secret_key = 'change this secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
force_instant_defaults()


class Gene(db.Model):
    __tablename__ = 'genes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, index=True)
    alt_name = db.Column(db.String(20))
    species = db.Column(db.String(20))
    uniprot = db.Column(db.String(20))
    _aliases = db.Column(db.Text, default='')
    sequence = db.Column(db.Text)

    @property
    def aliases(self):
        return [str(x) for x in self._aliases.split(', ')]

    @aliases.setter
    def aliases(self, value):
        if self._aliases != '':
            self._aliases = self._aliases+', %s' % str(value).replace(',', '')
        else:
            self._aliases = str(value).replace(', ', '')


def populate_db(filename):
    import csv
    all_data = []
    cleaned_data = []
    all_names = []
    with open('reference_files/Phosphosite_PTM_seq_sorted.txt', 'r') as f1:
        txt = f1.read()
        all_data = txt.split('>')

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            found = False
            aliases = row['Alias'].replace('"', '').split(', ')
            for li in all_data[1:]:
                if "_iso" in li.lower():
                    continue
                if "|"+row['Name'].lower()+"|" in li.lower():
                    found = True
                    sequence = ''.join(li.split('\n')[1:])
                    alt_name = li.split("|")[1]
                    uniprot = li.split("|")[3].split("\n")[0]
                    species = li.split("|")[2]
                    if row['Name'] in all_names:
                        print(row['Name'])
                    cleaned_data.append({"name": row['Name'], "sequence": sequence, "aliases": aliases,
                                         "alt_name": alt_name, "uniprot": uniprot, "species": species})
                    all_names.append(row['Name'])
                    break
            if not found:
                for li in all_data[1:]:
                    if "_iso" in li.lower():
                        continue
                    if ":"+row['Name'].lower()+"|" in li.lower():
                        found = True
                        sequence = ''.join(li.split('\n')[1:])
                        alt_name = li.split("|")[1]
                        uniprot = li.split("|")[3].split("\n")[0]
                        species = li.split("|")[2]
                        if row['Name'] in all_names:
                            print(row['Name'])
                        cleaned_data.append({"name": row['Name'], "sequence": sequence, "aliases": aliases,
                                             "alt_name": alt_name, "uniprot": uniprot, "species": species})
                        all_names.append(row['Name'])
                        break
                if not found:
                    for alias in aliases:
                        for li in all_data[1:]:
                            if "_iso" in li.lower():
                                continue
                            if "|"+alias.lower()+"|" in li.lower():
                                found = True
                                sequence = ''.join(li.split('\n')[1:])
                                alt_name = li.split("|")[1]
                                uniprot = li.split("|")[3].split("\n")[0]
                                species = li.split("|")[2]
                                if row['Name'] in all_names:
                                    print(row['Name'])
                                cleaned_data.append({"name": row['Name'], "sequence": sequence, "aliases": aliases,
                                                     "alt_name": alt_name, "uniprot": uniprot, "species": species})
                                all_names.append(row['Name'])
                                break
                        if found:
                            break
                    if not found:
                        for alias in aliases:
                            for li in all_data[1:]:
                                if "_iso" in li.lower():
                                    continue
                                if ":"+alias.lower()+"|" in li.lower():
                                    found = True
                                    sequence = ''.join(li.split('\n')[1:])
                                    alt_name = li.split("|")[1]
                                    uniprot = li.split("|")[3].split("\n")[0]
                                    species = li.split("|")[2]
                                    if row['Name'] in all_names:
                                        print(row['Name'])
                                    cleaned_data.append({"name": row['Name'], "sequence": sequence, "aliases": aliases,
                                                         "alt_name": alt_name, "uniprot": uniprot, "species": species})
                                    all_names.append(row['Name'])
                                    break
                            if found:
                                break
                        if not found:
                            print(row['Name'])
                            if row['Alias'].lower() == "none":
                                cleaned_data.append({"name": row['Name'], "sequence": "", "aliases": aliases,
                                                    "alt_name": "", "uniprot": "", "species": ""})
                                all_names.append(row['Name'])
    for item in cleaned_data:
        g = Gene(name=item['name'], sequence=item['sequence'], uniprot=item['uniprot'], alt_name=item['alt_name'], species=item['species'])
        for a in item['aliases']:
            g.aliases = a
        db.session.add(g)
    db.session.commit()


@app.route('/')
def index():
    return render_template('datatable.html')


@app.route('/_table/')
def get_table_data():
    genes = Gene.query.all()
    data = []
    for g in genes:
        data.append({
            'id': g.id,
            'name': g.name,
            'aliases': g._aliases,
        })
    return jsonify({'data': data})


@app.route('/details/')
def details():
    g = Gene.query.filter(Gene.id == int(request.args.get('g'))).first()
    chunks = [g.sequence[i:i+10] for i in range(0, len(g.sequence), 10)]
    data = {"id": g.id, "name": g.name, "aliases": g.aliases, "sequence": g.sequence, "chunks": chunks}
    return render_template('details.html', data=data)


@app.route('/download/')
def download():
    g = Gene.query.filter(Gene.id == int(request.args.get('g'))).first()
    chunks = [g.sequence[i:i+60] for i in range(0, len(g.sequence), 60)]
    s = "\n".join(chunks)
    data = {"name": g.name, "alt_name": g.alt_name, "species": g.species, "uniprot": g.uniprot, "sequence": s}
    return render_template('download.txt', data=data)


if __name__ == '__main__':
    db.create_all()
    # populate_db('reference_files/kinase_names.csv')
    # populate_db('reference_files/updated_data.csv')
    app.run()

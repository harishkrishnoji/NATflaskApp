from app import app
from flask import render_template, request
from app.models import nat

fields = ['Firewall', 'FirewallName', 'Method', 'OriginalDestination', 'OriginalSource', 'Name', 'TranslatedDestination', 'TranslatedSource']
total = nat.query.count()

@app.route("/")
def home():
    return render_template('home.html', total_nat=total)

@app.route("/nats", methods=['POST'])
def nat_records():
    addr = request.form.get("addr")
    if addr.count(".") == 3:
        rule = query_db(addr)
        return render_template('nat.html', nat=rule, address=addr)
    else:
        return render_template('home.html', total_nat=total)

def query_db(addr):
    rules = []
    rules.extend(_format_rule(nat.query.filter(nat.OriginalSource.contains(addr))))
    rules.extend(_format_rule(nat.query.filter(nat.TranslatedSource.contains(addr))))
    rules.extend(_format_rule(nat.query.filter(nat.OriginalDestination.contains(addr))))
    rules.extend(_format_rule(nat.query.filter(nat.TranslatedDestination.contains(addr))))
    filtered_list = [i for n, i in enumerate(rules) if i not in rules[n + 1:]]
    return filtered_list

def query_all(offset=0, limit=500):
    resp_data = {}
    resp_data["total"] = total
    resp_data["offset"] = offset
    resp_data["limit"] = limit
    resp_data["results"] = _format_all_rule(nat.query.offset(offset).limit(limit).all())
    return resp_data

def _format_all_rule(rules):
    frules = []
    for i in range(len(rules)):
        frule = {}
        for field in fields:
            frule[field] = getattr(rules[i], field)
        frules.append(frule)
    return frules

def _format_rule(rules):
    frules = []
    if rules.count() > 0:
        for i in range(rules.count()):
            frule = {}
            for field in fields:
                frule[field] = getattr(rules[i], field)
            frules.append(frule)
    return frules

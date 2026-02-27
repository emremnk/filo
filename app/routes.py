from datetime import date, timedelta

from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from . import db
from .models import Check, Driver, DriverAbsence, TrafficFine, Unit, Vehicle, to_iso

bp = Blueprint('main', __name__)


def parse_date(value):
    return date.fromisoformat(value) if value else None


@bp.route('/')
def dashboard():
    today_items = collect_today_tasks()
    stats = {
        'vehicles': Vehicle.query.count(),
        'drivers': Driver.query.count(),
        'units': Unit.query.count(),
        'fines': TrafficFine.query.count(),
        'checks': Check.query.count(),
    }
    return render_template('dashboard.html', stats=stats, today_items=today_items)


# Vehicles CRUD
@bp.route('/vehicles')
def vehicles_page():
    return render_template('vehicles.html', vehicles=Vehicle.query.order_by(Vehicle.plate).all())


@bp.route('/vehicles', methods=['POST'])
def vehicle_create():
    vehicle = Vehicle(
        plate=request.form['plate'],
        inspection_date=parse_date(request.form.get('inspection_date')),
        insurance_date=parse_date(request.form.get('insurance_date')),
        exam_date=parse_date(request.form.get('exam_date')),
    )
    db.session.add(vehicle)
    db.session.commit()
    return redirect(url_for('main.vehicles_page'))


@bp.route('/vehicles/<int:vehicle_id>')
def vehicle_detail(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return render_template('vehicle_detail.html', vehicle=vehicle)


@bp.route('/vehicles/<int:vehicle_id>/update', methods=['POST'])
def vehicle_update(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    vehicle.plate = request.form['plate']
    vehicle.inspection_date = parse_date(request.form.get('inspection_date'))
    vehicle.insurance_date = parse_date(request.form.get('insurance_date'))
    vehicle.exam_date = parse_date(request.form.get('exam_date'))
    db.session.commit()
    return redirect(url_for('main.vehicle_detail', vehicle_id=vehicle.id))


@bp.route('/vehicles/<int:vehicle_id>/delete', methods=['POST'])
def vehicle_delete(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for('main.vehicles_page'))


# Drivers CRUD
@bp.route('/drivers')
def drivers_page():
    return render_template('drivers.html', drivers=Driver.query.order_by(Driver.name).all())


@bp.route('/drivers', methods=['POST'])
def driver_create():
    driver = Driver(name=request.form['name'])
    db.session.add(driver)
    db.session.commit()
    return redirect(url_for('main.drivers_page'))


@bp.route('/drivers/<int:driver_id>')
def driver_detail(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    return render_template('driver_detail.html', driver=driver)


@bp.route('/drivers/<int:driver_id>/update', methods=['POST'])
def driver_update(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    driver.name = request.form['name']
    driver.identity_no = request.form.get('identity_no')
    driver.phone = request.form.get('phone')
    driver.license_info = request.form.get('license_info')
    driver.license_expiry = parse_date(request.form.get('license_expiry'))
    db.session.commit()
    return redirect(url_for('main.driver_detail', driver_id=driver.id))


@bp.route('/drivers/<int:driver_id>/delete', methods=['POST'])
def driver_delete(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    db.session.delete(driver)
    db.session.commit()
    return redirect(url_for('main.drivers_page'))


@bp.route('/drivers/<int:driver_id>/absences')
def driver_absences(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    return render_template('driver_absences.html', driver=driver)


@bp.route('/drivers/<int:driver_id>/absences', methods=['POST'])
def driver_absence_create(driver_id):
    Driver.query.get_or_404(driver_id)
    absence = DriverAbsence(driver_id=driver_id, absence_date=parse_date(request.form['absence_date']))
    db.session.add(absence)
    db.session.commit()
    return redirect(url_for('main.driver_absences', driver_id=driver_id))


@bp.route('/absences/<int:absence_id>/delete', methods=['POST'])
def driver_absence_delete(absence_id):
    absence = DriverAbsence.query.get_or_404(absence_id)
    driver_id = absence.driver_id
    db.session.delete(absence)
    db.session.commit()
    return redirect(url_for('main.driver_absences', driver_id=driver_id))


# Units CRUD
@bp.route('/units')
def units_page():
    return render_template('units.html', units=Unit.query.order_by(Unit.name).all())


@bp.route('/units', methods=['POST'])
def unit_create():
    unit = Unit(name=request.form['name'])
    db.session.add(unit)
    db.session.commit()
    return redirect(url_for('main.units_page'))


@bp.route('/units/<int:unit_id>')
def unit_detail(unit_id):
    unit = Unit.query.get_or_404(unit_id)
    return render_template('unit_detail.html', unit=unit)


@bp.route('/units/<int:unit_id>/update', methods=['POST'])
def unit_update(unit_id):
    unit = Unit.query.get_or_404(unit_id)
    unit.name = request.form['name']
    unit.contract_start = parse_date(request.form.get('contract_start'))
    unit.contract_end = parse_date(request.form.get('contract_end'))
    unit.invoice_date = parse_date(request.form.get('invoice_date'))
    db.session.commit()
    return redirect(url_for('main.unit_detail', unit_id=unit.id))


@bp.route('/units/<int:unit_id>/delete', methods=['POST'])
def unit_delete(unit_id):
    unit = Unit.query.get_or_404(unit_id)
    db.session.delete(unit)
    db.session.commit()
    return redirect(url_for('main.units_page'))


# Fines CRUD
@bp.route('/fines')
def fines_page():
    return render_template('fines.html', fines=TrafficFine.query.order_by(TrafficFine.payment_date.desc()).all(), vehicles=Vehicle.query.order_by(Vehicle.plate).all())


@bp.route('/fines', methods=['POST'])
def fine_create():
    fine = TrafficFine(
        vehicle_id=int(request.form['vehicle_id']),
        payment_date=parse_date(request.form['payment_date']),
        deducted_from_salary=request.form.get('deducted_from_salary') == 'on',
        description=request.form.get('description'),
    )
    db.session.add(fine)
    db.session.commit()
    return redirect(url_for('main.fines_page'))


@bp.route('/fines/<int:fine_id>/delete', methods=['POST'])
def fine_delete(fine_id):
    fine = TrafficFine.query.get_or_404(fine_id)
    db.session.delete(fine)
    db.session.commit()
    return redirect(url_for('main.fines_page'))


# Checks CRUD
@bp.route('/checks')
def checks_page():
    return render_template('checks.html', checks=Check.query.order_by(Check.due_date.desc()).all())


@bp.route('/checks', methods=['POST'])
def check_create():
    check = Check(
        due_date=parse_date(request.form['due_date']),
        amount=float(request.form['amount']),
        company=request.form['company'],
        received_date=parse_date(request.form.get('received_date')),
        issued_date=parse_date(request.form.get('issued_date')),
        payable_date=parse_date(request.form.get('payable_date')),
    )
    db.session.add(check)
    db.session.commit()
    return redirect(url_for('main.checks_page'))


@bp.route('/checks/<int:check_id>/delete', methods=['POST'])
def check_delete(check_id):
    check = Check.query.get_or_404(check_id)
    db.session.delete(check)
    db.session.commit()
    return redirect(url_for('main.checks_page'))


@bp.route('/calendar')
def calendar_page():
    return render_template('calendar.html')


@bp.route('/today-tasks')
def today_tasks_page():
    items = collect_today_tasks()
    return render_template('today_tasks.html', items=items)


# API
@bp.route('/api/events')
def api_events():
    return jsonify(collect_events())


@bp.route('/api/today-tasks')
def api_today_tasks():
    return jsonify(collect_today_tasks())


@bp.route('/api/vehicles')
def api_vehicles():
    return jsonify([
        {
            'id': v.id,
            'plate': v.plate,
            'inspection_date': to_iso(v.inspection_date),
            'insurance_date': to_iso(v.insurance_date),
            'exam_date': to_iso(v.exam_date),
        }
        for v in Vehicle.query.all()
    ])


def collect_events():
    events = []
    for v in Vehicle.query.all():
        for title, d in [
            (f'{v.plate} - Vize', v.inspection_date),
            (f'{v.plate} - Sigorta', v.insurance_date),
            (f'{v.plate} - Muayene', v.exam_date),
        ]:
            if d:
                events.append({'title': title, 'date': d.isoformat(), 'type': 'vehicle'})

    for d in Driver.query.all():
        if d.license_expiry:
            events.append({'title': f'{d.name} - Ehliyet Bitiş', 'date': d.license_expiry.isoformat(), 'type': 'driver'})

    for u in Unit.query.all():
        for title, dt in [
            (f'{u.name} - Sözleşme Bitiş', u.contract_end),
            (f'{u.name} - Fatura Kesim', u.invoice_date),
        ]:
            if dt:
                events.append({'title': title, 'date': dt.isoformat(), 'type': 'unit'})

    for f in TrafficFine.query.all():
        events.append({'title': f'{f.vehicle.plate} - Ceza Ödeme', 'date': f.payment_date.isoformat(), 'type': 'fine'})

    for c in Check.query.all():
        events.append({'title': f'{c.company} - Çek Vade', 'date': c.due_date.isoformat(), 'type': 'check'})
        if c.payable_date:
            events.append({'title': f'{c.company} - Çek Ödenecek', 'date': c.payable_date.isoformat(), 'type': 'check'})

    return events


def collect_today_tasks():
    all_events = collect_events()
    today = date.today()
    future_limit = today + timedelta(days=7)
    tasks = []
    for e in all_events:
        event_date = parse_date(e['date'])
        if event_date == today or event_date <= future_limit:
            if event_date < today:
                level = 'danger'
            elif event_date <= future_limit:
                level = 'warning'
            else:
                level = 'primary'
            tasks.append({**e, 'status': level})

    tasks.sort(key=lambda x: x['date'])
    return tasks

import paypalrestsdk
from flask import render_template, request, url_for, jsonify, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app import app, db
from app.forms import LoginForm, RegistrationParentForm
from app.models import Student, Bill, Parent, BillStatus


paypalrestsdk.configure({
  "mode": "sandbox",    # sandbox or live
  "client_id": "AVPgs8oh9gF92zOhcXhR8CE7jW2byuDPgq1AHFILOhDu9ijlsqJUDGYRx-48kaUxuyzIUv-opTw50FL_",
  "client_secret": "EGBwKFjVmOzzll6Tgp5VK8u1I9HyMjwZMhq1K29YThDyHkDJMZPBXkYzaeBly-IsZ8udwfqK1-mfy66X"})


# @app.route('/')
@app.route('/parent_dashboard')
@login_required
def parent_dashboard():
    your_children_data = db.session.query(
        Student.id, Student.name, Student.major,
        Student.student_registration_number).filter_by(parent_id=current_user.id).all()
    return render_template('parent_dashboard.html', your_children_data=your_children_data)


@app.route('/parent_login', methods=['GET', 'POST'])
def parent_login():
    if current_user.is_authenticated:
        return redirect(url_for('parent_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Parent.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('parent_login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('parent_dashboard')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('parent_dashboard'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('parent_dashboard'))
    form = RegistrationParentForm()
    if form.validate_on_submit():
        user = Parent(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, You are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/checkout/<student_id>')
@login_required
def checkout(student_id):
    student = db.session.query(Student.id, Student.name, Student.student_registration_number,
                               Student.major, Bill.total_bill).join(Bill).\
        filter(Student.bill_id == Bill.id). filter(Student.id == student_id).first()
    print('test', student)
    # bill = db.session.query(Bill.total_bill).filter_by(student=student_id).first()
    return render_template('billing_details.html', student=student)


@app.route('/payment/<student_id>', methods=['POST'])
def payment(student_id):
    student = Student.query.filter_by(id=student_id).first()
    student_name = student.name
    student_bill = db.session.query(Bill.total_bill).filter_by(student_id=student_id).first()
    student_bill = list(student_bill)[0]
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": student_name + " Tuition Payment",
                    "sku": "12345",
                    "price": student_bill,
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": student_bill,
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)
    return jsonify({'paymentID': payment.id})


@app.route('/execute/<student_id>', methods=['POST'])
def execute(student_id):
    bill = Bill.query.filter_by(student_id=student_id).first()
    student_bill = db.session.query(Bill.total_bill).filter_by(student_id=student_id).first()
    student_bill = list(student_bill)[0]
    bill_total = bill.total_bill - student_bill
    try:
        bill.bill_status = BillStatus.COMPLETED.value
        bill.total_bill = bill_total
        db.session.commit()
    except Exception as e:
        return {'error': str(e)}

    success = False
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])
    if payment.execute({'payer_id': request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)
    return jsonify({'success': success})

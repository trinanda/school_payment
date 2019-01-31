import paypalrestsdk
from flask import render_template, request, jsonify
from flask_login import login_required

from app import app, db
from app.models import Student, Bill, BillStatus
from config import Config


paypalrestsdk.configure({
  "mode": "sandbox",    # sandbox or live
  "client_id": Config.CLIENT_ID,
  "client_secret": Config.CLIENT_SECRET})


@app.route('/checkout/<student_id>')
@login_required
def checkout(student_id):
    student = db.session.query(Student.id, Student.name, Student.student_registration_number,
                               Student.major, Bill.total_bill).join(Bill).\
        filter(Student.bill_id == Bill.id).filter(Student.id == student_id).first()
    return render_template('checkout.html', student=student)


@app.route('/payment/<student_id>', methods=['POST'])
def payment(student_id):
    student = db.session.query(Student.id, Student.name, Bill.total_bill).join(Bill).\
        filter(Student.id == student_id).first()
    student_name = student.name
    student_bill = student.total_bill
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
    student = db.session.query(Student.id, Student.name, Bill.total_bill, Student.bill_id).join(Bill).\
        filter(Student.id == student_id).first()
    student_bill = student.total_bill
    bill = db.session.query(Bill).filter_by(id=student.bill_id).first()
    change_total_bill = bill.total_bill - student_bill
    try:
        bill.total_bill = change_total_bill
        if bill.total_bill <= 0:
            bill.bill_status = BillStatus.COMPLETED.value
        else:
            pass
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

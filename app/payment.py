import paypalrestsdk
from flask import render_template, request, jsonify
from flask_login import login_required

from app import app, db
from app.models import Student, Bill, BillStatus


paypalrestsdk.configure({
  "mode": "sandbox",    # sandbox or live
  "client_id": "AVPgs8oh9gF92zOhcXhR8CE7jW2byuDPgq1AHFILOhDu9ijlsqJUDGYRx-48kaUxuyzIUv-opTw50FL_",
  "client_secret": "EGBwKFjVmOzzll6Tgp5VK8u1I9HyMjwZMhq1K29YThDyHkDJMZPBXkYzaeBly-IsZ8udwfqK1-mfy66X"})


@app.route('/checkout/<student_id>')
@login_required
def checkout(student_id):
    student = db.session.query(Student.id, Student.name, Student.student_registration_number,
                               Student.major, Bill.total_bill).join(Bill).\
        filter(Student.bill_id == Bill.id). filter(Student.id == student_id).first()
    return render_template('checkout.html', student=student)


@app.route('/payment/<student_id>', methods=['POST'])
def payment(student_id):
    student = db.session.query(Student.id, Student.name, Bill.total_bill).filter(Student.id == student_id).first()
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
    student = db.session.query(Student.id, Bill.total_bill, Student.bill_id).filter(Student.id == student_id).first()
    student_bill = student.total_bill
    bill = db.session.query(Bill).filter_by(id=student.bill_id).first()
    # print('test', bill.total_bill)
    change_total_bill = bill.total_bill - student_bill
    try:
        bill.bill_status = BillStatus.COMPLETED.value
        bill.total_bill = change_total_bill
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

# @app.route('/execute/<student_id>', methods=['POST'])
# def execute(student_id):
#     ##
#     bill = Bill.query.filter_by(student_id=student_id).first()
#     student_bill = db.session.query(Bill.total_bill).filter_by(student_id=student_id).first()
#     student_bill = list(student_bill)[0]
#     bill_total = bill.total_bill - student_bill
#     try:
#         bill.bill_status = BillStatus.COMPLETED.value
#         bill.total_bill = bill_total
#         db.session.commit()
#     except Exception as e:
#         return {'error': str(e)}
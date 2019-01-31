# School Tuition Payments

### School tuition payment app with PayPal

Installation process
```bash
$ git clone https://github.com/trinanda/school_payment.git
$ cd school_payment
$ pip3 install -r requirements.txt
```

##### Get the PayPal credential from the PayPal Developer page:
1. go to this URL: https://developer.paypal.com/
2. Log into Dashboard
3. On **Sandbox** tab go to **Accounts**
4. Usually there has two's account there on is the business type followed by *yourmail-facilitator@example.com* and the other one is personal account type followed by *yourmail-buyer@example.com*.
5. If there has no account you can go create one for business type and the other one for personal type account.
6. Make sure you have done the steps above.
7. On the business type account click **Profile**
8. Then go to **API Credentials**
9. Click on your **App name**
10. There you can see the **Client ID** and the **Secret** which is hide that you can click **show**.

##### Export the Credential to your environment:
```bash
$ export CLIENT_ID=YOUR_PAYPAL_CLIENT_ID
$ export CLIENT_SECRET=YOUR_PAYPAL_CLIENT_SECRET
```

##### Run the app
```bash
$ flask run
```
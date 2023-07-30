import smtplib
import requests
from bs4 import BeautifulSoup
import lxml
import time
from smtplib import SMTP
import os
from dotenv import load_dotenv
Product_URL = "https://www.amazon.com/ODK-Shaped-" \
              "Outlets-Computer-Monitor/dp/B0BTNQ57BL" \
              "/ref=pd_rhf_d_se_s_pd_sbs_rvi_sccl_1_6/139-" \
              "1618391-2403431?pd_rd_w=n9BqF&content-id=amzn1." \
              "sym.a089f039-4dde-401a-9041-8b534ae99e65&pf_rd_p=a" \
              "089f039-4dde-401a-9041-8b534ae99e65&pf_rd_r=Z3D23MAPQE" \
              "YQSDAEM6FA&pd_rd_wg=nakFH&pd_rd_r=ada65a9b-0566-4c72-b74b-" \
              "366b1c5698eb&pd_rd_i=B0BTNRDPKJ&th=1"

headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Defined"
}
load_dotenv()
password = os.getenv("PASSWORD")
MY_EMAIL = os.getenv("MY_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

DEAL_PRICE = 190.99

def check():
    global Product_URL, headers
    response = requests.get(url=Product_URL, headers=headers)
    cart_url = response.text
    soup = BeautifulSoup(cart_url, "lxml")

    product_price = soup.find("span", class_="a-offscreen")
    if product_price is None:
        return None
    else:
        price = product_price.getText().strip("$")
        print(f"Price of product dropped and currently sitting at ${price}")
        return float(price)


loop = True
counter = 0
get_current_price = check()
while loop is True and get_current_price is None and counter < 15:
    print(f"Attempt {counter} returned {get_current_price}")
    counter += 1
    # time.sleep(2)
    get_current_price = check()
else:
    current_price = get_current_price
    if current_price < DEAL_PRICE:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=password)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=RECIPIENT_EMAIL,
                                msg=f"Subject:Amazon Price Alert \nPrice of product "
                                    f"dropped and currently sitting at ${current_price}")

        loop = False

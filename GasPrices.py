import urllib.request
import json
import sqlite3
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'

class GasPrices():
    def __init__(self, json_dict, type_of_gas, normal = True):
        self.normal_higher = "normal" if normal else "higher"
        self.type_of_gas = type_of_gas
        self.tax_co2 = json_dict[type_of_gas][self.normal_higher]["tax_co2"]
        self.tax = json_dict[type_of_gas][self.normal_higher]["tax"]
        self.charge = json_dict[type_of_gas][self.normal_higher]["charge"]
        self.updated = json_dict[type_of_gas][self.normal_higher]["updated"]
        self.excise_duty = json_dict[type_of_gas][self.normal_higher]["excise_duty"]
        self.price = json_dict[type_of_gas][self.normal_higher]["price"]
        self.price_neto = json_dict[type_of_gas][self.normal_higher]["price_neto"]

class Country():
    def __init__(self, country, json_dict):
        self.jsonDict = json_dict[country]
        self.country = country
        self.currency = self.jsonDict["currency"]
        self.gas_100 = GasPrices(self.jsonDict, "100")
        self.gas_95 = GasPrices(self.jsonDict, "95")
        self.diesel = GasPrices(self.jsonDict, "diesel")
        self.ko = GasPrices(self.jsonDict, "ko")

    def __repr__(self):
        print("price of Diesel: ", self.diesel.price)
        print("price for 100: ", self.gas_100.price)
        print("price for 95: ", self.gas_95.price)
        print("price for ko: ", self.ko.price)
        return(self.country)

    def save_to_database(self):
        con = sqlite3.connect("GasPrices.db")
        with con:
            cur = con.cursor()
            con.row_factory = sqlite3.Row

            # check if entry is updated!
            cur.execute("SELECT updated FROM GasPrice WHERE country=? AND gas_type=?", (self.country, self.diesel.type_of_gas))
            should_update_diesel = False
            i = 0
            while True:
                row = cur.fetchone()
                if (row == None):
                    if (i == 0):
                        should_update_diesel = True
                    break
                if (datetime.strptime(row[0], DATE_FORMAT) < datetime.strptime(self.diesel.updated, DATE_FORMAT)):
                    should_update_diesel = True
                i += 1

            # diesel
            if (should_update_diesel):
                cur.execute("INSERT INTO GasPrice"
                        "("
                        "country,"
                        "currency,"
                        "gas_type,"
                        "normal,"
                        "price,"
                        "price_neto,"
                        "charge,"
                        "excise_duty,"
                        "tax,"
                        "tax_co2,"
                        "updated"
                        ") VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (
                    self.country,
                    self.currency,
                    self.diesel.type_of_gas,
                    1,
                    self.diesel.price,
                    self.diesel.price_neto,
                    self.diesel.charge,
                    self.diesel.excise_duty,
                    self.diesel.tax,
                    self.diesel.tax_co2,
                    self.diesel.updated
                )
            )

            cur.execute("SELECT updated FROM GasPrice WHERE country=? AND gas_type=?", (self.country, self.gas_100.type_of_gas))
            should_update_gas_100 = False
            i = 0
            while True:
                row = cur.fetchone()
                if (row == None):
                    if (i == 0):
                        should_update_gas_100 = True
                    break
                if (datetime.strptime(row[0], DATE_FORMAT) < datetime.strptime(self.diesel.updated, DATE_FORMAT)):
                    should_update_gas_100 = True
                i += 1
            if (should_update_gas_100):
                # 100
                cur.execute("INSERT INTO GasPrice"
                            "("
                            "country,"
                            "currency,"
                            "gas_type,"
                            "normal,"
                            "price,"
                            "price_neto,"
                            "charge,"
                            "excise_duty,"
                            "tax,"
                            "tax_co2,"
                            "updated"
                            ") VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        self.country,
                        self.currency,
                        self.gas_100.type_of_gas,
                        1,
                        self.gas_100.price,
                        self.gas_100.price_neto,
                        self.gas_100.charge,
                        self.gas_100.excise_duty,
                        self.gas_100.tax,
                        self.gas_100.tax_co2,
                        self.gas_100.updated
                    )
                )


            cur.execute("SELECT updated FROM GasPrice WHERE country=? AND gas_type=?", (self.country, self.gas_95.type_of_gas))
            should_update_gas_95 = False
            i = 0
            while True:
                row = cur.fetchone()
                if (row == None):
                    if (i == 0):
                        should_update_gas_95 = True
                    break
                if (datetime.strptime(row[0], DATE_FORMAT) < datetime.strptime(self.diesel.updated, DATE_FORMAT)):
                    should_update_gas_95 = True
                i += 1
            # 95

            if (should_update_gas_95):
                cur.execute("INSERT INTO GasPrice"
                        "("
                        "country,"
                        "currency,"
                        "gas_type,"
                        "normal,"
                        "price,"
                        "price_neto,"
                        "charge,"
                        "excise_duty,"
                        "tax,"
                        "tax_co2,"
                        "updated"
                        ") VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (
                    self.country,
                    self.currency,
                    self.gas_95.type_of_gas,
                    1,
                    self.gas_95.price,
                    self.gas_95.price_neto,
                    self.gas_95.charge,
                    self.gas_95.excise_duty,
                    self.gas_95.tax,
                    self.gas_95.tax_co2,
                    self.gas_95.updated
                )
            )


            cur.execute("SELECT updated FROM GasPrice WHERE country=? AND gas_type=?", (self.country, self.ko.type_of_gas))
            should_update_ko = False
            i = 0
            while True:
                row = cur.fetchone()
                if (row == None):
                    if (i == 0):
                        should_update_ko = True
                    break
                if (datetime.strptime(row[0], DATE_FORMAT) < datetime.strptime(self.diesel.updated, DATE_FORMAT)):
                    should_update_ko = True
                i += 1
            if (should_update_ko):
                # kurilno olje
                cur.execute("INSERT INTO GasPrice"
                            "("
                            "country,"
                            "currency,"
                            "gas_type,"
                            "normal,"
                            "price,"
                            "price_neto,"
                            "charge,"
                            "excise_duty,"
                            "tax,"
                            "tax_co2,"
                            "updated"
                            ") VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        self.country,
                        self.currency,
                        self.ko.type_of_gas,
                        1,
                        self.ko.price,
                        self.ko.price_neto,
                        self.ko.charge,
                        self.ko.excise_duty,
                        self.ko.tax,
                        self.ko.tax_co2,
                        self.ko.updated
                    )
                )

    def open_connection(self):
        return sqlite3.connect("GasPrices.db")


# CREATE TABLE `GasPrice` (
# 	`_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
# 	`country`	TEXT NOT NULL,
# 	`currency`	TEXT NOT NULL,
# 	`gas_type`	TEXT NOT NULL,
# 	`normal`	INTEGER NOT NULL DEFAULT 1,
# 	`price`	REAL,
# 	`price_neto`	REAL,
# 	`charge`	REAL,
# 	`excise_duty`	REAL,
# 	`tax`	REAL,
# 	`tax_co2`	INTEGER,
# 	`updated`	TEXT
# );


# "Slovenia": {
#         "95": {
#             "normal": {
#                 "price": "1.29200000",
#                 "price_neto": "0.44837000",
#                 "charge": "0.00400000",
#                 "excise_duty": "0.56385000",
#                 "tax": "0.23298000",
#                 "tax_co2": "0.03456000",
#                 "updated": "2014-12-23"
#             }
#         },
#         "100": {
#             "normal": {
#                 "price": "1.32800000",
#                 "price_neto": "0.47787000",
#                 "charge": "0.00400000",
#                 "excise_duty": "0.56385000",
#                 "tax": "0.23948000",
#                 "tax_co2": "0.03456000",
#                 "updated": "2014-12-23"
#             }
#         },
#         "currency": "EUR",
#         "diesel": {
#             "normal": {
#                 "price": "1.22500000",
#                 "price_neto": "0.49560000",
#                 "charge": "0.00200000",
#                 "excise_duty": "0.46010000",
#                 "tax": "0.22090000",
#                 "tax_co2": "0.03744000",
#                 "updated": "2014-12-23"
#             }
#         },
#         "lpg": {
#             "normal": {
#                 "price": "0.69900000",
#                 "price_neto": "0.47413000",
#                 "charge": "0.01193000",
#                 "excise_duty": "0.07242000",
#                 "tax": "0.12605000",
#                 "tax_co2": "0.00000000",
#                 "updated": "2014-12-09"
#             }
#         },
#         "ko": {
#             "normal": {
#                 "price": "0.88000000",
#                 "price_neto": "0.45658000",
#                 "charge": "0.06500000",
#                 "excise_duty": "0.14237000",
#                 "tax": "0.15869000",
#                 "tax_co2": "0.03744000",
#                 "updated": "2014-12-23"
#             }
#         }
#     },

        


response = urllib.request.urlopen('http://www.petrol.si/api/fuel_prices.json')
a = str(response.read())
a = a[2:len(a)-1]
# print(a)
b = json.loads(a) # decode JSON format

# prices for Slovenia

prices_in_slo = Country("Slovenia", b)
prices_in_slo.save_to_database()

        

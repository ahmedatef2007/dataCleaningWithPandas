import numpy as np
import pandas as pd

marketing = pd.read_csv("bank_marketing.csv")

client = marketing[["client_id", "age", "job", "marital", "education",
                    "credit_default", "housing", "loan"]]
campaign = marketing[["client_id", "campaign", "month", "day",
                      "duration", "pdays", "previous", "poutcome", "y"]]
economics = marketing[["client_id", "emp_var_rate", "cons_price_idx",
                       "euribor3m", "nr_employed"]]

client.rename(columns={"client_id": "id"}, inplace=True)

campaign.rename(columns={"duration": "contact_duration",
                         "y": "campaign_outcome",
                         "campaign": "number_contacts",
                         "previous": "previous_campaign_contacts",
                         "poutcome": "previous_outcome"},
                inplace=True)

economics.rename(columns={"euribor3m": "euribor_three_months",
                          "nr_employed": "number_employed"},
                 inplace=True)

client["education"] = client["education"].str.replace(".", "_")
client["education"] = client["education"].replace("unknown", np.NaN)

client["job"] = client["job"].str.replace(".", "")

campaign["campaign_outcome"] = campaign["campaign_outcome"].map({"yes": 1,
                                                                 "no": 0})

campaign["previous_outcome"] = campaign["previous_outcome"].replace("nonexistent",
                                                                    np.NaN)
campaign["previous_outcome"] = campaign["previous_outcome"].map({"success": 1,
                                                                 "failure": 0})

campaign["campaign_id"] = 1

campaign["month"] = campaign["month"].str.capitalize()

campaign["year"] = "2022"

campaign["day"] = campaign["day"].astype(str)

campaign["last_contact_date"] = campaign["year"] + "-" + campaign["month"] + "-" + campaign["day"]

campaign["last_contact_date"] = pd.to_datetime(campaign["last_contact_date"],
                                               format="%Y-%b-%d")

campaign.drop(columns=["month", "day", "year"], inplace=True)

client.to_csv("client.csv", index=False)
campaign.to_csv("campaign.csv", index=False)
economics.to_csv("economics.csv", index=False)


pricevolume = [
        "open","close","high","low","vwap","volume","returns","adv20",
        "sharesout","cap","split","dividend","market","country","exchange",
        "sector","industry","subindustry"
    ]

fundamental = [
        "accounts_payable","accum_depre","assets","assets_curr","assets_curr_oth",
        "bookvalue_ps","capex","cash","cash_st","cashflow","cashflow_dividends",
        "cashflow_fin","cashflow_invst","cashflow_op","cogs","cost_of_revenue",
        "current_ratio",
        "debt","debt_lt","debt_lt_curr","debt_st","depre","depre_amort",
        "EBIT","EBITDA","employee","enterprise_value","eps","equity",
        "goodwill",
        "income","income_beforeextra","income_tax","income_tax_payable",
        "interest_expense","inventory","inventory_turnover","invested_capital",
        "liabilities","liabilities_cur_oth","liabilities_curr","liabilities_oth",
        "operating_expense","operating_income","operating_margin","ppent","ppent_net",
        "preferred_dividends","pretax_income","quick_ratio","rd_expense","receiveable",
        "retained_earnings","return_assets","return_equity","revenue","sales",
        "sales_growth","sales_ps","sga_expense","working_capital"
    ]

def groupAlphabetically(terms):
    out = {}
    for letter in "abcdefghijklmnopqrstuvwxyz":
        out[letter] = []
        for each in terms:
            tag0 = ""
            for tag in ["2","1"]:
                if tag == each[:len(tag)]:
                    tag0 = tag
            stripped = each.replace(tag0,"") 
            if stripped[0] == letter:
                out[letter].append(each)
    return out

def groupCountStats(groupings):
    total = 0
    for key in groupings.keys():
        groupsize = len(groupings[key])
        total+=groupsize
        if groupsize > 0:
            print(key,groupsize)
    print("Total:",total)

def drill(groupings):
    done = False
    
    while not done:
        groupCountStats(groupings)
        for key in groupings.keys():
            terms = groupings[key]
            correctGuesses = []
            if len(terms) != 0:
                print("\nWorking on Group:",key.upper(),len(terms))
            
            while len(correctGuesses) != len(terms):
                guess = input("item: ").lower()
                if guess in terms and not guess in correctGuesses:
                    correctGuesses.append(guess)
                    print("good",len(correctGuesses))
                else:
                    print("invalid")

        if input("done? (Y)").lower() == "y":
            done=True
               
    print("finished")


def start():
    ops = [
        pricevolume,
        fundamental,
        ]

    drill(groupAlphabetically(ops[int(input("""
    
    0:pricevolume
    1:fundamental
    

    which set:"""))]))


start()

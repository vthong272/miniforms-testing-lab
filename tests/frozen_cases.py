"""Frozen v1.0 test-design manifest for the MiniForms experiment."""


def case(test_id, technique, form, requirement_id, expected_result, **inputs):
    return {
        "test_id": test_id,
        "technique": technique,
        "form": form,
        "requirement_id": requirement_id,
        "expected_result": expected_result,
        **inputs,
    }


EP_CASES = [
    case("EP-REG-01", "EP", "registration", "REG-R1-R5", "Accepted", username="user01", email="user@example.com", age="30", password="Secret123", confirm_password="Secret123"),
    case("EP-REG-02", "EP", "registration", "REG-R1", "Rejected", username="abcd", email="user@example.com", age="30", password="Secret123", confirm_password="Secret123"),
    case("EP-REG-03", "EP", "registration", "REG-R1", "Rejected", username="abcdefghijklmnop", email="user@example.com", age="30", password="Secret123", confirm_password="Secret123"),
    case("EP-REG-04", "EP", "registration", "REG-R2", "Rejected", username="user01", email="user.example.com", age="30", password="Secret123", confirm_password="Secret123"),
    case("EP-REG-05", "EP", "registration", "REG-R3", "Rejected", username="user01", email="user@example.com", age="17", password="Secret123", confirm_password="Secret123"),
    case("EP-REG-06", "EP", "registration", "REG-R3", "Rejected", username="user01", email="user@example.com", age="61", password="Secret123", confirm_password="Secret123"),
    case("EP-REG-07", "EP", "registration", "REG-R3", "Rejected", username="user01", email="user@example.com", age="30.5", password="Secret123", confirm_password="Secret123"),
    case("EP-REG-08", "EP", "registration", "REG-R4", "Rejected", username="user01", email="user@example.com", age="30", password="Pass123", confirm_password="Pass123"),
    case("EP-REG-09", "EP", "registration", "REG-R4", "Rejected", username="user01", email="user@example.com", age="30", password="A" * 21, confirm_password="A" * 21),
    case("EP-REG-10", "EP", "registration", "REG-R5", "Rejected", username="user01", email="user@example.com", age="30", password="Secret123", confirm_password="Secret124"),
    case("EP-SHIP-01", "EP", "shipping", "SHIP-R1", "Rejected", customer_type="regular", order_value="0", region="local", coupon_status="none"),
    case("EP-SHIP-02", "EP", "shipping", "SHIP-input", "Rejected", customer_type="guest", order_value="400000", region="local", coupon_status="none"),
    case("EP-SHIP-03", "EP", "shipping", "SHIP-input", "Rejected", customer_type="regular", order_value="400000", region="overseas", coupon_status="none"),
    case("EP-SHIP-04", "EP", "shipping", "SHIP-input", "Rejected", customer_type="regular", order_value="400000", region="local", coupon_status="unknown"),
    case("EP-SHIP-05", "EP", "shipping", "SHIP-R5", "Calculated", customer_type="regular", order_value="400000", region="local", coupon_status="none", expected_discount_rate="0", expected_shipping_fee="30000", expected_final_amount="430000"),
    case("EP-SHIP-06", "EP", "shipping", "SHIP-R3,R5", "Calculated", customer_type="regular", order_value="600000", region="remote", coupon_status="valid", expected_discount_rate="5", expected_shipping_fee="50000", expected_final_amount="620000"),
    case("EP-SHIP-07", "EP", "shipping", "SHIP-R2,R5", "Calculated", customer_type="vip", order_value="1200000", region="local", coupon_status="none", expected_discount_rate="10", expected_shipping_fee="0", expected_final_amount="1080000"),
    case("EP-SHIP-08", "EP", "shipping", "SHIP-R2-R5", "Calculated", customer_type="vip", order_value="1200000", region="remote", coupon_status="valid", expected_discount_rate="10", expected_shipping_fee="50000", expected_final_amount="1130000"),
    case("EP-SHIP-09", "EP", "shipping", "SHIP-R3,R5", "Calculated", customer_type="regular", order_value="900000", region="local", coupon_status="invalid", expected_discount_rate="0", expected_shipping_fee="0", expected_final_amount="900000"),
    case("EP-LOAN-01", "EP", "loan", "LOAN-R1-R5", "Approved", age="30", monthly_income="20000000", credit_score="700", employment_status="employed", requested_loan="100000000"),
    case("EP-LOAN-02", "EP", "loan", "LOAN-R1", "Rejected", age="20", monthly_income="20000000", credit_score="700", employment_status="employed", requested_loan="100000000"),
    case("EP-LOAN-03", "EP", "loan", "LOAN-R1", "Rejected", age="61", monthly_income="20000000", credit_score="700", employment_status="employed", requested_loan="100000000"),
    case("EP-LOAN-04", "EP", "loan", "LOAN-R1", "Rejected", age="30.5", monthly_income="20000000", credit_score="700", employment_status="employed", requested_loan="100000000"),
    case("EP-LOAN-05", "EP", "loan", "LOAN-R2", "Rejected", age="30", monthly_income="14000000", credit_score="700", employment_status="employed", requested_loan="100000000"),
    case("EP-LOAN-06", "EP", "loan", "LOAN-R3", "Rejected", age="30", monthly_income="20000000", credit_score="649", employment_status="employed", requested_loan="100000000"),
    case("EP-LOAN-07", "EP", "loan", "LOAN-R3", "Rejected", age="30", monthly_income="20000000", credit_score="851", employment_status="employed", requested_loan="100000000"),
    case("EP-LOAN-08", "EP", "loan", "LOAN-R3", "Rejected", age="30", monthly_income="20000000", credit_score="700.5", employment_status="employed", requested_loan="100000000"),
    case("EP-LOAN-09", "EP", "loan", "LOAN-R4", "Rejected", age="30", monthly_income="20000000", credit_score="700", employment_status="unemployed", requested_loan="100000000"),
    case("EP-LOAN-10", "EP", "loan", "LOAN-R5", "Rejected", age="30", monthly_income="20000000", credit_score="700", employment_status="employed", requested_loan="0"),
    case("EP-LOAN-11", "EP", "loan", "LOAN-R5", "Rejected", age="30", monthly_income="20000000", credit_score="700", employment_status="employed", requested_loan="200000001"),
]


BVA_CASES = []
for test_id, username, expected in [
    ("BVA-REG-USER-01", "user", "Rejected"), ("BVA-REG-USER-02", "user1", "Accepted"),
    ("BVA-REG-USER-03", "user12", "Accepted"), ("BVA-REG-USER-04", "user1234567890", "Accepted"),
    ("BVA-REG-USER-05", "user12345678901", "Accepted"), ("BVA-REG-USER-06", "user123456789012", "Rejected"),
]:
    BVA_CASES.append(case(test_id, "BVA", "registration", "REG-R1", expected, username=username, email="test@example.com", age="30", password="Test1234", confirm_password="Test1234"))
for test_id, age, expected in [
    ("BVA-REG-AGE-01", "17", "Rejected"), ("BVA-REG-AGE-02", "18", "Accepted"),
    ("BVA-REG-AGE-03", "19", "Accepted"), ("BVA-REG-AGE-04", "59", "Accepted"),
    ("BVA-REG-AGE-05", "60", "Accepted"), ("BVA-REG-AGE-06", "61", "Rejected"),
]:
    BVA_CASES.append(case(test_id, "BVA", "registration", "REG-R3", expected, username="user123", email="test@example.com", age=age, password="Test1234", confirm_password="Test1234"))
for test_id, length, expected in [
    ("BVA-REG-PASS-01", 7, "Rejected"), ("BVA-REG-PASS-02", 8, "Accepted"),
    ("BVA-REG-PASS-03", 9, "Accepted"), ("BVA-REG-PASS-04", 19, "Accepted"),
    ("BVA-REG-PASS-05", 20, "Accepted"), ("BVA-REG-PASS-06", 21, "Rejected"),
]:
    password = "A" * length
    BVA_CASES.append(case(test_id, "BVA", "registration", "REG-R4", expected, username="user123", email="test@example.com", age="30", password=password, confirm_password=password))

for values in [
    ("BVA-SHIP-POS-01", "SHIP-R1", "regular", "-1", "local", "none", "Rejected", None, None, None),
    ("BVA-SHIP-POS-02", "SHIP-R1", "regular", "0", "local", "none", "Rejected", None, None, None),
    ("BVA-SHIP-POS-03", "SHIP-R1", "regular", "1", "local", "none", "Calculated", "0", "30000", "30001"),
    ("BVA-SHIP-COUPON-01", "SHIP-R3", "regular", "499999", "local", "valid", "Calculated", "0", "30000", "529999"),
    ("BVA-SHIP-COUPON-02", "SHIP-R3", "regular", "500000", "local", "valid", "Calculated", "5", "30000", "505000"),
    ("BVA-SHIP-COUPON-03", "SHIP-R3", "regular", "500001", "local", "valid", "Calculated", "5", "30000", "505000.95"),
    ("BVA-SHIP-FREE-01", "SHIP-R5", "regular", "799999", "local", "none", "Calculated", "0", "30000", "829999"),
    ("BVA-SHIP-FREE-02", "SHIP-R5", "regular", "800000", "local", "none", "Calculated", "0", "0", "800000"),
    ("BVA-SHIP-FREE-03", "SHIP-R5", "regular", "800001", "local", "none", "Calculated", "0", "0", "800001"),
    ("BVA-SHIP-VIP-01", "SHIP-R2", "vip", "999999", "local", "none", "Calculated", "0", "0", "999999"),
    ("BVA-SHIP-VIP-02", "SHIP-R2", "vip", "1000000", "local", "none", "Calculated", "10", "0", "900000"),
    ("BVA-SHIP-VIP-03", "SHIP-R2", "vip", "1000001", "local", "none", "Calculated", "10", "0", "900000.9"),
]:
    test_id, req, customer, order, region, coupon, expected, rate, fee, final = values
    extra = {} if expected == "Rejected" else {"expected_discount_rate": rate, "expected_shipping_fee": fee, "expected_final_amount": final}
    BVA_CASES.append(case(test_id, "BVA", "shipping", req, expected, customer_type=customer, order_value=order, region=region, coupon_status=coupon, **extra))

for test_id, req, age, income, score, loan, expected in [
    ("BVA-LOAN-AGE-01", "LOAN-R1", "20", "20000000", "700", "100000000", "Rejected"),
    ("BVA-LOAN-AGE-02", "LOAN-R1", "21", "20000000", "700", "100000000", "Approved"),
    ("BVA-LOAN-AGE-03", "LOAN-R1", "22", "20000000", "700", "100000000", "Approved"),
    ("BVA-LOAN-AGE-04", "LOAN-R1", "59", "20000000", "700", "100000000", "Approved"),
    ("BVA-LOAN-AGE-05", "LOAN-R1", "60", "20000000", "700", "100000000", "Approved"),
    ("BVA-LOAN-AGE-06", "LOAN-R1", "61", "20000000", "700", "100000000", "Rejected"),
    ("BVA-LOAN-INCOME-01", "LOAN-R2", "30", "14999999", "700", "100000000", "Rejected"),
    ("BVA-LOAN-INCOME-02", "LOAN-R2", "30", "15000000", "700", "100000000", "Approved"),
    ("BVA-LOAN-INCOME-03", "LOAN-R2", "30", "15000001", "700", "100000000", "Approved"),
    ("BVA-LOAN-SCORE-01", "LOAN-R3", "30", "20000000", "649", "100000000", "Rejected"),
    ("BVA-LOAN-SCORE-02", "LOAN-R3", "30", "20000000", "650", "100000000", "Approved"),
    ("BVA-LOAN-SCORE-03", "LOAN-R3", "30", "20000000", "651", "100000000", "Approved"),
    ("BVA-LOAN-SCORE-04", "LOAN-R3", "30", "20000000", "849", "100000000", "Approved"),
    ("BVA-LOAN-SCORE-05", "LOAN-R3", "30", "20000000", "850", "100000000", "Approved"),
    ("BVA-LOAN-SCORE-06", "LOAN-R3", "30", "20000000", "851", "100000000", "Rejected"),
    ("BVA-LOAN-POS-01", "LOAN-R5", "30", "20000000", "700", "-1", "Rejected"),
    ("BVA-LOAN-POS-02", "LOAN-R5", "30", "20000000", "700", "0", "Rejected"),
    ("BVA-LOAN-POS-03", "LOAN-R5", "30", "20000000", "700", "1", "Approved"),
    ("BVA-LOAN-MAX-01", "LOAN-R5", "30", "15000000", "700", "149999999", "Approved"),
    ("BVA-LOAN-MAX-02", "LOAN-R5", "30", "15000000", "700", "150000000", "Approved"),
    ("BVA-LOAN-MAX-03", "LOAN-R5", "30", "15000000", "700", "150000001", "Rejected"),
]:
    BVA_CASES.append(case(test_id, "BVA", "loan", req, expected, age=age, monthly_income=income, credit_score=score, employment_status="employed", requested_loan=loan))


DTT_CASES = [
    case("DT-REG-01", "DTT", "registration", "REG-R1-R5", "Accepted", username="user01", email="user@example.com", age="30", password="Secret123", confirm_password="Secret123"),
    case("DT-REG-02", "DTT", "registration", "REG-R1", "Rejected", username="abc", email="user@example.com", age="30", password="Secret123", confirm_password="Secret123"),
    case("DT-REG-03", "DTT", "registration", "REG-R2", "Rejected", username="user01", email="user@example", age="30", password="Secret123", confirm_password="Secret123"),
    case("DT-REG-04", "DTT", "registration", "REG-R3", "Rejected", username="user01", email="user@example.com", age="17", password="Secret123", confirm_password="Secret123"),
    case("DT-REG-05", "DTT", "registration", "REG-R4", "Rejected", username="user01", email="user@example.com", age="30", password="abc1234", confirm_password="abc1234"),
    case("DT-REG-06", "DTT", "registration", "REG-R5", "Rejected", username="user01", email="user@example.com", age="30", password="Secret123", confirm_password="Secret124"),
]

for values in [
    ("DT-SHIP-01", "SHIP-R1", "regular", "0", "local", "none", "Rejected", None, None, None),
    ("DT-SHIP-02", "SHIP-R2-R5", "regular", "400000", "local", "none", "Calculated", "0", "30000", "430000"),
    ("DT-SHIP-03", "SHIP-R2-R5", "vip", "400000", "remote", "valid", "Calculated", "0", "50000", "450000"),
    ("DT-SHIP-04", "SHIP-R2-R5", "regular", "600000", "local", "valid", "Calculated", "5", "30000", "600000"),
    ("DT-SHIP-05", "SHIP-R2-R5", "vip", "600000", "remote", "valid", "Calculated", "5", "50000", "620000"),
    ("DT-SHIP-06", "SHIP-R2-R5", "regular", "600000", "local", "invalid", "Calculated", "0", "30000", "630000"),
    ("DT-SHIP-07", "SHIP-R2-R5", "vip", "600000", "remote", "none", "Calculated", "0", "50000", "650000"),
    ("DT-SHIP-08", "SHIP-R2-R5", "regular", "900000", "local", "valid", "Calculated", "5", "0", "855000"),
    ("DT-SHIP-09", "SHIP-R2-R5", "vip", "900000", "remote", "valid", "Calculated", "5", "50000", "905000"),
    ("DT-SHIP-10", "SHIP-R2-R5", "vip", "900000", "local", "invalid", "Calculated", "0", "0", "900000"),
    ("DT-SHIP-11", "SHIP-R2-R5", "regular", "900000", "remote", "none", "Calculated", "0", "50000", "950000"),
    ("DT-SHIP-12", "SHIP-R2-R5", "vip", "1200000", "local", "valid", "Calculated", "10", "0", "1080000"),
    ("DT-SHIP-13", "SHIP-R2-R5", "vip", "1200000", "remote", "invalid", "Calculated", "10", "50000", "1130000"),
    ("DT-SHIP-14", "SHIP-R2-R5", "regular", "1200000", "local", "valid", "Calculated", "5", "0", "1140000"),
    ("DT-SHIP-15", "SHIP-R2-R5", "regular", "1200000", "remote", "valid", "Calculated", "5", "50000", "1190000"),
    ("DT-SHIP-16", "SHIP-R2-R5", "regular", "1200000", "local", "invalid", "Calculated", "0", "0", "1200000"),
    ("DT-SHIP-17", "SHIP-R2-R5", "regular", "1200000", "remote", "none", "Calculated", "0", "50000", "1250000"),
]:
    test_id, req, customer, order, region, coupon, expected, rate, fee, final = values
    extra = {} if expected == "Rejected" else {"expected_discount_rate": rate, "expected_shipping_fee": fee, "expected_final_amount": final}
    DTT_CASES.append(case(test_id, "DTT", "shipping", req, expected, customer_type=customer, order_value=order, region=region, coupon_status=coupon, **extra))

for test_id, req, age, income, score, employment, loan, expected in [
    ("DT-LOAN-01", "LOAN-R1-R5", "30", "20000000", "700", "employed", "100000000", "Approved"),
    ("DT-LOAN-02", "LOAN-R1", "20", "20000000", "700", "employed", "100000000", "Rejected"),
    ("DT-LOAN-03", "LOAN-R2", "30", "14000000", "700", "employed", "100000000", "Rejected"),
    ("DT-LOAN-04", "LOAN-R3", "30", "20000000", "600", "employed", "100000000", "Rejected"),
    ("DT-LOAN-05", "LOAN-R4", "30", "20000000", "700", "unemployed", "100000000", "Rejected"),
    ("DT-LOAN-06", "LOAN-R5", "30", "20000000", "700", "employed", "250000000", "Rejected"),
]:
    DTT_CASES.append(case(test_id, "DTT", "loan", req, expected, age=age, monthly_income=income, credit_score=score, employment_status=employment, requested_loan=loan))


ALL_CASES = EP_CASES + BVA_CASES + DTT_CASES
